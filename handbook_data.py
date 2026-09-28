# handbook_data.py
# Technical Agricultural Intelligence extracted from 'Farmer's Handbook on Basic Agriculture'
# (MANAGE - Ministry of Agriculture GoI, Desai Fruits & Vegetables, GIZ)
# Multilingual data across English ('en'), Hindi ('hi'), and Marathi ('mr').

NUTRIENT_DEFICIENCIES = [
    {
        "id": "nitrogen",
        "name": {"en": "Nitrogen (N)", "hi": "नाइट्रोजन (N)", "mr": "नत्र (N)"},
        "role": {"en": "Essential for vegetative growth, chlorophyll and protein synthesis.", "hi": "वानस्पतिक बढ़वार, क्लोरोफिल और प्रोटीन निर्माण के लिए आवश्यक।", "mr": "झाडांची वाढ, हरितद्रव्य आणि प्रथिनांच्या निर्मितीसाठी आवश्यक."},
        "symptoms": {
            "en": "Stunted plant growth. Appearance of light green to pale-yellow color on older leaves, starting from tips (V-shaped yellowing). Premature leaf drop and severely reduced flowering.",
            "hi": "पौधे का बौना रहना। निचली पुरानी पत्तियों की नोक से पीलापन शुरू होकर अंदर फैलना (V-आकार का पीलापन)। पत्तियों का झड़ना और फूल कम आना।",
            "mr": "झाडांची वाढ खुंटणे. खालच्या जुन्या पानांच्या टोकाकडून पिवळेपणा सुरू होणे (V-आकाराचा पिवळेपणा). पाने गळणे आणि फुले कमी येणे.",
        },
        "cure": {
            "en": "Apply Urea (46% N) as top dressing or spray 1-2% Urea solution on foliage.",
            "hi": "यूरिया (46% N) का टॉप ड्रेसिंग करें या 1-2% यूरिया घोल का पर्णीय छिड़काव करें।",
            "mr": "युरिया (४६% N) खताचा हप्ता द्या किंवा १-२% युरिया द्रावणाची फवारणी करा.",
        },
    },
    {
        "id": "phosphorus",
        "name": {"en": "Phosphorus (P)", "hi": "फास्फोरस (P)", "mr": "स्फुरद (P)"},
        "role": {"en": "Promotes root development, early maturity, tillering and flowering.", "hi": "जड़ों के विकास, शीघ्र पकने, कल्ले फूटने और फूल आने में सहायक।", "mr": "मुळांचा विकास, फुटवे, लवकर पक्वता आणि फुलधारणेसाठी आवश्यक."},
        "symptoms": {
            "en": "Overall stunted appearance, mature leaves turn dark blue-green to characteristic purple/bronze color along veins and stems. Restricted root development and delayed crop maturity.",
            "hi": "पौधे का विकास रुकना, पत्तियों व तनों पर बैंगनी-तांबई रंग के धब्बे दिखना, जड़ें कमजोर रहना और फसल देर से पकना।",
            "mr": "झाडांची वाढ थांबणे, पानांवर व खोडावर जांभळट-तांबूस रंग दिसणे, मुळांची वाढ खुंटणे आणि पीक उशिरा पक्व होणे.",
        },
        "cure": {
            "en": "Apply Single Super Phosphate (SSP 16% P2O5) or DAP (46% P2O5) near root zone at sowing. Use PSB (Phosphorus Solubilizing Bacteria).",
            "hi": "बुवाई के समय सिंगल सुपर फास्फेट (SSP) या DAP जड़ों के पास डालें। PSB बायोफर्टिलाइजर का प्रयोग करें।",
            "mr": "पेरणीवेळी सिंगल सुपर फॉस्फेट (SSP) किंवा DAP द्या. PSB जिवाणू संवर्धकाचा वापर करा.",
        },
    },
    {
        "id": "potassium",
        "name": {"en": "Potassium (K)", "hi": "पोटैशियम (K)", "mr": "पालाश (K)"},
        "role": {"en": "Increases disease resistance, drought tolerance, grain filling and fruit quality.", "hi": "रोग प्रतिरोधक क्षमता, सूखा सहनशीलता, दाना भराव और फल चमक बढ़ाता है।", "mr": "रोगप्रतिकारशक्ती, दुष्काळ सहनशीलता, दाणे भरणे व फळांची प्रत सुधारते."},
        "symptoms": {
            "en": "Marginal chlorosis followed by scorching and browning of tips of older leaves (fired/burnt margins progressing inward). Weak stalks causing lodging and shrivelled seeds.",
            "hi": "पुरानी पत्तियों के किनारे जलने जैसे भूरे हो जाना (किनारे झुलसना), तना कमजोर होकर फसल गिरना और दाने पिचके रह जाना।",
            "mr": "जुन्या पानांच्या कडा जळाल्यासारख्या तपकिरी होणे, खोड कमजोर होऊन पीक लोळणे आणि दाणे बारीक राहणे.",
        },
        "cure": {
            "en": "Apply Muriate of Potash (MOP 60% K2O) or Potassium Sulphate (0:0:50 @ 5g/L foliar spray).",
            "hi": "म्यूरेट ऑफ पोटाश (MOP) डालें या पोटैशियम सल्फेट (0:0:50 @ 5 ग्राम/ली.) का छिड़काव करें।",
            "mr": "म्युरेट ऑफ पोटॅश (MOP) द्या किंवा पोटॅशियम सल्फेट (०:०:५० @ ५ ग्रॅम/ली.) फवारा.",
        },
    },
    {
        "id": "calcium",
        "name": {"en": "Calcium (Ca)", "hi": "कैल्शियम (Ca)", "mr": "कॅल्शियम (Ca)"},
        "role": {"en": "Cell wall formation, root tip elongation and fruit firmness.", "hi": "कोशिका भित्ति निर्माण, जड़ विकास और फलों की मजबूती के लिए जरूरी।", "mr": "पेशीभित्तिका निर्मिती, मुळांची वाढ आणि फळांचा टणकपणा टिकवणे."},
        "symptoms": {
            "en": "Young leaves affected first, distorted small and cup-shaped. Growing points (terminal buds) die. Blossom End Rot in tomato and cracking in fruits.",
            "hi": "नई ऊपरी पत्तियां मुड़कर कप के आकार की हो जाती हैं। टर्मिनल कलियां सूख जाती हैं। टमाटर के नीचे काला सड़न (ब्लॉसम एंड रॉट)।",
            "mr": "वरची कोवळी पाने वाकडी होऊन वाटीसारखी होतात. शेंड्याची कळी वाळते. टोमॅटोच्या तळाशी काळा डाग (ब्लॉसम एंड रॉट) पडतो.",
        },
        "cure": {
            "en": "Apply Agricultural Lime / Gypsum in soil as per soil test, or spray Calcium Nitrate @ 2-3g/L.",
            "hi": "मिट्टी में चूना या जिप्सम डालें, या कैल्शियम नाइट्रेट 2-3 ग्राम/लीटर का छिड़काव करें।",
            "mr": "जमिनीत चुना किंवा जिप्सम टाका, किंवा कॅल्शियम नायट्रेट २-३ ग्रॅम/लिटर फवारा.",
        },
    },
    {
        "id": "magnesium",
        "name": {"en": "Magnesium (Mg)", "hi": "मैग्नीशियम (Mg)", "mr": "मॅग्नेशियम (Mg)"},
        "role": {"en": "Central component of chlorophyll molecule required for photosynthesis.", "hi": "क्लोरोफिल (हरितलवक) का केंद्रीय घटक जो प्रकाश संश्लेषण के लिए अनिवार्य है।", "mr": "हरितद्रव्याचा मुख्य घटक जो प्रकाशसंश्लेषणासाठी आवश्यक आहे."},
        "symptoms": {
            "en": "Interveinal chlorosis mainly on older leaves (green veins with yellow patches between veins). In severe cases, purple/red tints develop.",
            "hi": "पुरानी पत्तियों की नसों के बीच का भाग पीला पड़ना (नसों का रंग हरा और बीच में पीलापन)। पत्तियां ऊपर की ओर मुड़ना।",
            "mr": "जुन्या पानांच्या शिरांमधील भाग पिवळा पडणे (शिरा हिरव्या व मधील भाग पिवळा). पाने वरच्या बाजूला वळणे.",
        },
        "cure": {
            "en": "Apply Magnesium Sulphate @ 10-15 kg/acre in soil or spray @ 5g/L on standing crop.",
            "hi": "मैग्नीशियम सल्फेट 10-15 किग्रा/एकड़ मिट्टी में डालें या 5 ग्राम/लीटर का छिड़काव करें।",
            "mr": "मॅग्नेशियम सल्फेट १०-१५ किग्रॅ/एकर जमिनीत द्या किंवा ५ ग्रॅम/लिटर फवारा.",
        },
    },
    {
        "id": "sulphur",
        "name": {"en": "Sulphur (S)", "hi": "सल्फर / गंधक (S)", "mr": "गंधक (S)"},
        "role": {"en": "Essential for oil synthesis in oilseeds and protein formation in pulses.", "hi": "तिलहन में तेल की मात्रा और दलहन में प्रोटीन निर्माण के लिए अति आवश्यक।", "mr": "तेलबिया पिकांमध्ये तेलाचे प्रमाण आणि डाळवर्गीय पिकात प्रथिनांच्या वाढीसाठी आवश्यक."},
        "symptoms": {
            "en": "Younger top leaves turn uniformly pale-yellow or chlorotic (unlike nitrogen which affects older leaves first). Stems become stiff, woody and small in diameter.",
            "hi": "ऊपरी नई पत्तियां पूरी तरह हल्की पीली पड़ जाती हैं। तना कड़ा और पतला रह जाता है।",
            "mr": "वरची कोवळी पाने पूर्णपणे पिवळसर पडतात. खोड बारीक आणि लाकडासारखे कडक राहते.",
        },
        "cure": {
            "en": "Apply Bentonite Sulphur @ 15kg/acre or Single Super Phosphate (SSP) or spray Sulphur 80% WDG @ 2g/L.",
            "hi": "बेंटोनाइट सल्फर 15 किग्रा/एकड़ डालें या सल्फर 80% WDG 2 ग्राम/लीटर का छिड़काव करें।",
            "mr": "बेंटोनाईट गंधक १५ किग्रॅ/एकर टाका किंवा गंधक ८०% WDG २ ग्रॅम/लिटर फवारा.",
        },
    },
    {
        "id": "zinc",
        "name": {"en": "Zinc (Zn)", "hi": "जिंक / जस्ता (Zn)", "mr": "झिंक / जस्त (Zn)"},
        "role": {"en": "Enzyme activation, auxin hormone synthesis and cell elongation.", "hi": "एंजाइम सक्रियता, ऑक्सिन हार्मोन और पौधों की लंबाई बढ़ाने में सहायक।", "mr": "ऑक्सिन संप्रेरक निर्मिती आणि पेशींच्या वाढीसाठी अत्यंत महत्त्वाचे."},
        "symptoms": {
            "en": "Interveinal chlorosis on young leaves, reduction in leaf size ('Little Leaf'), rosetting. Causes Khaira disease in Rice and White Bud in Maize.",
            "hi": "पत्तियों का छोटा रह जाना (लिटिल लीफ), मक्के में सफेद कली (White Bud) और धान में खैरा रोग (पत्तियों पर कत्थई धब्बे)।",
            "mr": "पाने बारीक राहणे (लिटल लीफ), मक्यात पांढरी कळी (व्हाईट बड) आणि भातात खैरा रोग (तपकिरी डाग).",
        },
        "cure": {
            "en": "Soil application of Zinc Sulphate (21% or 33% @ 10-15 kg/acre) or foliar spray of Chelated Zinc (12% EDTA @ 1g/L).",
            "hi": "जिंक सल्फेट 10-15 किग्रा/एकड़ मिट्टी में डालें या चिलेटेड जिंक (12% EDTA @ 1 ग्राम/ली.) छिड़कें।",
            "mr": "झिंक सल्फेट १०-१५ किग्रॅ/एकर जमिनीत द्या किंवा चिलेटेड झिंक (१ ग्रॅम/ली.) फवारा.",
        },
    },
    {
        "id": "iron",
        "name": {"en": "Iron (Fe)", "hi": "आयरन / लोहा (Fe)", "mr": "लोह (Fe)"},
        "role": {"en": "Chlorophyll synthesis and electron transport in plant respiration.", "hi": "क्लोरोफिल संश्लेषण और पौधे के श्वसन तंत्र में महत्वपूर्ण भूमिका।", "mr": "हरितद्रव्य संश्लेषण आणि वनस्पती श्वसन क्रियेमध्ये महत्त्वाची भूमिका."},
        "symptoms": {
            "en": "Severe interveinal chlorosis on youngest leaves. In advanced stages, entire leaf becomes ivory-white/bleached while veins retain slight greenness.",
            "hi": "नई कोमल पत्तियों की नसों के बीच का भाग पूरी तरह सफेद या हल्का पीला पड़ना (ब्लीच जैसा)।",
            "mr": "वरची कोवळी पाने पांढरट-पिवळी पडणे (ब्लीच झाल्यासारखी), शिरा हिरवट राहतात पण तीव्र कमतरतेत पूर्ण पान पांढरे होते.",
        },
        "cure": {
            "en": "Spray Ferrous Sulphate (19% Fe @ 5g/L) + Citric acid (1g/L), or Chelated Fe-EDTA @ 1g/L.",
            "hi": "फेरस सल्फेट (5 ग्राम/ली.) + साइट्रिक एसिड (1 ग्राम/ली.) या चिलेटेड Fe-EDTA 1 ग्राम/ली. छिड़कें।",
            "mr": "फेरस सल्फेट (५ ग्रॅम/ली.) + लिंबू सत्व (१ ग्रॅम/ली.) किंवा चिलेटेड Fe-EDTA १ ग्रॅम/ली. फवारा.",
        },
    },
    {
        "id": "boron",
        "name": {"en": "Boron (B)", "hi": "बोरॉन (B)", "mr": "बोरॉन (B)"},
        "role": {"en": "Pollen germination, fruit setting, sugar translocation and cell wall strength.", "hi": "परागकण अंकुरण, फल बनने, शर्करा संचरण और फल फटने से रोकने में जरूरी।", "mr": "परागकण अंकुरण, फळधारणा आणि फळे तडकण्यापासून रोखण्यासाठी आवश्यक."},
        "symptoms": {
            "en": "Death of growing tips, hollow heart/brown heart in tubers and cauliflower, cracking of fruits (pomegranate, tomato, citrus), poor grain filling.",
            "hi": "पौधे के अग्र भाग का सूखना, गोभी में भूरा सड़न, अनार व टमाटर के फलों का फटना और दानों का न भरना।",
            "mr": "शेंड्याची वाढ थांबणे, डाळिंब व टोमॅटोची फळे तडकणे आणि धान्यात दाणे न भरणे.",
        },
        "cure": {
            "en": "Soil application of Borax @ 4-5 kg/acre or foliar spray of Solubor (20% B @ 1-1.5g/L) before flowering.",
            "hi": "बोरेक्स 4-5 किग्रा/एकड़ मिट्टी में डालें या घुलनशील बोरॉन (20% @ 1-1.5 ग्राम/ली.) फूल आने से पहले छिड़कें।",
            "mr": "बोरेक्स ४-५ किग्रॅ/एकर जमिनीत द्या किंवा सोलुबोर (२०% @ १-१.५ ग्रॅम/ली.) फुलधारणेपूर्वी फवारा.",
        },
    },
    {
        "id": "copper",
        "name": {"en": "Copper (Cu)", "hi": "कॉपर / तांबा (Cu)", "mr": "तांबे (Cu)"},
        "role": {"en": "Enzyme system catalyst and reproductive stage development.", "hi": "एंजाइम सक्रियता और फसल की प्रजनन अवस्था में आवश्यक।", "mr": "एंझाईम प्रणाली आणि पिकाच्या पुनरुत्पादक अवस्थेसाठी आवश्यक."},
        "symptoms": {
            "en": "Dieback of shoots in citrus/fruit trees, yellowing and curling of leaf tips, gum pockets under bark.",
            "hi": "शाखाओं का ऊपर से नीचे सूखना (डाईबैक), पत्तियों के किनारों का मुड़ना और तनों पर गोंद निकलना।",
            "mr": "फांद्या शेंड्याकडून वाळत जाणे (डायबॅक), पानांच्या कडा वळणे आणि सालीतून डिंक गळणे.",
        },
        "cure": {
            "en": "Spray Copper Oxychloride 50% WP @ 2.5g/L or Copper Sulphate @ 1-2g/L.",
            "hi": "कॉपर ऑक्सीक्लोराइड 50% WP (2.5 ग्राम/लीटर) या कॉपर सल्फेट का छिड़काव करें।",
            "mr": "कॉपर ऑक्सिक्लोराईड ५०% WP (२.५ ग्रॅम/लिटर) किंवा कॉपर सल्फेट फवारा.",
        },
    },
    {
        "id": "manganese",
        "name": {"en": "Manganese (Mn)", "hi": "मैंगनीज (Mn)", "mr": "मॅंगनीज (Mn)"},
        "role": {"en": "Chloroplast formation and nitrogen metabolism.", "hi": "क्लोरोप्लास्ट निर्माण और नाइट्रोजन चयापचय में सहायक।", "mr": "हरितलवक निर्मिती आणि नत्र पचन क्रियेसाठी आवश्यक."},
        "symptoms": {
            "en": "Interveinal chlorosis on middle and younger leaves with small grey-brown necrotic spots (Marsh spot in peas, Pahala blight in sugarcane).",
            "hi": "मध्यम और युवा पत्तियों पर नसों के बीच पीलापन और भूरे धब्बे (गन्ने में पहला ब्लाइट)।",
            "mr": "मधल्या व कोवळ्या पानांवर बारीक तपकिरी डाग (उसावरील पाहाळा ब्लाइट).",
        },
        "cure": {
            "en": "Foliar spray of Manganese Sulphate (0.5% @ 5g/L) on standing crop.",
            "hi": "मैंगनीज सल्फेट (5 ग्राम/लीटर) का पर्णीय छिड़काव करें।",
            "mr": "मॅंगनीज सल्फेट (५ ग्रॅम/लिटर) फवारा.",
        },
    },
    {
        "id": "molybdenum",
        "name": {"en": "Molybdenum (Mo)", "hi": "मोलिब्डेनम (Mo)", "mr": "मॉलिब्डेनम (Mo)"},
        "role": {"en": "Nitrate reductase enzyme and biological nitrogen fixation in legume root nodules.", "hi": "नाइट्रेट रिडक्टेस एंजाइम और दलहन की जड़ों में नाइट्रोजन स्थिरीकरण।", "mr": "डाळवर्गीय पिकांच्या मुळांवरील गाठींमध्ये हवेतील नत्र स्थिर करण्यासाठी आवश्यक."},
        "symptoms": {
            "en": "Whiptail syndrome in cauliflower (narrow strap-like leaves with only midrib), yellowing of older legume leaves.",
            "hi": "फूलगोभी में व्हिपटेल रोग (पत्तियां चाबुक जैसी संकरी हो जाना) और दलहन की पत्तियां पीली पड़ना।",
            "mr": "फ्लॉवरमध्ये व्हिपटेल रोग (पाने चाबकासारखी बारीक होणे) आणि कडधान्यांची पाने पिवळी पडणे.",
        },
        "cure": {
            "en": "Apply Sodium / Ammonium Molybdate @ 1-2g/L as foliar spray or seed treatment @ 1g/kg seed.",
            "hi": "सोडियम/अमोनियम मोलिब्डेट (1-2 ग्राम/ली.) छिड़कें या 1 ग्राम/किग्रा बीज उपचार करें।",
            "mr": "सोडियम/अमोनियम मॉलिब्डेट (१-२ ग्रॅम/ली.) फवारा किंवा १ ग्रॅम/किग्रॅ बीजप्रक्रिया करा.",
        },
    },
]

