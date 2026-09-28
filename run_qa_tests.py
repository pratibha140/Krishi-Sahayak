import subprocess
import sys
import time
import os
import signal
import threading
import json
from pathlib import Path

# External libraries (may not be installed)
try:
    import requests
except ImportError:
    print("[ERROR] 'requests' library is not installed. Install it to run HTTP tests.")
    sys.exit(1)

try:
    from docx import Document
    from docx.shared import Inches
except ImportError:
    print("[ERROR] 'python-docx' library is not installed. Install it to generate the report.")
    sys.exit(1)

# Optional UI testing with Selenium and webdriver-manager
try:
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options as ChromeOptions
    from webdriver_manager.chrome import ChromeDriverManager
    UI_AVAILABLE = True
except ImportError:
    UI_AVAILABLE = False
    print("[WARN] Selenium or webdriver-manager not installed. UI viewport tests will be BLOCKED.")


# Configuration
PROJECT_ROOT = Path(r"D:\Krishi-Sahayak")
APP_PATH = PROJECT_ROOT / "app.py"
REPORT_PATH = PROJECT_ROOT / "Krishi_Sahayak_Detailed_Software_Testing_Report.docx"
HOST = "127.0.0.1"
PORT = 5000
BASE_URL = f"http://{HOST}:{PORT}"

# Helper to start Flask app in a subprocess
def start_flask():
    # Ensure the environment has required variables
    env = os.environ.copy()
    # Flask will run app.py directly
    proc = subprocess.Popen(
        [sys.executable, str(APP_PATH)],
        cwd=str(PROJECT_ROOT),
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )
    return proc

# Wait until server responds or timeout
def wait_for_server(timeout=30, interval=1):
    start = time.time()
    while time.time() - start < timeout:
        try:
            r = requests.get(BASE_URL, timeout=5)
            if r.status_code == 200:
                return True
        except Exception:
            pass
        time.sleep(interval)
    return False

# Basic route test
def test_route(path, expected_status=200):
    url = f"{BASE_URL}{path}"
    try:
        r = requests.get(url, timeout=10)
        return {
            "url": url,
            "status": r.status_code,
            "expected": expected_status,
            "result": "PASS" if r.status_code == expected_status else "FAIL",
            "content": r.text[:200],
        }
    except Exception as e:
        return {
            "url": url,
            "status": None,
            "expected": expected_status,
            "result": "BLOCKED",
            "error": str(e),
        }

# Language switch helper (uses the set-language route)
def set_language(lang_code):
    return test_route(f"/set-language/{lang_code}")

# UI testing with Selenium (if available)
def ui_test(lang_code, viewport):
    """Perform UI test for a given language and viewport.
    Returns dict with result, title, screenshot path, console errors.
    """
    if not UI_AVAILABLE:
        return {"lang": lang_code, "viewport": viewport, "result": "BLOCKED", "reason": "Selenium not installed"}
    opts = ChromeOptions()
    opts.add_argument('--headless')
    opts.add_argument('--disable-gpu')
    # Enable performance logging for console errors
    opts.set_capability('goog:loggingPrefs', {'browser': 'ALL'})
    driver = webdriver.Chrome(options=opts)
    driver.set_window_size(viewport[0], viewport[1])
    screenshot_dir = PROJECT_ROOT / "qa_evidence"
    screenshot_dir.mkdir(exist_ok=True)
    screenshot_path = screenshot_dir / f"screenshot_{lang_code}_{viewport[0]}x{viewport[1]}.png"
    try:
        # Set language via endpoint first
        set_language(lang_code)
        driver.get(f"{BASE_URL}/")
        title = driver.title
        # Capture screenshot
        driver.save_screenshot(str(screenshot_path))
        # Retrieve console logs
        console_logs = driver.get_log('browser')
        errors = [log['message'] for log in console_logs if log['level'] == 'SEVERE']
        result = "PASS" if title and not errors else "FAIL"
        return {
            "lang": lang_code,
            "viewport": viewport,
            "title": title,
            "result": result,
            "screenshot": str(screenshot_path),
            "console_errors": errors,
        }
    except Exception as e:
        return {"lang": lang_code, "viewport": viewport, "result": "FAIL", "error": str(e)}
    finally:
        driver.quit()

