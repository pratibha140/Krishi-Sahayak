# assistant_service.py
# Multilingual Smart Agricultural Voice & AI Assistant for Krishi Sahayak
# Incorporating 'Farmer's Handbook on Basic Agriculture' (MANAGE, GIZ, DFV)
# Answers farming queries in English, Hindi (हिन्दी), and Marathi (मराठी).

import re
from crops_data import CROPS
from disease_service import DISEASES, search_diseases
from handbook_data import (
    BOTANICAL_RECIPES,
    FARM_MECHANIZATION_TOOLS,
    FARMER_SERVICES,
    FERTILIZER_COMPATIBILITY,
    GOVERNMENT_SCHEMES,
    NUTRIENT_DEFICIENCIES,
    PESTICIDE_TOXICITY_CLASSES,
)
from weather_service import get_weather_forecast


def process_query(user_text, lang="en", lat=None, lon=None):
    """
    Process agricultural voice or text query and generate structured answers
    with speakable audio text and suggested follow-ups.
    """
    query = (user_text or "").lower().strip()
    if not query:
        return default_greeting(lang)

    clean_q = query

    # 1. Greetings
    if any(w in clean_q for w in ["hello", "hi", "namaste", "namaskar", "नमस्ते", "नमस्कार", "pranam", "प्रणाम", "ram ram", "राम राम", "hey", "kem cho"]):
        return default_greeting(lang)

    # 2. Weather & Spraying queries
    if any(w in clean_q for w in ["weather", "rain", "spray", "mosam", "mausam", "havaman", "barish", "paus", "हवामान", "मौसम", "बारिश", "पाऊस", "फवारणी", "छिड़काव", "तापमान", "humidity", "wind"]):
        return handle_weather_query(query, lang, lat, lon)

    # 3. Emergency Poisoning & First Aid
    if any(w in clean_q for w in ["poison", "poisoning", "first aid", "emergency", "zahar", "vishbadha", "prathmik upchar", "prathamopchar", "जहर", "विषबाधा", "प्राथमिक उपचार", "इमरजेंसी", "विषारीकरण"]):
        return handle_poisoning_first_aid(lang)

    # 4. Pesticide Toxicity Color Bands
    if any(w in clean_q for w in ["toxicity", "color band", "red band", "yellow band", "blue band", "green band", "vishari", "vishela", "रंग कोड", "लाल पट्टी", "पीली पट्टी", "निळी पट्टी", "विषारी", "विषैला"]):
        return handle_toxicity_bands(lang)

    # 5. Kisan Call Center Helpline & Contact
    if any(w in clean_q for w in ["call center", "helpline", "toll free", "1800", "1551", "phone number", "contact", "कॉल सेंटर", "हेल्पलाइन", "टोल फ्री", "नंबर", "संपर्क", "फोन"]):
        return handle_helpline_query(lang)

    # 6. Government schemes & KCC
    if any(w in clean_q for w in ["yojana", "scheme", "pm kisan", "pmfby", "bima", "vima", "kcc", "credit card", "योजना", "योजनाएं", "योजनाओं", "पीएम किसान", "विमा", "बीमा", "सब्सिडी", "अनुदान", "क्रेडिट कार्ड", "सरकारी योजना", "शासकीय योजना"]):
        return handle_schemes_query(lang)

    # 7. Nutrient Deficiencies (Zinc, Nitrogen, Iron, Boron, Calcium, etc.)
    for nut in NUTRIENT_DEFICIENCIES:
        nut_id = nut["id"]
        nut_name_en = nut["name"]["en"].lower()
        nut_name_hi = nut["name"]["hi"].lower()
        nut_name_mr = nut["name"]["mr"].lower()
        if (
            nut_id in clean_q
            or nut_name_en in clean_q
            or nut_name_hi in clean_q
            or nut_name_mr in clean_q
            or ("khaira" in clean_q and nut_id == "zinc")
            or ("white bud" in clean_q and nut_id == "zinc")
            or ("खैरा" in clean_q and nut_id == "zinc")
            or ("सफेद कली" in clean_q and nut_id == "zinc")
        ):
            return handle_nutrient_deficiency_query(nut, lang)

    if any(w in clean_q for w in ["deficiency", "poshak tatva", "annadravya", "nutrient", "पोषक तत्व", "कमतरता", "अन्नद्रव्य", "खैरा", "पीली पत्ती", "पाने पिवळी", "yellow leaves"]):
        return handle_general_nutrient_query(lang)

    # 8. Fertilizer Mixing Compatibility & Dosage
    if any(w in clean_q for w in ["mixing", "compatibility", "mix fertilizer", "urea and dap", "can i mix", "ekatra mislane", "मिलाना", "मिश्रण", "यूरिया और डीएपी", "खते एकत्र", "खाद मिलाना"]):
        return handle_fertilizer_mixing_query(lang)

    # 9. Farm Mechanization & Weeders
    if any(w in clean_q for w in ["mechanization", "wheel hoe", "weeder", "cono weeder", "crida", "yantra", "avjare", "यंत्र", "वीडर", "अवजारे", "मशीन", "खुरपणी यंत्र", "ट्रैक्टर"]):
        return handle_mechanization_query(lang)

    # 10. Organic farming (Jeevamrut, Neem oil, NSKE, Vermicompost, Dashparni)
    if any(w in clean_q for w in ["organic", "jeevamrut", "neem", "nske", "tobacco", "kerosene emulsion", "bio", "जैविक", "जीवामृत", "नीम तेल", "दशपर्णी", "सेंद्रिय", "गांडूळ खत", "निंबोळी अर्क", "वर्मीकंपोस्ट"]):
        return handle_organic_query(query, lang)

    # 11. Crop specific fertilizer, disease & overview queries
    for crop_id, crop in CROPS.items():
        crop_names = [
            crop_id,
            crop["names"]["en"].lower(),
            crop["names"]["hi"].lower(),
            crop["names"]["mr"].lower(),
        ]
        if any(cn in clean_q for cn in crop_names):
            if any(w in clean_q for w in ["fertilizer", "khat", "khad", "urea", "dap", "mop", "dosage", "खाद", "खत", "यूरिया", "मात्रा", "डोस", "पोटाश"]):
                return handle_crop_fertilizer_query(crop, lang)
            if any(w in clean_q for w in ["disease", "pest", "kida", "rog", "ill", "कीट", "रोग", "इल्ली", "किडी", "करपा", "ब्लाइट", "बंची टॉप", "लाल्या", "कोलशी", "रतुआ", "तांबेरा", "अळी", "सुंडी"]):
                return handle_crop_disease_query(crop, query, lang)
            return handle_crop_overview_query(crop, lang)

    # 12. General Disease / Pest queries
    if any(w in clean_q for w in ["disease", "pest", "fungus", "insect", "rog", "keet", "kidi", "रोग", "कीट", "किडी", "करपा", "ब्लाइट", "सुंडी", "माहू", "थ्रिप्स", "बंची टॉप", "तांबेरा", "अळी", "अगेती"]):
        return handle_general_disease_query(query, lang)

    # 13. Sowing / Season queries
    if any(w in clean_q for w in ["sow", "sowing", "season", "kharif", "rabi", "buwai", "perani", "बुवाई", "पेरणी", "खरीफ", "रबी", "हंगाम", "सीजन"]):
        return handle_season_query(lang)

    # 14. Intelligent Fallback Search across all database categories
    matched_search = search_knowledge_base(query, lang)
    if matched_search:
        return matched_search

    # Standard fallback response
    return handle_general_fallback(query, lang)


