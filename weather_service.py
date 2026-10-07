# weather_service.py
# Live Weather Forecasting and Agricultural Weather Advisory Engine
# Powered by Open-Meteo Free Weather & Geocoding APIs (No API Key Required)
# Incorporating agricultural variables: Soil Temp, Soil Moisture, ET0 Evapotranspiration, Wind Compass, and 48-Hr Spray Windows.

import math
import threading
import time
from datetime import datetime, timedelta
import requests

class TTLCache:
    """Thread-safe bounded in-memory cache with time-to-live (TTL) expiration."""
    def __init__(self, maxsize=500, default_ttl=600):
        self.maxsize = maxsize
        self.default_ttl = default_ttl
        self._cache = {}  # key -> (timestamp, value)
        self._lock = threading.Lock()

    def get(self, key):
        with self._lock:
            entry = self._cache.get(key)
            if not entry:
                return None, None
            timestamp, value = entry
            is_expired = (time.time() - timestamp) > self.default_ttl
            return value, is_expired

    def set(self, key, value):
        with self._lock:
            if len(self._cache) >= self.maxsize and key not in self._cache:
                # Deterministic LRU/FIFO eviction: evict oldest entry
                oldest_key = min(self._cache, key=lambda k: self._cache[k][0])
                del self._cache[oldest_key]
            self._cache[key] = (time.time(), value)

    def clear(self):
        with self._lock:
            self._cache.clear()

    def __len__(self):
        with self._lock:
            return len(self._cache)

_WEATHER_CACHE = TTLCache(maxsize=500, default_ttl=600)        # 10 minutes (600s)
_REVERSE_GEO_CACHE = TTLCache(maxsize=500, default_ttl=86400)  # 24 hours (86400s)
_SEARCH_LOCATIONS_CACHE = TTLCache(maxsize=500, default_ttl=3600)  # 1 hour (3600s)

def clear_weather_caches():
    """Clear all in-memory weather, geocoding, and location caches (for unit testing)."""
    _WEATHER_CACHE.clear()
    _REVERSE_GEO_CACHE.clear()
    _SEARCH_LOCATIONS_CACHE.clear()

# Pre-defined major agricultural hubs across India
POPULAR_LOCATIONS = {
    "pune": {"name": {"en": "Pune, Maharashtra", "hi": "पुणे, महाराष्ट्र", "mr": "पुणे, महाराष्ट्र"}, "lat": 18.5204, "lon": 73.8567},
    "nagpur": {"name": {"en": "Nagpur (Vidarbha), MH", "hi": "नागपुर (विदर्भ), महाराष्ट्र", "mr": "नागपूर (विदर्भ), महाराष्ट्र"}, "lat": 21.1458, "lon": 79.0882},
    "nashik": {"name": {"en": "Nashik (Grape & Onion Belt), MH", "hi": "नासिक, महाराष्ट्र", "mr": "नाशिक, महाराष्ट्र"}, "lat": 19.9975, "lon": 73.7898},
    "aurangabad": {"name": {"en": "Chhatrapati Sambhajinagar, MH", "hi": "छत्रपति संभाजीनगर, महाराष्ट्र", "mr": "छत्रपती संभाजीनगर, महाराष्ट्र"}, "lat": 19.8762, "lon": 75.3433},
    "kolhapur": {"name": {"en": "Kolhapur (Sugarcane Hub), MH", "hi": "कोल्हापुर, महाराष्ट्र", "mr": "कोल्हापूर (ऊस पट्टा), महाराष्ट्र"}, "lat": 16.7050, "lon": 74.2433},
    "baramati": {"name": {"en": "Baramati (Sugar & Fruit Hub), MH", "hi": "बारामती, महाराष्ट्र", "mr": "बारामती, महाराष्ट्र"}, "lat": 18.1517, "lon": 74.5772},
    "jalgaon": {"name": {"en": "Jalgaon (Banana Capital), MH", "hi": "जलगांव, महाराष्ट्र", "mr": "जळगाव (केळी पट्टा), महाराष्ट्र"}, "lat": 21.0077, "lon": 75.5626},
    "solapur": {"name": {"en": "Solapur (Pomegranate/Jowar), MH", "hi": "सोलापुर, महाराष्ट्र", "mr": "सोलापूर, महाराष्ट्र"}, "lat": 17.6599, "lon": 75.9064},
    "indore": {"name": {"en": "Indore (Malwa Soybean Belt), MP", "hi": "इंदौर (मालवा), मध्य प्रदेश", "mr": "इंदूर (माळवा), मध्य प्रदेश"}, "lat": 22.7196, "lon": 75.8577},
    "bhopal": {"name": {"en": "Bhopal, Madhya Pradesh", "hi": "भोपाल, मध्य प्रदेश", "mr": "भोपाळ, मध्य प्रदेश"}, "lat": 23.2599, "lon": 77.4126},
    "jaipur": {"name": {"en": "Jaipur (Mustard/Bajra), Rajasthan", "hi": "जयपुर, राजस्थान", "mr": "जयपूर, राजस्थान"}, "lat": 26.9124, "lon": 75.7873},
    "ludhiana": {"name": {"en": "Ludhiana (Wheat & Rice), Punjab", "hi": "लुधियाना, पंजाब", "mr": "लुधियाना, पंजाब"}, "lat": 30.9010, "lon": 75.8573},
    "karnal": {"name": {"en": "Karnal (Basmati Rice Belt), Haryana", "hi": "करनाल (धान बेल्ट), हरियाणा", "mr": "कर्नाल (बासमती पट्टा), हरियाणा"}, "lat": 29.6857, "lon": 76.9905},
    "lucknow": {"name": {"en": "Lucknow, Uttar Pradesh", "hi": "लखनऊ, उत्तर प्रदेश", "mr": "लखनौ, उत्तर प्रदेश"}, "lat": 26.8467, "lon": 80.9462},
    "patna": {"name": {"en": "Patna, Bihar", "hi": "पटना, बिहार", "mr": "पाटणा, बिहार"}, "lat": 25.5941, "lon": 85.1376},
    "hyderabad": {"name": {"en": "Hyderabad, Telangana", "hi": "हैदराबाद, तेलंगाना", "mr": "हैदराबाद, तेलंगणा"}, "lat": 17.3850, "lon": 78.4867},
    "bengaluru": {"name": {"en": "Bengaluru, Karnataka", "hi": "बेंगलुरु, कर्नाटक", "mr": "बंगळुरू, कर्नाटक"}, "lat": 12.9716, "lon": 77.5946},
    "ahmedabad": {"name": {"en": "Ahmedabad (Cotton Belt), Gujarat", "hi": "अहमदाबाद, गुजरात", "mr": "अहमदाबाद, गुजरात"}, "lat": 23.0225, "lon": 72.5714},
    "guntur": {"name": {"en": "Guntur (Chili & Tobacco Hub), AP", "hi": "गुंटूर (मिर्च बेल्ट), आंध्र प्रदेश", "mr": "गुंटूर (मिरची पट्टा), आंध्र प्रदेश"}, "lat": 16.3067, "lon": 80.4365},
}