FERTILIZER_COMPATIBILITY = [
    {
        "name": {"en": "Urea", "hi": "यूरिया", "mr": "युरिया"},
        "compatible_with": "MOP (Potash), SSP, Ammonium Sulphate",
        "incompatible_with": "Lime, Calcium Ammonium Nitrate (CAN), Basic Slag",
        "notes": "Can be mixed with DAP only immediately before application; prolonged storage causes moisture absorption and caking."
    },
    {
        "name": {"en": "DAP (Di-ammonium Phosphate)", "hi": "डीएपी", "mr": "डीएपी"},
        "compatible_with": "MOP (Potash), Urea (apply immediately)",
        "incompatible_with": "Lime, Zinc Sulphate (causes precipitation of insoluble zinc phosphate)",
        "notes": "Never mix DAP and Zinc Sulphate in same tank; maintain at least 3-4 days gap between soil applications."
    },
    {
        "name": {"en": "MOP (Muriate of Potash)", "hi": "एमओपी (पोटाश)", "mr": "पोटॅश (MOP)"},
        "compatible_with": "Urea, DAP, SSP, Ammonium Sulphate",
        "incompatible_with": "None under standard dry storage",
        "notes": "Highly compatible with all major straight fertilizers."
    },
    {
        "name": {"en": "Single Super Phosphate (SSP)", "hi": "सिंगल सुपर फास्फेट", "mr": "सिंगल सुपर फॉस्फेट (SSP)"},
        "compatible_with": "Urea, MOP, Ammonium Sulphate",
        "incompatible_with": "Lime, Rock Phosphate, Uncured FYM",
        "notes": "Do not mix with lime as it fixes available phosphate into insoluble tricalcium phosphate."
    },
    {
        "name": {"en": "Zinc Sulphate", "hi": "जिंक सल्फेट", "mr": "झिंक सल्फेट"},
        "compatible_with": "Urea (in solution), Ferrous Sulphate",
        "incompatible_with": "DAP, SSP, NPK complexes (Phosphatic fertilizers)",
        "notes": "Phosphate binds with Zinc to form insoluble Zinc Phosphate which plants cannot absorb."
    }
]