def default_greeting(lang):
    if lang == "hi":
        text = (
            "**नमस्ते किसान मित्र! मैं कृषि सहायक आवाज़ सहायक हूँ।**\n\n"
            "मैं आपकी निम्न वैज्ञानिक विषयों में सहायता कर सकता हूँ:\n"
            "• **लाइव मौसम व छिड़काव सूचकांक** (जैसे: *आज बारिश होगी क्या?*)\n"
            "• **पोषक तत्व व कमी निदान** (जैसे: *मक्के में सफेद पत्ती / जिंक की कमी*)\n"
            "• **फसलवार खाद व कैलेंडर** (जैसे: *केले या गन्ने में खाद की मात्रा*)\n"
            "• **कीट-रोग नियंत्रण व जहर प्राथमिक उपचार** (जैसे: *कोलशी रोग, कीटनाशक जहर उपचार*)\n"
            "• **सरकारी सेवाएं व KCC** (जैसे: *किसान कॉल सेंटर 1800-180-1551*)\n\n"
            "बोलें या नीचे दिए गए सुझावों में से चुनें।"
        )
        speak_text = "नमस्ते किसान भाई! मैं कृषि सहायक हूँ। आप मुझसे मौसम, फसल खाद, पोषक तत्व कमी, रोग नियंत्रण और किसान कॉल सेंटर के बारे में पूछ सकते हैं।"
        suggestions = ["आज मौसम व छिड़काव सलाह", "जिंक की कमी के लक्षण", "केले में खाद की मात्रा", "किसान कॉल सेंटर नंबर"]
    elif lang == "mr":
        text = (
            "**नमस्कार शेतकरी बंधूंनो! मी कृषी सहाय्यक आवाज सहाय्यक आहे.**\n\n"
            "मी खालील वैज्ञानिक विषयांवर आपली मदत करू शकतो:\n"
            "• **थेट हवामान व फवारणी सल्ला** (उदा: *आज पाऊस पडेल का?*)\n"
            "• **अन्नद्रव्य कमतरता निदान** (उदा: *मक्यामध्ये पांढरी पाने / झिंक कमतरता*)\n"
            "• **पीक खत व्यवस्थापन** (उदा: *केळी किंवा संत्रा खत नियोजन*)\n"
            "• **रोग नियंत्रण व विषबाधा प्रथमोपचार** (उदा: *संत्र्यावरील कोलशी, कीटकनाशक प्रथमोपचार*)\n"
            "• **शासकीय सेवा व KCC** (उदा: *किसान कॉल सेंटर १८००-१८०-१५५१*)\n\n"
            "बोला किंवा खालील पर्यायांमधून निवडा."
        )
        speak_text = "नमस्कार शेतकरी मित्रा! मी कृषी सहाय्यक आहे. हवामान, अन्नद्रव्य कमतरता, खत मात्रा, पीक रोग आणि किसान कॉल सेंटरविषयी विचारा."
        suggestions = ["आज हवामान व फवारणी सल्ला", "झिंक कमतरता उपाय", "केळी खत व्यवस्थापन", "किसान कॉल सेंटर १८००-१८०-१५५१"]
    else:
        text = (
            "**Welcome to Krishi Sahayak Voice Assistant!**\n\n"
            "I can assist you with:\n"
            "• **Live Weather & Spraying Suitability** (e.g. *Will it rain today?*)\n"
            "• **12 Nutrient Deficiency Diagnostics** (e.g. *Zinc deficiency in maize/rice*)\n"
            "• **Fertilizer Calculation & Crop Packages** (e.g. *Banana, Mango, Citrus dosage*)\n"
            "• **Pesticide Safety & First Aid** (e.g. *Toxicity color bands, Poison first aid*)\n"
            "• **Farmer Helplines & KCC** (e.g. *Kisan Call Center 1800-180-1551*)\n\n"
            "Speak your question or pick a suggested topic below."
        )
        speak_text = "Hello! I am your Krishi Sahayak assistant. Ask me about weather, nutrient deficiencies, crop packages, pesticide safety, or Kisan Call Center."
        suggestions = ["Live Weather & Spraying", "Zinc deficiency in Maize", "Fertilizer for Banana", "Kisan Call Center 1800-180-1551"]

    return {"text": text, "speak_text": speak_text, "suggestions": suggestions}


def handle_weather_query(query, lang, lat, lon):
    weather = get_weather_forecast(lat or 18.5204, lon or 73.8567, lang=lang)
    curr = weather.get("current", {})
    advisory = weather.get("advisory", {})
    temp = curr.get("temp", 28)
    condition = curr.get("condition", "Clear")
    rain_prob = curr.get("rain_prob", 10)
    spray = advisory.get("spray", {})
    spray_badge = spray.get("badge", "Check conditions")
    spray_tip = spray.get("tip", "")

    if lang == "hi":
        text = (
            f"### 🌦️ लाइव मौसम व कृषि सलाह ({weather.get('location_name', 'आपका क्षेत्र')})\n\n"
            f"• **वर्तमान तापमान:** {temp}°C (स्थिति: {condition})\n"
            f"• **बारिश की संभावना:** {rain_prob}%\n"
            f"• **नमी:** {curr.get('humidity', 60)}% | **हवा की गति:** {curr.get('wind_speed', 8)} किमी/घंटा\n\n"
            f"**🌾 छिड़काव सलाह:** **{spray_badge}**\n"
            f"{spray_tip}\n\n"
            f"**💧 सिंचाई सलाह:** {advisory.get('irrigation', {}).get('tip', '')}"
        )
        speak_text = f"वर्तमान तापमान {temp} डिग्री सेल्सियस है और मौसम {condition} है। बारिश की संभावना {rain_prob} प्रतिशत है। {spray_tip}"
        suggestions = ["7 दिनों का मौसम पूर्वानुमान", "खाद की मात्रा जानें", "पोषक तत्व कमी निदान", "फसल कैलेंडर"]
    elif lang == "mr":
        text = (
            f"### 🌦️ थेट हवामान व कृषी सल्ला ({weather.get('location_name', 'तुमचा परिसर')})\n\n"
            f"• **सध्याचे तापमान:** {temp}°C (स्थिती: {condition})\n"
            f"• **पावसाची शक्यता:** {rain_prob}%\n"
            f"• **आर्द्रता:** {curr.get('humidity', 60)}% | **वाऱ्याचा वेग:** {curr.get('wind_speed', 8)} किमी/तास\n\n"
            f"**🌾 फवारणी सल्ला:** **{spray_badge}**\n"
            f"{spray_tip}\n\n"
            f"**💧 पाणी व्यवस्थापन:** {advisory.get('irrigation', {}).get('tip', '')}"
        )
        speak_text = f"सध्याचे तापमान {temp} अंश सेल्सिअस असून हवामान {condition} आहे. पावसाची शक्यता {rain_prob} टक्के आहे. {spray_tip}"
        suggestions = ["७ दिवसांचा हवामान अंदाज", "कापूस खत मात्रा", "माती पोषण केंद्र", "पीक कॅलेंडर"]
    else:
        text = (
            f"### 🌦️ Live Weather & Farm Advisory ({weather.get('location_name', 'Your Location')})\n\n"
            f"• **Current Temperature:** {temp}°C ({condition})\n"
            f"• **Rain Probability:** {rain_prob}%\n"
            f"• **Humidity:** {curr.get('humidity', 60)}% | **Wind Speed:** {curr.get('wind_speed', 8)} km/h\n\n"
            f"**🌾 Spraying Advisory:** **{spray_badge}**\n"
            f"{spray_tip}\n\n"
            f"**💧 Irrigation Advisory:** {advisory.get('irrigation', {}).get('tip', '')}"
        )
        speak_text = f"The temperature is {temp} degrees Celsius with {condition}. Rain probability is {rain_prob} percent. {spray_tip}"
        suggestions = ["7-day weather forecast", "Nutrient deficiency guide", "Banana fertilizer", "Crop Calendar"]

    return {"text": text, "speak_text": speak_text, "suggestions": suggestions}


def handle_poisoning_first_aid(lang):
    if lang == "hi":
        text = (
            "### 🚨 कीटनाशक विषबाधा आपातकालीन प्राथमिक उपचार (Emergency First Aid)\n\n"
            "1. **त्वचा संसर्ग:** तुरंत कपड़े उतारकर साबुन व प्रचुर मात्रा में साफ पानी से धोएं।\n"
            "2. **आंखों में दवा जाना:** आंखों को 15 मिनट तक लगातार साफ पानी से धोएं।\n"
            "3. **सांस द्वारा दवा खिंचना:** पीड़ित को तुरंत खुली व ताजी हवा में ले जाएं।\n"
            "4. **निगल जाना:** यदि रोगी होश में हो तो गुनगुना नमकीन पानी पिलाकर उल्टी कराने का प्रयास करें (पेट्रोलियम विषाक्तता में न कराएं)।\n"
            "5. **आपातकालीन नंबर:** किसान कॉल सेंटर **1800-180-1551** या निकटतम अस्पताल 108 पर तुरंत संपर्क करें।"
        )
        speak_text = "कीटनाशक जहर के मामले में पीड़ित को तुरंत ताजी हवा में लाएं, कपड़े बदलकर त्वचा को साबुन से धोएं और 108 या 1800-180-1551 पर कॉल करें।"
        suggestions = ["कीटनाशक विषाक्तता रंग पट्टी", "किसान कॉल सेंटर नंबर", "आज का मौसम", "जैविक कीटनाशक"]
    elif lang == "mr":
        text = (
            "### 🚨 कीटकनाशक विषबाधा आपत्कालीन प्रथमोपचार (Emergency First Aid)\n\n"
            "१. **त्वचेचा संपर्क:** ताबडतोब कपडे काढून साबण व भरपूर स्वच्छ पाण्याने त्वचा धुवा.\n"
            "२. **डोळ्यात औषध जाणे:** डोळे १५ मिनिटे सतत स्वच्छ पाण्याने धुवावेत.\n"
            "३. **श्वासावाटे विष जाणे:** रुग्णाला ताबडतोब मोकळ्या व ताज्या हवेत आणा.\n"
            "४. **औषध पोटात जाणे:** रुग्ण शुद्धीवर असल्यास कोमट मिठाचे पाणी देऊन उलट्या करवण्याचा प्रयत्न करा.\n"
            "५. **आपत्कालीन संपर्क:** किसान कॉल सेंटर **१८००-१८०-१५५१** किंवा १०८ रुग्णवाहिकेला तात्काळ कॉल करा."
        )
        speak_text = "कीटकनाशक विषबाधा झाल्यास रुग्णाला मोकळ्या हवेत आणा, कपडे बदलून साबणाने त्वचा धुवा आणि १८००-१८०-१५५१ वर कॉल करा."
        suggestions = ["कीटकनाशक विषारीपण रंग पट्टी", "किसान कॉल सेंटर १८००-१८०-१५५१", "हवामान अंदाज", "सेंद्रिय कीटकनाशक"]
    else:
        text = (
            "### 🚨 Pesticide Poisoning Emergency First Aid Protocol\n\n"
            "1. **Skin Contact:** Remove contaminated clothing immediately and wash skin with soap and copious clean water.\n"
            "2. **Eye Contact:** Rinse eyes continuously with clean running water for at least 15 minutes.\n"
            "3. **Inhalation:** Move victim immediately to fresh open air.\n"
            "4. **Ingestion:** If victim is conscious, induce vomiting by offering warm salt water (except for hydrocarbon/petroleum poisons).\n"
            "5. **Emergency Contacts:** Call Kisan Call Center **1800-180-1551** or Emergency Medical Services (108) immediately."
        )
        speak_text = "In case of pesticide poisoning, move victim to fresh air, wash skin thoroughly with soap and water, and call 1800-180-1551 immediately."
        suggestions = ["Pesticide toxicity color bands", "Kisan Call Center Helpline", "Live Weather", "Organic Pesticides"]

    return {"text": text, "speak_text": speak_text, "suggestions": suggestions}