# Build report using python-docx
def generate_report(test_results, ui_results, blocked_info):
    doc = Document()
    doc.add_heading('Krishi Sahayak – Detailed Software Testing Report', 0)
    doc.add_paragraph(f"Generated on: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    doc.add_paragraph(f"Application URL: {BASE_URL}")
    doc.add_heading('1. Functional Route Tests', level=1)
    table = doc.add_table(rows=1, cols=5)
    hdr_cells = table.rows[0].cells
    hdr_cells[0].text = 'Test'
    hdr_cells[1].text = 'URL'
    hdr_cells[2].text = 'Expected Status'
    hdr_cells[3].text = 'Actual Status'
    hdr_cells[4].text = 'Result'
    for tr in test_results:
        row_cells = table.add_row().cells
        row_cells[0].text = tr.get('test_name', 'Route Test')
        row_cells[1].text = tr['url']
        row_cells[2].text = str(tr['expected'])
        row_cells[3].text = str(tr['status'])
        row_cells[4].text = tr['result']
    doc.add_heading('2. UI/UX Language & Viewport Tests', level=1)
    table2 = doc.add_table(rows=1, cols=4)
    hdr2 = table2.rows[0].cells
    hdr2[0].text = 'Language'
    hdr2[1].text = 'Viewport (WxH)'
    hdr2[2].text = 'Result'
    hdr2[3].text = 'Details'
    for ur in ui_results:
        row = table2.add_row().cells
        row[0].text = ur.get('lang', '')
        row[1].text = f"{ur.get('viewport', '')}"
        row[2].text = ur.get('result', '')
        detail = ur.get('error') or ur.get('reason') or ''
        row[3].text = detail
    if blocked_info:
        doc.add_heading('3. Blocked Tests / Limitations', level=1)
        for b in blocked_info:
            doc.add_paragraph(b)
    # Save the document
    doc.save(str(REPORT_PATH))
    return str(REPORT_PATH)

# Verify the generated DOCX
def verify_report(path):
    try:
        doc = Document(path)
        # Simple verification: check that we have at least two tables (functional + UI)
        tables = doc.tables
        if len(tables) < 2:
            return False, "Report missing expected tables"
        # Check that there is some content in the first paragraph
        if not doc.paragraphs:
            return False, "Report is empty"
        return True, "Report appears valid"
    except Exception as e:
        return False, str(e)

def main():
    print("[INFO] Starting Flask server...")
    flask_proc = start_flask()
    try:
        if not wait_for_server():
            print("[ERROR] Server did not become reachable in time.")
            return
        print("[INFO] Server is up. Beginning tests.")
        # Define route tests
        routes = [
            {"path": "/", "expected": 200, "name": "Home"},
            {"path": "/weather", "expected": 200, "name": "Weather"},
            {"path": "/crops", "expected": 200, "name": "Crops"},
            {"path": "/calendar", "expected": 200, "name": "Calendar"},
            {"path": "/soil", "expected": 200, "name": "Soil"},
            {"path": "/disease", "expected": 200, "name": "Disease"},
            {"path": "/voice", "expected": 200, "name": "Voice Assistant"},
        ]
        functional_results = []
        for r in routes:
            res = test_route(r["path"], r["expected"])
            res["test_name"] = r["name"]
            functional_results.append(res)
        # Language route tests (just invoking the endpoint)
        for lang in ["en", "hi", "mr"]:
            functional_results.append(set_language(lang))
        # UI tests (if Selenium available)
        ui_results = []
        blocked_info = []
        viewports = [(375, 667), (768, 1024), (1440, 900)]
        for lang in ["en", "hi", "mr"]:
            for vp in viewports:
                ui_res = ui_test(lang, vp)
                ui_results.append(ui_res)
                if ui_res["result"] == "BLOCKED":
                    blocked_info.append(f"UI test blocked for language {lang} viewport {vp}: {ui_res.get('reason', ui_res.get('error'))}")
        # Generate report
        report_path = generate_report(functional_results, ui_results, blocked_info)
        print(f"[INFO] Report generated at {report_path}")
        # Verify report
        ok, msg = verify_report(report_path)
        if ok:
            print("[INFO] Report verification successful.")
        else:
            print(f"[WARN] Report verification failed: {msg}")
    finally:
        # Terminate Flask process gracefully on Windows
        if flask_proc.poll() is None:
            try:
                # On Windows, use terminate instead of SIGINT
                flask_proc.terminate()
                flask_proc.wait(timeout=5)
            except Exception:
                flask_proc.kill()
        print("[INFO] Done.")

if __name__ == "__main__":
    main()