PESTICIDE_TOXICITY_CLASSES = [
    {
        "color": "Red",
        "symbol": "💀 SKULL & CROSSBONES",
        "name": {"en": "Extremely Toxic (Category A/B)", "hi": "अत्यधिक विषैला (रेड बैंड)", "mr": "अतिविषारी (लाल पट्टी)"},
        "examples": "Phorate 10G, Monocrotophos, Phosphamidon, Methyl Parathion",
        "precaution": {
            "en": "Lethal hazard. Use full protective suit, rubber gloves, respirator mask, eye goggles. Keep locked away.",
            "hi": "प्राणघातक। पूरी पीपीई किट, रबर के दस्ताने, मास्क और चश्मा पहनें। बच्चों व पशुओं से दूर ताले में रखें।",
            "mr": "जीवघेणा धोका. संपूर्ण सुरक्षा किट, रबरी हातमोजे, मास्क व चष्मा वापरा. कुलपात ठेवा."
        }
    },
    {
        "color": "Yellow",
        "symbol": "⚠️ POISONOUS",
        "name": {"en": "Highly Toxic (Category C)", "hi": "अति विषैला (येलो बैंड)", "mr": "विषारी (पिवळी पट्टी)"},
        "examples": "Endosulfan, Profenofos, Triazophos, Carbaryl",
        "precaution": {
            "en": "Severe poison hazard. Always spray in wind direction with masks and wash thoroughly with soap afterwards.",
            "hi": "गंभीर विष जोखिम। हमेशा हवा की दिशा में मास्क पहनकर छिड़कें और बाद में साबुन से स्नान करें।",
            "mr": "तीव्र विषारी धोका. नेहमी वाऱ्याच्या दिशेने मास्क लावून फवारा आणि नंतर साबणाने स्वच्छ धुवा."
        }
    },
    {
        "color": "Blue",
        "symbol": "🔷 MODERATELY TOXIC",
        "name": {"en": "Moderately Toxic (Category D)", "hi": "मध्यम विषैला (ब्लू बैंड)", "mr": "मध्यम विषारी (निळी पट्टी)"},
        "examples": "Malathion, Chlorpyrifos, Mancozeb, Thiamethoxam",
        "precaution": {
            "en": "Moderate risk. Avoid skin contact or aerosol inhalation. Do not eat, drink or smoke during spraying.",
            "hi": "मध्यम जोखिम। त्वचा संपर्क से बचें। छिड़काव के दौरान धूम्रपान, खाना या पीना सख्त मना है।",
            "mr": "मध्यम धोका. त्वचेचा संपर्क टाळा. फवारणी करताना खाणे, पिणे किंवा धूम्रपान करू नका."
        }
    },
    {
        "color": "Green",
        "symbol": "🟢 SLIGHTLY TOXIC",
        "name": {"en": "Slightly Toxic (Category E)", "hi": "कम विषैला (ग्रीन बैंड)", "mr": "कमी विषारी (हिरवी पट्टी)"},
        "examples": "Neem-based formulations (Azadirachtin), Trichoderma, Bio-pesticides",
        "precaution": {
            "en": "Safest category when used according to label dosages. Standard personal hygiene required.",
            "hi": "अनुशंसित मात्रा में सबसे सुरक्षित। प्रयोग के बाद सामान्य रूप से हाथ-मुंह धोएं।",
            "mr": "योग्य प्रमाणात वापरल्यास सुरक्षित. वापरानंतर हात-पाय स्वच्छ साबणाने धुवा."
        }
    }
]