def handle_toxicity_bands(lang):
    if lang == "hi":
        text = (
            "### 🔴🟡🔵🟢 कीटनाशक विषाक्तता रंग कोड पट्टी (Toxicity Color Bands)\n\n"
            "1. 🔴 **लाल पट्टी (Red Band - Extremely Toxic):** अत्यधिक विषैला। चिन्ह: खोपड़ी व क्रास बोन। सावधानी: अत्यंत सतर्कता व पीपीई किट अनिवार्य।\n"
            "2. 🟡 **पीली पट्टी (Yellow Band - Highly Toxic):** उच्च विषैला। शब्द: POISON (विष)।\n"
            "3. 🔵 **नीली पट्टी (Blue Band - Moderately Toxic):** मध्यम विषैला। शब्द: DANGER (खतरा)।\n"
            "4. 🟢 **हरी पट्टी (Green Band - Slightly Toxic):** हल्का विषैला। शब्द: CAUTION (सावधान)।"
        )
        speak_text = "लाल पट्टी सबसे खतरनाक अत्यधिक विषैली होती है। पीली उच्च विषैली, नीली मध्यम और हरी हल्की विषैली होती है।"
        suggestions = ["कीटनाशक जहर का प्राथमिक उपचार", "किसान कॉल सेंटर 1800-180-1551", "जैविक कीटनाशक बनाएं", "मौसम रिपोर्ट"]
    elif lang == "mr":
        text = (
            "### 🔴🟡🔵🟢 कीटकनाशक विषारीपणाचे रंग कोड (Toxicity Color Bands)\n\n"
            "१. 🔴 **लाल पट्टी (Red Band):** अतिविषारी. चिन्ह: कवटी व दोन हाडे. अत्यंत काळजीपूर्वक वापरणे आवश्यक.\n"
            "२. 🟡 **पिवळी पट्टी (Yellow Band):** जास्त विषारी. शब्द: POISON (विष).\n"
            "३. 🔵 **निळी पट्टी (Blue Band):** मध्यम विषारी. शब्द: DANGER (धोका).\n"
            "४. 🟢 **हिरवी पट्टी (Green Band):** कमी विषारी. शब्द: CAUTION (सावधान)."
        )
        speak_text = "लाल पट्टी अतिविषारी व घातक असते. पिवळी जास्त विषारी, निळी मध्यम आणि हिरवी कमी विषारी असते."
        suggestions = ["विषबाधा प्रथमोपचार", "किसान कॉल सेंटर १८००-१८०-१५५१", "सेंद्रिय अर्क बनवा", "हवामान अंदाज"]
    else:
        text = (
            "### 🔴🟡🔵🟢 Insecticide Toxicity Color Band Classification\n\n"
            "1. 🔴 **Red Band (Extremely Toxic):** Symbol: Skull & Crossbones. Requires extreme caution & protective gear.\n"
            "2. 🟡 **Yellow Band (Highly Toxic):** Word: POISON.\n"
            "3. 🔵 **Blue Band (Moderately Toxic):** Word: DANGER.\n"
            "4. 🟢 **Green Band (Slightly Toxic):** Word: CAUTION."
        )
        speak_text = "Red band insecticides are extremely toxic with a skull symbol. Yellow is highly toxic, Blue is moderately toxic, and Green is slightly toxic."
        suggestions = ["Poisoning First Aid Protocol", "Kisan Call Center 1800-180-1551", "Organic Formulations", "Live Weather"]

    return {"text": text, "speak_text": speak_text, "suggestions": suggestions}


def handle_helpline_query(lang):
    if lang == "hi":
        text = (
            "### 📞 किसान कॉल सेंटर (Kisan Call Center) व हेल्पलाइन\n\n"
            "• **टोल फ्री नंबर:** **1800-180-1551** (सुबह 6:00 बजे से रात 10:00 बजे तक)\n"
            "• **भाषाएं:** हिंदी, मराठी, अंग्रेजी सहित 22 भाषाओं में कृषि वैज्ञानिकों द्वारा मुफ्त सलाह।\n"
            "• **पीएम किसान सहायता:** 155261 / 011-24300606\n"
            "• **फसल बीमा हेल्पलाइन (PMFBY):** 14447"
        )
        speak_text = "किसान कॉल सेंटर का टोल फ्री नंबर है 1800-180-1551। यह सुबह 6 से रात 10 बजे तक सभी भाषाओं में उपलब्ध है।"
        suggestions = ["पीएम किसान योजना", "फसल बीमा योजना", "आज का मौसम", "खाद की मात्रा"]
    elif lang == "mr":
        text = (
            "### 📞 किसान कॉल सेंटर (Kisan Call Center) हेल्पलाइन\n\n"
            "• **टोल फ्री क्रमांक:** **१८००-१८०-१५५१** (सकाळी ६:०० ते रात्री १०:००)\n"
            "• **भाषा:** मराठी, हिंदी, इंग्रजीसह २२ भाषांमध्ये कृषी तज्ज्ञांचा मोफत सल्ला.\n"
            "• **पीएम किसान हेल्पलाइन:** १५५२६१ / ०११-२४३००६०६\n"
            "• **पीक विमा हेल्पलाइन (PMFBY):** १४४४७"
        )
        speak_text = "किसान कॉल सेंटरचा टोल फ्री नंबर १८००-१८०-१५५१ आहे. हा सकाळी ६ ते रात्री १० पर्यंत मोफत उपलब्ध आहे."
        suggestions = ["पीएम किसान सन्मान निधी", "पीक विमा योजना", "हवामान अंदाज", "खत नियोजन"]
    else:
        text = (
            "### 📞 Kisan Call Center (KCC) & Agri Helplines\n\n"
            "• **Toll-Free Number:** **1800-180-1551** (Operating 6:00 AM to 10:00 PM daily)\n"
            "• **Languages:** Free guidance by agri-scientists in 22 local languages including Hindi, Marathi, and English.\n"
            "• **PM-Kisan Helpline:** 155261 / 011-24300606\n"
            "• **PMFBY Crop Insurance Toll-Free:** 14447"
        )
        speak_text = "The Kisan Call Center toll-free helpline number is 1800-180-1551 available daily from 6 AM to 10 PM."
        suggestions = ["PM-Kisan Scheme", "PMFBY Insurance", "Live Weather", "Fertilizer Calculator"]

    return {"text": text, "speak_text": speak_text, "suggestions": suggestions}


def handle_nutrient_deficiency_query(nut, lang):
    name = nut["name"].get(lang, nut["name"]["en"])
    symp = nut["symptoms"].get(lang, nut["symptoms"]["en"])
    corr_dict = nut.get("cure") or nut.get("correction") or {}
    corr = corr_dict.get(lang, corr_dict.get("en", ""))

    if lang == "hi":
        text = (
            f"### 🌾 {name} की कमी: लक्षण व उपचार\n\n"
            f"• **मुख्य लक्षण:** {symp}\n\n"
            f"• **निदान व पूर्ति उपाय:** {corr}\n\n"
            f"💡 *सलाह:* खड़ी फसल में छिड़काव के लिए सूक्ष्म पोषक तत्व हमेशा सुबह या शाम के समय दें।"
        )
        speak_text = f"{name} की कमी में {symp}। इसके उपचार के लिए: {corr}।"
        suggestions = ["अन्य पोषक तत्वों की कमी", "खातों की अनुकूलता तालिका", "मृदा परीक्षण कार्ड", "आज का मौसम"]
    elif lang == "mr":
        text = (
            f"### 🌾 {name} कमतरता: लक्षणे व उपाय\n\n"
            f"• **प्रमुख लक्षणे:** {symp}\n\n"
            f"• **उपाय व डोस:** {corr}\n\n"
            f"💡 *सल्ला:* सूक्ष्म अन्नद्रव्यांची फवारणी नेहमी सकाळी किंवा संध्याकाळी करा."
        )
        speak_text = f"{name} च्या कमतरतेमुळे {symp}। यावर उपाय: {corr}।"
        suggestions = ["इतर अन्नद्रव्य कमतरता", "खतांची सुसंगतता तक्ता", "माती आरोग्य पत्रिका", "हवामान अंदाज"]
    else:
        text = (
            f"### 🌾 {name} Deficiency Diagnostics & Correction\n\n"
            f"• **Key Symptoms:** {symp}\n\n"
            f"• **Recommended Correction:** {corr}\n\n"
            f"💡 *Tip:* Foliar sprays of micronutrients should be applied in early morning or late afternoon."
        )
        speak_text = f"For {name} deficiency, symptoms include {symp}. Correction is: {corr}."
        suggestions = ["Other nutrient deficiencies", "Fertilizer mixing chart", "Soil Health Card", "Live Weather"]

    return {"text": text, "speak_text": speak_text, "suggestions": suggestions}