# WMO Weather interpretation codes (WW)
WEATHER_CODES = {
    0: {"en": "Clear sky", "hi": "साफ आसमान", "mr": "निरभ्र आकाश", "icon": "☀️", "type": "sunny"},
    1: {"en": "Mainly clear", "hi": "मुख्यतः साफ", "mr": "मुख्यतः स्वच्छ", "icon": "🌤️", "type": "partly_sunny"},
    2: {"en": "Partly cloudy", "hi": "आंशिक बादल", "mr": "अंशतः ढगाळ", "icon": "⛅", "type": "partly_cloudy"},
    3: {"en": "Overcast", "hi": "घने बादल", "mr": "ढगाळ वातावरण", "icon": "☁️", "type": "cloudy"},
    45: {"en": "Foggy", "hi": "कोहरा", "mr": "धुके", "icon": "🌫️", "type": "fog"},
    48: {"en": "Depositing rime fog", "hi": "सफेद घना कोहरा", "mr": "दाट धुके", "icon": "🌫️", "type": "fog"},
    51: {"en": "Light drizzle", "hi": "हल्की बूंदाबांदी", "mr": "हलकी रिमझिम", "icon": "🌦️", "type": "rain"},
    53: {"en": "Moderate drizzle", "hi": "मध्यम बूंदाबांदी", "mr": "मध्यम रिमझिम", "icon": "🌦️", "type": "rain"},
    55: {"en": "Dense drizzle", "hi": "तेज बूंदाबांदी", "mr": "दाट रिमझिम", "icon": "🌧️", "type": "rain"},
    61: {"en": "Slight rain", "hi": "हल्की बारिश", "mr": "हलका पाऊस", "icon": "🌧️", "type": "rain"},
    63: {"en": "Moderate rain", "hi": "मध्यम बारिश", "mr": "मध्यम पाऊस", "icon": "🌧️", "type": "rain"},
    65: {"en": "Heavy rain", "hi": "भारी बारिश", "mr": "मुसळधार पाऊस", "icon": "⛈️", "type": "heavy_rain"},
    71: {"en": "Slight snow", "hi": "हल्की बर्फबारी", "mr": "हलका हिमवर्षाव", "icon": "🌨️", "type": "snow"},
    73: {"en": "Moderate snow", "hi": "मध्यम बर्फबारी", "mr": "मध्यम हिमवर्षाव", "icon": "❄️", "type": "snow"},
    75: {"en": "Heavy snow", "hi": "भारी बर्फबारी", "mr": "मुसळधार हिमवर्षाव", "icon": "❄️", "type": "snow"},
    80: {"en": "Rain showers", "hi": "बारिश की बौछारें", "mr": "पावसाच्या सरी", "icon": "🌦️", "type": "rain"},
    81: {"en": "Moderate rain showers", "hi": "मध्यम बौछारें", "mr": "मध्यम पावसाच्या सरी", "icon": "🌧️", "type": "rain"},
    82: {"en": "Violent rain showers", "hi": "तेज बौछारें", "mr": "जोरदार पावसाच्या सरी", "icon": "⛈️", "type": "heavy_rain"},
    95: {"en": "Thunderstorm", "hi": "गरज-चमक के साथ तूफान", "mr": "वादळी पाऊस / मेघगर्जना", "icon": "⛈️", "type": "thunder"},
    96: {"en": "Thunderstorm with slight hail", "hi": "ओलावृष्टि के साथ तूफान", "mr": "गारपिटीसह वादळी पाऊस", "icon": "⛈️", "type": "thunder"},
    99: {"en": "Thunderstorm with heavy hail", "hi": "भारी ओलावृष्टि व तूफान", "mr": "तीव्र गारपीट व वादळ", "icon": "⛈️", "type": "thunder"},
}