FARM_MECHANIZATION_TOOLS = [
    {
        "name": {"en": "Wheel Hoe & Grubber Weeder", "hi": "व्हील हो एवं ग्रबर वीडर", "mr": "व्हील हो व सायकल वीडर"},
        "stage": {"en": "Inter-cultivation & Weeding", "hi": "निराई-गुड़ाई", "mr": "खुरपणी व तण नियंत्रण"},
        "benefit": {"en": "Reduces cost of weeding by 50% to 60% in early crop stages. Eliminates human drudgery.", "hi": "निराई के खर्च में 50% से 60% की बचत। शारीरिक थकान से मुक्ति।", "mr": "खुरपणीच्या खर्चात ५०% ते ६०% बचत. मजुरांवरील अवलंबित्व कमी."}
    },
    {
        "name": {"en": "Cono Weeder for Wetland Paddy", "hi": "धान का कोनो वीडर", "mr": "भाताचा कोनो वीडर"},
        "stage": {"en": "Wetland Paddy Weeding & Aeration", "hi": "धान के खेत में निराई व वायु संचार", "mr": "चिखलणी भात शेतातील तण नियंत्रण"},
        "benefit": {"en": "Uproots weeds and incorporates them into soil as green manure while aerating rice roots.", "hi": "खरपतवारों को उखाड़कर मिट्टी में दबाकर हरी खाद बनाता है और जड़ों को हवा देता है।", "mr": "तण उपटून चिखलात गाडतो ज्यामुळे हिरवळीचे खत तयार होते आणि मुळांना हवा मिळते."}
    },
    {
        "name": {"en": "Laser Guided Land Leveller", "hi": "लेजर लैंड लेवलर", "mr": "लेझर लँड लेव्हलर"},
        "stage": {"en": "Land Preparation", "hi": "खेत का समतलीकरण", "mr": "जमीन सपाटीकरण"},
        "benefit": {"en": "Saves 20-25% irrigation water, ensures uniform seed germination and fertilizer distribution.", "hi": "20-25% सिंचाई पानी की बचत, एकसमान अंकुरण और खाद का बेहतर उपयोग।", "mr": "२०-२५% पाण्याची बचत, एकसारखी उगवण आणि खतांचा योग्य वापर."}
    },
    {
        "name": {"en": "CRIDA Tractor Planters & Seed Treating Drum", "hi": "क्रीडा ट्रैक्टर प्लांटर व बीज उपचार ड्रम", "mr": "क्रीडा ट्रॅक्टर पेरणी यंत्र व बीज प्रक्रिया ड्रम"},
        "stage": {"en": "Seed Treatment & Precision Sowing", "hi": "बीज उपचार व बुवाई", "mr": "बीज प्रक्रिया व अचूक पेरणी"},
        "benefit": {"en": "Saves 15-20% seed, maintains precise plant spacing and achieves uniform seedling emergence.", "hi": "15-20% बीज की बचत, पौधों के बीच सटीक दूरी और एकसमान पौध जमाव।", "mr": "१५-२०% बियाण्याची बचत, अचूक अंतर आणि एकसारखी जोमदार उगवण."}
    }
]