def handle_general_nutrient_query(lang):
    if lang == "hi":
        text = (
            "### 🌿 प्रमुख पादप पोषक तत्व कमी निदान (Diagnostic Summary)\n\n"
            "• **नाइट्रोजन (N):** पुरानी पत्तियों की नोक से शुरू होकर V-आकार में पीलापन।\n"
            "• **फास्फोरस (P):** पत्तियां गहरी बैंगनी/तामिया रंग की होना, जड़ों की कम वृद्धि।\n"
            "• **पोटाश (K):** पुरानी पत्तियों के किनारे जलने या झुलसने जैसे (Leaf Scorch)।\n"
            "• **जिंक (Zn):** मक्के में सफेद पत्ती (White Bud) व धान में खैरा रोग।\n"
            "• **लोहा / आयरन (Fe):** नई पत्तियों की नसों के बीच पीलापन व सफेद होना।\n"
            "• **बोरॉन (B):** फल फटना, ऊपरी कली का सूखना व भूरा दिल (Brown Heart)।"
        )
        speak_text = "नाइट्रोजन की कमी से पुरानी पत्तियां पीली होती हैं, फास्फोरस से बैंगनी, पोटाश से किनारे जलते हैं और जिंक से मक्के में सफेद पत्ती व धान में खैरा रोग होता है।"
        suggestions = ["जिंक की कमी के लक्षण", "बोरॉन कमी के लक्षण", "खाद मिलाने की सारणी", "आज का मौसम"]
    elif lang == "mr":
        text = (
            "### 🌿 प्रमुख वनस्पती अन्नद्रव्य कमतरता निदान\n\n"
            "• **नत्र (Nitrogen):** जुन्या पानांवर शेंड्याकडून V-आकाराचे पिवळेपण.\n"
            "• **स्फुरद (Phosphorus):** पाने गडद जांभळट-तांबूस होणे, मुळांची वाढ खुंटणे.\n"
            "• **पालश (Potassium):** जुन्या पानांच्या कडा करपल्यासारख्या दिसणे.\n"
            "• **झिंक (Zinc):** मक्यामध्ये पांढरी पाने व भातात खैरा रोग होतो.\n"
            "• **लोह (Iron):** नव्या कोवळ्या पानांच्या शिरांमधील भाग पिवळा-पांढरा होणे.\n"
            "• **बोरॉन (Boron):** फळे तडकणे व शेंडा सुकणे."
        )
        speak_text = "नत्राच्या कमतरतेने पाने पिवळी पडतात, स्फुरदाने जांभळी होतात, पालशने कडा जळतात आणि झिंकमुळे मक्यात पांढरी पाने व भातात खैरा रोग होतो."
        suggestions = ["झिंक कमतरता उपाय", "बोरॉन कमतरता लक्षणे", "खते एकत्र मिसळणे", "हवामान अंदाज"]
    else:
        text = (
            "### 🌿 Major Plant Nutrient Deficiencies (Diagnostic Summary)\n\n"
            "• **Nitrogen (N):** V-shaped yellowing on older leaves starting at tip.\n"
            "• **Phosphorus (P):** Dark purplish-bronze leaves, restricted root growth.\n"
            "• **Potassium (K):** Marginal leaf scorching and tip firing on older leaves.\n"
            "• **Zinc (Zn):** White bud striping in Maize; Khaira rust disease in Rice.\n"
            "• **Iron (Fe):** Interveinal chlorosis on youngest leaves turning bleached white.\n"
            "• **Boron (B):** Terminal bud death, fruit cracking, Brown Heart in roots.\n\n"
            "👉 Ask about any specific nutrient for detailed dosage."
        )
        speak_text = "Nitrogen causes yellowing of older leaves, Phosphorus causes purple discoloration, Potassium causes leaf edge burning, and Zinc causes white striping."
        suggestions = ["Zinc deficiency treatment", "Boron symptoms", "Fertilizer mixing chart", "Soil Sampling Guide"]

    return {"text": text, "speak_text": speak_text, "suggestions": suggestions}


def handle_fertilizer_mixing_query(lang):
    if lang == "hi":
        text = (
            "### 📊 क्या यूरिया और डीएपी (DAP) को मिला सकते हैं?\n\n"
            "• **यूरिया + DAP:** बुवाई/प्रयोग से **तुरंत पहले** मिलाया जा सकता है। मिलाकर लंबे समय तक रखने पर नमी सोखकर गांठें बन जाती हैं।\n"
            "• **MOP (पोटाश):** यूरिया, DAP, SSP सभी के साथ आसानी से मिलाया जा सकता है।\n"
            "• ❌ **कभी न मिलाएं:** यूरिया या अमोनियम सल्फेट को **चूने (Lime) या बेसिक स्लैग** के साथ कभी न मिलाएं, क्योंकि अमोनिया गैस बनकर नाइट्रोजन उड़ जाती है।"
        )
        speak_text = "यूरिया और डीएपी को प्रयोग से तुरंत पहले मिला सकते हैं, लेकिन मिलाकर रखें नहीं। चूने के साथ यूरिया कभी न मिलाएं।"
        suggestions = ["खाद की पूरी अनुकूलता तालिका", "धान में खाद की मात्रा", "जिंक सल्फेट कब डालें?", "आज का मौसम"]
    elif lang == "mr":
        text = (
            "### 📊 युरिया आणि डीएपी (DAP) एकत्र मिसळू शकतो का?\n\n"
            "• **युरिया + DAP:** वापरण्यापूर्वी **लगेच** एकत्र मिसळू शकता. जास्त वेळ एकत्र ठेवल्यास खताचा चिखल होतो.\n"
            "• **MOP (पोटॅश):** युरिया, DAP, सिंगल सुपर फॉस्फेटसोबत सहज मिसळता येते.\n"
            "• ❌ **कधीही मिसळू नका:** युरिया किंवा अमोनियम सल्फेट **चुना किंवा बेसिक स्लॅग** सोबत अजिबात मिसळू नका, अन्यथा अमोनिया वायू निघून नत्राचे नुकसान होते."
        )
        speak_text = "युरिया आणि डीएपी फवारणी किंवा पेरणीपूर्वी लगेच मिसळू शकता, पण साठवून ठेवू नका. चुन्यासोबत युरिया कधीही मिसळू नका."
        suggestions = ["खते सुसंगतता तक्ता", "कापूस खत नियोजन", "झिंक सल्फेट कसे द्यावे?", "हवामान अंदाज"]
    else:
        text = (
            "### 📊 Fertilizer Mixing Compatibility Guide\n\n"
            "• **Urea + DAP:** Can be mixed **shortly before application**. Storing them together absorbs moisture and forms cakes.\n"
            "• **MOP (Potash):** Compatible with Urea, DAP, SSP, and Ammonium sulphate.\n"
            "• ❌ **Never Mix:** Urea or Ammonium sulphate with **Lime or Basic Slag** (causes volatilization of Nitrogen as ammonia gas)."
        )
        speak_text = "Urea and DAP can be mixed immediately before use. Never mix Urea with Lime as it causes nitrogen loss."
        suggestions = ["Fertilizer Compatibility Matrix", "Banana fertilizer plan", "Zinc application rules", "Live Weather"]

    return {"text": text, "speak_text": speak_text, "suggestions": suggestions}