def get_weather_desc(code, lang="en"):
    entry = WEATHER_CODES.get(code, WEATHER_CODES[0])
    text = entry.get(lang, entry["en"])
    return {"text": text, "icon": entry["icon"], "type": entry["type"]}


def get_severity_icon_type(code, rain_prob=0):
    if code in [0, 1]:
        return "sunny"
    elif code in [2, 3]:
        return "cloudy"
    elif code in [45, 48]:
        return "fog"
    elif code in [51, 53, 61] or (0 < rain_prob <= 30):
        return "drizzle_light"
    elif code in [55, 63] or (30 < rain_prob <= 60):
        return "drizzle_heavy"
    elif code in [65, 80, 81, 82] or rain_prob > 60:
        return "rain_shower"
    elif code in [95, 96, 99]:
        return "storm"
    return "cloudy"


def degrees_to_compass(deg, lang="en"):
    """
    Convert wind direction degrees (0-360) into localized compass directions.
    """
    try:
        val = int((float(deg) / 22.5) + 0.5) % 16
    except (ValueError, TypeError):
        val = 0

    compass_en = ["N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE", "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW"]
    compass_hi = ["उत्तर (N)", "उत्तर-उत्तर-पूर्व", "उत्तर-पूर्व (NE)", "पूर्व-उत्तर-पूर्व", "पूर्व (E)", "पूर्व-दक्षिण-पूर्व", "दक्षिण-पूर्व (SE)", "दक्षिण-दक्षिण-पूर्व", "दक्षिण (S)", "दक्षिण-दक्षिण-पश्चिम", "दक्षिण-पश्चिम (SW)", "पश्चिम-दक्षिण-पश्चिम", "पश्चिम (W)", "पश्चिम-उत्तर-पश्चिम", "उत्तर-पश्चिम (NW)", "उत्तर-उत्तर-पश्चिम"]
    compass_mr = ["उत्तर (N)", "उत्तर-उत्तर-पूर्व", "ईशान्य (NE)", "पूर्व-उत्तर-पूर्व", "पूर्व (E)", "पूर्व-आग्नेय", "आग्नेय (SE)", "दक्षिण-आग्नेय", "दक्षिण (S)", "दक्षिण-नैऋत्य", "नैऋत्य (SW)", "पश्चिम-नैऋत्य", "पश्चिम (W)", "पश्चिम-वायव्य", "वायव्य (NW)", "उत्तर-वायव्य"]

    if lang == "hi":
        return compass_hi[val]
    elif lang == "mr":
        return compass_mr[val]
    return compass_en[val]


def search_locations(query):
    """
    Search for Indian cities, districts, talukas, and villages via Open-Meteo Geocoding API.
    India results are sorted to the top; other countries follow.
    """
    q = (query or "").strip()
    if len(q) < 2:
        return []

    cache_key = q.lower()
    cached_val, is_expired = _SEARCH_LOCATIONS_CACHE.get(cache_key)
    if cached_val is not None and not is_expired:
        return cached_val

    url = f"https://geocoding-api.open-meteo.com/v1/search?name={q}&count=15&language=en&format=json"
    try:
        resp = requests.get(url, timeout=7)
        resp.raise_for_status()
        data = resp.json()
        india_results = []
        other_results = []
        for item in data.get("results", []):
            name = item.get("name", "")
            admin1 = item.get("admin1", "")  # State
            country = item.get("country", "")
            lat = item.get("latitude")
            lon = item.get("longitude")

            display_name = name
            if admin1:
                display_name += f", {admin1}"
            if country and country != "India":
                display_name += f", {country}"

            entry = {
                "name": display_name,
                "lat": lat,
                "lon": lon,
                "state": admin1,
                "country": country,
            }
            if country == "India":
                india_results.append(entry)
            else:
                other_results.append(entry)

        # Return India results first, then others, capped at 8 total
        combined = (india_results + other_results)[:8]
        _SEARCH_LOCATIONS_CACHE.set(cache_key, combined)
        return combined
    except Exception:
        if cached_val is not None:
            return cached_val
        return []