BOTANICAL_RECIPES = [
    {
        "name": {"en": "Neem Seed Suspension (NSKE 5%)", "hi": "नीम बीज अर्क (NSKE 5%)", "mr": "निंबोळी अर्क (५%)"},
        "target": {"en": "Locusts, Grasshoppers, Sucking pests (Aphids, Jassids, Whiteflies)", "hi": "टिड्डियां, माहू, हरा तेला, सफेद मक्खी और सुंडियां", "mr": "टोळ, मावा, तुडतुडे, पांढरी माशी आणि लहान अळ्या"},
        "recipe": {
            "en": "Crush 50g mature neem seed kernels into coarse powder per liter of water (5kg for 100L). Tie in muslin cloth, suspend in water bucket and squeeze repeatedly until water turns milky brown. Mix 1ml liquid soap as sticker before spraying.",
            "hi": "50 ग्राम नीम बीज की गिरी प्रति लीटर पानी (5 किग्रा प्रति 100 ली.) कूटकर कपड़े की पोटली में बांधें। पानी में डुबोकर बार-बार निचोड़ें। छिड़काव से पहले 1 मिली साबुन का घोल मिलाएं।",
            "mr": "५० ग्रॅम निंबोळी पावडर प्रति लिटर पाणी (५ किलो/१०० ली.) सुती कपड्यात बांधून पाण्यात पिळा जोपर्यंत पाणी दुधाळ-तपकिरी होत नाही. फवारणीपूर्वी १ मिली शाम्पू/साबणाचे पाणी मिसळा."
        }
    },
    {
        "name": {"en": "Tobacco Decoction", "hi": "तम्बाकू का काढ़ा", "mr": "तंबाखूचा अर्क"},
        "target": {"en": "Severe aphid and thrips infestation on vegetables", "hi": "सब्जियों पर माहू (चेपा) और थ्रिप्स का भारी प्रकोप", "mr": "भाजीपाल्यावरील मावा आणि थ्रिप्सचा प्रादुर्भाव"},
        "recipe": {
            "en": "Boil 500g tobacco in 4.5 liters water for 24 hours. Dissolve 320g bar soap in separate vessel and mix together. Dilute stock solution 6-7 times with water before spraying.",
            "hi": "500 ग्राम तम्बाकू 4.5 लीटर पानी में 24 घंटे उबालें। 320 ग्राम साबुन अलग घोलकर दोनों मिलाएं। इस घोल को 6-7 गुना पानी मिलाकर छिड़कें।",
            "mr": "५०० ग्रॅम तंबाखू ४.५ लिटर पाण्यात २४ तास उकळा. ३२० ग्रॅम साबण वेगळा विरघळवून एकत्र करा. फवारणीपूर्वी या द्रावणात ६-७ पट पाणी मिसळा."
        }
    },
    {
        "name": {"en": "Kerosene Emulsion", "hi": "मिट्टी के तेल (केरोसिन) का इमल्शन", "mr": "रॉकेल इमल्शन"},
        "target": {"en": "Contact insecticide for scales, mealybugs, and sucking insects", "hi": "मिलीबग, शल्क कीट और रस चूसक कीड़ों का संपर्क नियंत्रण", "mr": "पिठ्या ढेकूण (मिलीबग) आणि रसशोषक किडींचे नियंत्रण"},
        "recipe": {
            "en": "Dissolve 500g bar soap in 4.5 liters boiling water. Cool and add 9 liters kerosene. Agitate vigorously until completely emulsified. Dilute 15-20 times with water before spraying.",
            "hi": "500 ग्राम साबुन 4.5 लीटर उबलते पानी में घोलें। ठंडा कर 9 लीटर केरोसिन मिलाएं और हिलाएं। छिड़काव के लिए 15-20 गुना पानी मिलाएं।",
            "mr": "५०० ग्रॅम साबण ४.५ लिटर उकळत्या पाण्यात विरघळवा. थंड झाल्यावर ९ लिटर रॉकेल मिसळून चांगले ढवळा. फवारणीसाठी १५-२० पट पाण्यात मिसळा."
        }
    }
]

