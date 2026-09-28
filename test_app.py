# test_app.py
# Automated Verification Test Suite for Krishi Sahayak
# Incorporating MANAGE Farmer's Handbook, Weather Engine, Schemes, Reminders & SQLite Auth Persistence

import datetime
import io
import os
import secrets
import subprocess
import sys
import time
import unittest
from unittest.mock import patch, MagicMock
from PIL import Image
from werkzeug.security import generate_password_hash
from app import app, clear_rate_limits, is_rate_limited
import database
from crops_data import CROPS, calculate_crop_plan, CRITICAL_IRRIGATION_STAGES, DRIP_SPRINKLER_BENEFITS
from weather_service import (
    get_weather_forecast,
    search_locations,
    reverse_geocode,
    clear_weather_caches,
    _WEATHER_CACHE,
    _REVERSE_GEO_CACHE,
    _SEARCH_LOCATIONS_CACHE,
)
from assistant_service import process_query
from disease_service import search_diseases, diagnose_plant_photo
from handbook_data import NUTRIENT_DEFICIENCIES, PESTICIDE_TOXICITY_CLASSES, FARMER_SERVICES, GOVERNMENT_SCHEMES


class KrishiSahayakTestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['SECRET_KEY'] = 'test-secret-key'
        app.config.pop('ENABLE_RATE_LIMIT_TESTING', None)
        clear_rate_limits()
        self.client = app.test_client()
        self._prev_mock_auth = os.environ.get('ENABLE_DEV_MOCK_AUTH')
        os.environ['ENABLE_DEV_MOCK_AUTH'] = '1'

    def tearDown(self):
        app.config['TESTING'] = True
        app.config.pop('ENABLE_RATE_LIMIT_TESTING', None)
        clear_rate_limits()
        if self._prev_mock_auth is None:
            os.environ.pop('ENABLE_DEV_MOCK_AUTH', None)
        else:
            os.environ['ENABLE_DEV_MOCK_AUTH'] = self._prev_mock_auth

    def test_routes_status_code(self):
        with self.client.session_transaction() as sess:
            sess['language'] = 'en'
            sess['user'] = {
                'id': 1,
                'name': 'Test Farmer',
                'email': 'test.farmer@gmail.com',
                'language': 'en'
            }

        routes = [
            '/', '/language', '/login', '/profile', '/weather', '/crops', '/calendar',
            '/disease', '/voice', '/soil', '/practices', '/services', '/schemes', '/reminders'
        ]
        for route in routes:
            response = self.client.get(route)
            self.assertEqual(response.status_code, 200, f"Route {route} failed with status {response.status_code}")

    def test_onboarding_redirection_flow(self):
        # 1. Uninitialized session redirects to /language
        with self.client as c:
            res = c.get('/', follow_redirects=False)
            self.assertEqual(res.status_code, 302)
            self.assertIn('/language', res.location)

        # 2. Select language -> redirects to /login?onboarding=1
        res_lang = self.client.post('/language', data={'language': 'hi'}, follow_redirects=False)
        self.assertEqual(res_lang.status_code, 302)
        self.assertIn('/login', res_lang.location)

        # 3. Login farmer -> redirects to home dashboard /
        res_login = self.client.post('/login', data={
            'name': 'Ramesh Patil',
            'email': 'ramesh.patil@gmail.com'
        }, follow_redirects=False)
        self.assertEqual(res_login.status_code, 302)
        self.assertIn('/', res_login.location)

    def test_reminders_crud_api(self):
        # Create test session user
        with self.client.session_transaction() as sess:
            db_user = database.save_user('reminders.farmer@gmail.com', 'Reminder Farmer')
            sess['user'] = db_user
            sess['language'] = 'en'

        # 1. Add Reminder
        res_add = self.client.post('/api/reminders', json={
            'title': 'Apply Urea Top Dressing',
            'category': 'fertilizer',
            'due_date': '2026-06-25'
        })
        self.assertEqual(res_add.status_code, 200)
        data_add = res_add.get_json()
        self.assertTrue(data_add['success'])
        rem_id = data_add['reminder_id']

        # 2. Get Reminders
        res_get = self.client.get('/api/reminders')
        self.assertEqual(res_get.status_code, 200)
        data_get = res_get.get_json()
        self.assertTrue(data_get['success'])
        self.assertGreater(len(data_get['reminders']), 0)

        # 3. Update Status
        res_put = self.client.put('/api/reminders', json={'id': rem_id, 'status': 'completed'})
        self.assertEqual(res_put.status_code, 200)
        self.assertTrue(res_put.get_json()['success'])

        # 4. Delete Reminder
        res_del = self.client.delete(f'/api/reminders?id={rem_id}')
        self.assertEqual(res_del.status_code, 200)
        self.assertTrue(res_del.get_json()['success'])

    def test_gps_location_persistence_api(self):
        with self.client.session_transaction() as sess:
            db_user = database.save_user('gps.farmer@gmail.com', 'GPS Farmer')
            sess['user'] = db_user
            sess['language'] = 'en'

        res = self.client.post('/api/location/save', json={
            'lat': 19.9975,
            'lon': 73.7898
        })
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertTrue(data['success'])
        self.assertTrue('location_name' in data)

        # Verify DB persisted values
        saved_user = database.get_user_by_email('gps.farmer@gmail.com')
        self.assertAlmostEqual(saved_user['lat'], 19.9975, places=3)
        self.assertAlmostEqual(saved_user['lon'], 73.7898, places=3)

    def test_schemes_page_rendering(self):
        with self.client.session_transaction() as sess:
            sess['language'] = 'hi'
            sess['user'] = {'id': 1, 'name': 'Scheme Test', 'email': 'scheme@test.com'}

        res = self.client.get('/schemes')
        self.assertEqual(res.status_code, 200)
        html = res.get_data(as_text=True)
        self.assertIn('पीएम-किसान', html)
        self.assertIn('pmkisan.gov.in', html)
        self.assertIn('rel="noopener noreferrer"', html)
        self.assertIn('data-category="insurance"', html)
        self.assertIn('data-category="irrigation"', html)
        self.assertIn('data-category="financial"', html)

    def test_user_login_and_profile_flow(self):
        # 1. Standard farmer login
        res_login = self.client.post('/login', data={
            'name': 'Ramesh Patil',
            'email': 'ramesh.patil@gmail.com'
        }, follow_redirects=True)
        self.assertEqual(res_login.status_code, 200)

        # 2. View Profile Page
        res_prof = self.client.get('/profile')
        self.assertEqual(res_prof.status_code, 200)
        html = res_prof.get_data(as_text=True)
        self.assertIn('Ramesh Patil', html)
        self.assertIn('ramesh.patil@gmail.com', html)

        # 3. Update Profile Preferences
        res_update = self.client.post('/profile', data={
            'name': 'Ramesh Patil Updated',
            'email': 'ramesh.patil@gmail.com',
            'state': 'Maharashtra',
            'district': 'Nashik',
            'land_size': '3.5',
            'primary_crop': 'banana',
            'soil_type': 'Black Cotton Soil'
        }, follow_redirects=True)
        self.assertEqual(res_update.status_code, 200)
        self.assertIn('Ramesh Patil Updated', res_update.get_data(as_text=True))

    def test_google_auth_and_session(self):
        # Test Google login API callback
        res = self.client.post('/api/auth/google', json={
            'name': 'Ramesh Patil',
            'email': 'ramesh.patil@gmail.com',
            'picture': 'https://api.dicebear.com/7.x/initials/svg?seed=Ramesh'
        })
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertTrue(data['success'])
        self.assertEqual(data['user']['name'], 'Ramesh Patil')
        self.assertEqual(data['user']['auth_type'], 'google')

    def test_plant_photo_diagnosis_api(self):
        image = Image.new('RGB', (224, 224), color=(20, 160, 50))
        buffer = io.BytesIO()
        image.save(buffer, format='PNG')
        photo = (io.BytesIO(buffer.getvalue()), "tomato_blight_leaf.jpg")
        res = self.client.post('/api/diagnose-disease', data={
            'leaf_photo': photo,
            'crop': 'tomato',
            'lang': 'en'
        }, content_type='multipart/form-data')
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertTrue(data['success'])
        self.assertIn('disease', data)

    def test_plant_photo_diagnosis_uses_image_bytes_not_filename(self):
        image = Image.new('RGB', (224, 224), color=(20, 160, 50))
        buffer = io.BytesIO()
        image.save(buffer, format='PNG')
        payload = buffer.getvalue()

        first_result = self.client.post('/api/diagnose-disease', data={
            'leaf_photo': (io.BytesIO(payload), 'septoria_leaf_spot.jpg'),
            'crop': 'tomato',
            'lang': 'en'
        }, content_type='multipart/form-data')
        second_result = self.client.post('/api/diagnose-disease', data={
            'leaf_photo': (io.BytesIO(payload), 'banana_leaf_burn.jpg'),
            'crop': 'wheat',
            'lang': 'en'
        }, content_type='multipart/form-data')

        self.assertEqual(first_result.status_code, 200)
        self.assertEqual(second_result.status_code, 200)
        self.assertEqual(first_result.get_json()['disease']['name'], second_result.get_json()['disease']['name'])

    def test_language_switching(self):
        res_hi = self.client.get('/set-language/hi', follow_redirects=True)
        self.assertEqual(res_hi.status_code, 200)

        res_mr = self.client.get('/set-language/mr', follow_redirects=True)
        self.assertEqual(res_mr.status_code, 200)

        res_en = self.client.get('/set-language/en', follow_redirects=True)
        self.assertEqual(res_en.status_code, 200)

    def test_crop_calculation_engine_and_new_crops(self):
        banana_plan = calculate_crop_plan('banana', '2026-06-15', 2.0, 'acre')
        self.assertEqual(banana_plan['crop']['id'], 'banana')
        self.assertEqual(banana_plan['acres_calculated'], 2.0)

    def test_weather_service_and_extended_agri_metrics(self):
        data = get_weather_forecast(18.5204, 73.8567, "Pune, Maharashtra", lang='hi')
        self.assertIn('current', data)
        self.assertIn('temp', data['current'])

    def test_voice_assistant_api(self):
        res_nut = self.client.post('/api/voice-assistant', json={'query': 'zinc deficiency symptoms', 'lang': 'en'})
        self.assertEqual(res_nut.status_code, 200)
        self.assertIn('Zinc', res_nut.get_json()['text'])

    def test_reminder_idor_protection(self):
        # Create User 1 and User 2 in database
        user1 = database.save_user('user1.idor@gmail.com', 'User One')
        user2 = database.save_user('user2.idor@gmail.com', 'User Two')

        # User 1 creates a reminder
        rem_id1 = database.add_reminder(user1['id'], 'User 1 Private Task', 'fertilizer', '2026-07-01')

        # 1. User 2 logs in and attempts to access User 1's reminder via GET
        with self.client.session_transaction() as sess:
            sess['user'] = user2
            sess['language'] = 'en'

        res_get = self.client.get('/api/reminders')
        self.assertEqual(res_get.status_code, 200)
        user2_reminders = res_get.get_json().get('reminders', [])
        user2_rem_ids = [r['id'] for r in user2_reminders]
        self.assertNotIn(rem_id1, user2_rem_ids)

        # 2. User 2 attempts to modify User 1's reminder via PUT
        res_put = self.client.put('/api/reminders', json={'id': rem_id1, 'status': 'completed'})
        self.assertEqual(res_put.status_code, 404)
        self.assertFalse(res_put.get_json()['success'])

        # Verify User 1's reminder was NOT modified
        reminders_u1 = database.get_user_reminders(user1['id'])
        u1_target = next(r for r in reminders_u1 if r['id'] == rem_id1)
        self.assertEqual(u1_target['status'], 'pending')

        # 3. User 2 attempts to delete User 1's reminder via DELETE
        res_del = self.client.delete(f'/api/reminders?id={rem_id1}')
        self.assertEqual(res_del.status_code, 404)
        self.assertFalse(res_del.get_json()['success'])

        # Verify User 1's reminder was NOT deleted
        reminders_u1_after = database.get_user_reminders(user1['id'])
        self.assertTrue(any(r['id'] == rem_id1 for r in reminders_u1_after))

        # 4. User 1 logs in and legitimate access to own reminder works
        with self.client.session_transaction() as sess:
            sess['user'] = user1
            sess['language'] = 'en'

        # User 1 can see it
        res_u1_get = self.client.get('/api/reminders')
        self.assertEqual(res_u1_get.status_code, 200)
        u1_ids = [r['id'] for r in res_u1_get.get_json().get('reminders', [])]
        self.assertIn(rem_id1, u1_ids)

        # User 1 can update it
        res_u1_put = self.client.put('/api/reminders', json={'id': rem_id1, 'status': 'completed'})
        self.assertEqual(res_u1_put.status_code, 200)
        self.assertTrue(res_u1_put.get_json()['success'])

        # User 1 can delete it
        res_u1_del = self.client.delete(f'/api/reminders?id={rem_id1}')
        self.assertEqual(res_u1_del.status_code, 200)
        self.assertTrue(res_u1_del.get_json()['success'])

    def test_location_save_validation(self):
        with self.client.session_transaction() as sess:
            user = database.save_user('loc.val@gmail.com', 'Location Val Farmer')
            sess['user'] = user
            sess['language'] = 'en'

        # 1. Valid coordinates accepted (standard & boundary)
        valid_cases = [
            (19.9975, 73.7898),
            (0.0, 0.0),
            (-90.0, -180.0),
            (90.0, 180.0)
        ]
        for lat, lon in valid_cases:
            res = self.client.post('/api/location/save', json={'lat': lat, 'lon': lon})
            self.assertEqual(res.status_code, 200, f"Expected 200 for ({lat}, {lon})")
            self.assertTrue(res.get_json()['success'])

        # 2. Out-of-range coordinates rejected (status 400)
        out_of_range_cases = [
            (90.1, 73.7898),
            (-90.1, 73.7898),
            (18.5204, 180.1),
            (18.5204, -180.1),
            (999.0, 999.0)
        ]
        for lat, lon in out_of_range_cases:
            res = self.client.post('/api/location/save', json={'lat': lat, 'lon': lon})
            self.assertEqual(res.status_code, 400, f"Expected 400 for out-of-range ({lat}, {lon})")
            self.assertFalse(res.get_json()['success'])
            self.assertIn("out of range", res.get_json().get('error', '').lower())

        # 3. Malformed coordinates rejected (status 400)
        malformed_cases = [
            {'lat': 'invalid_lat', 'lon': 73.7898},
            {'lat': 18.5204, 'lon': 'invalid_lon'},
            {'lat': [18.5], 'lon': 73.0},
            {'lat': 'null_val', 'lon': 'null_val'}
        ]
        for payload in malformed_cases:
            res = self.client.post('/api/location/save', json=payload)
            self.assertEqual(res.status_code, 400, f"Expected 400 for malformed payload {payload}")
            self.assertFalse(res.get_json()['success'])
            self.assertIn("invalid coordinates", res.get_json().get('error', '').lower())

        # 4. Missing/Null coordinate values rejected safely (status 400)
        missing_cases = [
            {'lat': None, 'lon': 73.7898},
            {'lat': 18.5204, 'lon': None},
            {'lat': '', 'lon': 73.7898},
            {'lat': 18.5204, 'lon': ''}
        ]
        for payload in missing_cases:
            res = self.client.post('/api/location/save', json=payload)
            self.assertEqual(res.status_code, 400, f"Expected 400 for missing/null value {payload}")
            self.assertFalse(res.get_json()['success'])

    def test_diagnose_disease_file_upload_validation(self):
        # Helper to create real in-memory image
        def make_image_bytes(fmt='PNG'):
            img = Image.new('RGB', (100, 100), color=(34, 139, 34))
            buf = io.BytesIO()
            img.save(buf, format=fmt)
            return buf.getvalue()

        # 1. Valid JPG, PNG, WebP image content is accepted
        valid_formats = [
            ('JPEG', 'leaf.jpg'),
            ('PNG', 'leaf.png'),
            ('WEBP', 'leaf.webp'),
        ]
        for fmt, fname in valid_formats:
            payload = make_image_bytes(fmt)
            res = self.client.post('/api/diagnose-disease', data={
                'leaf_photo': (io.BytesIO(payload), fname),
                'crop': 'tomato',
                'lang': 'en'
            }, content_type='multipart/form-data')
            self.assertEqual(res.status_code, 200, f"Valid format {fmt} ({fname}) failed")
            data = res.get_json()
            self.assertTrue(data['success'])
            self.assertIn('disease', data)

        # 2. Invalid extensions are rejected
        invalid_extensions = ['malware.exe', 'script.sh', 'doc.pdf', 'data.txt', 'image.svg']
        for fname in invalid_extensions:
            res = self.client.post('/api/diagnose-disease', data={
                'leaf_photo': (io.BytesIO(b"dummy payload"), fname),
                'crop': 'tomato',
                'lang': 'en'
            }, content_type='multipart/form-data')
            self.assertEqual(res.status_code, 400, f"Expected rejection for invalid extension: {fname}")
            self.assertFalse(res.get_json()['success'])
            self.assertIn("not allowed", res.get_json().get('error', '').lower())

        # 3. Fake/non-image content with an image filename is rejected
        fake_payloads = [
            (b"fake leaf image content", "tomato_leaf.jpg"),
            (b"<!DOCTYPE html><html><script>alert(1)</script></html>", "evil.png"),
            (b"\x00\x00\x00\x00CORRUPT_BYTES", "broken.webp")
        ]
        for content, fname in fake_payloads:
            res = self.client.post('/api/diagnose-disease', data={
                'leaf_photo': (io.BytesIO(content), fname),
                'crop': 'tomato',
                'lang': 'en'
            }, content_type='multipart/form-data')
            self.assertEqual(res.status_code, 400, f"Expected rejection for fake content with name: {fname}")
            self.assertFalse(res.get_json()['success'])
            self.assertIn("not a valid image", res.get_json().get('error', '').lower())

        # 4. Missing file is rejected
        # Case A: No leaf_photo field in form
        res_missing = self.client.post('/api/diagnose-disease', data={
            'crop': 'tomato',
            'lang': 'en'
        }, content_type='multipart/form-data')
        self.assertEqual(res_missing.status_code, 400)
        self.assertFalse(res_missing.get_json()['success'])
        self.assertIn("no image file provided", res_missing.get_json().get('error', '').lower())

        # Case B: Empty filename
        res_empty_fname = self.client.post('/api/diagnose-disease', data={
            'leaf_photo': (io.BytesIO(b""), ""),
            'crop': 'tomato',
            'lang': 'en'
        }, content_type='multipart/form-data')
        self.assertEqual(res_empty_fname.status_code, 400)
        self.assertFalse(res_empty_fname.get_json()['success'])
        self.assertIn("no image file provided", res_empty_fname.get_json().get('error', '').lower())

    def test_voice_assistant_xss_protection(self):
        # 1. Verify template contains escapeHtml helper and applies it in appendMessage
        with self.client.session_transaction() as sess:
            sess['language'] = 'en'
            sess['user'] = {'id': 1, 'name': 'Voice Farmer', 'email': 'voice@farmer.com'}

        res = self.client.get('/voice')
        self.assertEqual(res.status_code, 200)
        html = res.get_data(as_text=True)

        self.assertIn('function escapeHtml(text)', html)
        self.assertIn('const safeText = escapeHtml(rawText);', html)
        self.assertIn('let formatted = safeText', html)

        # 2. Logic verification mirroring the client-side escapeHtml and markdown pipeline
        def escape_html(text):
            if not text:
                return ''
            mapping = [
                ('&', '&amp;'),
                ('<', '&lt;'),
                ('>', '&gt;'),
                ('"', '&quot;'),
                ("'", '&#039;')
            ]
            res = str(text)
            for k, v in mapping:
                res = res.replace(k, v)
            return res

        import re
        def parse_voice_markdown(raw_text):
            safe = escape_html(raw_text)
            formatted = re.sub(r'^### (.*$)', r'<h4>\1</h4>', safe, flags=re.MULTILINE | re.IGNORECASE)
            formatted = re.sub(r'^## (.*$)', r'<h3>\1</h3>', formatted, flags=re.MULTILINE | re.IGNORECASE)
            formatted = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', formatted)
            formatted = re.sub(r'\*(.*?)\*', r'<em>\1</em>', formatted)
            formatted = formatted.replace('\n\n', '<br><br>').replace('\n', '<br>')
            return formatted

        xss_payloads = [
            "<script>alert(1)</script>",
            "<img src=x onerror=alert(1)>",
            "\"><svg onload=alert(1)>",
            "' onfocus='alert(1)"
        ]

        for payload in xss_payloads:
            sanitized = parse_voice_markdown(payload)
            # Ensure raw dangerous characters and unescaped tags are not present
            self.assertNotIn('<script>', sanitized)
            self.assertNotIn('<img', sanitized)
            self.assertNotIn('<svg', sanitized)
            # Ensure proper HTML entity escaping
            if '<' in payload:
                self.assertIn('&lt;', sanitized)
            if '>' in payload:
                self.assertIn('&gt;', sanitized)
            if '"' in payload:
                self.assertIn('&quot;', sanitized)
            if "'" in payload:
                self.assertIn('&#039;', sanitized)

        # 3. Verify legitimate Markdown works as expected
        md_heading3 = parse_voice_markdown("### Heading 3")
        self.assertIn("<h4>Heading 3</h4>", md_heading3)

        md_heading2 = parse_voice_markdown("## Heading 2")
        self.assertIn("<h3>Heading 2</h3>", md_heading2)

        md_bold = parse_voice_markdown("**bold advice**")
        self.assertIn("<strong>bold advice</strong>", md_bold)

        md_italic = parse_voice_markdown("*italic advice*")
        self.assertIn("<em>italic advice</em>", md_italic)

        md_breaks = parse_voice_markdown("Line 1\nLine 2")
        self.assertIn("Line 1<br>Line 2", md_breaks)

        # 4. Verify mixed Markdown with XSS payload
        mixed = parse_voice_markdown("**Warning:** <script>alert('hack')</script>")
        self.assertIn("<strong>Warning:</strong>", mixed)
        self.assertIn("&lt;script&gt;", mixed)
        self.assertNotIn("<script>", mixed)

        # 5. Verify backend voice assistant API handles XSS query payloads safely
        api_res = self.client.post('/api/voice-assistant', json={'query': '<script>alert(1)</script>', 'lang': 'en'})
        self.assertEqual(api_res.status_code, 200)
        self.assertTrue('text' in api_res.get_json())

    def test_csrf_token_generation_and_storage(self):
        # 1. Calling GET on a template initializes CSRF token in session
        res = self.client.get('/login')
        self.assertEqual(res.status_code, 200)

        with self.client.session_transaction() as sess:
            self.assertIn('_csrf_token', sess)
            csrf_token = sess['_csrf_token']
            self.assertIsInstance(csrf_token, str)
            # 32 bytes hex format = 64 characters
            self.assertEqual(len(csrf_token), 64)
            self.assertTrue(all(c in '0123456789abcdef' for c in csrf_token))

    def test_csrf_templates_render_hidden_inputs(self):
        # 1. /login contains CSRF input
        res_login = self.client.get('/login')
        self.assertEqual(res_login.status_code, 200)
        self.assertIn('<input type="hidden" name="csrf_token"', res_login.get_data(as_text=True))

        # 2. /language contains CSRF input
        res_lang = self.client.get('/language')
        self.assertEqual(res_lang.status_code, 200)
        self.assertIn('<input type="hidden" name="csrf_token"', res_lang.get_data(as_text=True))

        # Authenticated session for protected templates
        with self.client.session_transaction() as sess:
            sess['language'] = 'en'
            sess['user'] = {'id': 1, 'name': 'CSRF Farmer', 'email': 'csrf@farmer.com'}

        # 3. /profile contains CSRF input
        res_profile = self.client.get('/profile')
        self.assertEqual(res_profile.status_code, 200)
        self.assertIn('<input type="hidden" name="csrf_token"', res_profile.get_data(as_text=True))

        # 4. /calendar contains CSRF input
        res_calendar = self.client.get('/calendar')
        self.assertEqual(res_calendar.status_code, 200)
        self.assertIn('<input type="hidden" name="csrf_token"', res_calendar.get_data(as_text=True))

        # 5. AJAX templates include X-CSRFToken headers
        for route in ['/reminders', '/disease', '/voice', '/weather']:
            res = self.client.get(route)
            self.assertEqual(res.status_code, 200)
            self.assertIn('X-CSRFToken', res.get_data(as_text=True))

    def test_csrf_protection_enforcement_and_rejection(self):
        # Temporarily enable CSRF protection by disabling TESTING mode
        app.config['TESTING'] = False
        try:
            token = secrets.token_hex(32)
            user = database.save_user('csrf.enforce@gmail.com', 'CSRF Enforce')

            with self.client.session_transaction() as sess:
                sess['_csrf_token'] = token
                sess['user'] = user

            # A. Rejection of Missing CSRF token (HTTP 403) across state-changing API routes
            api_endpoints = [
                ('POST', '/api/reminders', {'title': 'Weed Farm', 'category': 'general'}),
                ('PUT', '/api/reminders', {'id': 1, 'status': 'completed'}),
                ('DELETE', '/api/reminders?id=1', None),
                ('POST', '/api/location/save', {'lat': 19.99, 'lon': 73.78}),
                ('POST', '/api/voice-assistant', {'query': 'test pest', 'lang': 'en'}),
                ('POST', '/api/diagnose-disease', {'crop': 'wheat'}),
                ('POST', '/api/auth/google', {'name': 'test', 'email': 'test@test.com'}),
            ]

            for method, path, payload in api_endpoints:
                if method == 'POST':
                    res = self.client.post(path, json=payload if payload else {})
                elif method == 'PUT':
                    res = self.client.put(path, json=payload if payload else {})
                elif method == 'DELETE':
                    res = self.client.delete(path)
                self.assertEqual(res.status_code, 403, f"Expected 403 for {method} {path} without CSRF token")
                data = res.get_json()
                self.assertFalse(data.get('success', True))
                self.assertEqual(data.get('error'), 'CSRF token missing or invalid')

            # B. Rejection of Missing CSRF token (HTTP 403) across HTML form routes
            form_endpoints = [
                ('/language', {'language': 'hi'}),
                ('/login', {'email': 'farmer@gmail.com'}),
                ('/profile', {'name': 'New Name'}),
                ('/calendar', {'crop': 'wheat'}),
                ('/resend-verification', {'email': 'unverified@test.com'}),
            ]
            for path, form_data in form_endpoints:
                res_form = self.client.post(path, data=form_data)
                self.assertEqual(res_form.status_code, 403, f"Expected 403 for form POST {path} without CSRF token")

            # C. Rejection of Tampered / Invalid CSRF tokens (HTTP 403)
            res_bad_hdr = self.client.post(
                '/api/reminders',
                json={'title': 'Test'},
                headers={'X-CSRFToken': 'tampered_invalid_hex_token_12345'}
            )
            self.assertEqual(res_bad_hdr.status_code, 403)
            self.assertEqual(res_bad_hdr.get_json().get('error'), 'CSRF token missing or invalid')

            res_bad_form = self.client.post(
                '/language',
                data={'language': 'hi', 'csrf_token': 'wrong_token'}
            )
            self.assertEqual(res_bad_form.status_code, 403)

            # D. Acceptance of Legitimate CSRF token via X-CSRFToken header
            res_valid_hdr = self.client.post(
                '/api/reminders',
                json={'title': 'Authorized Reminder', 'category': 'irrigation'},
                headers={'X-CSRFToken': token}
            )
            self.assertEqual(res_valid_hdr.status_code, 200)
            self.assertTrue(res_valid_hdr.get_json().get('success'))

            # E. Acceptance of Legitimate CSRF token via form field
            res_valid_form = self.client.post(
                '/language',
                data={'language': 'mr', 'csrf_token': token}
            )
            self.assertEqual(res_valid_form.status_code, 302)

            # F. Acceptance of Legitimate CSRF token via JSON body fallback
            res_valid_json = self.client.post(
                '/api/location/save',
                json={'lat': 19.9975, 'lon': 73.7898, 'csrf_token': token}
            )
            self.assertEqual(res_valid_json.status_code, 200)
            self.assertTrue(res_valid_json.get_json().get('success'))

        finally:
            # Strictly restore TESTING mode so subsequent tests are unaffected
            app.config['TESTING'] = True

    def test_session_cookie_flags_in_response(self):
        """SEC-05: Ensure session cookie security flags are configured and enforced in responses."""
        self.assertTrue(app.config.get('SESSION_COOKIE_HTTPONLY'))
        self.assertEqual(app.config.get('SESSION_COOKIE_SAMESITE'), 'Lax')

        # When accessing /login, the session creates or refreshes the session cookie
        res = self.client.get('/login')
        set_cookie = res.headers.get('Set-Cookie', '')
        self.assertIn('HttpOnly', set_cookie)
        self.assertIn('SameSite=Lax', set_cookie)

    def test_production_missing_secret_key_refuses_startup(self):
        """SEC-05: Ensure missing or empty SECRET_KEY in production aborts startup with RuntimeError."""
        env = os.environ.copy()
        env['FLASK_ENV'] = 'production'
        env.pop('SECRET_KEY', None)
        cmd = [sys.executable, '-c', 'from app import app']
        proc = subprocess.run(cmd, env=env, capture_output=True, text=True)
        self.assertNotEqual(proc.returncode, 0)
        self.assertIn('CRITICAL SECURITY ERROR: SECRET_KEY must be set in production environment!', proc.stderr)

    def test_production_valid_secret_key_adopted(self):
        """SEC-05: Ensure production environment with valid SECRET_KEY adopts key and enables Secure cookie flag."""
        env = os.environ.copy()
        env['FLASK_ENV'] = 'production'
        env['SECRET_KEY'] = 'test-prod-secret-key-12345'
        code = 'from app import app; print(app.secret_key); print(app.config["SESSION_COOKIE_SECURE"])'
        cmd = [sys.executable, '-c', code]
        proc = subprocess.run(cmd, env=env, capture_output=True, text=True)
        self.assertEqual(proc.returncode, 0)
        output_lines = proc.stdout.strip().splitlines()
        self.assertEqual(output_lines[0], 'test-prod-secret-key-12345')
        self.assertEqual(output_lines[1], 'True')

    def test_dev_fallback_secret_key_randomness(self):
        """SEC-05: Ensure development fallback key is cryptographically random and changes across processes."""
        env = os.environ.copy()
        env.pop('FLASK_ENV', None)
        env.pop('SECRET_KEY', None)
        code = 'from app import app; print(app.secret_key)'
        cmd = [sys.executable, '-c', code]

        proc1 = subprocess.run(cmd, env=env, capture_output=True, text=True)
        proc2 = subprocess.run(cmd, env=env, capture_output=True, text=True)

        self.assertEqual(proc1.returncode, 0)
        self.assertEqual(proc2.returncode, 0)
        key1 = proc1.stdout.strip()
        key2 = proc2.stdout.strip()

        self.assertTrue(key1.startswith('krishi-sahayak-dev-key-'))
        self.assertTrue(key2.startswith('krishi-sahayak-dev-key-'))
        self.assertNotEqual(key1, key2)

    def test_sec06_resend_verification_uniformity(self):
        """SEC-06: Verify /resend-verification returns uniform neutral response without leaking account state."""
        # 1. Registered + unverified email
        unverified_email = f"unverified_{secrets.token_hex(4)}@example.com"
        initial_token = "init_token_" + secrets.token_hex(8)
        database.create_user_with_password(
            email=unverified_email,
            name="Unverified Farmer",
            password_hash=generate_password_hash("StrongPass123"),
            verification_token=initial_token,
            token_created_at=datetime.datetime.utcnow().isoformat(),
            is_verified=0
        )

        # 2. Registered + verified email
        verified_email = f"verified_{secrets.token_hex(4)}@example.com"
        database.create_user_with_password(
            email=verified_email,
            name="Verified Farmer",
            password_hash=generate_password_hash("StrongPass123"),
            verification_token="token_verified",
            token_created_at=datetime.datetime.utcnow().isoformat(),
            is_verified=1
        )

        # 3. Unregistered email
        unregistered_email = f"nonexistent_{secrets.token_hex(4)}@example.com"

        expected_msg = "If that email is registered and unverified, a fresh verification link has been sent."

        # Test all three scenarios
        res_unverified = self.client.post('/resend-verification', data={'email': unverified_email})
        res_verified = self.client.post('/resend-verification', data={'email': verified_email})
        res_unregistered = self.client.post('/resend-verification', data={'email': unregistered_email})

        # Uniform HTTP status code
        self.assertEqual(res_unverified.status_code, 200)
        self.assertEqual(res_verified.status_code, 200)
        self.assertEqual(res_unregistered.status_code, 200)

        # Uniform alert message
        html_unverified = res_unverified.get_data(as_text=True)
        html_verified = res_verified.get_data(as_text=True)
        html_unregistered = res_unregistered.get_data(as_text=True)

        self.assertIn(expected_msg, html_unverified)
        self.assertIn(expected_msg, html_verified)
        self.assertIn(expected_msg, html_unregistered)

        # Zero dev_verify_link leakage
        self.assertNotIn("Verify Email Link (Instant Test)", html_unverified)
        self.assertNotIn("Verify Email Link (Instant Test)", html_verified)
        self.assertNotIn("Verify Email Link (Instant Test)", html_unregistered)

        # Legitimate unverified token was still refreshed in the database
        user_after = database.get_user_by_email(unverified_email)
        self.assertNotEqual(user_after['verification_token'], initial_token)

    def test_sec06_login_failure_uniformity(self):
        """SEC-06: Ensure login failure message is strictly uniform between nonexistent and incorrect password."""
        # 1. Nonexistent user
        ghost_email = f"ghost_{secrets.token_hex(4)}@example.com"
        res_no_user = self.client.post('/login', data={
            'action': 'login',
            'email': ghost_email,
            'password': 'SomePassword123'
        })

        # 2. Existing user with wrong password
        real_email = f"real_{secrets.token_hex(4)}@example.com"
        database.create_user_with_password(
            email=real_email,
            name="Real Farmer",
            password_hash=generate_password_hash("CorrectPassword123"),
            verification_token="token_real",
            token_created_at=datetime.datetime.utcnow().isoformat(),
            is_verified=1
        )
        res_bad_pw = self.client.post('/login', data={
            'action': 'login',
            'email': real_email,
            'password': 'WrongPassword999'
        })

        self.assertEqual(res_no_user.status_code, 200)
        self.assertEqual(res_bad_pw.status_code, 200)

        expected_msg = "Invalid email or password. Please check your credentials."
        self.assertIn(expected_msg, res_no_user.get_data(as_text=True))
        self.assertIn(expected_msg, res_bad_pw.get_data(as_text=True))

    def test_sec06_registration_enumeration_prevention(self):
        """SEC-06: Ensure attempting registration with existing email does not confirm account existence."""
        existing_email = f"existing_{secrets.token_hex(4)}@example.com"
        database.create_user_with_password(
            email=existing_email,
            name="Existing Farmer",
            password_hash=generate_password_hash("Pass123456"),
            verification_token="token_reg",
            token_created_at=datetime.datetime.utcnow().isoformat(),
            is_verified=1
        )

        res = self.client.post('/login', data={
            'action': 'register',
            'name': 'Duplicate Registrant',
            'email': existing_email,
            'password': 'Pass123456',
            'confirm_password': 'Pass123456'
        })

        self.assertEqual(res.status_code, 200)
        html = res.get_data(as_text=True)

        # Must NOT leak that the email address is already registered
        self.assertNotIn("This email address is already registered", html)
        self.assertIn("If that email is not already registered", html)
        self.assertNotIn("Verify Email Link (Instant Test)", html)

    def test_sec06_legitimate_registration_and_verification_regression(self):
        """SEC-06: Ensure legitimate new user registration, token verification and login continue working."""
        new_email = f"legit_{secrets.token_hex(4)}@example.com"
        res_reg = self.client.post('/login', data={
            'action': 'register',
            'name': 'Legit Farmer',
            'email': new_email,
            'password': 'ValidPassword123',
            'confirm_password': 'ValidPassword123'
        })
        self.assertEqual(res_reg.status_code, 200)
        self.assertIn("Registration successful!", res_reg.get_data(as_text=True))

        # Check DB
        user = database.get_user_by_email(new_email)
        self.assertIsNotNone(user)
        self.assertEqual(user['is_verified'], 0)
        token = user['verification_token']
        self.assertTrue(token)

        # Click verification link
        res_verify = self.client.get(f'/verify-email/{token}', follow_redirects=False)
        self.assertEqual(res_verify.status_code, 302)
        self.assertIn('/login?verified=1', res_verify.location)

        user_verified = database.get_user_by_email(new_email)
        self.assertEqual(user_verified['is_verified'], 1)

        # Legitimate login with new credentials
        res_login = self.client.post('/login', data={
            'action': 'login',
            'email': new_email,
            'password': 'ValidPassword123'
        }, follow_redirects=False)
        self.assertEqual(res_login.status_code, 302)
        self.assertIn('/', res_login.location)

    def test_be02_database_import_no_side_effects(self):
        """BE-02: Ensure importing database alone produces zero database connection and DDL side effects."""
        code = '''
import sqlite3
connect_calls = []
orig_connect = sqlite3.connect
def spy_connect(*args, **kwargs):
    connect_calls.append(args)
    return orig_connect(*args, **kwargs)
sqlite3.connect = spy_connect

import database
print(f"BEFORE_INIT={len(connect_calls)}")
database.init_db()
print(f"AFTER_INIT={len(connect_calls)}")
'''
        cmd = [sys.executable, '-c', code]
        proc = subprocess.run(cmd, capture_output=True, text=True)
        self.assertEqual(proc.returncode, 0)
        self.assertIn("BEFORE_INIT=0", proc.stdout)
        self.assertIn("AFTER_INIT=1", proc.stdout)

    def test_be02_explicit_app_initialization_tables_exist(self):
        """BE-02: Ensure explicit app bootstrap initializes the database schema and required tables."""
        code = '''
from app import app
import database
conn = database.get_db_connection()
tables = [row[0] for row in conn.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()]
conn.close()
print(",".join(tables))
'''
        cmd = [sys.executable, '-c', code]
        proc = subprocess.run(cmd, capture_output=True, text=True)
        self.assertEqual(proc.returncode, 0)
        tables = proc.stdout.strip().split(',')
        self.assertIn("users", tables)
        self.assertIn("reminders", tables)
        self.assertIn("crop_progress", tables)

    def test_be02_init_db_idempotency_hardening_and_data_preservation(self):
        """BE-02: Verify SQLite WAL mode, foreign keys, idempotency, and data preservation across init_db."""
        # 1. Verify WAL mode and foreign keys on connection
        conn = database.get_db_connection()
        try:
            journal_mode = conn.execute("PRAGMA journal_mode;").fetchone()[0]
            self.assertEqual(journal_mode.lower(), "wal")
            foreign_keys = conn.execute("PRAGMA foreign_keys;").fetchone()[0]
            self.assertEqual(foreign_keys, 1)
        finally:
            conn.close()

        # 2. Verify idempotency - sequential init_db calls cause no error or lock
        database.init_db()
        database.init_db()
        database.init_db()

        # 3. Verify data preservation across init_db
        test_email = f"preserve_{secrets.token_hex(4)}@example.com"
        db_user = database.save_user(test_email, "Preserve User")
        self.assertIsNotNone(db_user)

        # Run init_db again
        database.init_db()

        # Verify existing record remains intact
        retrieved = database.get_user_by_email(test_email)
        self.assertIsNotNone(retrieved)
        self.assertEqual(retrieved['email'], test_email)
        self.assertEqual(retrieved['name'], "Preserve User")

    def test_be03_weather_cache_hit_and_language_key_specificity(self):
        """BE-03: Verify get_weather_forecast caches results, reuses entries, and separates by language."""
        clear_weather_caches()
        lat, lon = 18.5204, 73.8567

        # 1. First call: populates cache for English
        res_en_1 = get_weather_forecast(lat, lon, lang="en")
        self.assertTrue(res_en_1.get("success", False))

        # 2. Second call with same lat, lon, lang: should be served from cache without HTTP request
        with patch("requests.get") as mock_get:
            res_en_2 = get_weather_forecast(lat, lon, lang="en")
            # Zero external HTTP calls
            mock_get.assert_not_called()
            self.assertEqual(res_en_1["current"]["temp"], res_en_2["current"]["temp"])
            self.assertEqual(res_en_1["current"]["condition"], res_en_2["current"]["condition"])

        # 3. Third call with Hindi (hi): produces separate language cache entry
        with patch("requests.get") as mock_get:
            mock_resp = MagicMock()
            mock_resp.json.return_value = {
                "current": {"temperature_2m": 29, "relative_humidity_2m": 55, "weather_code": 0},
                "hourly": {
                    "time": ["2026-06-01T00:00"],
                    "temperature_2m": [29],
                    "relative_humidity_2m": [55],
                    "precipitation_probability": [0],
                    "precipitation": [0],
                    "wind_speed_10m": [5],
                    "wind_direction_10m": [90],
                    "weather_code": [0]
                },
                "daily": {
                    "time": ["2026-06-01"],
                    "weather_code": [0],
                    "temperature_2m_max": [32],
                    "temperature_2m_min": [20],
                    "precipitation_probability_max": [5],
                    "precipitation_sum": [0],
                    "uv_index_max": [7],
                    "sunrise": ["06:00"],
                    "sunset": ["18:30"]
                }
            }
            mock_resp.raise_for_status = MagicMock()
            mock_get.return_value = mock_resp

            res_hi = get_weather_forecast(lat, lon, lang="hi")
            # HTTP call occurred because Hindi is a distinct cache key
            self.assertEqual(mock_get.call_count, 1)
            self.assertIn("साफ आसमान", res_hi["current"]["condition"])

    def test_be03_weather_ttl_expiration_and_stale_fallback(self):
        """BE-03: Verify TTL expiration triggers fresh request and stale cache is used as resilience fallback."""
        clear_weather_caches()
        lat, lon = 21.1458, 79.0882  # Nagpur

        # Populate cache
        res_initial = get_weather_forecast(lat, lon, lang="en")
        self.assertTrue(res_initial.get("success", False))

        # Simulate TTL expiration (>600 seconds) by modifying cache timestamp
        cache_key = (round(lat, 2), round(lon, 2), "en")
        with _WEATHER_CACHE._lock:
            ts, val = _WEATHER_CACHE._cache[cache_key]
            _WEATHER_CACHE._cache[cache_key] = (ts - 601, val)

        # Stale Fallback Verification: When refresh request encounters network exception, return stale cache
        with patch("requests.get", side_effect=Exception("Network Connection Failed")):
            res_fallback = get_weather_forecast(lat, lon, lang="en")
            # Returns the previously cached data rather than generic failure
            self.assertEqual(res_fallback["lat"], lat)
            self.assertEqual(res_fallback["lon"], lon)
            self.assertEqual(res_fallback["current"]["temp"], res_initial["current"]["temp"])

    def test_be03_reverse_geocoding_and_search_locations_cache(self):
        """BE-03: Verify reverse_geocode and search_locations cache results across repeated lookups."""
        clear_weather_caches()

        # 1. Reverse Geocode caching
        with patch("requests.get") as mock_get:
            mock_resp = MagicMock()
            mock_resp.json.return_value = {"address": {"city": "Nashik", "state": "Maharashtra"}}
            mock_resp.raise_for_status = MagicMock()
            mock_get.return_value = mock_resp

            # Call twice with equivalent coordinates (within 3 decimal places)
            name1 = reverse_geocode(19.9974, 73.7899)
            name2 = reverse_geocode(19.9974, 73.7899)

            self.assertEqual(mock_get.call_count, 1)
            self.assertEqual(name1, name2)
            self.assertEqual(name1, "Nashik, Maharashtra")

        # 2. Search Locations caching
        with patch("requests.get") as mock_get:
            mock_resp = MagicMock()
            mock_resp.json.return_value = {
                "results": [
                    {"name": "Baramati", "admin1": "Maharashtra", "country": "India", "latitude": 18.15, "longitude": 74.57}
                ]
            }
            mock_resp.raise_for_status = MagicMock()
            mock_get.return_value = mock_resp

            # Call twice with case/whitespace variations
            res1 = search_locations("Baramati ")
            res2 = search_locations(" baramati")

            self.assertEqual(mock_get.call_count, 1)
            self.assertEqual(len(res1), 1)
            self.assertEqual(res1[0]["name"], res2[0]["name"])

    def test_be03_cache_bounds_and_deterministic_eviction(self):
        """BE-03: Verify cache size cannot exceed maxsize and oldest entries are deterministically evicted."""
        clear_weather_caches()
        from weather_service import TTLCache
        small_cache = TTLCache(maxsize=3, default_ttl=600)

        small_cache.set("k1", "v1")
        time.sleep(0.01)
        small_cache.set("k2", "v2")
        time.sleep(0.01)
        small_cache.set("k3", "v3")

        self.assertEqual(len(small_cache), 3)

        # Insert 4th element - should evict "k1" (oldest)
        time.sleep(0.01)
        small_cache.set("k4", "v4")

        self.assertEqual(len(small_cache), 3)
        self.assertIsNone(small_cache.get("k1")[0])  # Evicted
        self.assertEqual(small_cache.get("k2")[0], "v2")  # Preserved
        self.assertEqual(small_cache.get("k4")[0], "v4")  # New

    def test_perf01_hero_video_optimization_and_size_bounds(self):
        """PERF-01: Verify hero background video and poster exist and meet size constraints."""
        import os
        video_path = os.path.join(app.root_path, "static", "videos", "agrovia-crops.mp4")
        poster_path = os.path.join(app.root_path, "static", "videos", "agrovia-crops-poster.jpg")

        # 1. Assert assets exist
        self.assertTrue(os.path.isfile(video_path), "Optimized video file must exist")
        self.assertTrue(os.path.isfile(poster_path), "Hero poster image file must exist")

        # 2. Assert optimized video size is <= 5 MB
        video_size = os.path.getsize(video_path)
        max_video_size = 5 * 1024 * 1024  # 5 MB threshold
        self.assertLessEqual(
            video_size,
            max_video_size,
            f"Optimized video size ({video_size} bytes / {video_size / (1024 * 1024):.2f} MB) must be <= 5 MB"
        )
        # Ensure it is not empty
        self.assertGreater(video_size, 500 * 1024, "Video must be a valid encoded media stream")

        # 3. Assert poster size is < 150 KB
        poster_size = os.path.getsize(poster_path)
        max_poster_size = 150 * 1024  # 150 KB threshold
        self.assertLessEqual(
            poster_size,
            max_poster_size,
            f"Poster size ({poster_size} bytes / {poster_size / 1024:.2f} KB) must be <= 150 KB"
        )
        self.assertGreater(poster_size, 10 * 1024, "Poster must be a valid image")

    def test_perf01_homepage_hero_video_element_attributes(self):
        """PERF-01: Verify GET / renders video tag with poster, preload='metadata', and playback attributes."""
        with self.client.session_transaction() as sess:
            db_user = database.save_user("hero.test@example.com", "Hero Test User")
            sess["user"] = db_user
            sess["language"] = "en"

        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        html = response.data.decode("utf-8")

        # Verify video element attributes
        self.assertIn('preload="metadata"', html, "Video element must use preload='metadata'")
        self.assertNotIn('preload="auto"', html, "Video element must not use preload='auto'")
        self.assertIn('poster="/static/videos/agrovia-crops-poster.jpg"', html, "Video element must specify poster image")
        self.assertIn('autoplay', html)
        self.assertIn('muted', html)
        self.assertIn('loop', html)
        self.assertIn('playsinline', html)
        self.assertIn('/static/videos/agrovia-crops.mp4', html)

        # Verify homepage core structure is preserved
        self.assertIn('hero-section', html)
        self.assertIn('hero-overlay', html)
        self.assertIn('hero-actions', html)

    def test_perf02_stylesheet_integrity_and_balance(self):
        """PERF-02: Verify style.css exists, is not empty, has balanced braces, and contains core selectors."""
        import os
        css_path = os.path.join(app.root_path, "static", "style.css")
        self.assertTrue(os.path.isfile(css_path), "style.css must exist in static directory")

        with open(css_path, "r", encoding="utf-8") as f:
            css_content = f.read()

        # 1. Not empty or truncated
        self.assertGreater(len(css_content), 100000, "style.css must not be empty or truncated")

        # 2. Balanced braces
        open_braces = css_content.count("{")
        close_braces = css_content.count("}")
        self.assertEqual(open_braces, close_braces, f"CSS braces must be balanced: {open_braces} open != {close_braces} close")

        # 3. Core selectors present
        core_selectors = [".navbar", ".hero-section", ".hero-video", ".button", ".card"]
        for selector in core_selectors:
            self.assertIn(selector, css_content, f"Core selector '{selector}' must exist in style.css")

        # 4. Static asset HTTP loadability
        res_css = self.client.get("/static/style.css")
        self.assertEqual(res_css.status_code, 200, "Static asset request for style.css must return HTTP 200")
        self.assertIn("text/css", res_css.content_type)
        res_css.close()

    def test_perf02_core_selectors_and_route_rendering(self):
        """PERF-02: Verify core routes render with valid style.css link and key components intact."""
        routes_to_check = ["/weather", "/crops", "/voice"]
        for route in routes_to_check:
            res = self.client.get(route)
            self.assertEqual(res.status_code, 200, f"Route {route} must return HTTP 200")
            html = res.data.decode("utf-8")
            self.assertIn("style.css", html, f"Route {route} must reference style.css")

    def test_a11y01_skip_link_navigation_and_target_elements(self):
        """A11Y-01: Verify shared navigation contains skip link pointing to #mainContent, and pages contain exactly one target."""
        import os
        nav_path = os.path.join(app.root_path, "templates", "nav.html")
        with open(nav_path, "r", encoding="utf-8") as f:
            nav_html = f.read()

        # 1. Nav template contains skip link
        self.assertIn('class="skip-link"', nav_html)
        self.assertIn('href="#mainContent"', nav_html)

        # 2. Rendered pages check
        with self.client.session_transaction() as sess:
            db_user = database.save_user("a11y.tester@example.com", "A11y Tester")
            sess["user"] = db_user
            sess["language"] = "en"

        pages_to_test = ["/", "/weather", "/crops", "/calendar", "/voice", "/schemes", "/reminders"]
        for path in pages_to_test:
            res = self.client.get(path)
            self.assertEqual(res.status_code, 200, f"Page {path} must return 200")
            html = res.data.decode("utf-8")

            # Must contain skip link
            self.assertIn('href="#mainContent"', html, f"Page {path} must render skip link")
            self.assertIn('class="skip-link"', html, f"Page {path} must render skip-link class")

            # Must contain exactly ONE id="mainContent" target
            main_count = html.count('id="mainContent"')
            self.assertEqual(main_count, 1, f"Page {path} must contain exactly 1 id='mainContent' (found {main_count})")

    def test_a11y01_skip_link_css_and_styling(self):
        """A11Y-01: Verify skip-link CSS is present, off-screen by default, and visible on focus."""
        import os
        css_path = os.path.join(app.root_path, "static", "style.css")
        with open(css_path, "r", encoding="utf-8") as f:
            css = f.read()

        self.assertIn(".skip-link", css)
        self.assertIn(".skip-link:focus", css)
        self.assertIn("outline", css)

    def test_a11y02_mobile_menu_toggle_aria_attributes_and_sync(self):
        """A11Y-02: Verify #mobileMenuToggle defines aria-expanded='false', aria-controls='navLinks', and sync JS."""
        import os
        nav_path = os.path.join(app.root_path, "templates", "nav.html")
        with open(nav_path, "r", encoding="utf-8") as f:
            nav_html = f.read()

        # 1. Template markup contains ARIA attributes
        self.assertIn('id="mobileMenuToggle"', nav_html)
        self.assertIn('aria-expanded="false"', nav_html)
        self.assertIn('aria-controls="navLinks"', nav_html)

        # 2. Template JavaScript contains aria-expanded state synchronization logic
        self.assertIn("toggle.setAttribute('aria-expanded', isOpen ? 'true' : 'false');", nav_html)

        # 3. Rendered pages include the ARIA-enabled toggle
        routes_to_test = ["/weather", "/calendar", "/crops"]
        for route in routes_to_test:
            res = self.client.get(route)
            self.assertEqual(res.status_code, 200)
            html = res.data.decode("utf-8")
            self.assertIn('id="mobileMenuToggle"', html)
            self.assertIn('aria-expanded="false"', html)
            self.assertIn('aria-controls="navLinks"', html)

    def test_a11y03_dropdown_escape_key_listener(self):
        """A11Y-03: Verify Escape keydown listener closes open dropdowns, updates aria-expanded, and restores focus.
        (Note: Source-level template and rendered-page verification)."""
        import os
        nav_path = os.path.join(app.root_path, "templates", "nav.html")
        with open(nav_path, "r", encoding="utf-8") as f:
            nav_html = f.read()

        # 1. Template contains Escape keydown listener
        self.assertIn("document.addEventListener('keydown', function(e)", nav_html)
        self.assertIn("if (e.key === 'Escape')", nav_html)

        # 2. toolsMenu Escape handling: closes menu, resets aria-expanded, restores focus to trigger
        self.assertIn("toolsMenu.classList.remove('show');", nav_html)
        self.assertIn("toolsBtn.setAttribute('aria-expanded', 'false');", nav_html)
        self.assertIn("toolsBtn.focus();", nav_html)

        # 3. langMenu Escape handling: closes menu, resets aria-expanded, restores focus to trigger
        self.assertIn("langMenu.classList.remove('show');", nav_html)
        self.assertIn("langBtn.setAttribute('aria-expanded', 'false');", nav_html)
        self.assertIn("langBtn.focus();", nav_html)

        # 4. userProfileMenu Escape handling: closes menu, resets aria-expanded, restores focus to trigger
        self.assertIn("userProfileMenu.classList.remove('show');", nav_html)
        self.assertIn("userProfileBtn.setAttribute('aria-expanded', 'false');", nav_html)
        self.assertIn("userProfileBtn.focus();", nav_html)

        # 5. Rendered pages include the Escape listener and focus restore logic
        routes_to_test = ["/weather", "/calendar", "/crops"]
        for route in routes_to_test:
            res = self.client.get(route)
            self.assertEqual(res.status_code, 200)
            html = res.data.decode("utf-8")
            self.assertIn("e.key === 'Escape'", html)
            self.assertIn("toolsBtn.focus();", html)
            self.assertIn("langBtn.focus();", html)
            self.assertIn("userProfileBtn.focus();", html)

    def test_a11y04_voice_assistant_chat_aria_live_attributes(self):
        """A11Y-04: Verify #chatMessages in templates/voice.html and GET /voice has role='log' and aria-live='polite'."""
        import os
        voice_path = os.path.join(app.root_path, "templates", "voice.html")
        with open(voice_path, "r", encoding="utf-8") as f:
            voice_html = f.read()

        # 1. Template source checks
        self.assertIn('id="chatMessages"', voice_html)
        self.assertIn('role="log"', voice_html)
        self.assertIn('aria-live="polite"', voice_html)
        self.assertIn('<div class="chat-messages" id="chatMessages" role="log" aria-live="polite">', voice_html)

        # 2. Rendered route check
        res = self.client.get('/voice')
        self.assertEqual(res.status_code, 200)
        html = res.data.decode("utf-8")
        self.assertIn('id="chatMessages"', html)
        self.assertIn('role="log"', html)
        self.assertIn('aria-live="polite"', html)
        self.assertIn('<div class="chat-messages" id="chatMessages" role="log" aria-live="polite">', html)

    def test_a11y05_tools_dropdown_touch_target_size(self):
        """A11Y-05 / UIUX-05: Verify .nav-dropdown-item rule provides at least 44px touch target height and no 40px restriction."""
        import os
        import re
        css_path = os.path.join(app.root_path, "static", "style.css")
        with open(css_path, "r", encoding="utf-8") as f:
            css = f.read()

        # Find all .nav-dropdown-item rule declarations
        matches = re.findall(r'\.nav-dropdown-item\s*\{([^}]+)\}', css)
        self.assertTrue(len(matches) > 0, "Stylesheet must contain at least one .nav-dropdown-item rule")

        # The last rule in the stylesheet is the active override
        active_rule = matches[-1]

        # 1. Active rule must declare at least 44px height or min-height
        has_min_height_44 = bool(re.search(r'min-height:\s*44px', active_rule))
        has_height_44 = bool(re.search(r'height:\s*44px', active_rule))
        self.assertTrue(has_min_height_44 or has_height_44,
                        f"Active .nav-dropdown-item rule must provide at least 44px target height. Found: {active_rule}")

        # 2. Active rule must NOT contain the old undersized 40px height declaration
        self.assertNotIn('height: 40px', active_rule,
                         "Active .nav-dropdown-item rule must not contain undersized 40px height")

    def test_uiux01_profitability_calculator_dynamic_unit_labels(self):
        """UIUX-01: Verify calendar template includes dynamic unit label bindings and hooks for #landUnit."""
        import os
        cal_path = os.path.join(app.root_path, "templates", "calendar.html")
        with open(cal_path, "r", encoding="utf-8") as f:
            cal_html = f.read()

        # 1. #landUnit exists
        self.assertIn('id="landUnit"', cal_html)

        # 2. Dynamic label/suffix hooks exist
        self.assertIn('id="yieldUnitLabel"', cal_html)
        self.assertIn('id="costUnitLabel"', cal_html)
        self.assertIn('id="costUnitSuffix"', cal_html)

        # 3. JavaScript contains unit synchronization logic
        self.assertIn("landUnitSelect.addEventListener('change'", cal_html)
        self.assertIn("updateUnitLabels", cal_html)
        self.assertIn("Expected Yield per Hectare", cal_html)
        self.assertIn("Cultivation Cost per Hectare", cal_html)
        self.assertIn("'/ Hectare'", cal_html)

        # 4. GET /calendar still returns HTTP 200
        res = self.client.get('/calendar')
        self.assertEqual(res.status_code, 200)
        html = res.data.decode("utf-8")
        self.assertIn('id="landUnit"', html)
        self.assertIn('id="yieldUnitLabel"', html)
        self.assertIn('id="costUnitLabel"', html)
        self.assertIn('id="costUnitSuffix"', html)

    def test_uiux02_weather_geolocation_fallback_banner(self):
        """UIUX-02: Verify weather template includes geolocation fallback status banner, a11y attributes, and trigger hooks."""
        import os
        weather_path = os.path.join(app.root_path, "templates", "weather.html")
        with open(weather_path, "r", encoding="utf-8") as f:
            weather_html = f.read()

        # 1. #geoFallbackBanner exists with accessibility attributes and hidden default state
        self.assertIn('id="geoFallbackBanner"', weather_html)
        self.assertIn('role="status"', weather_html)
        self.assertIn('aria-live="polite"', weather_html)
        self.assertIn('style="display: none;"', weather_html)

        # 2. Focus search and dismiss action buttons exist
        self.assertIn('id="btnFocusSearch"', weather_html)
        self.assertIn('id="btnDismissGeoBanner"', weather_html)

        # 3. JavaScript contains fallback activation logic and search focus hook
        self.assertIn('geoFallbackBanner', weather_html)
        self.assertIn('showFallbackBanner', weather_html)
        self.assertIn('btnFocusSearch.addEventListener', weather_html)
        self.assertIn('btnDismissGeoBanner.addEventListener', weather_html)
        self.assertIn('locationSearchInput', weather_html)

        # 4. GET /weather returns HTTP 200 and renders the banner element and localized strings
        res = self.client.get('/weather')
        self.assertEqual(res.status_code, 200)
        html = res.data.decode("utf-8")
        self.assertIn('id="geoFallbackBanner"', html)
        self.assertIn('role="status"', html)
        self.assertIn('aria-live="polite"', html)
        self.assertIn('Location access disabled', html)
        self.assertIn('Search District', html)

        # 5. Multilingual verification (Hindi)
        self.client.get('/set-language/hi')
        res_hi = self.client.get('/weather')
        self.assertEqual(res_hi.status_code, 200)
        html_hi = res_hi.data.decode("utf-8")
        self.assertIn('लोकेशन एक्सेस अक्षम है।', html_hi)
        self.assertIn('जिला खोजें', html_hi)

        # Reset language back to en
        self.client.get('/set-language/en')

    def test_uiux03_voice_assistant_unsupported_speech_card(self):
        """UIUX-03: Verify voice assistant template includes Web Speech API unsupported browser card and keyboard fallback."""
        import os
        voice_path = os.path.join(app.root_path, "templates", "voice.html")
        with open(voice_path, "r", encoding="utf-8") as f:
            voice_html = f.read()

        # 1. #speechUnsupportedCard exists with required accessibility attributes
        self.assertIn('id="speechUnsupportedCard"', voice_html)
        self.assertIn('role="status"', voice_html)
        self.assertIn('aria-live="polite"', voice_html)

        # 2. Text input fallback element and action exist
        self.assertIn('id="txtQueryInput"', voice_html)
        self.assertIn('focusTextInput', voice_html)
        self.assertIn('id="btnFocusTextFallback"', voice_html)

        # 3. Unsupported SpeechRecognition logic references #speechUnsupportedCard
        self.assertIn('speechUnsupportedCard', voice_html)

        # 4. Old native speech-not-supported alert is removed
        self.assertNotIn('alert("{{ t.speech_not_supported }}")', voice_html)
        self.assertNotIn("alert('{{ t.speech_not_supported }}')", voice_html)

        # 5. GET /voice returns HTTP 200 and renders the card
        res = self.client.get('/voice')
        self.assertEqual(res.status_code, 200)
        html = res.data.decode("utf-8")
        self.assertIn('id="speechUnsupportedCard"', html)
        self.assertIn('role="status"', html)
        self.assertIn('aria-live="polite"', html)
        self.assertIn('id="txtQueryInput"', html)

        # 6. Multilingual rendering verification
        self.client.get('/set-language/hi')
        res_hi = self.client.get('/voice')
        self.assertEqual(res_hi.status_code, 200)
        html_hi = res_hi.data.decode("utf-8")
        self.assertIn('इस ब्राउज़र में आवाज़ पहचान उपलब्ध नहीं है', html_hi)

        # Reset language back to en
        self.client.get('/set-language/en')

    def test_uiux04_disease_scan_confirmation_step(self):
        """UIUX-04: Verify disease template includes scan confirmation and cancellation buttons and deferred upload flow."""
        import os
        disease_path = os.path.join(app.root_path, "templates", "disease.html")
        with open(disease_path, "r", encoding="utf-8") as f:
            disease_html = f.read()

        # 1. Confirmation and cancellation elements exist
        self.assertIn('id="scanConfirmActions"', disease_html)
        self.assertIn('id="btnConfirmScan"', disease_html)
        self.assertIn('id="btnCancelScan"', disease_html)

        # 2. Flow separation: file change listener displays preview without immediate fetch
        self.assertIn('selectedLeafFile', disease_html)
        self.assertIn('btnConfirmScan.addEventListener', disease_html)
        self.assertIn('btnCancelScan.addEventListener', disease_html)
        self.assertIn('resetPhotoSelection', disease_html)

        # 3. GET /disease returns HTTP 200 and renders the buttons and localized strings
        res = self.client.get('/disease')
        self.assertEqual(res.status_code, 200)
        html = res.data.decode("utf-8")
        self.assertIn('id="btnConfirmScan"', html)
        self.assertIn('id="btnCancelScan"', html)
        self.assertIn('Analyze Leaf Photo', html)
        self.assertIn('Retake / Choose Another', html)

        # 4. Multilingual verification (Hindi)
        self.client.get('/set-language/hi')
        res_hi = self.client.get('/disease')
        self.assertEqual(res_hi.status_code, 200)
        html_hi = res_hi.data.decode("utf-8")
        self.assertIn('पत्ती की जांच करें', html_hi)
        self.assertIn('फोटो बदलें / रद्द करें', html_hi)

        # Reset language back to en
        self.client.get('/set-language/en')

    def test_sec_content_security_policy_headers(self):
        """SEC Section 6.3: Verify Content-Security-Policy (CSP) and existing security headers on application responses."""
        with self.client.session_transaction() as sess:
            db_user = database.save_user("csp.test@example.com", "CSP Tester")
            sess["user"] = db_user
            sess["language"] = "en"

        res = self.client.get('/')
        self.assertEqual(res.status_code, 200)

        # 1. Existing security headers remain intact
        self.assertEqual(res.headers.get("X-Content-Type-Options"), "nosniff")
        self.assertEqual(res.headers.get("X-Frame-Options"), "SAMEORIGIN")
        self.assertEqual(res.headers.get("Referrer-Policy"), "strict-origin-when-cross-origin")

        # 2. Content-Security-Policy header presence
        csp = res.headers.get("Content-Security-Policy")
        self.assertIsNotNone(csp, "Response must include Content-Security-Policy header")

        # 3. Core directives presence
        core_directives = [
            "default-src",
            "script-src",
            "style-src",
            "font-src",
            "img-src",
            "media-src",
            "connect-src",
            "frame-src",
            "frame-ancestors"
        ]
        for directive in core_directives:
            self.assertIn(directive, csp, f"CSP must include '{directive}' directive")

        # 4. Legitimate origins and sources permitted
        required_sources = [
            "'self'",
            "'unsafe-inline'",
            "https://accounts.google.com",
            "https://api.dicebear.com",
            "https://fonts.googleapis.com",
            "https://fonts.gstatic.com",
            "https://api.open-meteo.com",
            "https://nominatim.openstreetmap.org",
            "data:",
            "frame-ancestors 'self'"
        ]
        for src in required_sources:
            self.assertIn(src, csp, f"CSP must permit required source or clause '{src}'")

        # 5. Verify CSP is also returned on other routes (/login, /weather, /disease, /voice)
        for route in ['/login', '/weather', '/disease', '/voice']:
            resp = self.client.get(route)
            self.assertIn("Content-Security-Policy", resp.headers, f"Route {route} must return CSP header")

    def test_perf01_hero_video_reduced_motion_accessibility(self):
        """PERF-01 / Section 5.1 Item 4: Verify hero video and animations respect prefers-reduced-motion: reduce."""
        import os
        css_path = os.path.join(app.root_path, "static", "style.css")
        with open(css_path, "r", encoding="utf-8") as f:
            css = f.read()

        # 1. Media query exists in stylesheet
        self.assertIn("@media (prefers-reduced-motion: reduce)", css,
                      "Stylesheet must contain @media (prefers-reduced-motion: reduce) rule")

        # Extract the reduced motion rule block
        rm_block = css[css.find("@media (prefers-reduced-motion: reduce)"):]

        # 2. .hero-video is hidden
        self.assertIn(".hero-video", rm_block)
        self.assertIn("display: none", rm_block,
                      "Reduced motion rule must hide .hero-video with display: none")

        # 3. .hero-video-container uses existing poster image
        self.assertIn(".hero-video-container", rm_block)
        self.assertIn("/static/videos/agrovia-crops-poster.jpg", rm_block,
                      "Reduced motion rule must use /static/videos/agrovia-crops-poster.jpg as container background")

        # 4. .pulse-dot animation is disabled
        self.assertIn(".pulse-dot", rm_block)
        self.assertIn("animation: none", rm_block,
                      "Reduced motion rule must disable .pulse-dot animation with animation: none")

        # 5. Verify normal-motion behavior is intact: GET / returns HTML with video tag and poster
        with self.client.session_transaction() as sess:
            db_user = database.save_user("motion.test@example.com", "Motion Test User")
            sess["user"] = db_user
            sess["language"] = "en"

        res = self.client.get('/')
        self.assertEqual(res.status_code, 200)
        html = res.data.decode("utf-8")
        self.assertIn('<video class="hero-video"', html)
        self.assertIn('/static/videos/agrovia-crops-poster.jpg', html)

    def test_section64_gunicorn_configuration(self):
        """SEC Section 6.4: Verify gunicorn.conf.py exists, is valid Python, and configures 2 workers and 60s timeout."""
        import ast
        import os
        conf_path = os.path.join(app.root_path, "gunicorn.conf.py")
        self.assertTrue(os.path.isfile(conf_path), "gunicorn.conf.py must exist in project root")

        with open(conf_path, "r", encoding="utf-8") as f:
            code = f.read()

        # Syntax check
        parsed = ast.parse(code)
        self.assertIsNotNone(parsed)

        # Execute in isolated dict to check configuration attributes
        config_vars = {}
        exec(compile(parsed, filename="gunicorn.conf.py", mode="exec"), config_vars)

        self.assertEqual(config_vars.get("bind"), "127.0.0.1:5000",
                         "Gunicorn must bind strictly to 127.0.0.1:5000 behind reverse proxy")
        self.assertEqual(config_vars.get("workers"), 2,
                         "Gunicorn must be configured with exactly 2 workers for ML + SQLite stability")
        self.assertEqual(config_vars.get("timeout"), 60,
                         "Gunicorn timeout must be 60 seconds to accommodate ML inference")
        self.assertFalse(config_vars.get("preload_app", True),
                         "preload_app must be False to ensure per-worker DB/model initialization isolation")

    def test_section64_nginx_configuration(self):
        """SEC Section 6.4: Verify nginx.conf exists and defines reverse proxy, forwarded headers, and upload limits."""
        import os
        conf_path = os.path.join(app.root_path, "nginx.conf")
        self.assertTrue(os.path.isfile(conf_path), "nginx.conf must exist in project root")

        with open(conf_path, "r", encoding="utf-8") as f:
            nginx_conf = f.read()

        # 1. Reverse proxy configuration
        self.assertIn("proxy_pass", nginx_conf)
        self.assertIn("http://127.0.0.1:5000", nginx_conf)

        # 2. Forwarded headers
        self.assertIn("X-Forwarded-For", nginx_conf)
        self.assertIn("X-Forwarded-Proto", nginx_conf)
        self.assertIn("X-Forwarded-Host", nginx_conf)
        self.assertIn("X-Real-IP", nginx_conf)

        # 3. Payload size ceiling
        self.assertIn("client_max_body_size 10M", nginx_conf)

        # 4. Direct static file serving with placeholder
        self.assertIn("location /static/", nginx_conf)

        # 5. Must NOT pretend to configure fake TLS certificate paths
        self.assertNotIn("ssl_certificate", nginx_conf)

    def test_section64_env_example_template(self):
        """SEC Section 6.4: Verify .env.example exists, documents required variables, and contains no real secrets."""
        import os
        env_path = os.path.join(app.root_path, ".env.example")
        self.assertTrue(os.path.isfile(env_path), ".env.example must exist in project root")

        with open(env_path, "r", encoding="utf-8") as f:
            lines = f.readlines()

        content = "".join(lines)
        self.assertIn("SECRET_KEY", content)
        self.assertIn("FLASK_ENV", content)
        self.assertIn("PORT", content)
        self.assertIn("ENABLE_DEV_MOCK_AUTH", content)
        self.assertIn("DATABASE_PATH", content)

        # Verify no actual secret values are committed in SECRET_KEY=
        for line in lines:
            stripped = line.strip()
            if stripped.startswith("SECRET_KEY="):
                val = stripped.split("=", 1)[1].strip()
                self.assertEqual(val, "", ".env.example must NOT contain a real SECRET_KEY value")

    def test_section64_wsgi_proxy_fix_headers(self):
        """SEC Section 6.4: Verify ProxyFix accurately resolves X-Forwarded-For, X-Forwarded-Proto, and X-Forwarded-Host."""
        from werkzeug.test import EnvironBuilder
        from werkzeug.wrappers import Request
        from werkzeug.middleware.proxy_fix import ProxyFix

        captured = {}

        def sample_app(environ, start_response):
            req = Request(environ)
            captured['remote_addr'] = req.remote_addr
            captured['is_secure'] = req.is_secure
            captured['scheme'] = req.scheme
            captured['host'] = req.host
            start_response('200 OK', [('Content-Type', 'text/plain')])
            return [b'OK']

        builder = EnvironBuilder(headers={
            'X-Forwarded-For': '203.0.113.195',
            'X-Forwarded-Proto': 'https',
            'X-Forwarded-Host': 'krishi.example.com'
        })
        env = builder.get_environ()

        # 1. Without ProxyFix: forwarded headers are NOT trusted (prevents dev spoofing)
        sample_app(env.copy(), lambda s, h: None)
        self.assertNotEqual(captured.get('remote_addr'), '203.0.113.195',
                            "Without ProxyFix, X-Forwarded-For must NOT be trusted")
        self.assertFalse(captured.get('is_secure'),
                         "Without ProxyFix, X-Forwarded-Proto must NOT be trusted")

        # 2. With ProxyFix(x_for=1, x_proto=1, x_host=1): exactly 1 hop is trusted
        proxied_app = ProxyFix(sample_app, x_for=1, x_proto=1, x_host=1)
        proxied_app(env.copy(), lambda s, h: None)
        self.assertEqual(captured.get('remote_addr'), '203.0.113.195',
                         "ProxyFix must resolve remote_addr from X-Forwarded-For")
        self.assertTrue(captured.get('is_secure'),
                        "ProxyFix must resolve is_secure from X-Forwarded-Proto")
        self.assertEqual(captured.get('scheme'), 'https',
                         "ProxyFix must resolve scheme from X-Forwarded-Proto")
        self.assertEqual(captured.get('host'), 'krishi.example.com',
                         "ProxyFix must resolve host from X-Forwarded-Host")

    def test_section65_rate_limit_bucket_isolation(self):
        """SEC Section 6.5: Verify separate action buckets (login, resend, diagnose) and client IPs are completely isolated."""
        clear_rate_limits()
        ip_a = "198.51.100.10"
        ip_b = "198.51.100.20"

        # 1. Fill login quota for ip_a (max 10)
        for _ in range(10):
            self.assertFalse(is_rate_limited(f"login:{ip_a}", max_requests=10, window_seconds=60))
        # 11th login attempt for ip_a is blocked
        self.assertTrue(is_rate_limited(f"login:{ip_a}", max_requests=10, window_seconds=60))

        # 2. Verify resend and diagnose buckets for ip_a are NOT exhausted
        self.assertFalse(is_rate_limited(f"resend:{ip_a}", max_requests=5, window_seconds=60),
                         "Exhausting login bucket must not affect resend bucket")
        self.assertFalse(is_rate_limited(f"diagnose:{ip_a}", max_requests=10, window_seconds=60),
                         "Exhausting login bucket must not affect diagnose bucket")

        # 3. Verify different IP ip_b is NOT affected by ip_a's rate limiting
        self.assertFalse(is_rate_limited(f"login:{ip_b}", max_requests=10, window_seconds=60),
                         "Exhausting login for ip_a must not affect ip_b")

    def test_section65_login_rate_limiting(self):
        """SEC Section 6.5: Verify /login enforces 10 requests / 60 seconds per IP rate limit."""
        clear_rate_limits()
        app.config['ENABLE_RATE_LIMIT_TESTING'] = True
        try:
            # 10 allowed attempts
            for i in range(10):
                res = self.client.post('/login', data={
                    'action': 'login',
                    'email': 'nonexistent@example.com',
                    'password': 'badpassword'
                }, environ_base={'REMOTE_ADDR': '198.51.100.30'})
                # Expect normal rejection (e.g. invalid credentials alert)
                self.assertNotIn(b"Too many sign-in attempts", res.data,
                                 f"Request {i+1} should not be rate limited")

            # 11th attempt must be throttled
            res_throttled = self.client.post('/login', data={
                'action': 'login',
                'email': 'nonexistent@example.com',
                'password': 'badpassword'
            }, environ_base={'REMOTE_ADDR': '198.51.100.30'})
            self.assertIn(b"Too many sign-in attempts", res_throttled.data)
        finally:
            app.config.pop('ENABLE_RATE_LIMIT_TESTING', None)
            clear_rate_limits()

    def test_section65_resend_verification_rate_limiting_429(self):
        """SEC Section 6.5: Verify /resend-verification enforces 5 requests / 60s per IP limit and returns HTTP 429."""
        clear_rate_limits()
        app.config['ENABLE_RATE_LIMIT_TESTING'] = True
        try:
            # First 5 requests within limit
            for i in range(5):
                res = self.client.post('/resend-verification', data={
                    'email': 'unverified.farmer@example.com'
                }, environ_base={'REMOTE_ADDR': '198.51.100.40'})
                self.assertEqual(res.status_code, 200, f"Request {i+1} must succeed within quota")
                self.assertNotIn(b"Too many verification requests", res.data)

            # 6th request must exceed limit and return 429
            res_throttled = self.client.post('/resend-verification', data={
                'email': 'unverified.farmer@example.com'
            }, environ_base={'REMOTE_ADDR': '198.51.100.40'})
            self.assertEqual(res_throttled.status_code, 429)
            self.assertIn(b"Too many verification requests", res_throttled.data)
            self.assertIn(b"Please wait 1 minute before trying again", res_throttled.data)
        finally:
            app.config.pop('ENABLE_RATE_LIMIT_TESTING', None)
            clear_rate_limits()

    def test_section65_diagnose_disease_rate_limiting_429(self):
        """SEC Section 6.5: Verify /api/diagnose-disease enforces 10 req/60s limit, returns JSON 429, and prevents ML execution."""
        clear_rate_limits()
        app.config['ENABLE_RATE_LIMIT_TESTING'] = True
        try:
            img = Image.new('RGB', (10, 10), color='green')
            buf = io.BytesIO()
            img.save(buf, format='JPEG')
            img_bytes = buf.getvalue()

            with patch('app.diagnose_plant_photo') as mock_diagnose:
                mock_diagnose.return_value = {
                    "success": True,
                    "crop": "wheat",
                    "disease": "Healthy",
                    "confidence": 0.95
                }

                # 10 allowed requests
                for i in range(10):
                    res = self.client.post('/api/diagnose-disease', data={
                        'crop': 'wheat',
                        'lang': 'en',
                        'leaf_photo': (io.BytesIO(img_bytes), 'leaf.jpg')
                    }, content_type='multipart/form-data', environ_base={'REMOTE_ADDR': '198.51.100.50'})
                    self.assertEqual(res.status_code, 200, f"Scan request {i+1} must succeed")
                    data = res.get_json()
                    self.assertTrue(data.get('success'))

                self.assertEqual(mock_diagnose.call_count, 10)

                # 11th request must be throttled before model processing
                res_throttled = self.client.post('/api/diagnose-disease', data={
                    'crop': 'wheat',
                    'lang': 'en',
                    'leaf_photo': (io.BytesIO(img_bytes), 'leaf.jpg')
                }, content_type='multipart/form-data', environ_base={'REMOTE_ADDR': '198.51.100.50'})

                self.assertEqual(res_throttled.status_code, 429)
                self.assertEqual(res_throttled.content_type, 'application/json')
                data_throttled = res_throttled.get_json()
                self.assertFalse(data_throttled.get('success'))
                self.assertIn("Too many image diagnosis requests", data_throttled.get('error', ''))
                self.assertIn("Please wait 1 minute before trying again", data_throttled.get('error', ''))

                # Crucial check: diagnose_plant_photo was NOT called on the 11th request!
                self.assertEqual(mock_diagnose.call_count, 10,
                                 "diagnose_plant_photo must NOT be called when rate limited")
        finally:
            app.config.pop('ENABLE_RATE_LIMIT_TESTING', None)
            clear_rate_limits()

    def test_section65_upload_size_protection_intact(self):
        """SEC Section 6.5: Verify MAX_CONTENT_LENGTH = 8 MB upload protection remains intact."""
        self.assertEqual(app.config.get('MAX_CONTENT_LENGTH'), 8 * 1024 * 1024,
                         "MAX_CONTENT_LENGTH must be exactly 8 MB (8 * 1024 * 1024)")

    def test_login_usability_issue1_farmer_name_hidden_in_login_mode(self):
        """UIUX Login Audit Issue 1: Verify #groupFarmerName is hidden with display:none and aria-hidden in login mode."""
        res = self.client.get('/login?mode=login')
        self.assertEqual(res.status_code, 200)
        html = res.data.decode('utf-8')
        self.assertIn('id="groupFarmerName"', html)
        self.assertTrue(
            'id="groupFarmerName" style="display:none;" aria-hidden="true"' in html or
            'id="groupFarmerName" style="display: none;" aria-hidden="true"' in html,
            "#groupFarmerName must be hidden with display:none and aria-hidden in login mode"
        )

    def test_login_usability_issue1_farmer_name_visible_in_register_mode(self):
        """UIUX Login Audit Issue 1: Verify #groupFarmerName is visible without display:none in register mode."""
        res = self.client.get('/login?mode=register')
        self.assertEqual(res.status_code, 200)
        html = res.data.decode('utf-8')
        self.assertIn('id="groupFarmerName"', html)
        self.assertNotIn('id="groupFarmerName" style="display:none;"', html)
        self.assertNotIn('id="groupFarmerName" style="display: none;"', html)
        self.assertNotIn('id="groupFarmerName" aria-hidden="true"', html)

    def test_login_usability_issue1_dynamic_switch_auth_mode_logic(self):
        """UIUX Login Audit Issue 1: Verify switchAuthMode contains dynamic show/hide and aria-hidden toggling for #groupFarmerName."""
        res = self.client.get('/login')
        self.assertEqual(res.status_code, 200)
        html = res.data.decode('utf-8')
        self.assertIn('groupFarmerName.style.display', html,
                      "switchAuthMode must dynamically toggle groupFarmerName display")
        self.assertIn('groupFarmerName.setAttribute', html,
                      "switchAuthMode must dynamically set aria-hidden on groupFarmerName")
        self.assertIn('groupFarmerName.removeAttribute', html,
                      "switchAuthMode must dynamically remove aria-hidden on groupFarmerName")

    def test_login_usability_issue2_step_indicator_hierarchy_placement(self):
        """UIUX Login Audit Issue 2: Verify Step 2 of 2 indicator is repositioned above brand lockup/headings in card hierarchy."""
        res = self.client.get('/login')
        self.assertEqual(res.status_code, 200)
        html = res.data.decode('utf-8')
        self.assertIn('onboarding-step-wrapper', html, "Step indicator wrapper must be present")
        self.assertIn('Step 2 of 2', html, "Step indicator label must be present")
        step_pos = html.find('class="onboarding-step-wrapper"')
        brand_pos = html.find('class="onboarding-brand"')
        heading_pos = html.find('id="pageHeading"')
        self.assertTrue(step_pos != -1 and brand_pos != -1 and heading_pos != -1,
                        "Step indicator, brand, and heading elements must all exist")
        self.assertTrue(step_pos < brand_pos,
                        "Step indicator must be positioned above brand lockup at the top of the card")
        self.assertTrue(step_pos < heading_pos,
                        "Step indicator must be positioned above pageHeading in card hierarchy")

    def test_login_usability_issue3_divider_spacing_css(self):
        """UIUX Login Audit Issue 3: Verify .onboarding-divider has increased vertical breathing room CSS."""
        res = self.client.get('/login')
        self.assertEqual(res.status_code, 200)
        html = res.data.decode('utf-8')
        self.assertIn('onboarding-divider', html)
        self.assertTrue(
            '.onboarding-divider' in html and 'margin:' in html,
            ".onboarding-divider rule must be present with margin definition"
        )
        self.assertTrue(
            'margin: 28px 0 30px' in html or 'margin:28px 0 30px' in html,
            ".onboarding-divider must have expanded vertical margins (28px 0 30px)"
        )


    def test_backup_db_creates_valid_sqlite_file(self):
        """SEC Section 6.2 Item 4: Verify database.backup_db creates a valid, readable SQLite backup file."""
        import tempfile
        import sqlite3
        with tempfile.TemporaryDirectory() as temp_dir:
            backup_file = database.backup_db(backup_dir=temp_dir)
            self.assertTrue(os.path.isfile(backup_file), "Backup file must exist on disk")
            self.assertTrue(backup_file.startswith(temp_dir), "Backup must reside inside configured backup_dir")
            self.assertTrue(
                os.path.basename(backup_file).startswith("krishi_sahayak_backup_") and backup_file.endswith(".db"),
                "Backup filename must follow krishi_sahayak_backup_YYYYMMDD_HHMMSS.db format"
            )

            # Verify the backup is a valid SQLite database with expected schema
            conn = sqlite3.connect(backup_file)
            try:
                tables = [row[0] for row in conn.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()]
                self.assertIn("users", tables, "Users table must exist in backup")
                self.assertIn("reminders", tables, "Reminders table must exist in backup")
                self.assertIn("crop_progress", tables, "Crop progress table must exist in backup")
            finally:
                conn.close()

    def test_backup_db_captures_wal_state(self):
        """SEC Section 6.2 Item 4: Verify VACUUM INTO captures uncheckpointed WAL transactions cleanly."""
        import tempfile
        import sqlite3
        with tempfile.TemporaryDirectory() as temp_dir:
            test_db_path = os.path.join(temp_dir, "wal_source.db")
            conn = sqlite3.connect(test_db_path, timeout=20.0)
            conn.execute("PRAGMA journal_mode = WAL;")
            conn.execute("CREATE TABLE test_wal (id INTEGER PRIMARY KEY, note TEXT);")
            conn.commit()

            # Insert transaction into WAL
            unique_note = f"WAL_ENTRY_{secrets.token_hex(8)}"
            conn.execute("INSERT INTO test_wal (note) VALUES (?);", (unique_note,))
            conn.commit()

            # Verify that the WAL file exists and contains active uncheckpointed pages
            wal_path = test_db_path + "-wal"
            self.assertTrue(os.path.exists(wal_path), "WAL file should be active")

            # Perform backup with source database connection still open (concurrent operation)
            backup_dest_dir = os.path.join(temp_dir, "backups_dest")
            backup_file = database.backup_db(backup_dir=backup_dest_dir, db_path=test_db_path)
            conn.close()

            # Connect to the backup file independently and verify uncheckpointed data was captured
            b_conn = sqlite3.connect(backup_file)
            try:
                row = b_conn.execute("SELECT note FROM test_wal WHERE note = ?;", (unique_note,)).fetchone()
                self.assertIsNotNone(row, "Backup created with VACUUM INTO must capture uncheckpointed WAL data")
                self.assertEqual(row[0], unique_note)
            finally:
                b_conn.close()

    def test_backup_db_retention_pruning(self):
        """SEC Section 6.2 Item 4: Verify backup pruning preserves newest keep_count backups and ignores other files."""
        import tempfile
        with tempfile.TemporaryDirectory() as temp_dir:
            # 1. Create 9 mock backup files matching the pattern
            mock_files = []
            for i in range(1, 10):
                filename = f"krishi_sahayak_backup_2026010{i}_120000.db"
                filepath = os.path.join(temp_dir, filename)
                with open(filepath, "w") as f:
                    f.write(f"mock backup {i}")
                mock_files.append(filepath)

            # 2. Create unrelated files that must NEVER be pruned
            unrelated_txt = os.path.join(temp_dir, "notes.txt")
            with open(unrelated_txt, "w") as f:
                f.write("Important notes")
            unrelated_db = os.path.join(temp_dir, "custom_data.db")
            with open(unrelated_db, "w") as f:
                f.write("Custom DB")

            # 3. Call backup_db with keep_count=7
            new_backup = database.backup_db(backup_dir=temp_dir, keep_count=7)
            self.assertTrue(os.path.isfile(new_backup))

            # 4. Check remaining files in temp_dir
            remaining_matching = [
                f for f in os.listdir(temp_dir)
                if database.BACKUP_FILENAME_PATTERN.match(f)
            ]
            self.assertEqual(len(remaining_matching), 7, "Exactly 7 newest matching backups must be retained")

            # The 3 oldest mock files (20260101, 20260102, 20260103) should have been pruned
            self.assertFalse(os.path.exists(mock_files[0]), "Oldest backup 01 should be pruned")
            self.assertFalse(os.path.exists(mock_files[1]), "Oldest backup 02 should be pruned")
            self.assertFalse(os.path.exists(mock_files[2]), "Oldest backup 03 should be pruned")

            # Unrelated files must remain completely untouched
            self.assertTrue(os.path.exists(unrelated_txt), "Unrelated text file must not be pruned")
            self.assertTrue(os.path.exists(unrelated_db), "Unrelated custom db file must not be pruned")

            # 5. Invalid keep_count validation
            with self.assertRaises(ValueError):
                database.backup_db(backup_dir=temp_dir, keep_count=0)
            with self.assertRaises(ValueError):
                database.backup_db(backup_dir=temp_dir, keep_count=-5)

    def test_flask_cli_backup_command(self):
        """SEC Section 6.2 Item 4: Verify 'flask backup-db' CLI command executes successfully and reports status."""
        import tempfile
        from unittest.mock import patch

        runner = app.test_cli_runner()
        with tempfile.TemporaryDirectory() as temp_dir:
            with patch("database.DEFAULT_BACKUP_DIR", temp_dir):
                result = runner.invoke(args=["backup-db"])
                self.assertEqual(result.exit_code, 0, f"CLI command failed: {result.output}")
                self.assertIn("Database backup created successfully:", result.output)
                created_files = os.listdir(temp_dir)
                self.assertEqual(len(created_files), 1)
                self.assertTrue(created_files[0].startswith("krishi_sahayak_backup_"))

    def test_backup_safety_and_gitignore(self):
        """SEC Section 6.2 Item 4: Ensure .gitignore protects backups and no leaked test artifacts remain."""
        gitignore_path = os.path.join(app.root_path, ".gitignore")
        self.assertTrue(os.path.isfile(gitignore_path), ".gitignore must exist in project root")
        with open(gitignore_path, "r", encoding="utf-8") as f:
            content = f.read()
        self.assertIn("backups/", content, ".gitignore must exclude backups/ directory")
        self.assertIn("*.db", content, ".gitignore must exclude *.db files")

        # Verify real default backups directory (if it exists) has no test artifacts left over
        default_backup_dir = os.path.join(app.root_path, "backups")
        if os.path.exists(default_backup_dir):
            for fname in os.listdir(default_backup_dir):
                self.assertFalse(fname.startswith("wal_source"), "No test databases should leak into project backups/")


    def test_database_path_environment_override(self):
        """SEC Section 6.2 Item 3: Verify DATABASE_PATH environment override creates and uses custom database location."""
        import tempfile
        import sqlite3
        orig_env = os.environ.get("DATABASE_PATH")
        with tempfile.TemporaryDirectory() as temp_dir:
            custom_db = os.path.join(temp_dir, "custom_krishi.db")
            try:
                os.environ["DATABASE_PATH"] = custom_db
                self.assertEqual(database.get_db_path(), os.path.abspath(custom_db))

                # Initialize database at custom path
                database.init_db()
                self.assertTrue(os.path.isfile(custom_db), "Database file must be created at custom DATABASE_PATH")

                # Verify tables exist in the custom database
                conn = sqlite3.connect(custom_db)
                try:
                    tables = [row[0] for row in conn.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()]
                    self.assertIn("users", tables)
                    self.assertIn("reminders", tables)
                    self.assertIn("crop_progress", tables)
                finally:
                    conn.close()

                # Verify CRUD works on custom database path
                test_email = f"custom_path_{secrets.token_hex(4)}@example.com"
                saved = database.save_user(test_email, "Custom Path Farmer")
                self.assertIsNotNone(saved)
                retrieved = database.get_user_by_email(test_email)
                self.assertIsNotNone(retrieved)
                self.assertEqual(retrieved["name"], "Custom Path Farmer")
            finally:
                if orig_env is not None:
                    os.environ["DATABASE_PATH"] = orig_env
                else:
                    os.environ.pop("DATABASE_PATH", None)

    def test_database_path_default_fallback(self):
        """SEC Section 6.2 Item 3: Verify get_db_path safely falls back to <project root>/database.db when unset or blank."""
        orig_env = os.environ.get("DATABASE_PATH")
        expected_default = os.path.abspath(os.path.join(os.path.dirname(database.__file__), "database.db"))
        try:
            # 1. When unset
            os.environ.pop("DATABASE_PATH", None)
            self.assertEqual(database.get_db_path(), expected_default)

            # 2. When empty string
            os.environ["DATABASE_PATH"] = ""
            self.assertEqual(database.get_db_path(), expected_default)

            # 3. When whitespace only
            os.environ["DATABASE_PATH"] = "   "
            self.assertEqual(database.get_db_path(), expected_default)
        finally:
            if orig_env is not None:
                os.environ["DATABASE_PATH"] = orig_env
            else:
                os.environ.pop("DATABASE_PATH", None)

    def test_database_path_automatic_parent_directory_creation(self):
        """SEC Section 6.2 Item 3: Verify get_db_path automatically creates non-existent nested parent directories."""
        import tempfile
        import sqlite3
        orig_env = os.environ.get("DATABASE_PATH")
        with tempfile.TemporaryDirectory() as temp_dir:
            nested_dir = os.path.join(temp_dir, "deeply", "nested", "storage")
            custom_db = os.path.join(nested_dir, "krishi_isolated.db")
            self.assertFalse(os.path.exists(nested_dir), "Parent directories must not exist prior to test")

            try:
                os.environ["DATABASE_PATH"] = custom_db
                resolved_path = database.get_db_path()
                self.assertEqual(resolved_path, os.path.abspath(custom_db))
                self.assertTrue(os.path.isdir(nested_dir), "Parent directory must be created automatically by get_db_path")

                # Verify connection and initialization succeed in newly created nested directory
                database.init_db()
                self.assertTrue(os.path.isfile(custom_db))
                conn = sqlite3.connect(custom_db)
                try:
                    tables = [row[0] for row in conn.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()]
                    self.assertIn("users", tables)
                finally:
                    conn.close()
            finally:
                if orig_env is not None:
                    os.environ["DATABASE_PATH"] = orig_env
                else:
                    os.environ.pop("DATABASE_PATH", None)

    def test_nginx_conf_database_file_protection(self):
        """SEC Section 6.2 Item 3: Verify nginx.conf includes explicit location rule blocking direct SQLite database access."""
        nginx_path = os.path.join(app.root_path, "nginx.conf")
        self.assertTrue(os.path.isfile(nginx_path), "nginx.conf must exist in project root")

        with open(nginx_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Check location block regex
        self.assertIn("location ~*", content, "nginx.conf must contain regex location block")
        import re
        match = re.search(r'location\s+~\*\s+\\\.\((.*?)\)\$', content)
        self.assertIsNotNone(match, "nginx.conf must contain regex location block for database file extensions")
        exts = [e.strip() for e in match.group(1).split('|')]
        for ext in ["db", "db-wal", "db-shm", "sqlite", "sqlite3"]:
            self.assertIn(ext, exts, f"Extension .{ext} must be protected in nginx.conf")

        self.assertIn("deny all;", content, "nginx.conf must specify 'deny all;' for database files")
        self.assertIn("return 404;", content, "nginx.conf must return 404 for protected database file requests")


class AuthenticationEmergencyRepairTestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['SECRET_KEY'] = 'test-secret-key-auth-emergency'
        clear_rate_limits()
        self.client = app.test_client()

    def tearDown(self):
        clear_rate_limits()

    def test_existing_user_with_valid_hash_can_login(self):
        """1. Existing user with valid password hash can log in."""
        test_email = f"valid_hash_{secrets.token_hex(4)}@example.com"
        test_pass = "ValidPass123"
        database.create_user_with_password(
            email=test_email,
            name="Valid User",
            password_hash=generate_password_hash(test_pass, method="pbkdf2:sha256"),
            is_verified=1
        )

        res = self.client.post('/login', data={
            'action': 'login',
            'email': test_email,
            'password': test_pass
        }, follow_redirects=False)

        # Successful login returns redirect (302) to home page
        self.assertEqual(res.status_code, 302)
        with self.client.session_transaction() as sess:
            self.assertIsNotNone(sess.get('user'))
            self.assertEqual(sess['user']['email'], test_email)

    def test_wrong_password_rejected(self):
        """2. Wrong password is rejected with uniform error message."""
        test_email = f"wrong_pass_{secrets.token_hex(4)}@example.com"
        database.create_user_with_password(
            email=test_email,
            name="Wrong Pass User",
            password_hash=generate_password_hash("CorrectPass123", method="pbkdf2:sha256"),
            is_verified=1
        )

        res = self.client.post('/login', data={
            'action': 'login',
            'email': test_email,
            'password': 'IncorrectPass999'
        })
        self.assertEqual(res.status_code, 200)
        self.assertIn("Invalid email or password. Please check your credentials.", res.get_data(as_text=True))

    def test_null_password_hash_cannot_authenticate_until_reset(self):
        """3. User with NULL password_hash cannot authenticate unless a password is explicitly established through the safe reset mechanism."""
        null_email = f"legacy_null_{secrets.token_hex(4)}@example.com"
        # Create legacy-style user with NULL password_hash
        database.save_user(
            email=null_email,
            name="Legacy Farmer",
            is_verified=1,
            password_hash=None
        )

        # 3a. Prior to reset, login attempt with ANY password must fail
        res_fail = self.client.post('/login', data={
            'action': 'login',
            'email': null_email,
            'password': 'AnyPassword123'
        })
        self.assertEqual(res_fail.status_code, 200)
        self.assertIn("Invalid email or password. Please check your credentials.", res_fail.get_data(as_text=True))

        # 3b. Use safe reset mechanism to establish password
        new_pass = "EstablishedPass123"
        hashed = generate_password_hash(new_pass, method="pbkdf2:sha256")
        success = database.update_user_password(null_email, hashed)
        self.assertTrue(success)

        # Verify DB reflects updated hash
        user_updated = database.get_user_by_email(null_email)
        self.assertIsNotNone(user_updated['password_hash'])
        self.assertEqual(user_updated['is_verified'], 1)

        # 3c. Login now succeeds with the newly established password
        res_success = self.client.post('/login', data={
            'action': 'login',
            'email': null_email,
            'password': new_pass
        }, follow_redirects=False)
        self.assertEqual(res_success.status_code, 302)

    def test_google_mock_auth_works_only_in_dev_with_flag(self):
        """4. Google mock authentication works ONLY when development mock mode is explicitly enabled."""
        with patch.dict(os.environ, {'FLASK_ENV': 'development', 'ENABLE_DEV_MOCK_AUTH': '1'}):
            res = self.client.post('/api/auth/google', json={
                'name': 'Dev Google Farmer',
                'email': 'dev.farmer@gmail.com'
            })
            self.assertEqual(res.status_code, 200)
            data = res.get_json()
            self.assertTrue(data.get('success'))
            self.assertEqual(data.get('user', {}).get('email'), 'dev.farmer@gmail.com')

    def test_google_mock_auth_rejected_when_mock_disabled_or_production(self):
        """5. Google mock authentication is rejected when development mock mode is disabled or in production."""
        # 5a. Disabled in development (ENABLE_DEV_MOCK_AUTH=0)
        with patch.dict(os.environ, {'FLASK_ENV': 'development', 'ENABLE_DEV_MOCK_AUTH': '0'}):
            res_dev_off = self.client.post('/api/auth/google', json={
                'name': 'Dev Google Farmer',
                'email': 'dev.farmer@gmail.com'
            })
            self.assertEqual(res_dev_off.status_code, 401)
            self.assertFalse(res_dev_off.get_json().get('success'))
            self.assertIn("Mock authentication is disabled", res_dev_off.get_json().get('error', ''))

        # 5b. Strictly rejected in production even if ENABLE_DEV_MOCK_AUTH=1
        with patch.dict(os.environ, {'FLASK_ENV': 'production', 'ENABLE_DEV_MOCK_AUTH': '1'}):
            res_prod = self.client.post('/api/auth/google', json={
                'name': 'Prod Impersonator',
                'email': 'prod.fake@gmail.com'
            })
            self.assertEqual(res_prod.status_code, 401)
            self.assertFalse(res_prod.get_json().get('success'))

    def test_session_remains_usable_after_restart_with_persistent_secret_key(self):
        """6. Session remains usable after normal application restart when persistent development SECRET_KEY is configured."""
        persistent_key = "krishi-persistent-dev-test-key-abcdef123456"

        # Process 1 creates session and outputs cookie value
        code1 = f'''
import os
os.environ["SECRET_KEY"] = "{persistent_key}"
from app import app
client = app.test_client()
with client.session_transaction() as sess:
    sess["user"] = {{"id": 999, "email": "persist@example.com", "name": "Persistent Farmer"}}
cookie = client.get_cookie("session")
print(cookie.value if cookie else "")
'''
        proc1 = subprocess.run([sys.executable, '-c', code1], capture_output=True, text=True)
        self.assertEqual(proc1.returncode, 0, f"Proc1 error: {proc1.stderr}")
        cookie_val = proc1.stdout.strip()
        self.assertTrue(len(cookie_val) > 10, f"Invalid cookie output: {proc1.stdout}")

        # Process 2 (simulating fresh application restart with same persistent key) restores session
        code2 = f'''
import os
os.environ["SECRET_KEY"] = "{persistent_key}"
from app import app
client = app.test_client()
client.set_cookie("session", "{cookie_val}")
res = client.get("/profile")
print(f"STATUS={{res.status_code}}")
print(f"HAS_NAME={{'Persistent Farmer' in res.get_data(as_text=True)}}")
'''
        proc2 = subprocess.run([sys.executable, '-c', code2], capture_output=True, text=True)
        self.assertEqual(proc2.returncode, 0, f"Proc2 error: {proc2.stderr}")
        self.assertIn("STATUS=200", proc2.stdout)
        self.assertIn("HAS_NAME=True", proc2.stdout)

    def test_production_configuration_still_rejects_missing_secret_key(self):
        """7. Production configuration still strictly rejects missing SECRET_KEY."""
        env = os.environ.copy()
        env['FLASK_ENV'] = 'production'
        env.pop('SECRET_KEY', None)
        cmd = [sys.executable, '-c', 'from app import app']
        proc = subprocess.run(cmd, env=env, capture_output=True, text=True)
        self.assertNotEqual(proc.returncode, 0)
        self.assertIn('CRITICAL SECURITY ERROR: SECRET_KEY must be set in production environment!', proc.stderr)


if __name__ == '__main__':
    unittest.main()