def reverse_geocode(lat, lon):
    """
    Convert lat/lon coordinates to a human-readable location name using
    OpenStreetMap Nominatim reverse geocoding API with BigDataCloud fallback.
    Returns a string like "Pune, Maharashtra" or "Lat X, Lon Y" as fallback.
    """
    try:
        lat_f = float(lat)
        lon_f = float(lon)
    except (ValueError, TypeError):
        lat_f = 18.5204
        lon_f = 73.8567

    cache_key = (round(lat_f, 3), round(lon_f, 3))
    cached_val, is_expired = _REVERSE_GEO_CACHE.get(cache_key)
    if cached_val is not None and not is_expired:
        return cached_val

    # 1. Primary provider: OpenStreetMap Nominatim
    try:
        url = (
            f"https://nominatim.openstreetmap.org/reverse"
            f"?lat={lat_f}&lon={lon_f}&format=json&zoom=10&addressdetails=1"
        )
        headers = {"User-Agent": "KrishiSahayak/1.0 (agricultural-assistant)"}
        resp = requests.get(url, timeout=7, headers=headers)
        resp.raise_for_status()
        data = resp.json()
        address = data.get("address", {})
        # Build a short human-readable name: city/town/village + state
        city = (
            address.get("city")
            or address.get("town")
            or address.get("village")
            or address.get("county")
            or address.get("district")
            or ""
        )
        state = address.get("state", "")
        parts = [p for p in [city, state] if p]
        if parts:
            res = ", ".join(parts)
            _REVERSE_GEO_CACHE.set(cache_key, res)
            return res
    except Exception:
        pass

    # 2. Resilient fallback provider: BigDataCloud Reverse Geocoding Client API
    # Keyless, unmetered, cloud-friendly endpoint that works reliably in server environments
    try:
        bdc_url = (
            f"https://api.bigdatacloud.net/data/reverse-geocode-client"
            f"?latitude={lat_f}&longitude={lon_f}&localityLanguage=en"
        )
        bdc_resp = requests.get(bdc_url, timeout=5)
        bdc_resp.raise_for_status()
        bdc_data = bdc_resp.json()
        city = (
            bdc_data.get("city")
            or bdc_data.get("locality")
            or ""
        )
        state = bdc_data.get("principalSubdivision", "")
        if not city and bdc_data.get("localityInfo"):
            for admin in bdc_data.get("localityInfo", {}).get("administrative", []):
                admin_name = admin.get("name", "")
                if admin_name and admin_name not in ["India", state]:
                    city = admin_name
                    break
        parts = [p for p in [city, state] if p]
        if parts:
            res = ", ".join(parts)
            _REVERSE_GEO_CACHE.set(cache_key, res)
            return res
    except Exception:
        pass

    if cached_val is not None:
        return cached_val
    fallback = f"Lat {lat_f:.2f}, Lon {lon_f:.2f}"
    _REVERSE_GEO_CACHE.set(cache_key, fallback)
    return fallback