# Real-Time Government Agricultural Schemes
GOVERNMENT_SCHEMES = [
    {
        "id": "pm_kisan",
        "name": {"en": "PM-Kisan Samman Nidhi", "hi": "प्रधानमंत्री किसान सम्मान निधि (PM-KISAN)", "mr": "पंतप्रधान किसान सन्मान निधी (PM-KISAN)"},
        "benefit": {"en": "Direct income support of ₹6,000 per year paid in 3 equal four-monthly installments of ₹2,000 directly into farmer's Aadhaar-seeded bank account.", "hi": "प्रत्येक पात्र किसान परिवार को ₹6,000 प्रति वर्ष 3 समान किस्तों (₹2,000) में सीधे आधार लिंक बैंक खाते में।", "mr": "सर्व पात्र शेतकरी कुटुंबांना दरवर्षी ₹६,००० चे थेट आर्थिक सहाय्य ३ हप्त्यांमध्ये (₹२,०००) थेट बँक खात्यात."},
        "subsidy": "100% Direct Central Benefit (₹6,000/yr)",
        "eligibility": {"en": "All landholding farmer families with cultivable land in their names. Requires e-KYC and land seeding.", "hi": "खेती योग्य भूमि वाले सभी किसान परिवार। ई-केवाईसी व लैंड सीडिंग अनिवार्य।", "mr": "जमीनधारक सर्व शेतकरी कुटुंबे. ई-केवायसी व जमीन नोंदणी आवश्यक."},
        "portal_url": "https://pmkisan.gov.in",
        "helpline": "155261 / 1800-11-5526 / 011-24300606"
    },
    {
        "id": "pmfby",
        "name": {"en": "Pradhan Mantri Fasal Bima Yojana (PMFBY)", "hi": "प्रधानमंत्री फसल बीमा योजना (PMFBY)", "mr": "पंतप्रधान पीक विमा योजना (PMFBY)"},
        "benefit": {"en": "Comprehensive insurance coverage against non-preventable natural risks from pre-sowing to post-harvest. Farmer premium: 2% for Kharif, 1.5% for Rabi, 5% for Annual Commercial/Horticultural crops.", "hi": "प्राकृतिक आपदाओं, कीट व रोगों से फसल नुकसान का व्यापक बीमा। खरीफ 2%, रबी 1.5%, बागवानी/व्यावसायिक फसल 5% प्रीमियम।", "mr": "नैसर्गिक आपत्ती व कीड-रोगामुळे होणाऱ्या पीक नुकसानीपासून विमा संरक्षण. खरीप २%, रब्बी १.५%, बागायती ५% प्रीमियम."},
        "subsidy": "Up to 90% premium subsidy by Centre + State",
        "eligibility": {"en": "All farmers including sharecroppers and tenant farmers growing notified crops in notified areas.", "hi": "अधिसूचित क्षेत्रों में अधिसूचित फसल उगाने वाले सभी किसान व बटाईदार।", "mr": "अधिसूचित पिके घेणारे सर्व खातेदार व भाडेकरू शेतकरी."},
        "portal_url": "https://pmfby.gov.in",
        "helpline": "14447 / Crop Insurance Mobile App"
    },
    {
        "id": "pmksy",
        "name": {"en": "PM Krishi Sinchayee Yojana (Per Drop More Crop)", "hi": "प्रधानमंत्री कृषि सिंचाई योजना (प्रति बूंद अधिक फसल)", "mr": "पंतप्रधान कृषी सिंचन योजना (प्रति थेंब अधिक पीक)"},
        "benefit": {"en": "55% subsidy for Small & Marginal farmers and 45% for other farmers for installing Drip and Sprinkler micro-irrigation systems.", "hi": "ड्रिप एवं स्प्रिंकलर सिस्टम लगाने पर लघु व सीमांत किसानों को 55% तथा अन्य किसानों को 45% तक सरकारी अनुदान।", "mr": "ठिबक व तुषार सिंचन बसवण्यासाठी अल्प व अत्यल्प भूधारक शेतकऱ्यांना ५५% व इतर शेतकऱ्यांना ४५% शासकीय अनुदान."},
        "subsidy": "55% Subsidy (Small/Marginal) · 45% (General)",
        "eligibility": {"en": "Farmers having cultivable land with assured water source.", "hi": "सुनिश्चित जल स्रोत व खेती योग्य भूमि वाले सभी किसान।", "mr": "पाण्याचा शाश्वत स्रोत व शेतीजमीन असलेले सर्व शेतकरी."},
        "portal_url": "https://pmksy.gov.in",
        "helpline": "Contact District Agriculture Office / Taluka Krishi Adhikari"
    },
    {
        "id": "kcc_credit",
        "name": {"en": "Kisan Credit Card (KCC) Crop Loan", "hi": "किसान क्रेडिट कार्ड (KCC) रियायती फसली ऋण", "mr": "किसान क्रेडिट कार्ड (KCC) सवलतीचे पीक कर्ज"},
        "benefit": {"en": "Short-term crop loan up to ₹3 Lakh at an effective interest rate of only 4% (7% base interest minus 3% prompt repayment incentive). Includes ₹50,000 accidental insurance.", "hi": "3 लाख तक का फसली ऋण केवल 4% प्रभावी ब्याज दर पर (समय पर भुगतान पर 3% छूट)। साथ में ₹50,000 का दुर्घटना बीमा।", "mr": "३ लाखांपर्यंतचे पीक कर्ज केवळ ४% सवलतीच्या व्याजदरात (वेळेवर परतफेड केल्यास ३% सूट). ₹५०,००० चा अपघात विमा."},
        "subsidy": "3% Interest Subvention Incentive",
        "eligibility": {"en": "Individual/joint farmers, tenant farmers, self-help groups, animal husbandry & fisheries farmers.", "hi": "व्यक्तिगत किसान, काश्तकार, पशुपालक एवं मत्स्य पालक किसान।", "mr": "वैयक्तिक शेतकरी, कुळ शेतकरी, पशुपालक व मत्स्य व्यावसायिक."},
        "portal_url": "https://www.myscheme.gov.in/schemes/kcc",
        "helpline": "1800-180-1551 or nearest Bank Branch"
    },
    {
        "id": "smam_machinery",
        "name": {"en": "Sub-Mission on Agricultural Mechanization (SMAM)", "hi": "कृषि यंत्रीकरण उप-मिशन (SMAM कृषि यंत्र अनुदान)", "mr": "कृषी यांत्रिकीकरण उपअभियान (SMAM अवजारे अनुदान)"},
        "benefit": {"en": "40% to 50% financial subsidy on purchase of modern farm machinery including Tractors, Power Tillers, Rotavators, Multi-crop Threshers, and Laser Levellers. Up to 80% for Custom Hiring Centers (CHCs).", "hi": "ट्रैक्टर, रोटावेटर, पावर टिलर, थ्रेशर व लेजर लेवलर की खरीद पर 40% से 50% तक की सब्सिडी। कस्टम हायरिंग सेंटर पर 80% तक।", "mr": "ट्रॅक्टर, रोटाव्हेटर, पॉवर टिलर, मळणी यंत्र खरेदीसाठी ४०% ते ५०% थेट अनुदान. कृषी अवजार बँकेसाठी ८०% पर्यंत अनुदान."},
        "subsidy": "40% to 50% on Implements · 80% on CHC",
        "eligibility": {"en": "All categories of farmers. Priority to SC/ST, Women and Small/Marginal farmers via DBT portal.", "hi": "सभी किसान। लघु-सीमांत, महिला व आरक्षित वर्ग को विशेष प्राथमिकता।", "mr": "सर्व शेतकरी. अल्पभूधारक, महिला व आरक्षित प्रवर्गाला प्राधान्य."},
        "portal_url": "https://agrimachinery.nic.in",
        "helpline": "1800-180-1551"
    },
    {
        "id": "soil_health_card",
        "name": {"en": "Soil Health Card Scheme (SHC)", "hi": "मृदा स्वास्थ्य कार्ड योजना (सॉइल हेल्थ कार्ड)", "mr": "मृदा आरोग्य पत्रिका योजना (Soil Health Card)"},
        "benefit": {"en": "Free laboratory testing of 12 critical soil parameters (N, P, K, S, Zn, Fe, Cu, Mn, Bo, pH, EC, OC) issued every 2 years with crop-wise customized fertilizer dosage recommendations.", "hi": "12 पोषक तत्वों की मुफ्त प्रयोगशाला जांच व फसलवार उर्वरक सिफारिशों युक्त मृदा स्वास्थ्य कार्ड हर 2 वर्ष में जारी।", "mr": "१२ अन्नद्रव्यांची मोफत प्रयोगशाळा तपासणी व पिकांनुसार खतांच्या अचूक शिफारशींसह दर २ वर्षांनी आरोग्य पत्रिका."},
        "subsidy": "100% Free Soil Testing by Government",
        "eligibility": {"en": "All farm holdings across India via district soil testing laboratories and KVKs.", "hi": "देश भर के सभी किसान अपनी मिट्टी की जांच नजदीकी लैब या KVK में करा सकते हैं।", "mr": "सर्व शेतकरी जवळच्या माती परीक्षण प्रयोगशाळा किंवा KVK मध्ये मोफत तपासणी करू शकतात."},
        "portal_url": "https://soilhealth.dac.gov.in",
        "helpline": "Nearest KVK / District Soil Testing Laboratory"
    },
    {
        "id": "pm_kusum",
        "name": {"en": "PM-KUSUM Solar Pump Scheme", "hi": "प्रधानमंत्री कुसुम सोलर पंप योजना (PM-KUSUM)", "mr": "पंतप्रधान कुसुम सौर कृषी पंप योजना (PM-KUSUM)"},
        "benefit": {"en": "Up to 60% government subsidy (30% Central + 30% State) for installing standalone off-grid Solar Agriculture Water Pumps (3 HP to 10 HP), with bank loan for 30% and only 10% farmer contribution.", "hi": "3 से 10 एचपी तक के सोलर वाटर पंप लगाने पर 60% तक सरकारी अनुदान (30% केंद्र + 30% राज्य)। किसान को केवल 10% देना होता है।", "mr": "३ ते १० एचपी सौर कृषी पंप बसवण्यासाठी ६०% शासकीय अनुदान (३०% केंद्र + ३०% राज्य). शेतकऱ्याला फक्त १०% रक्कम भरावी लागते."},
        "subsidy": "60% Subsidy (30% Central + 30% State)",
        "eligibility": {"en": "Individual farmers, water user associations, and cooperatives with cultivable land lacking grid power.", "hi": "व्यक्तिगत किसान, किसान समूह व सहकारी समितियां।", "mr": "वैयक्तिक शेतकरी, शेतकरी गट व सहकारी संस्था."},
        "portal_url": "https://pmkusum.mnre.gov.in",
        "helpline": "1800-180-3333"
    },
    {
        "id": "enam_portal",
        "name": {"en": "National Agriculture Market (e-NAM)", "hi": "राष्ट्रीय कृषि बाजार (ई-नाम / e-NAM)", "mr": "राष्ट्रीय कृषी बाजार (ई-नाम / e-NAM)"},
        "benefit": {"en": "Pan-India electronic trading portal uniting 1300+ APMC mandis across 23 States, enabling online transparent price discovery, quality assaying, and direct inter-mandi online bidding and electronic payment to farmers.", "hi": "1300 से अधिक मंडियों का राष्ट्रीय ऑनलाइन नेटवर्क। किसान अपनी उपज का पारदर्शी मूल्य खोज कर देश के किसी भी व्यापारी को ऑनलाइन बेच सकते हैं।", "mr": "देशातील १३००+ कृषी उत्पन्न बाजार समित्यांचे ऑनलाइन जाळे. पारदर्शक लिलाव व थेट बँक खात्यात चुकारे."},
        "subsidy": "Free Electronic Trading Platform for Farmers",
        "eligibility": {"en": "Any farmer with Aadhaar card, bank passbook, and harvest produce at enrolled mandis.", "hi": "आधार कार्ड और बैंक खाता धारक कोई भी किसान अपनी फसल लेकर पंजीकृत मंडी में जा सकता है।", "mr": "आधार कार्ड व बँक खाते असलेला कोणताही शेतकरी."},
        "portal_url": "https://enam.gov.in",
        "helpline": "1800-270-0224"
    },
    {
        "id": "pkvy_organic",
        "name": {"en": "Paramparagat Krishi Vikas Yojana (PKVY Organic)", "hi": "परम्परागत कृषि विकास योजना (पीकेवीवाई जैविक खेती)", "mr": "पारंपारिक कृषी विकास योजना (PKVY सेंद्रिय शेती)"},
        "benefit": {"en": "Financial assistance of ₹50,000 per hectare over 3 years for cluster organic farming, biological inputs, PGS-India organic certification, and value addition/packaging.", "hi": "जैविक खेती क्लस्टर हेतु 3 वर्ष में ₹50,000 प्रति हेक्टेयर की वित्तीय सहायता, पीजीएस प्रमाणीकरण और जैविक खाद व कीटनाशक निर्माण।", "mr": "सेंद्रिय शेती क्लस्टरसाठी ३ वर्षांत ₹५०,००० प्रति हेक्टर आर्थिक मदत, सेंद्रिय प्रमाणीकरण व ब्रँडिंग सहाय्य."},
        "subsidy": "₹50,000 / hectare over 3 years",
        "eligibility": {"en": "Farmer clusters forming groups of 20 or more farmers covering minimum 50 acres.", "hi": "20 या अधिक किसानों का समूह जो कम से कम 50 एकड़ क्षेत्र में जैविक खेती करे।", "mr": "२० किंवा अधिक शेतकऱ्यांचा ५० एकर परिसरातील सेंद्रिय शेती गट."},
        "portal_url": "https://pgsindia-ncof.gov.in",
        "helpline": "1800-180-1551"
    }
]