def handle_mechanization_query(lang):
    if lang == "hi":
        text = (
            "### 🚜 आधुनिक कृषि यंत्र (लागत व श्रम बचत)\n\n"
            "1. **व्हील हो एवं ग्रबर वीडर (Wheel Hoe / Weeder):**\n"
            "   • फसल की शुरुआती अवस्था में निराई-गुड़ाई के खर्च में **50% से 60% की बचत**।\n\n"
            "2. **कोनो वीडर (Cono Weeder for Paddy):**\n"
            "   • धान के खेत में खरपतवारों को उखाड़कर चिखल में दबाता है (हरी खाद) और जड़ों को हवा देता है।\n\n"
            "3. **लेजर लैंड लेवलर (Laser Land Leveller):**\n"
            "   • खेत समतल करने पर **20-25% सिंचाई पानी की बचत** और एकसमान अंकुरण।\n\n"
            "4. **क्रीडा प्लांटर (CRIDA Planter):**\n"
            "   • 15-20% बीज की बचत और कतार में सटीक बुवाई।"
        )
        speak_text = "व्हील हो वीडर से निराई में 50 से 60 प्रतिशत खर्च बचता है, और लेजर लेवलर से 20 से 25 प्रतिशत पानी बचता है।"
        suggestions = ["उत्तम कृषि पद्धतियां (GAP)", "घर पर प्राकृतिक कीटनाशक", "सूक्ष्म सिंचाई ड्रिप योजना", "आज का मौसम"]
    elif lang == "mr":
        text = (
            "### 🚜 आधुनिक कृषी अवजारे (खर्च व कष्ट बचत)\n\n"
            "१. **व्हील हो व सायकल वीडर:**\n"
            "   • सुरुवातीच्या काळात खुरपणीच्या खर्चात **५०% ते ६०% बचत** होते.\n\n"
            "२. **भाताचा कोनो वीडर (Cono Weeder):**\n"
            "   • भातातील तण उपटून चिखलात गाडतो ज्यामुळे हिरवळीचे खत होते व मुळांना हवा मिळते.\n\n"
            "३. **लेझर लँड लेव्हलर:**\n"
            "   • जमीन सपाटीकरणामुळे **२०-२५% पाण्याची बचत** आणि एकसारखी जोमदार उगवण.\n\n"
            "४. **क्रीडा ट्रॅक्टर पेरणी यंत्र:**\n"
            "   • १५-२०% बियाण्याची बचत व अचूक अंतरावर पेरणी."
        )
        speak_text = "व्हील हो व सायकल वीडरमुळे खुरपणीचा ५० ते ६० टक्के खर्च वाचतो, आणि लेझर लेव्हलरमुळे २५ टक्के पाणी वाचते."
        suggestions = ["आधुनिक कृषी पद्धती (GAP)", "घरगुती सेंद्रिय अर्क", "ठिबक सिंचन अनुदान", "हवामान अंदाज"]
    else:
        text = (
            "### 🚜 Farm Mechanization & Drudgery Reduction\n\n"
            "1. **Wheel Hoe & Grubber Weeder:**\n"
            "   • Reduces weeding cost by **50% to 60%** in early stages. Eliminates drudgery.\n\n"
            "2. **Cono Weeder for Paddy:**\n"
            "   • Uproots weeds and incorporates them as green manure while aerating roots.\n\n"
            "3. **Laser Guided Land Leveller:**\n"
            "   • Saves **20-25% irrigation water** and ensures uniform germination.\n\n"
            "4. **CRIDA Tractor Planters:**\n"
            "   • Saves 15-20% seed with precision line sowing."
        )
        speak_text = "Wheel hoe reduces weeding cost by 50 to 60 percent, and laser land levellers save up to 25 percent irrigation water."
        suggestions = ["Good Agricultural Practices (GAP)", "Home bio-pesticide recipes", "Micro-irrigation subsidy", "Live Weather"]

    return {"text": text, "speak_text": speak_text, "suggestions": suggestions}


def handle_crop_fertilizer_query(crop, lang):
    ferts = crop.get("fertilizer_per_acre_kg", {})
    crop_name = crop["names"].get(lang, crop["names"]["en"])

    if lang == "hi":
        text = (
            f"### 🌿 {crop_name} के लिए प्रति एकड़ अनुशंसित खाद (NPK)\n\n"
            f"• **यूरिया (Urea):** {ferts.get('urea', 0)} किग्रा प्रति एकड़ (2-3 किस्तों में बांटकर डालें)\n"
            f"• **डीएपी (DAP):** {ferts.get('dap', 0)} किग्रा प्रति एकड़ (बुवाई के समय बेसल दें)\n"
            f"• **एमओपी (पोटाश):** {ferts.get('mop', 0)} किग्रा प्रति एकड़\n"
            f"• **गोबर की खाद (FYM):** {ferts.get('fym_tonnes', 3)} टन प्रति एकड़ खेत की तैयारी के समय\n\n"
            f"💡 *टिप:* सही तिथि-वार खाद कार्यक्रम देखने के लिए **फसल कैलेंडर** टूल का उपयोग करें।"
        )
        speak_text = f"{crop_name} के लिए प्रति एकड़ {ferts.get('urea', 0)} किलो यूरिया, {ferts.get('dap', 0)} किलो डीएपी और {ferts.get('mop', 0)} किलो पोटाश की आवश्यकता होती है।"
        suggestions = [f"{crop_name} का फसल कैलेंडर बनाएं", f"{crop_name} के मुख्य रोग", "आज का मौसम", "जैविक खाद कैसे बनाएं"]
    elif lang == "mr":
        text = (
            f"### 🌿 {crop_name} साठी प्रति एकर खत व्यवस्थापन\n\n"
            f"• **युरिया (Urea):** {ferts.get('urea', 0)} किग्रॅ प्रति एकर (२-३ हप्त्यांमध्ये विभागून द्या)\n"
            f"• **डीएपी (DAP):** {ferts.get('dap', 0)} किग्रॅ प्रति एकर (पेरणीच्या वेळी बेसल डोस)\n"
            f"• **एमओपी (पोटॅश):** {ferts.get('mop', 0)} किग्रॅ प्रति एकर\n"
            f"• **शेणखत (FYM):** {ferts.get('fym_tonnes', 3)} टन प्रति एकर पूर्वमशागतीवेळी\n\n"
            f"💡 *टीप:* अचूक तारखेनुसार वेळापत्रक मिळवण्यासाठी **पीक कॅलेंडर** वापरा."
        )
        speak_text = f"{crop_name} पिकासाठी प्रति एकर {ferts.get('urea', 0)} किलो युरिया, {ferts.get('dap', 0)} किलो डीएपी आणि {ferts.get('mop', 0)} किलो पोटॅशची शिफारस आहे."
        suggestions = [f"{crop_name} पीक कॅलेंडर बनवा", f"{crop_name} वरील कीड नियंत्रण", "थेट हवामान अंदाज", "जीवामृत कसे बनवावे"]
    else:
        text = (
            f"### 🌿 Recommended Fertilizer per Acre for {crop_name}\n\n"
            f"• **Urea:** {ferts.get('urea', 0)} kg/acre (split across 2-3 top dressings)\n"
            f"• **DAP:** {ferts.get('dap', 0)} kg/acre (apply as basal dose at sowing)\n"
            f"• **MOP (Potash):** {ferts.get('mop', 0)} kg/acre\n"
            f"• **Farmyard Manure (FYM):** {ferts.get('fym_tonnes', 3)} tonnes/acre during land prep\n\n"
            f"💡 *Tip:* Use our **Crop Calendar** tool for day-by-day dates customized to your land size."
        )
        speak_text = f"For {crop_name}, recommended fertilizer per acre is {ferts.get('urea', 0)} kg Urea, {ferts.get('dap', 0)} kg DAP, and {ferts.get('mop', 0)} kg Potash."
        suggestions = [f"Plan {crop_name} calendar", f"{crop_name} pests and diseases", "Live Weather", "Organic fertilizers"]

    return {"text": text, "speak_text": speak_text, "suggestions": suggestions}


def handle_crop_disease_query(crop, query, lang):
    pests = crop.get("pests_and_diseases", [])
    crop_name = crop["names"].get(lang, crop["names"]["en"])

    if not pests:
        return handle_general_disease_query(query, lang)

    pest = pests[0]
    p_name = pest["name"].get(lang, pest["name"]["en"])
    p_symp = pest["symptoms"].get(lang, pest["symptoms"]["en"])
    p_org = pest["organic_remedy"].get(lang, pest["organic_remedy"]["en"])
    p_chem = pest["chemical_remedy"].get(lang, pest["chemical_remedy"]["en"])

    if lang == "hi":
        text = (
            f"### 🛡️ {crop_name} में मुख्य रोग व नियंत्रण: **{p_name}**\n\n"
            f"• **लक्षण:** {p_symp}\n\n"
            f"• **जैविक उपाय:** {p_org}\n\n"
            f"• **रासायनिक दवा व मात्रा:** {p_chem}\n\n"
            f"🔬 *सलाह:* छिड़काव हमेशा मौसम साफ होने पर और स्टीकर मिलाकर करें।"
        )
        speak_text = f"{crop_name} में {p_name} के लिए जैविक उपाय है: {p_org}। रासायनिक नियंत्रण के लिए: {p_chem}।"
        suggestions = [f"{crop_name} में खाद की मात्रा", "पत्ती रोग डॉक्टर टूल", "आज का मौसम", "जीवामृत बनाने की विधि"]
    elif lang == "mr":
        text = (
            f"### 🛡️ {crop_name} वरील प्रमुख रोग व नियंत्रण: **{p_name}**\n\n"
            f"• **लक्षणे:** {p_symp}\n\n"
            f"• **सेंद्रिय उपाय:** {p_org}\n\n"
            f"• **रासायनिक औषध व प्रमाण:** {p_chem}\n\n"
            f"🔬 *सल्ला:* फवारणी नेहमी निरभ्र वातावरणात आणि स्टिकर मिसळून करा."
        )
        speak_text = f"{crop_name} पिकावरील {p_name} साठी सेंद्रिय उपाय: {p_org} आणि रासायनिक औषध: {p_chem}."
        suggestions = [f"{crop_name} खत व्यवस्थापन", "रोग निदान डॉक्टर टूल", "हवामान अंदाज", "दशपर्णी अर्क कसा करावा"]
    else:
        text = (
            f"### 🛡️ Disease & Pest Control for {crop_name}: **{p_name}**\n\n"
            f"• **Symptoms:** {p_symp}\n\n"
            f"• **Organic Remedy:** {p_org}\n\n"
            f"• **Chemical Control:** {p_chem}\n\n"
            f"🔬 *Tip:* Always spray in calm weather and add a wetting/sticking agent."
        )
        speak_text = f"For {p_name} in {crop_name}, organic remedy is {p_org}. Recommended chemical spray is {p_chem}."
        suggestions = [f"Fertilizer dose for {crop_name}", "Plant Disease Doctor", "Live Weather", "Crop Calendar"]

    return {"text": text, "speak_text": speak_text, "suggestions": suggestions}