def calculate_agri_advisory(temp, humidity, wind_speed, rain_prob, current_rain, lang="en"):
    """
    Generate farmer-centric agricultural advisories for spraying, irrigation, and pest risk.
    """
    # 1. Spray suitability
    if current_rain > 0 or rain_prob >= 40:
        spray_status = "unsafe"
        spray_badge = {"en": "Not Recommended", "hi": "छिड़काव न करें", "mr": "फवारणी टाळा"}
        spray_tip = {
            "en": f"Rain probability is {rain_prob}%. Pesticide or foliar spray will wash away.",
            "hi": f"बारिश की संभावना {rain_prob}% है। छिड़काव धुलने का जोखिम है, इसलिए अभी टालें।",
            "mr": f"पावसाची शक्यता {rain_prob}% आहे. औषध वाहून जाण्याची भीती असल्याने फवारणी करू नका.",
        }
    elif wind_speed > 15:
        spray_status = "warning"
        spray_badge = {"en": "Caution - High Wind", "hi": "सावधानी - तेज हवा", "mr": "सावध - वेगवान वारा"}
        spray_tip = {
            "en": f"Wind speed is {wind_speed} km/h (>15 km/h). Spray drift causes uneven coverage and chemical loss.",
            "hi": f"हवा की गति {wind_speed} किमी/घंटा है। तेज हवा से दवा इधर-उधर उड़कर नष्ट होगी।",
            "mr": f"वाऱ्याचा वेग {wind_speed} किमी/तास आहे. वाऱ्यामुळे औषध उडून वाया जाऊ शकते.",
        }
    elif temp > 35:
        spray_status = "warning"
        spray_badge = {"en": "Spray in Morning / Evening", "hi": "सुबह या शाम को छिड़कें", "mr": "सकाळी किंवा संध्याकाळी फवारा"}
        spray_tip = {
            "en": f"High temperature ({temp}°C) causes rapid evaporation. Spray only between 6:30-9:30 AM or 4:30-6:30 PM.",
            "hi": f"अधिक तापमान ({temp}°C) से दवा जल्दी सूखती है। केवल सुबह 6:30-9:30 या शाम 4:30-6:30 बजे छिड़कें।",
            "mr": f"जास्त तापमानामुळे ({temp}°C) औषधाचे बाष्पीभवन होते. फक्त सकाळी ६:३०-९:३० किंवा संध्याकाळी फवारा.",
        }
    else:
        spray_status = "safe"
        spray_badge = {"en": "Ideal for Spraying", "hi": "छिड़काव के लिए उत्तम", "mr": "फवारणीसाठी उत्तम"}
        spray_tip = {
            "en": f"Calm wind ({wind_speed} km/h) and low rain risk ({rain_prob}%). Excellent window for pesticide & nutrient sprays.",
            "hi": f"शांत हवा ({wind_speed} किमी/घंटा) और बारिश का जोखिम नहीं ({rain_prob}%)। कीटनाशक व टॉनिक छिड़काव के लिए श्रेष्ठ समय।",
            "mr": f"शांत हवामान ({wind_speed} किमी/तास) व पावसाचा धोका नाही ({rain_prob}%). फवारणीसाठी अत्यंत योग्य वेळ.",
        }

    # 2. Irrigation advisory
    if rain_prob >= 50 or current_rain > 2:
        irrigation_tip = {
            "en": "Rain expected. Postpone irrigation to prevent waterlogging and save electricity/water.",
            "hi": "बारिश की प्रबल संभावना है। सिंचाई टालें ताकि खेत में जलभराव न हो और बिजली-पानी की बचत हो।",
            "mr": "पावसाची शक्यता असल्याने पाणी देणे पुढे ढकला; शेतात पाणी साचू देऊ नका.",
        }
    elif temp >= 34 and humidity < 40:
        irrigation_tip = {
            "en": "Hot and dry climate. Provide light evening irrigation or drip to prevent plant heat stress.",
            "hi": "गर्म व शुष्क मौसम। फसलों को सूखने से बचाने हेतु शाम को ड्रिप या हल्की सिंचाई करें।",
            "mr": "उष्ण व कोरडे हवामान. पिकांवर ताण येऊ नये म्हणून संध्याकाळी हलके पाणी किंवा ठिबक सुरू ठेवा.",
        }
    else:
        irrigation_tip = {
            "en": "Normal weather. Follow standard irrigation schedule based on current crop growth stage.",
            "hi": "सामान्य मौसम। फसल की अवस्था के अनुसार नियमित सिंचाई जारी रखें।",
            "mr": "हवामान सामान्य आहे. पिकाच्या वाढीनुसार नियमित पाणी द्या.",
        }

    # 3. Fungal / Pest Risk
    if humidity >= 78 and 20 <= temp <= 32:
        pest_status = "warning"
        pest_alert = {
            "en": "High humidity + warm temperature: High risk of fungal diseases (Blast, Rust, Blight, Powdery Mildew). Inspect crops closely.",
            "hi": "अधिक नमी + मध्यम तापमान: फफूंद जनित रोगों (झुलसा, रतुआ, करपा) का अधिक जोखिम। खेत का नियमित निरीक्षण करें।",
            "mr": "जास्त आर्द्रता + उबदार हवामान: बुरशीजन्य रोगांचा (करपा, तांबेरा, भुरी) धोका. पिकांची नियमित पाहणी करा.",
        }
    elif humidity < 35 and temp > 32:
        pest_status = "warning"
        pest_alert = {
            "en": "Dry and hot weather: Risk of sucking pests (Mites, Thrips, Aphids, Whiteflies). Keep soil moist and install yellow sticky traps.",
            "hi": "शुष्क और गर्म मौसम: रस चूसक कीटों (माहू, थ्रिप्स, माइट्स, सफेद मक्खी) का प्रकोप बढ़ सकता है। पीले ट्रैप लगाएं।",
            "mr": "कोरडे व उष्ण हवामान: रसशोषक किडींचा (थ्रिप्स, मावा, कोळी, पांढरी माशी) प्रादुर्भाव वाढू शकतो. पिवळे चिकट सापळे लावा.",
        }
    else:
        pest_status = "safe"
        pest_alert = {
            "en": "Pest & disease climate risk is currently low. Continue standard IPM scouting.",
            "hi": "कीट व रोग का मौसमी जोखिम सामान्य है। नियमित देखभाल जारी रखें।",
            "mr": "कीड व रोगाचा हवामानविषयक धोका सध्या कमी आहे. नेहमीप्रमाणे पिकाची पाहणी सुरू ठेवा.",
        }

    return {
        "spray": {
            "status": spray_status,
            "badge": spray_badge.get(lang, spray_badge["en"]),
            "tip": spray_tip.get(lang, spray_tip["en"]),
        },
        "irrigation": {
            "tip": irrigation_tip.get(lang, irrigation_tip["en"]),
        },
        "pest": {
            "status": pest_status,
            "alert": pest_alert.get(lang, pest_alert["en"]),
        },
    }