# Official Extension Helplines
FARMER_SERVICES = [
    {
        "title": {"en": "Kisan Call Center (KCC) - National Toll Free", "hi": "किसान कॉल सेंटर (केसीसी) - राष्ट्रीय टोल फ्री", "mr": "किसान कॉल सेंटर (राष्ट्रीय टोल फ्री)"},
        "contact": "1800-180-1551 or 1551 (6:00 AM to 10:00 PM daily)",
        "desc": {
            "en": "Nationwide toll-free telephone advisory answering crop production, veterinary, market prices and weather queries directly in 22 local languages.",
            "hi": "स्थानीय भाषा में कृषि विशेषज्ञों द्वारा फसलों, पशुपालन, मंडी भाव और मौसम की तत्काल मुफ्त सलाह (प्रतिदिन सुबह 6 से रात 10 बजे)।",
            "mr": "स्थानिक भाषेत कृषी तज्ञांकडून पिके, पशुपालन, बाजारभाव व हवामानाची थेट मोफत माहिती (दररोज सकाळी ६ ते रात्री १०)."
        }
    },
    {
        "title": {"en": "Agricultural Technology Management Agency (ATMA)", "hi": "आत्मा (ATMA) एवं जिला विस्तार तंत्र", "mr": "आत्मा (ATMA) व जिल्हा कृषी यंत्रणा"},
        "contact": "Block Technology Manager / District Agriculture Officer",
        "desc": {
            "en": "Farmer Interest Groups (FIGs), on-field demonstrations, farm schools, exposure visits, and modern farm technology dissemination.",
            "hi": "खेत पाठशाला, किसान गोष्ठी, अग्रिम पंक्ति प्रदर्शन और नवीन तकनीकों का किसान स्तर पर व्यावहारिक प्रशिक्षण।",
            "mr": "शेतकरी शाळा, प्रात्यक्षिके, अभ्यास दौरे आणि आधुनिक कृषी तंत्रज्ञानाचा गावपातळीवर प्रसार."
        }
    },
    {
        "title": {"en": "Krishi Vigyan Kendra (KVK) Scientist Network", "hi": "कृषि विज्ञान केंद्र (KVK) वैज्ञानिक नेटवर्क", "mr": "कृषी विज्ञान केंद्र (KVK) शास्त्रज्ञ नेटवर्क"},
        "contact": "730+ KVKs across all Indian districts",
        "desc": {
            "en": "Frontline extension, soil & water testing laboratories, high-yielding quality seed production, and plant clinic diagnostic support.",
            "hi": "जिला स्तर पर मृदा व जल परीक्षण प्रयोगशाला, उन्नत बीज उत्पादन और विशेषज्ञ वैज्ञानिकों द्वारा प्रत्यक्ष मार्गदर्शन।",
            "mr": "जिल्हा स्तरावर माती व पाणी परीक्षण प्रयोगशाळा, सुधारित बियाणे उत्पादन व पीक रोग निदान केंद्र."
        }
    }
]