def handle_crop_overview_query(crop, lang):
    crop_name = crop["names"].get(lang, crop["names"]["en"])
    season = crop["season"].get(lang, crop["season"]["en"])
    soil = crop["soil"].get(lang, crop["soil"]["en"])

    if lang == "hi":
        text = (
            f"### 🌾 {crop_name} - प्रमुख फसल जानकारी\n\n"
            f"• **मौसम / सीजन:** {season}\n"
            f"• **फसल अवधि:** {crop.get('duration_days', 120)} दिन\n"
            f"• **उपयुक्त तापमान:** {crop.get('optimal_temp', '20-30°C')}\n"
            f"• **उपयुक्त मिट्टी:** {soil}\n"
            f"• **अनुमानित पैदावार:** {crop.get('expected_yield_per_acre', '20 Quintals')} प्रति एकड़\n\n"
            f"👉 आप मुझसे इस फसल के खाद कार्यक्रम या रोग नियंत्रण के बारे में पूछ सकते हैं।"
        )
        speak_text = f"{crop_name} {season} की फसल है। इसकी अवधि {crop.get('duration_days', 120)} दिन और औसत पैदावार {crop.get('expected_yield_per_acre', '20 क्विंटल')} प्रति एकड़ है।"
        suggestions = [f"{crop_name} में खाद की मात्रा", f"{crop_name} के रोग व दवा", f"{crop_name} का कैलेंडर", "मौसम रिपोर्ट"]
    elif lang == "mr":
        text = (
            f"### 🌾 {crop_name} - पीक माहिती\n\n"
            f"• **हंगाम:** {season}\n"
            f"• **कालावधी:** {crop.get('duration_days', 120)} दिवस\n"
            f"• **योग्य तापमान:** {crop.get('optimal_temp', '20-30°C')}\n"
            f"• **जमीन:** {soil}\n"
            f"• **अपेक्षित उत्पादन:** {crop.get('expected_yield_per_acre', '20 क्विंटल')} प्रति एकर\n\n"
            f"👉 आपण या पिकाच्या खत नियोजनाबद्दल किंवा कीड व्यवस्थापनाबद्दल विचारू शकता."
        )
        speak_text = f"{crop_name} हे {season} चे पीक असून कालावधी {crop.get('duration_days', 120)} दिवस आहे आणि उत्पादन {crop.get('expected_yield_per_acre', '20 क्विंटल')} प्रति एकर मिळते."
        suggestions = [f"{crop_name} खत मात्रा", f"{crop_name} रोग नियंत्रण", f"{crop_name} पीक कॅलेंडर", "हवामान अंदाज"]
    else:
        text = (
            f"### 🌾 {crop_name} - Agronomic Guide\n\n"
            f"• **Season:** {season}\n"
            f"• **Duration:** {crop.get('duration_days', 120)} days\n"
            f"• **Ideal Temp:** {crop.get('optimal_temp', '20-30°C')}\n"
            f"• **Soil:** {soil}\n"
            f"• **Expected Yield:** {crop.get('expected_yield_per_acre', '20 Quintals')} per acre\n\n"
            f"👉 Ask me about fertilizer calculation or pest management for {crop_name}."
        )
        speak_text = f"{crop_name} is grown in {season} season taking about {crop.get('duration_days', 120)} days with yield of {crop.get('expected_yield_per_acre', '20 Quintals')} per acre."
        suggestions = [f"Fertilizer for {crop_name}", f"Pests in {crop_name}", f"Plan {crop_name} calendar", "Live Weather"]

    return {"text": text, "speak_text": speak_text, "suggestions": suggestions}


def handle_schemes_query(lang):
    if lang == "hi":
        text = (
            "### 🏛️ प्रमुख सरकारी कृषि योजनाएं एवं सब्सिडी\n\n"
            "1. **प्रधानमंत्री किसान सम्मान निधि (PM-KISAN):**\n"
            "   • प्रति वर्ष ₹6,000 की प्रत्यक्ष आर्थिक सहायता (₹2,000 की 3 किस्तें) सीधे बैंक खाते में। पोर्टल: pmkisan.gov.in\n\n"
            "2. **प्रधानमंत्री फसल बीमा योजना (PMFBY):**\n"
            "   • प्राकृतिक आपदाओं से फसल नुकसान पर व्यापक बीमा सुरक्षा। खरीफ 2%, रबी 1.5% प्रीमियम। हेल्पलाइन: 14447\n\n"
            "3. **किसान क्रेडिट कार्ड (KCC):**\n"
            "   • 4% रियायती ब्याज दर पर 3 लाख तक का सस्ता फसली ऋण + ₹50,000 का दुर्घटना बीमा।\n\n"
            "4. **प्रधानमंत्री कृषि सिंचाई योजना (PMKSY):**\n"
            "   • ड्रिप एवं स्प्रिंकलर लगाने पर लघु-सीमांत किसानों को 55% तथा अन्य को 45% सब्सिडी।\n\n"
            "5. **कृषि यंत्रीकरण योजना (SMAM):**\n"
            "   • ट्रैक्टर, रोटावेटर, कल्टीवेटर व थ्रेशर खरीदने पर 40% से 50% तक सरकारी अनुदान।\n\n"
            "6. **पीएम कुसुम सोलर पंप योजना:**\n"
            "   • 3 से 10 एचपी सोलर वाटर पंप पर 60% तक सरकारी सब्सिडी (30% केंद्र + 30% राज्य)।"
        )
        speak_text = "भारत सरकार की प्रमुख योजनाएं हैं: पीएम किसान में 6000 रुपये सालाना, फसल बीमा में आपदा सुरक्षा, किसान क्रेडिट कार्ड पर 4 प्रतिशत ब्याज दर पर ऋण, ड्रिप पर 55 प्रतिशत सब्सिडी, और कुसुम सोलर पंप पर 60 प्रतिशत अनुदान मिलता है।"
        suggestions = ["किसान कॉल सेंटर 1800-180-1551", "ड्रिप सिंचाई सब्सिडी", "मृदा स्वास्थ्य कार्ड", "आज का मौसम"]
    elif lang == "mr":
        text = (
            "### 🏛️ प्रमुख शासकीय कृषी योजना व अनुदान\n\n"
            "1. **प्रधानमंत्री किसान सन्मान निधी (PM-KISAN):**\n"
            "   • दरवर्षी ₹६,००० थेट बँक खात्यात (₹२,००० चे ३ हप्ते). पोर्टल: pmkisan.gov.in\n\n"
            "2. **प्रधानमंत्री पीक विमा योजना (PMFBY):**\n"
            "   • नैसर्गिक आपत्तीपासून पिकाचे संपूर्ण संरक्षण (१ रुपयात पीक विमा योजना). हेल्पलाइन: 14447\n\n"
            "3. **किसान क्रेडिट कार्ड (KCC):**\n"
            "   • ४% सवलतीच्या व्याजदरात ३ लाखांपर्यंत सहज कृषी कर्ज + ₹५०,००० चा अपघात विमा.\n\n"
            "4. **प्रधानमंत्री कृषी सिंचन योजना (PMKSY):**\n"
            "   • ठिबक व तुषार सिंचनासाठी अल्पभूधारक शेतकऱ्यांना ५५% व इतरांना ४५% शासकीय अनुदान.\n\n"
            "5. **कृषी यांत्रिकीकरण उपअभियान (SMAM):**\n"
            "   • ट्रॅक्टर, रोटाव्हेटर, पॉवर टिलर अवजारांवर ४०% ते ५०% थेट शासकीय अनुदान.\n\n"
            "6. **पीएम कुसुम सौर पंप योजना:**\n"
            "   • सौर कृषी पंप बसवण्यासाठी ६०% शासकीय अनुदान (३०% केंद्र + ३०% राज्य)."
        )
        speak_text = "शासनाच्या प्रमुख योजना: पीएम किसान मध्ये ६००० रुपये, पीक विमा संरक्षण, किसान क्रेडिट कार्डवर ४ टक्के व्याजदरात कर्ज, ठिबकवर ५५ टक्के अनुदान, आणि सौर पंपावर ६० टक्के शासकीय अनुदान मिळते."
        suggestions = ["किसान कॉल सेंटर १८००-१८०-१५५१", "ठिबक अनुदान योजना", "माती परीक्षण कसे करावे?", "हवामान अंदाज"]
    else:
        text = (
            "### 🏛️ Major Government Agricultural Schemes & Subsidies\n\n"
            "1. **PM-KISAN:** ₹6,000 per year direct income support in 3 equal instalments of ₹2,000. Portal: pmkisan.gov.in\n\n"
            "2. **PMFBY Crop Insurance:** Comprehensive crop loss coverage against natural perils (2% Kharif / 1.5% Rabi). Helpline: 14447\n\n"
            "3. **Kisan Credit Card (KCC):** Low interest credit up to ₹3 Lakh at 4% effective interest + ₹50,000 accidental insurance.\n\n"
            "4. **PMKSY Micro-Irrigation:** 55% subsidy for small/marginal farmers and 45% for general farmers for Drip & Sprinklers.\n\n"
            "5. **Farm Mechanization (SMAM):** 40% to 50% subsidy on Tractors, Rotavators, Power Tillers, and Threshers.\n\n"
            "6. **PM-KUSUM Solar Pumps:** Up to 60% subsidy (30% Central + 30% State) for off-grid Solar Agri Pumps."
        )
        speak_text = "Key government schemes include: PM-Kisan with 6000 rupees direct benefit, PMFBY crop insurance, KCC loan at 4 percent interest, Micro-irrigation with 55 percent subsidy, and PM-Kusum Solar Pump with 60 percent subsidy."
        suggestions = ["Kisan Call Center 1800-180-1551", "Micro-irrigation subsidy", "Soil Health Card", "Live Weather"]

    return {"text": text, "speak_text": speak_text, "suggestions": suggestions}