def compute_best_spray_windows(hourly_times, hourly_temps, hourly_winds, hourly_probs, lang="en"):
    """
    Identify optimal pesticide/fertilizer spraying windows within the next 48 hours.
    Criteria: Wind speed <= 15 km/h, Rain probability <= 25%, Daylight hours (06:00 to 10:00, 16:00 to 19:00).
    """
    windows = []
    now_iso = datetime.now().strftime("%Y-%m-%dT%H:00")

    for i in range(len(hourly_times)):
        t_str = hourly_times[i]
        if t_str < now_iso:
            continue
        if len(windows) >= 4:
            break

        try:
            dt = datetime.strptime(t_str, "%Y-%m-%dT%H:%M")
        except Exception:
            continue

        hour = dt.hour
        wind = hourly_winds[i] if i < len(hourly_winds) else 10
        rain_p = hourly_probs[i] if i < len(hourly_probs) else 0
        temp = hourly_temps[i] if i < len(hourly_temps) else 25

        # Daylight spraying windows
        is_morning = 6 <= hour <= 10
        is_evening = 16 <= hour <= 18

        if (is_morning or is_evening) and wind <= 15 and rain_p <= 25 and temp <= 35:
            day_label = dt.strftime("%a, %d %b")
            time_label = dt.strftime("%I:%M %p")
            slot_type = "Morning" if is_morning else "Evening"

            if lang == "hi":
                label = f"{day_label} ({'प्रातः' if is_morning else 'सायं'} {time_label})"
                status_text = f"उत्तम - हवा {wind} किमी/घं, बारिश {rain_p}%, तापमान {round(temp)}°C"
            elif lang == "mr":
                label = f"{day_label} ({'सकाळी' if is_morning else 'संध्याकाळी'} {time_label})"
                status_text = f"उत्कृष्ट - वारा {wind} किमी/तास, पाऊस {rain_p}%, तापमान {round(temp)}°C"
            else:
                label = f"{day_label} ({slot_type} {time_label})"
                status_text = f"Optimal - Wind {wind} km/h, Rain {rain_p}%, Temp {round(temp)}°C"

            windows.append({
                "time_slot": label,
                "status": "safe",
                "details": status_text,
                "wind": wind,
                "rain_prob": rain_p,
                "temp": round(temp),
            })

    return windows


