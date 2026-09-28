import subprocess, sys, os, time
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

# Helper to start Flask server
def start_server():
    cwd = os.getcwd()
    proc = subprocess.Popen([sys.executable, "app.py"], cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    for _ in range(30):
        try:
            r = requests.get('http://127.0.0.1:5000/')
            if r.status_code == 200:
                return proc
        except Exception:
            pass
        time.sleep(1)
    proc.terminate()
    raise RuntimeError('Flask server failed to start')

def stop_server(proc):
    proc.terminate()
    try:
        proc.wait(timeout=5)
    except subprocess.TimeoutExpired:
        proc.kill()

def run_ui_checks():
    proc = start_server()
    try:
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        options.add_argument('--no-sandbox')
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        driver.get('http://127.0.0.1:5000/weather')
        results = []
        # Check hero heading exists
        try:
            heading = driver.find_element(By.CSS_SELECTOR, '.hero-heading')
            results.append(('Hero Heading', 'PASS', heading.text))
        except Exception as e:
            results.append(('Hero Heading', 'FAIL', str(e)))
        # Check video element present
        try:
            video = driver.find_element(By.TAG_NAME, 'video')
            results.append(('Hero Video', 'PASS', video.get_attribute('src') or 'found'))
        except Exception as e:
            results.append(('Hero Video', 'FAIL', str(e)))
        # Check stat items count
        try:
            stats = driver.find_elements(By.CSS_SELECTOR, '.stat-item')
            if len(stats) >= 3:
                results.append(('Stat Items', 'PASS', f'found {len(stats)}'))
            else:
                results.append(('Stat Items', 'FAIL', f'found {len(stats)}'))
        except Exception as e:
            results.append(('Stat Items', 'FAIL', str(e)))
        # Check forecast cards
        try:
            cards = driver.find_elements(By.CSS_SELECTOR, '.forecast-card')
            if cards:
                results.append(('Forecast Cards', 'PASS', f'found {len(cards)}'))
            else:
                results.append(('Forecast Cards', 'FAIL', 'none'))
        except Exception as e:
            results.append(('Forecast Cards', 'FAIL', str(e)))
        driver.quit()
        for name, status, detail in results:
            print(f"{name}: {status} ({detail})")
    finally:
        stop_server(proc)

if __name__ == '__main__':
    run_ui_checks()