def handle_organic_query(query, lang):
    if lang == "hi":
        text = (
            "### 🌿 जैविक खेती व प्राकृतिक कीटनाशक निर्माण विधि\n\n"
            "1. **नीम बीज अर्क (NSKE 5%):**\n"
            "   • 50 ग्राम नीम गिरी पाउडर प्रति लीटर पानी में कपड़े की पोटली से निचोड़ें + 1 मिली साबुन घोल मिलाएं।\n\n"
            "2. **जीवामृत (Jeevamrut):**\n"
            "   • 10 किग्रा देसी गोबर + 10 ली. गोमूत्र + 2 किग्रा गुड़ + 2 किग्रा बेसन + मेड़ की मिट्टी को 200 ली. पानी में 48-72 घंटे सड़ाएं।\n\n"
            "3. **तम्बाकू का काढ़ा:**\n"
            "   • 500 ग्राम तम्बाकू 4.5 ली. पानी में 24 घंटे उबालें + 320 ग्राम साबुन घोलकर 6-7 गुना पानी में मिलाकर छिड़कें।"
        )
        speak_text = "नीम बीज अर्क 5% रस चूसक कीटों के लिए अत्यंत प्रभावी है। जीवामृत बनाने के लिए गोबर, गोमूत्र, गुड़ और बेसन 3 दिन पानी में सड़ाएं।"
        suggestions = ["कीटनाशक विषाक्तता रंग पट्टी", "वर्मीकंपोस्ट (केंचुआ खाद)", "फसल कैलेंडर बनाएं", "मौसम रिपोर्ट"]
    elif lang == "mr":
        text = (
            "### 🌿 सेंद्रिय शेती व सेंद्रिय कीटकनाशक कृती\n\n"
            "१. **निंबोळी अर्क (NSKE ५%):**\n"
            "   • ५० ग्रॅम निंबोळी पावडर प्रति लिटर पाण्यात कपड्यात बांधून पिळा + १ मिली साबणाचे पाणी मिसळा.\n\n"
            "२. **जीवामृत:**\n"
            "   • १० किलो शेण + १० ली. गोमूत्र + २ किलो गूळ + २ किलो बेसन २०० ली. पाण्यात ३ दिवस आंबवून द्या.\n\n"
            "३. **तंबाखूचा अर्क:**\n"
            "   • ५०० ग्रॅम तंबाखू ४.५ ली. पाण्यात २४ तास उकळा + ३२० ग्रॅम साबण मिसळून ६-७ पट पाण्यात फवारा."
        )
        speak_text = "निंबोळी अर्क ५% रसशोषक किडींवर अत्यंत प्रभावी आहे. जीवामृत बनवण्यासाठी शेण, गोमूत्र, गूळ व बेसन ३ दिवस आंबवा."
        suggestions = ["कीटकनाशक विषारीपण रंग", "गांडूळ खत पद्धत", "पीक कॅलेंडर बनवा", "हवामान अंदाज"]
    else:
        text = (
            "### 🌿 Organic Farming & Botanical Formulations\n\n"
            "1. **Neem Seed Kernel Extract (NSKE 5%):** 50g crushed neem kernels per liter water squeezed in muslin cloth + 1ml soap sticker.\n"
            "2. **Jeevamrut:** 10kg cow dung + 10L urine + 2kg jaggery + 2kg pulse flour fermented in 200L water for 48-72 hrs.\n"
            "3. **Tobacco Decoction:** 500g tobacco boiled in 4.5L water + 320g bar soap diluted 6-7 times."
        )
        speak_text = "NSKE 5 percent is highly effective against sucking pests. Jeevamrut is made by fermenting cow dung, urine, jaggery and gram flour."
        suggestions = ["Pesticide toxicity bands", "Vermicomposting guide", "Crop Calendar", "Live Weather"]

    return {"text": text, "speak_text": speak_text, "suggestions": suggestions}


def handle_general_disease_query(query, lang):
    results = search_diseases(query=query, lang=lang)
    if not results:
        results = search_diseases(crop_id="wheat", lang=lang)

    d = results[0]
    c_name = d["crop_name"].get(lang, d["crop_name"]["en"]) if isinstance(d["crop_name"], dict) else d["crop_name"]
    d_name = d["name"].get(lang, d["name"]["en"]) if isinstance(d["name"], dict) else d["name"]
    d_symp = d["symptoms"].get(lang, d["symptoms"]["en"]) if isinstance(d["symptoms"], dict) else d["symptoms"]
    d_org = d["organic_remedy"].get(lang, d["organic_remedy"]["en"]) if isinstance(d["organic_remedy"], dict) else d["organic_remedy"]
    d_chem = d["chemical_remedy"].get(lang, d["chemical_remedy"]["en"]) if isinstance(d["chemical_remedy"], dict) else d["chemical_remedy"]

    if lang == "hi":
        text = (
            f"### 🩺 रोग पहचान एवं समाधान: **{d_name}** ({c_name})\n\n"
            f"• **पहचान लक्षण:** {d_symp}\n\n"
            f"• **प्राकृतिक / जैविक उपाय:** {d_org}\n\n"
            f"• **रासायनिक दवा व मात्रा:** {d_chem}\n\n"
            f"👉 आप **पादप रोग डॉक्टर** टूल में पत्ती की फोटो अपलोड कर भी जांच सकते हैं।"
        )
        speak_text = f"{c_name} में {d_name} के लिए जैविक उपाय: {d_org}। रासायनिक दवा: {d_chem}।"
        suggestions = ["पत्ती की फोटो से जांच करें", "कीटनाशक जहर का प्राथमिक उपचार", "आज का मौसम व छिड़काव", "खाद की मात्रा"]
    elif lang == "mr":
        text = (
            f"### 🩺 रोग निदान व उपाय: **{d_name}** ({c_name})\n\n"
            f"• **लक्षणे:** {d_symp}\n\n"
            f"• **सेंद्रिय उपाय:** {d_org}\n\n"
            f"• **रासायनिक औषध व डोस:** {d_chem}\n\n"
            f"👉 आपण **पीक डॉक्टर** टूलमध्ये पानाचा फोटो टाकूनही थेट निदान करू शकता."
        )
        speak_text = f"{c_name} पिकावरील {d_name} रोगावर सेंद्रिय उपाय: {d_org} आणि रासायनिक औषध: {d_chem}."
        suggestions = ["पानाचा फोटो टाकून तपासा", "विषबाधा प्रथमोपचार", "थेट हवामान व फवारणी", "खत नियोजन"]
    else:
        text = (
            f"### 🩺 Disease Diagnosis: **{d_name}** ({c_name})\n\n"
            f"• **Symptoms:** {d_symp}\n\n"
            f"• **Organic Remedy:** {d_org}\n\n"
            f"• **Chemical Control:** {d_chem}\n\n"
            f"👉 You can also upload a leaf photo to the **Plant Disease Doctor**."
        )
        speak_text = f"For {d_name} in {c_name}, organic remedy is {d_org}. Recommended chemical is {d_chem}."
        suggestions = ["Upload leaf photo to Doctor", "Emergency poison first aid", "Weather & spray index", "Fertilizer Calculator"]

    return {"text": text, "speak_text": speak_text, "suggestions": suggestions}