def get_weather_forecast(lat=18.5204, lon=73.8567, location_name=None, lang="en"):
    """
    Fetch comprehensive, real-time agricultural weather dataset from Open-Meteo API.
    Includes: Soil Temp & Moisture, ET0 Evapotranspiration, Wind Compass, 48-Hr Spray Windows, Hourly & 7-Day Forecasts.
    """
    try:
        lat = float(lat)
        lon = float(lon)
    except (ValueError, TypeError):
        lat = 18.5204
        lon = 73.8567

    cache_key = (round(lat, 2), round(lon, 2), lang)
    cached_val, is_expired = _WEATHER_CACHE.get(cache_key)
    if cached_val is not None and not is_expired:
        if location_name and cached_val.get("location_name") != location_name:
            res = dict(cached_val)
            res["location_name"] = location_name
            return res
        return cached_val

    url = (
        f"https://api.open-meteo.com/v1/forecast"
        f"?latitude={lat}&longitude={lon}"
        f"&current=temperature_2m,relative_humidity_2m,apparent_temperature,is_day,precipitation,weather_code,wind_speed_10m,wind_direction_10m,surface_pressure"
        f"&hourly=temperature_2m,relative_humidity_2m,precipitation_probability,precipitation,weather_code,wind_speed_10m,wind_direction_10m,soil_temperature_0cm,soil_moisture_0_to_1cm,et0_fao_evapotranspiration"
        f"&daily=weather_code,temperature_2m_max,temperature_2m_min,precipitation_probability_max,precipitation_sum,uv_index_max,sunrise,sunset,et0_fao_evapotranspiration"
        f"&timezone=auto"
    )

    try:
        resp = requests.get(url, timeout=7)
        resp.raise_for_status()
        data = resp.json()

        curr = data.get("current", {})
        daily = data.get("daily", {})
        hourly = data.get("hourly", {})

        current_temp = round(curr.get("temperature_2m", 28))
        apparent_temp = round(curr.get("apparent_temperature", current_temp))
        humidity = round(curr.get("relative_humidity_2m", 60))
        wind_speed = round(curr.get("wind_speed_10m", 8))
        wind_direction_deg = curr.get("wind_direction_10m", 0)
        wind_compass = degrees_to_compass(wind_direction_deg, lang)
        current_precip = curr.get("precipitation", 0)
        weather_code = curr.get("weather_code", 0)
        surface_pressure = round(curr.get("surface_pressure", 1013))
        desc_info = get_weather_desc(weather_code, lang)

        # 7-Day Daily Forecast
        daily_forecast = []
        time_list = daily.get("time", [])
        max_temps = daily.get("temperature_2m_max", [])
        min_temps = daily.get("temperature_2m_min", [])
        daily_codes = daily.get("weather_code", [])
        rain_probs = daily.get("precipitation_probability_max", [])
        rain_sums = daily.get("precipitation_sum", [])
        uv_indices = daily.get("uv_index_max", [])
        sunrises = daily.get("sunrise", [])
        sunsets = daily.get("sunset", [])
        et0_list = daily.get("et0_fao_evapotranspiration", [])

        today_rain_prob = rain_probs[0] if rain_probs else 10
        today_et0 = round(et0_list[0], 1) if et0_list and et0_list[0] is not None else 4.5
        today_sunrise = sunrises[0][-5:] if sunrises else "06:00"
        today_sunset = sunsets[0][-5:] if sunsets else "18:30"

        for i in range(min(7, len(time_list))):
            date_str = time_list[i]
            try:
                dt = datetime.strptime(date_str, "%Y-%m-%d")
                day_name = dt.strftime("%a, %d %b")
            except Exception:
                day_name = date_str

            day_w_code = daily_codes[i] if i < len(daily_codes) else 0
            day_w_desc = get_weather_desc(day_w_code, lang)
            w_type = get_severity_icon_type(day_w_code, rain_probs[i] if i < len(rain_probs) else 0)
            day_str = dt.strftime("%A") if 'dt' in locals() else "Day"

            daily_forecast.append({
                "date": day_name,
                "weekday": day_str,
                "max_temp": round(max_temps[i]) if i < len(max_temps) else current_temp,
                "min_temp": round(min_temps[i]) if i < len(min_temps) else current_temp - 8,
                "temp_max": round(max_temps[i]) if i < len(max_temps) else current_temp,
                "temp_min": round(min_temps[i]) if i < len(min_temps) else current_temp - 8,
                "rain_prob": rain_probs[i] if i < len(rain_probs) else 0,
                "rain_sum": round(rain_sums[i], 1) if i < len(rain_sums) else 0,
                "uv_index": round(uv_indices[i]) if i < len(uv_indices) else 5,
                "et0": round(et0_list[i], 1) if i < len(et0_list) and et0_list[i] is not None else 4.0,
                "condition": day_w_desc["text"],
                "icon": day_w_desc["icon"],
                "icon_type": w_type,
            })

        # 24-Hour Hourly Forecast
        hourly_forecast = []
        h_times = hourly.get("time", [])
        h_temps = hourly.get("temperature_2m", [])
        h_humidity = hourly.get("relative_humidity_2m", [])
        h_probs = hourly.get("precipitation_probability", [])
        h_precips = hourly.get("precipitation", [])
        h_codes = hourly.get("weather_code", [])
        h_winds = hourly.get("wind_speed_10m", [])
        h_soil_temps = hourly.get("soil_temperature_0cm", [])
        h_soil_moists = hourly.get("soil_moisture_0_to_1cm", [])

        # Find current hour index
        current_iso_hour = datetime.now().strftime("%Y-%m-%dT%H:00")
        start_idx = 0
        for idx, t_str in enumerate(h_times):
            if t_str >= current_iso_hour:
                start_idx = idx
                break

        current_soil_temp = round(h_soil_temps[start_idx], 1) if h_soil_temps and start_idx < len(h_soil_temps) and h_soil_temps[start_idx] is not None else current_temp - 1
        current_soil_moist_val = round(h_soil_moists[start_idx] * 100, 1) if h_soil_moists and start_idx < len(h_soil_moists) and h_soil_moists[start_idx] is not None else 28.0

        for i in range(start_idx, min(start_idx + 24, len(h_times))):
            t_str = h_times[i]
            try:
                dt = datetime.strptime(t_str, "%Y-%m-%dT%H:%M")
                time_label = dt.strftime("%I %p")
            except Exception:
                time_label = t_str[-5:]

            w_code = h_codes[i] if i < len(h_codes) else 0
            w_desc = get_weather_desc(w_code, lang)

            hourly_forecast.append({
                "time": time_label,
                "temp": round(h_temps[i]) if i < len(h_temps) else current_temp,
                "humidity": round(h_humidity[i]) if i < len(h_humidity) else 60,
                "wind_speed": round(h_winds[i]) if i < len(h_winds) else wind_speed,
                "rain_prob": h_probs[i] if i < len(h_probs) else 0,
                "precipitation": round(h_precips[i], 1) if i < len(h_precips) else 0,
                "icon": w_desc["icon"],
                "condition": w_desc["text"],
            })

        # Calculate 48-hour best spray windows
        spray_windows = compute_best_spray_windows(
            hourly_times=h_times,
            hourly_temps=h_temps,
            hourly_winds=h_winds,
            hourly_probs=h_probs,
            lang=lang,
        )

        # Agricultural Advisory
        advisory = calculate_agri_advisory(
            temp=current_temp,
            humidity=humidity,
            wind_speed=wind_speed,
            rain_prob=today_rain_prob,
            current_rain=current_precip,
            lang=lang,
        )

        loc_display = location_name
        if not loc_display:
            loc_display = f"Lat {lat:.2f}, Lon {lon:.2f}"

        result = {
            "success": True,
            "location_name": loc_display,
            "lat": lat,
            "lon": lon,
            "current": {
                "temp": current_temp,
                "feels_like": apparent_temp,
                "humidity": humidity,
                "wind_speed": wind_speed,
                "wind_direction": wind_direction_deg,
                "wind_compass": wind_compass,
                "precipitation": current_precip,
                "surface_pressure": surface_pressure,
                "weather_code": weather_code,
                "condition": desc_info["text"],
                "icon": desc_info["icon"],
                "type": desc_info["type"],
                "today_max": daily_forecast[0]["max_temp"] if daily_forecast else current_temp + 3,
                "today_min": daily_forecast[0]["min_temp"] if daily_forecast else current_temp - 6,
                "rain_prob": today_rain_prob,
                "uv_index": daily_forecast[0]["uv_index"] if daily_forecast else 6,
                "et0": today_et0,
                "sunrise": today_sunrise,
                "sunset": today_sunset,
                "soil_temp": current_soil_temp,
                "soil_moisture": current_soil_moist_val,
            },
            "spray_windows": spray_windows,
            "hourly": hourly_forecast,
            "daily": daily_forecast,
            "advisory": advisory,
            "updated_at": datetime.now().strftime("%I:%M %p"),
        }
        _WEATHER_CACHE.set(cache_key, result)
        return result

    except Exception as e:
        # If external request fails but a previous cached value exists, return stale cached value
        if cached_val is not None:
            if location_name and cached_val.get("location_name") != location_name:
                res = dict(cached_val)
                res["location_name"] = location_name
                return res
            return cached_val

        # Fallback simulation
        desc_info = get_weather_desc(1, lang)
        advisory = calculate_agri_advisory(28, 62, 10, 15, 0, lang=lang)
        return {
            "success": False,
            "error": str(e),
            "location_name": location_name or "Pune, Maharashtra",
            "lat": lat,
            "lon": lon,
            "current": {
                "temp": 28,
                "feels_like": 30,
                "humidity": 62,
                "wind_speed": 10,
                "wind_direction": 180,
                "wind_compass": degrees_to_compass(180, lang),
                "precipitation": 0,
                "surface_pressure": 1012,
                "weather_code": 1,
                "condition": desc_info["text"],
                "icon": desc_info["icon"],
                "type": desc_info["type"],
                "today_max": 31,
                "today_min": 21,
                "rain_prob": 15,
                "uv_index": 6,
                "et0": 4.5,
                "sunrise": "06:12",
                "sunset": "18:45",
                "soil_temp": 26.5,
                "soil_moisture": 32.0,
            },
            "spray_windows": [
                {"time_slot": "Tomorrow Morning (06:30 AM - 09:30 AM)", "status": "safe", "details": "Optimal window - Calm wind 8 km/h, Rain 5%"},
                {"time_slot": "Tomorrow Evening (04:30 PM - 06:30 PM)", "status": "safe", "details": "Good window - Wind 10 km/h, Rain 10%"},
            ],
            "hourly": [
                {"time": "Now", "temp": 28, "humidity": 62, "wind_speed": 10, "rain_prob": 15, "precipitation": 0, "icon": "🌤️", "condition": desc_info["text"]},
                {"time": "3 PM", "temp": 30, "humidity": 55, "wind_speed": 12, "rain_prob": 10, "precipitation": 0, "icon": "☀️", "condition": "Sunny"},
                {"time": "6 PM", "temp": 27, "humidity": 65, "wind_speed": 8, "rain_prob": 10, "precipitation": 0, "icon": "🌤️", "condition": "Mainly Clear"},
                {"time": "9 PM", "temp": 24, "humidity": 75, "wind_speed": 6, "rain_prob": 5, "precipitation": 0, "icon": "🌙", "condition": "Clear"},
            ],
            "daily": [
                {"date": "Today", "max_temp": 31, "min_temp": 21, "rain_prob": 15, "rain_sum": 0, "uv_index": 6, "et0": 4.5, "condition": desc_info["text"], "icon": "🌤️"},
                {"date": "Tomorrow", "max_temp": 32, "min_temp": 22, "rain_prob": 20, "rain_sum": 0, "uv_index": 7, "et0": 4.8, "condition": desc_info["text"], "icon": "☀️"},
                {"date": "Day 3", "max_temp": 30, "min_temp": 21, "rain_prob": 40, "rain_sum": 3.5, "uv_index": 5, "et0": 3.8, "condition": "Scattered Rain", "icon": "🌦️"},
            ],
            "advisory": advisory,
            "updated_at": datetime.now().strftime("%I:%M %p"),
        }