def handle_season_query(lang):
    if lang == "hi":
        text = (
            "### 📅 प्रमुख भारतीय फसल मौसम (Seasons)\n\n"
            "1. **खरीफ (Kharif - जून से अक्टूबर):** मानसून आधारित फसलें जैसे धान, कपास, सोयाबीन, मक्का, मूंगफली, गन्ना।\n"
            "2. **रबी (Rabi - अक्टूबर से मार्च):** कम तापमान की फसलें जैसे गेहूं, चना, सरसों, आलू, प्याज।\n"
            "3. **जायद / ग्रीष्मकालीन (Summer - मार्च से मई):** सब्जियां, मूंग, उड़द, खीरा-ककड़ी और तरबूज।"
        )
        speak_text = "खरीफ में धान, कपास और सोयाबीन; रबी में गेहूं, चना और सरसों; और जायद में सब्जियां व तरबूज उगाए जाते हैं।"
        suggestions = ["गेहूं बुवाई कैलेंडर", "कपास बुवाई कैलेंडर", "लाइव मौसम देखें", "खाद की मात्रा"]
    elif lang == "mr":
        text = (
            "### 📅 प्रमुख भारतीय कृषी हंगाम (Seasons)\n\n"
            "१. **खरीप (जून ते ऑक्टोबर):** पावसाळी पिके जसे की कापूस, सोयाबीन, भात, मका, भुईमूग, ऊस.\n"
            "२. **रब्बी (ऑक्टोबर ते मार्च):** हिवाळी पिके जसे की गहू, हरभरा, मोहरी, कांदा, बटाटा.\n"
            "३. **उन्हाळी (मार्च ते मे):** भाजीपाला, मूग, उडीद, टरबूज व काकडी."
        )
        speak_text = "खरीप हंगामात कापूस, सोयाबीन व भात; रब्बी हंगामात गहू, हरभरा व कांदा; आणि उन्हाळी हंगामात भाजीपाला घेतला जातो."
        suggestions = ["गहू पीक कॅलेंडर", "कापूस पीक कॅलेंडर", "हवामान अंदाज", "खत नियोजन"]
    else:
        text = (
            "### 📅 Major Indian Cropping Seasons\n\n"
            "1. **Kharif (June - October):** Monsoon rainfed crops (Rice, Cotton, Soybean, Maize, Groundnut, Sugarcane).\n"
            "2. **Rabi (October - March):** Winter moisture crops (Wheat, Chickpea, Mustard, Potato, Onion).\n"
            "3. **Zaid / Summer (March - May):** Short duration vegetables, pulses, and watermelons."
        )
        speak_text = "Kharif includes rice, cotton, and soybean; Rabi includes wheat, chickpea, and mustard; Zaid includes vegetables."
        suggestions = ["Wheat crop calendar", "Cotton crop calendar", "Live weather forecast", "Fertilizer calculator"]

    return {"text": text, "speak_text": speak_text, "suggestions": suggestions}


def search_knowledge_base(query, lang="en"):
    """
    Full-text fallback search across crops, diseases, nutrients, recipes, and schemes.
    Returns matched result or None.
    """
    q_words = [w for w in re.split(r'\W+', query.lower()) if len(w) > 2]
    if not q_words:
        return None

    # Search diseases
    for d in DISEASES:
        d_name = d["name"].get(lang, d["name"]["en"]).lower()
        d_symp = d["symptoms"].get(lang, d["symptoms"]["en"]).lower()
        if any(w in d_name or w in d_symp for w in q_words):
            c_name = d["crop_name"].get(lang, d["crop_name"]["en"])
            name = d["name"].get(lang, d["name"]["en"])
            symp = d["symptoms"].get(lang, d["symptoms"]["en"])
            org = d["organic_remedy"].get(lang, d["organic_remedy"]["en"])
            chem = d["chemical_remedy"].get(lang, d["chemical_remedy"]["en"])

            if lang == "hi":
                text = f"### 🩺 **{name}** ({c_name})\n\n• **लक्षण:** {symp}\n• **जैविक उपाय:** {org}\n• **रासायनिक दवा:** {chem}"
                speak_text = f"{c_name} के {name} रोग के लिए जैविक उपाय: {org}। रासायनिक दवा: {chem}।"
            elif lang == "mr":
                text = f"### 🩺 **{name}** ({c_name})\n\n• **लक्षणे:** {symp}\n• **सेंद्रिय उपाय:** {org}\n• **रासायनिक औषध:** {chem}"
                speak_text = f"{c_name} पिकावरील {name} रोगावर सेंद्रिय उपाय: {org} आणि रासायनिक औषध: {chem}."
            else:
                text = f"### 🩺 **{name}** ({c_name})\n\n• **Symptoms:** {symp}\n• **Organic Remedy:** {org}\n• **Chemical Control:** {chem}"
                speak_text = f"For {name} in {c_name}, organic remedy is {org} and chemical treatment is {chem}."
            return {"text": text, "speak_text": speak_text, "suggestions": ["Plant Disease Doctor", "Live Weather", "Crop Calendar"]}

    # Search crops
    for c_id, c in CROPS.items():
        c_names = [c_id, c["names"]["en"].lower(), c["names"]["hi"].lower(), c["names"]["mr"].lower()]
        if any(w in " ".join(c_names) for w in q_words):
            return handle_crop_overview_query(c, lang)

    # Search schemes
    for s in GOVERNMENT_SCHEMES:
        s_name = s["name"].get(lang, s["name"]["en"]).lower()
        s_ben = s["benefit"].get(lang, s["benefit"]["en"]).lower()
        if any(w in s_name or w in s_ben for w in q_words):
            name = s["name"].get(lang, s["name"]["en"])
            ben = s["benefit"].get(lang, s["benefit"]["en"])
            sub = s.get("subsidy", "")
            port = s.get("portal_url", "")
            if lang == "hi":
                text = f"### 🏛️ **{name}**\n\n• **लाभ व विवरण:** {ben}\n• **अनुदान / सब्सिडी:** {sub}\n• **पोर्टल:** {port}"
                speak_text = f"{name}: {ben}."
            elif lang == "mr":
                text = f"### 🏛️ **{name}**\n\n• **फायदे व माहिती:** {ben}\n• **अनुदान:** {sub}\n• **पोर्टल:** {port}"
                speak_text = f"{name}: {ben}."
            else:
                text = f"### 🏛️ **{name}**\n\n• **Benefits:** {ben}\n• **Subsidy:** {sub}\n• **Portal:** {port}"
                speak_text = f"{name}: {ben}."
            return {"text": text, "speak_text": speak_text, "suggestions": ["Helpline 1800-180-1551", "All Government Schemes", "Live Weather"]}

    return None


def handle_general_fallback(query, lang):
    if lang == "hi":
        text = (
            f"मैं **'{query}'** पर कृषि हैंडबुक के आधार पर जानकारी खोज रहा हूँ।\n\n"
            "कृपया निम्न में से किसी विषय पर पूछें:\n"
            "• **मौसम व छिड़काव:** *आज बारिश होगी क्या?*\n"
            "• **पोषक तत्व:** *मक्के में जिंक की कमी / पत्ती पीली होना*\n"
            "• **फसल खाद:** *केला, आम, संतरा, गन्ना, गेहूं या कपास में खाद*\n"
            "• **कीट-रोग व सुरक्षा:** *रोग दवा, कीटनाशक जहर का प्राथमिक उपचार*\n"
            "• **हेल्पलाइन:** *किसान कॉल सेंटर 1800-180-1551*"
        )
        speak_text = "खेती से जुड़े किसी भी सवाल के लिए आप मौसम, पोषक तत्व, खाद की मात्रा, फसल रोग या किसान कॉल सेंटर के बारे में पूछ सकते हैं।"
        suggestions = ["आज मौसम व छिड़काव", "जिंक की कमी के लक्षण", "केले में खाद की मात्रा", "किसान कॉल सेंटर नंबर"]
    elif lang == "mr":
        text = (
            f"मी **'{query}'** बाबत कृषी हँडबुक माहिती शोधत आहे.\n\n"
            "कृपया खालील विषयांवर विचारा:\n"
            "• **हवामान व फवारणी:** *आज पाऊस पडेल का?*\n"
            "• **अन्नद्रव्य कमतरता:** *मक्यात झिंकची कमतरता / पाने पिवळी पडणे*\n"
            "• **पीक खत मात्रा:** *केळी, आंबा, संत्रा, ऊस, कापूस किंवा गहू खत नियोजन*\n"
            "• **रोग व सुरक्षा:** *कीड औषध, कीटकनाशक विषबाधा प्रथमोपचार*\n"
            "• **हेल्पलाइन:** *किसान कॉल सेंटर १८००-१८०-१५५१*"
        )
        speak_text = "शेतीसंबंधी हवामान, अन्नद्रव्य कमतरता, खतांचे प्रमाण, पीक रोग किंवा किसान कॉल सेंटरबद्दल विचारा."
        suggestions = ["आज हवामान व फवारणी", "झिंक कमतरता उपाय", "केळी खत व्यवस्थापन", "किसान कॉल सेंटर १८००-१८०-१५५१"]
    else:
        text = (
            f"I am matching **'{query}'** with our scientific agriculture handbook.\n\n"
            "Try asking about:\n"
            "• **Live Weather:** *Will it rain today? / Spraying advice*\n"
            "• **Nutrient Deficiencies:** *Zinc deficiency in maize / Leaf yellowing*\n"
            "• **Crop Packages:** *Fertilizer dosage for Banana, Mango, Citrus, Sugarcane, Wheat*\n"
            "• **Pest Safety:** *Pesticide toxicity color bands, Poison first aid*\n"
            "• **Helpline:** *Kisan Call Center 1800-180-1551*"
        )
        speak_text = "You can ask about live weather, nutrient deficiencies, crop fertilizer packages, pesticide safety, or Kisan Call Center."
        suggestions = ["Live Weather & Spraying", "Zinc deficiency in Maize", "Fertilizer for Banana", "Kisan Call Center 1800-180-1551"]

    return {"text": text, "speak_text": speak_text, "suggestions": suggestions}
