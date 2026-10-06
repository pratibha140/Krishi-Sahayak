# crops_data.py
# Comprehensive Agricultural Database for Krishi Sahayak
# Incorporating authoritative agronomic guidelines from 'Farmer's Handbook on Basic Agriculture'
# (MANAGE, Ministry of Agriculture GoI, Desai Fruits & Vegetables, GIZ).
# Multilingual data across English ('en'), Hindi ('hi'), and Marathi ('mr').

from datetime import datetime, timedelta

CROPS = {
    "rice": {
        "id": "rice",
        "category": "cereals",
        "names": {"en": "Rice (Paddy)", "hi": "धान (चावल)", "mr": "भात (धान)"},
        "scientific_name": "Oryza sativa",
        "season": {"en": "Kharif / Rabi", "hi": "खरीफ / रबी", "mr": "खरीप / रब्बी"},
        "duration_days": 125,
        "optimal_temp": "20°C - 35°C",
        "rainfall_mm": "1000 - 1500 mm",
        "soil": {
            "en": "Clayey loam, alluvial soil with good water retention (pH 5.5 - 6.5)",
            "hi": "चिकनी दोमट, जलोढ़ मिट्टी जिसमें जल धारण क्षमता अच्छी हो (pH 5.5 - 6.5)",
            "mr": "चिकणमाती, गाळाची जमीन ज्यामध्ये पाणी धरून ठेवण्याची क्षमता चांगली असेल (pH 5.5 - 6.5)",
        },
        "sowing_months": {
            "en": "June - July (Kharif), Nov - Dec (Rabi)",
            "hi": "जून - जुलाई (खरीफ), नवंबर - दिसंबर (रबी)",
            "mr": "जून - जुलै (खरीप), नोव्हेंबर - डिसेंबर (रब्बी)",
        },
        "expected_yield_per_acre": "20 - 28 Quintals",
        "fertilizer_per_acre_kg": {
            "urea": 100,
            "dap": 50,
            "mop": 35,
            "zinc_sulphate": 10,
            "fym_tonnes": 4,
        },
        "growth_stages": [
            {
                "day_start": 0,
                "day_end": 20,
                "stage": {"en": "Nursery & Sowing", "hi": "नर्सरी व बुवाई", "mr": "रोपवाटिका व पेरणी"},
                "task": {
                    "en": "Seed treatment with Carbendazim (2g/kg) or Trichoderma (5-10g/kg). Apply basal dose of 50kg DAP + 18kg MOP + 10kg Zinc Sulphate per acre.",
                    "hi": "कार्बेंडाजिम (2 ग्राम/किग्रा) या ट्राइकोडर्मा (5-10 ग्राम/किग्रा) से बीज उपचार। 50 किग्रा DAP + 18 किग्रा MOP + 10 किग्रा जिंक सल्फेट प्रति एकड़ आधार खाद डालें।",
                    "mr": "कार्बेंडाझिम (२ ग्रॅम/किग्रॅ) किंवा ट्रायकोडर्मा (५-१० ग्रॅम/किग्रॅ) ने बीज प्रक्रिया. ५० किग्रॅ DAP + १८ किग्रॅ MOP + १० किग्रॅ झिंक सल्फेट प्रति एकर बेसल डोस द्या.",
                },
                "water_advice": {
                    "en": "Maintain shallow water level (2-3 cm) in nursery bed.",
                    "hi": "नर्सरी में 2-3 सेमी उथला पानी बनाए रखें।",
                    "mr": "रोपवाटिकेत २-३ सेमी उथळ पाणी साठवून ठेवा.",
                },
            },
            {
                "day_start": 21,
                "day_end": 45,
                "stage": {"en": "Tillering & Vegetative", "hi": "कल्ले फूटना व वानस्पतिक वृद्धि", "mr": "फुटवे फुटणे व वाढ"},
                "task": {
                    "en": "Transplant seedlings (2-3 per hill). Apply first top dressing: 40kg Urea per acre at 25-30 days after transplanting.",
                    "hi": "पौध रोपाई करें (2-3 पौधे प्रति थान)। रोपाई के 25-30 दिन बाद 40 किग्रा यूरिया प्रति एकड़ का पहला छिड़काव करें।",
                    "mr": "रोपांची पुनर्लागवड करा. पुनर्लागवडीच्या २५-३० दिवसांनी ४० किग्रॅ युरिया प्रति एकर पहिला हप्ता द्या.",
                },
                "water_advice": {
                    "en": "Keep 4-5 cm standing water in main field.",
                    "hi": "मुख्य खेत में 4-5 सेमी पानी भरा रखें।",
                    "mr": "मुख्य शेतात ४-५ सेमी पाणी साठवून ठेवा.",
                },
            },
            {
                "day_start": 46,
                "day_end": 80,
                "stage": {"en": "Panicle Initiation & Flowering", "hi": "बाली निकलना व फूल आना", "mr": "पोंगा अवस्था व फुलधारणा"},
                "task": {
                    "en": "Apply second top dressing: 35kg Urea + 17kg MOP per acre. Monitor for Stem Borer and Blast disease.",
                    "hi": "दूसरा छिड़काव: 35 किग्रा यूरिया + 17 किग्रा MOP प्रति एकड़। तना छेदक और झुलसा रोग की निगरानी करें।",
                    "mr": "दुसरा हप्ता: ३५ किग्रॅ युरिया + १७ किग्रॅ MOP प्रति एकर. खोडकीड आणि करपा रोगाची तपासणी करा.",
                },
                "water_advice": {
                    "en": "Ensure critical moisture; avoid water stress during flowering.",
                    "hi": "फूल आने के समय पानी की कमी न होने दें।",
                    "mr": "फुलधारणेच्या वेळी पाण्याची अजिबात टंचाई होऊ देऊ नका.",
                },
            },
            {
                "day_start": 81,
                "day_end": 110,
                "stage": {"en": "Milking & Grain Filling", "hi": "दूधिया अवस्था व दाना भराव", "mr": "दाणे भरणे अवस्था"},
                "task": {
                    "en": "Apply 13:00:45 foliar spray (10g/L) for bold grains. Check for Gundhi bug and Brown Planthopper.",
                    "hi": "मोटे दानों के लिए 13:00:45 (10 ग्राम/ली.) का पर्णीय छिड़काव करें। गांधी बग और भूरे फुदके की जांच करें।",
                    "mr": "टपोऱ्या दाण्यांसाठी १३:००:४५ (१० ग्रॅम/ली.) फवारणी करा. गंधी बग आणि तुडतुड्यांचे निरीक्षण करा.",
                },
                "water_advice": {
                    "en": "Keep soil saturated but drain standing water 10 days before harvest.",
                    "hi": "मिट्टी में नमी बनाए रखें पर कटाई से 10 दिन पहले पानी निकाल दें।",
                    "mr": "जमीन ओलसर ठेवा, कापणीपूर्वी १० दिवस आधी पाणी काढून टाका.",
                },
            },
            {
                "day_start": 111,
                "day_end": 125,
                "stage": {"en": "Maturity & Harvesting", "hi": "परिपक्वता व कटाई", "mr": "पक्वता व कापणी"},
                "task": {
                    "en": "Harvest when 85% grains turn golden yellow. Thresh and dry grains to 12-14% moisture before storage.",
                    "hi": "जब 85% बालियां सुनहरी पीली हो जाएं तो कटाई करें। गहाई कर दानों को 12-14% नमी तक सुखाकर भंडारण करें।",
                    "mr": "८५% लोंब्या पिवळ्या झाल्यावर कापणी करा. मळणी करून दाण्यांमधील ओलावा १२-१४% पर्यंत सुकवून साठवणूक करा.",
                },
                "water_advice": {
                    "en": "Completely dry field for smooth harvesting machinery operation.",
                    "hi": "कटाई के लिए खेत को पूरी तरह सूखा रखें।",
                    "mr": "कापणी यंत्रांच्या सुलभ हालचालीसाठी शेत कोरडे ठेवा.",
                },
            },
        ],
        "pests_and_diseases": [
            {
                "name": {"en": "Rice Blast (Fungal)", "hi": "धान का झुलसा (ब्लास्ट)", "mr": "भाताचा करपा"},
                "symptoms": {
                    "en": "Spindle-shaped lesions with grey center and brown margins on leaves and panicles.",
                    "hi": "पत्तियों और बालियों पर नाव के आकार के धब्बे जिनका केंद्र धूसर व किनारे भूरे होते हैं।",
                    "mr": "पानांवर आणि लोंब्यांवर मध्यभागी राखाडी आणि कडेला तपकिरी रंगाचे डोळ्यासारखे डाग.",
                },
                "organic_remedy": {
                    "en": "Spray Pseudomonas fluorescens @ 10g/L or fermented butter milk (5%).",
                    "hi": "स्यूडोमोनास फ्लोरोसेंस 10 ग्राम/ली. या खट्टी छाछ (5%) का छिड़काव करें।",
                    "mr": "स्यूडोमोनास फ्लोरोसन्स १० ग्रॅम/ली. किंवा आंबट ताक (५%) फवारा.",
                },
                "chemical_remedy": {
                    "en": "Spray Tricyclazole 75% WP @ 0.6g/L or Kasugamycin 3% SL @ 2ml/L.",
                    "hi": "ट्राइसाइक्लाजोल 75% WP 0.6 ग्राम/ली. या कासुगामाइसिन 3% SL 2 मिली/ली. छिड़कें।",
                    "mr": "ट्रायसायक्लॅझोल ७५% WP ०.६ ग्रॅम/ली. किंवा कासुगामायसिन ३% SL २ मिली/ली. फवारा.",
                },
            },
            {
                "name": {"en": "Yellow Stem Borer", "hi": "पीला तना छेदक", "mr": "पिवळी खोडकीड"},
                "symptoms": {
                    "en": "Dead hearts in vegetative stage and white heads at panicle stage.",
                    "hi": "वानस्पतिक अवस्था में 'डेड हार्ट' और बाली निकलने पर सफेद बालियां दिखाई देना।",
                    "mr": "वाढीच्या काळात पोंगे सुकणे (डेड हार्ट) आणि लोंबीच्या वेळी पांढऱ्या लोंब्या दिसणे.",
                },
                "organic_remedy": {
                    "en": "Install pheromone traps @ 8/acre; release Trichogramma chilonis @ 20,000/acre.",
                    "hi": "फेरोमोन ट्रैप 8 प्रति एकड़ लगाएं; ट्राइकोग्रामा चिलोनीस 20,000 प्रति एकड़ छोड़ें।",
                    "mr": "प्रति एकर ८ कामगंध सापळे लावा; ट्रायकोगामा चिलोनीस २०,००० प्रति एकर सोडा.",
                },
                "chemical_remedy": {
                    "en": "Apply Cartap Hydrochloride 4G @ 7.5kg/acre or spray Chlorantraniliprole 18.5% SC @ 0.3ml/L.",
                    "hi": "कार्टाप हाइड्रोक्लोराइड 4G 7.5 किग्रा/एकड़ डालें या क्लोरेंट्रानिलिप्रोल 18.5% SC 0.3 मिली/ली. छिड़कें।",
                    "mr": "कार्टाप हायड्रोक्लोराईड ४G ७.५ किग्रॅ/एकर द्या किंवा क्लोरँट्रानिलीप्रोल १८.५% SC ०.३ मिली/ली. फवारा.",
                },
            },
        ],
    },

    "banana": {
        "id": "banana",
        "category": "fruits",
        "names": {"en": "Banana", "hi": "केला", "mr": "केळी"},
        "scientific_name": "Musa acuminata",
        "season": {"en": "Year-round (Planting: June - July)", "hi": "वार्षिक (रोपाई: 15 जून - 15 जुलाई)", "mr": "वार्षिक (लागवड: १५ जून - १५ जुलै)"},
        "duration_days": 360,
        "optimal_temp": "25°C - 30°C",
        "rainfall_mm": "2000 - 2500 mm (Drip: 900 - 1080 mm)",
        "soil": {
            "en": "Rich loamy and silty clay loam soils with good drainage, rich in organic matter (pH 6.5 - 7.5)",
            "hi": "उत्तम जल निकासी वाली उपजाऊ दोमट या चिकनी दोमट मिट्टी जिसमें जीवांश प्रचुर हो (pH 6.5 - 7.5)",
            "mr": "पाण्याचा उत्तम निचरा होणारी कसदार पोयटा किंवा काळी चिकणमाती जमीन (pH ६.५ - ७.५)",
        },
        "sowing_months": {
            "en": "15th June to 15th July (Monsoon planting)",
            "hi": "15 जून से 15 जुलाई",
            "mr": "१५ जून ते १५ जुलै",
        },
        "expected_yield_per_acre": "28 - 35 Tonnes (70 - 80 t/ha)",
        "fertilizer_per_acre_kg": {
            "urea": 180,
            "dap": 80,
            "mop": 180,
            "fym_tonnes": 10,
        },
        "growth_stages": [
            {
                "day_start": 0,
                "day_end": 30,
                "stage": {"en": "Pit Prep & Planting", "hi": "गड्ढा तैयारी व रोपाई", "mr": "खड्डे भरणे व लागवड"},
                "task": {
                    "en": "Dig pits of 30x30x30 cm at 1.5x1.5m spacing. Expose to sun for 15 days (solarization). Fill with 15kg FYM + 80kg DAP basal. Treat suckers (500-1500g) with Aurofugin (10g/100L) or Trichoderma for 1.5 hrs.",
                    "hi": "1.5x1.5 मीटर पर 30x30x30 सेमी गड्ढे खोदें। 15 दिन धूप दिखाएं। 15 किग्रा गोबर खाद + 80 किग्रा DAP भरें। कंदों (500-1500 ग्राम) को 1.5 घंटे ऑरोफ्यूजिन (10 ग्राम/100 ली.) या ट्राइकोडर्मा में डुबोएं।",
                    "mr": "१.५x१.५ मीटर अंतरावर ३०x३०x३० सेमी खड्डे घ्या. १५ दिवस उन्हात तापू द्या. १५ किग्रॅ शेणखत + ८० किग्रॅ DAP भरा. बेणे (५००-१५०० ग्रॅम) ऑरोफ्युजिन (१० ग्रॅम/१०० ली.) किंवा ट्रायकोडर्मामध्ये १.५ तास बुडवून लावा.",
                },
                "water_advice": {
                    "en": "Drip irrigation: 5 Litres/day/plant in months 1-3.",
                    "hi": "ड्रिप सिंचाई: पहले 1-3 महीनों में 5 लीटर/दिन/पौधा।",
                    "mr": "ठिबक सिंचन: पहिल्या १-३ महिन्यांत ५ लिटर/दिवस/झाड.",
                },
            },
            {
                "day_start": 31,
                "day_end": 120,
                "stage": {"en": "Vegetative & Desuckering", "hi": "वानस्पतिक बढ़वार व कंद छंटाई", "mr": "झाडांची वाढ व पिलवे काढणे"},
                "task": {
                    "en": "Apply water-soluble fertilizers in 7-8 splits (180g N + 72g P + 180g K per plant). Remove extra side suckers manually and inject 3ml diesel/kerosene in cut portion to stop regrowth. Mulch with black plastic (50 micron) or sugarcane trash (4 t/acre).",
                    "hi": "घुलनशील खाद 7-8 किस्तों में दें (180g N + 72g P + 180g K प्रति पौधा)। अनावश्यक कल्ले (सकर्स) हटाएं व कटे भाग पर 3 मिली केरोसिन लगाएं। काली प्लास्टिक मल्चिंग (50 माइक्रोन) या गन्ने की पत्ती बिछाएं।",
                    "mr": "खतांचे ७-८ हप्ते द्या (१८० ग्रॅम N + ७२ ग्रॅम P + १८० ग्रॅम K प्रति झाड). अनावश्यक पिलवे कापून त्यावर ३ मिली रॉकेल टाका जेणेकरून पुन्हा फुटणार नाहीत. ५० मायक्रॉन काळी प्लास्टिक मल्चिंग करा.",
                },
                "water_advice": {
                    "en": "Drip irrigation: 9 Litres/day/plant in months 3-5.",
                    "hi": "ड्रिप सिंचाई: 3-5 महीनों में 9 लीटर/दिन/पौधा।",
                    "mr": "ठिबक सिंचन: ३-५ महिन्यांत ९ लिटर/दिवस/झाड.",
                },
            },
            {
                "day_start": 121,
                "day_end": 240,
                "stage": {"en": "Shooting & Bunch Emergence", "hi": "फूल निकलना (कमल) व घार बनना", "mr": "केळफूल बाहेर पडणे व घड धरणे"},
                "task": {
                    "en": "Provide bamboo / rope staking to prevent lodging under bunch weight. Apply remaining Potash split. Spray Acetamiprid (0.2g/L) for aphids (Bunchy top vector).",
                    "hi": "घार के वजन से पौधे को गिरने से बचाने के लिए बांस का सहारा दें। बचा हुआ पोटाश दें। एफिड (गुच्छा रोग वाहक) के लिए एसिटामिप्रिड 0.2 ग्राम/ली. छिड़कें।",
                    "mr": "घडाच्या वजनाने झाड पडू नये म्हणून बांबूचा आधार द्या. पोटॅशचा हप्ता द्या. मावा (बंची टॉप वाहक) नियंत्रणासाठी ॲसिटामिप्रिड ०.२ ग्रॅम/ली. फवारा.",
                },
                "water_advice": {
                    "en": "Peak water demand: 11 Litres/day/plant in months 5-8.",
                    "hi": "सर्वाधिक पानी की जरूरत: 5-8 महीनों में 11 लीटर/दिन/पौधा।",
                    "mr": "पाण्याची सर्वाधिक गरज: ५-८ महिन्यांत ११ लिटर/दिवस/झाड.",
                },
            },
            {
                "day_start": 241,
                "day_end": 360,
                "stage": {"en": "Bunch Maturation & Harvest", "hi": "घार विकास, बैगिंग व कटाई", "mr": "घड भरणे, बॅगिंग व काढणी"},
                "task": {
                    "en": "Cover bunches with blue/white LLDP film bags to protect from sun-scorch and thrips, improving fruit shine. Harvest at 75-80% maturity when angles of fingers turn round. Yield 70-80 t/ha.",
                    "hi": "घार को नीली/सफेद LLDP पॉलीथीन बैग से ढकें (बैगिंग)। जब केलों की धारियां गोल होने लगें (75-80% परिपक्वता) तो सुबह काटें। पैदावार 70-80 टन/हेक्टेयर।",
                    "mr": "घडाला निळ्या किंवा पांढऱ्या LLDP बॅगने झाका (बॅगिंग). केळीच्या शिरा गोल झाल्यावर (७५-८०% पक्वता) सकाळी कापणी करा. उत्पादन ७०-८० टन/हेक्टर.",
                },
                "water_advice": {
                    "en": "Drip: 10 Litres/day/plant in months 8-11. Reduce 10 days before harvest.",
                    "hi": "8-11 महीनों में 10 लीटर/दिन/पौधा। कटाई से 10 दिन पहले पानी कम करें।",
                    "mr": "८-११ महिन्यांत १० लिटर/दिवस/झाड. कापणीपूर्वी १० दिवस पाणी कमी करा.",
                },
            },
        ],
        "pests_and_diseases": [
            {
                "name": {"en": "Banana Bunchy Top Virus (BBTV)", "hi": "केले का गुच्छा रोग (बंची टॉप)", "mr": "केळीचा बंची टॉप (माथा तुरा)"},
                "symptoms": {
                    "en": "Dark green broken streaks on leaf veins, extremely stunted crowded upright leaves forming a rosette at top.",
                    "hi": "पत्तियों की नसों पर गहरे हरे टूटे हुए धब्बे, ऊपर की पत्तियां छोटी व खड़ी होकर गुच्छा बन जाना, फल न लगना।",
                    "mr": "पानांच्या शिरांवर गडद हिरव्या तुटक रेषा, पाने वरच्या बाजूला गोळा होऊन झाडाचा माथा झाडूंसारखा दिसणे.",
                },
                "organic_remedy": {
                    "en": "Uproot and destroy infected plants immediately. Spray Neem oil 10000 ppm @ 2ml/L.",
                    "hi": "संक्रमित पौधों को तुरंत उखाड़कर नष्ट करें। नीम तेल 10000 ppm 2 मिली/ली. छिड़कें।",
                    "mr": "रोगग्रस्त झाडे लगेच उपटून नष्ट करा. कडुलिंब तेल १०००० ppm २ मिली/ली. फवारा.",
                },
                "chemical_remedy": {
                    "en": "Spray Acetamiprid @ 0.2g/L or Methyl Demeton 2ml/L directed towards crown to kill vector aphids at 21-day intervals.",
                    "hi": "एफिड वाहक नष्ट करने के लिए एसिटामिप्रिड 0.2 ग्राम/ली. या मिथाइल डिमेटॉन 2 मिली/ली. तने व पत्तियों के बीच छिड़कें।",
                    "mr": "मावा नियंत्रणासाठी ॲसिटामिप्रिड ०.२ ग्रॅम/ली. किंवा मिथाईल डिमेटॉन २ मिली/ली. झाडाच्या पोंग्यात फवारा.",
                },
            },
            {
                "name": {"en": "Panama Wilt (Fusarium oxysporum)", "hi": "पनामा विल्ट (उकठा रोग)", "mr": "पनामा मर रोग"},
                "symptoms": {
                    "en": "Yellowing of lower leaf margins, leaves break at petiole and hang down like a skirt around pseudostem, longitudinal splitting of stem.",
                    "hi": "निचली पत्तियों का पीला पड़ना, डंठल से टूटकर तने के चारों ओर लटक जाना, तने का फटना और अंदर भूरी धारियां दिखना।",
                    "mr": "खालची पाने पिवळी पडून देठाजवळ मोडून खोडाभोवती लटकणे, खोडाला उभी चीर पडणे व आतून तपकिरी होणे.",
                },
                "organic_remedy": {
                    "en": "Corm injection of 50mg Pseudomonas fluorescens capsule at 2nd, 4th, 6th month. Apply 1-2kg lime in pit after uprooting.",
                    "hi": "रोपाई के 2, 4, 6 माह पर 50 मिग्रा स्यूडोमोनास फ्लोरोसेंस का कंद इंजेक्शन दें। पौधा हटाने पर गड्ढे में 1-2 किग्रा चूना डालें।",
                    "mr": "लागवडीनंतर २, ४, ६ व्या महिन्यात ५० मिग्रॅ स्यूडोमोनास कॅप्सूल कंदात टोचा. खड्ड्यात १-२ किग्रॅ चुना टाका.",
                },
                "chemical_remedy": {
                    "en": "Soil drenching with Carbendazim 50% WP @ 2g/L around root zone.",
                    "hi": "कार्बेंडाजिम 50% WP 2 ग्राम/ली. घोल बनाकर जड़ों के पास मिट्टी में डालें।",
                    "mr": "कार्बेंडाझिम ५०% WP २ ग्रॅम/ली. द्रावण मुळांच्या भागात आळवणी करा.",
                },
            },
            {
                "name": {"en": "Sigatoka Leaf Spot", "hi": "सिगाटोका पत्ती धब्बा", "mr": "सिगाटोका करपा"},
                "symptoms": {
                    "en": "Small light yellow narrow streaks enlarging into oblong brown-to-black spots with yellow halos; rapid defoliation.",
                    "hi": "पत्तियों पर पीले-भूरे संकरे धब्बे जो बढ़कर काले हो जाते हैं और पत्तियां तेजी से सूखकर गिर जाती हैं।",
                    "mr": "पानांवर पिवळसर-तपकिरी लांबट ठिपके, नंतर काळे डाग पडून पाने जळून गळणे.",
                },
                "organic_remedy": {
                    "en": "Remove affected leaves and burn. Spray fermented buttermilk (5%) or Trichoderma viride @ 5g/L.",
                    "hi": "प्रभावित पत्तियां काटकर जलाएं। 5% खट्टी छाछ या ट्राइकोडर्मा 5 ग्राम/ली. छिड़कें।",
                    "mr": "रोगट पाने कापून नष्ट करा. ५% आंबट ताक किंवा ट्रायकोडर्मा ५ ग्रॅम/ली. फवारा.",
                },
                "chemical_remedy": {
                    "en": "Spray Difenoconazole @ 2ml/L or Azoxystrobin @ 2ml/L or Copper Oxychloride @ 2.5g/L + Sandovit (5ml/10L) at monthly intervals.",
                    "hi": "डिफेनोकोनाजोल 2 मिली/ली. या एजॉक्सीस्ट्रोबिन 2 मिली/ली. + सैंडोविट स्टीकर 5 मिली/10 ली. पानी में मिलाकर छिड़कें।",
                    "mr": "डायफेनोकोनाझोल २ मिली/ली. किंवा अॅझॉक्सीस्ट्रोबिन २ मिली/ली. + स्टिकर ५ मिली/१० ली. पाण्यात मिसळून फवारा.",
                },
            },
        ],
    },

    "mango": {
        "id": "mango",
        "category": "fruits",
        "names": {"en": "Mango", "hi": "आम", "mr": "आंबा"},
        "scientific_name": "Mangifera indica",
        "season": {"en": "Perennial (Planting: July - Sept)", "hi": "बहुवर्षीय (रोपाई: जुलाई - सितंबर)", "mr": "बहुवार्षिक (लागवड: जुलै - सप्टेंबर)"},
        "duration_days": 365,
        "optimal_temp": "24°C - 27°C",
        "rainfall_mm": "750 - 1500 mm",
        "soil": {
            "en": "Deep, well-drained alluvial to lateritic loamy soils (avoid poorly drained heavy black cotton soils)",
            "hi": "गहरी, उत्तम जल निकास वाली जलोढ़ या लाल दोमट मिट्टी (जलभराव वाली भारी काली मिट्टी में न लगाएं)",
            "mr": "खोल, पाण्याचा चांगला निचरा होणारी गाळाची किंवा जांभा पोयटा जमीन (पाणी साचणाऱ्या जमिनीत लावू नये)",
        },
        "sowing_months": {
            "en": "July to September (Graft planting)",
            "hi": "जुलाई से सितंबर",
            "mr": "जुलै ते सप्टेंबर",
        },
        "expected_yield_per_acre": "6 - 10 Tonnes (15-20 t/ha at full bearing)",
        "fertilizer_per_acre_kg": {
            "urea": 160,
            "dap": 70,
            "mop": 120,
            "fym_tonnes": 10,
        },
        "growth_stages": [
            {
                "day_start": 0,
                "day_end": 60,
                "stage": {"en": "Pit Prep & Planting", "hi": "गड्ढा भराई व कलमी रोपाई", "mr": "खड्डे भरणे व कलमे लावणे"},
                "task": {
                    "en": "Dig pits of 1m x 1m x 1m 1 month prior to planting. Expose to sun for 2-4 weeks. Fill with 15-20kg FYM + 1kg SSP per pit. High density spacing 5m x 5m (160 plants/acre) or normal 8m x 8m. Plant genuine veneer/wedge grafts during July-Sept.",
                    "hi": "रोपाई से 1 माह पूर्व 1x1x1 मीटर गड्ढे खोदें। 2-4 हफ्ते धूप दिखाएं। 15-20 किग्रा गोबर खाद + 1 किग्रा सिंगल सुपर फास्फेट भरें। सघन बागवानी 5x5 मीटर या सामान्य 8x8 मीटर। जुलाई-सितंबर में कलमें लगाएं।",
                    "mr": "लागवडीच्या १ महिना आधी १x१x१ मीटर खड्डे घ्या. २-४ आठवडे उन्हात तापू द्या. १५-२० किग्रॅ शेणखत + १ किग्रॅ SSP भरा. ५x५ मीटर (सघन) किंवा ८x८ मीटर अंतरावर जुलै-सप्टेंबरमध्ये कलमे लावा.",
                },
                "water_advice": {
                    "en": "Young plants (up to 3 yrs): 9-12 Litres/day/tree (2 drippers at 1m distance).",
                    "hi": "छोटे पौधे (3 वर्ष तक): 9-12 लीटर/दिन/पेड़ (2 ड्रिपर 1 मीटर दूरी पर)।",
                    "mr": "लहान झाडे (३ वर्षांपर्यंत): ९-१२ लिटर/दिवस/झाड (२ ड्रिपर १ मीटर अंतरावर).",
                },
            },
            {
                "day_start": 61,
                "day_end": 180,
                "stage": {"en": "Canopy Training & Weeding", "hi": "कटाई-छंटाई (कैनोपी) व निराई", "mr": "झाडाला आकार देणे व स्वच्छता"},
                "task": {
                    "en": "Train branches after 6 months to maintain branching height at 60-70 cm from ground. Intercrop vegetables (onion, tomato, cabbage) in initial 4-5 years. Apply black plastic mulch (100 micron, 1x1m for young, 2.5x2.5m for adult) to suppress weeds.",
                    "hi": "6 माह बाद प्राथमिक शाखाएं जमीन से 60-70 सेमी ऊंचाई पर रखें। शुरुआती 4-5 वर्षों में बीच में प्याज, टमाटर, पत्तागोभी लगाएं। खरपतवार रोकने के लिए 100 माइक्रोन ब्लैक प्लास्टिक मल्चिंग लगाएं।",
                    "mr": "६ महिन्यांनंतर झाडांची पहिली फांदी जमिनीपासून ६०-७० सेमी उंचीवर ठेवा. सुरुवातीच्या ४-५ वर्षांत आंतरपीक म्हणून कांदा, टोमॅटो घ्या. तण नियंत्रणासाठी १०० मायक्रॉन काळी मल्चिंग वापरा.",
                },
                "water_advice": {
                    "en": "3-6 years trees: 30-35 Litres/day/tree; 6-10 years: 50-60 Litres/day/tree.",
                    "hi": "3-6 वर्ष: 30-35 लीटर/दिन; 6-10 वर्ष: 50-60 लीटर/दिन/पेड़।",
                    "mr": "३-६ वर्षे: ३०-३५ लिटर/दिवस; ६-१० वर्षे: ५०-६० लिटर/दिवस/झाड.",
                },
            },
            {
                "day_start": 181,
                "day_end": 300,
                "stage": {"en": "Flowering & Fruit Setting", "hi": "मंजर (फूल) आना व फल विकास", "mr": "मोहर येणे व फळधारणा"},
                "task": {
                    "en": "Apply Paclobutrazol (5-10g/m canopy diameter) 3 months before budburst (Sept-Oct) through soil drenching for regular annual bearing. Deblossom malformed buds (1cm long) + spray NAA 200ppm. Spray Wettable Sulphur (0.2%) for powdery mildew and Acetamiprid (0.2g/L) for hoppers.",
                    "hi": "नियमित फलन के लिए कली फूटने से 3 माह पहले (सितंबर-अक्टूबर) पैक्लोबुट्राजोल (5-10 ग्राम/मीटर घेरा) मिट्टी में डालें। विकृत मंजर हटाएं + NAA 200ppm छिड़कें। हॉपर के लिए एसिटामिप्रिड 0.2 ग्राम/ली. छिड़कें।",
                    "mr": "दरवर्षी नियमित उत्पादनासाठी पॅक्लोब्युट्राझोल (५-१० ग्रॅम/मीटर विस्तार) सप्टेंबर-ऑक्टोबरमध्ये मुळांत आळवणी करा. तुडतुड्यांसाठी ॲसिटामिप्रिड ०.२ ग्रॅम/ली. आणि भुरीसाठी पाण्यात मिसळणारे गंधक (०.२%) फवारा.",
                },
                "water_advice": {
                    "en": "Stop watering during flower bud differentiation (Oct-Nov); resume light drip after fruit set (pea size). Fully grown tree: 120 Litres/day.",
                    "hi": "फूल आने से पहले अक्टूबर-नवंबर में पानी रोकें; फल मटर के दाने जितने होने पर ड्रिप चालू करें। वयस्क पेड़: 120 लीटर/दिन।",
                    "mr": "मोहर येण्यापूर्वी ऑक्टोबर-नोव्हेंबरमध्ये पाण्याचा ताण द्या; वाटाण्याएवढी फळे झाल्यावर पाणी सुरू करा. मोठे झाड: १२० लिटर/दिवस.",
                },
            },
            {
                "day_start": 301,
                "day_end": 365,
                "stage": {"en": "Fruit Maturity & Harvest", "hi": "फल परिपक्वता, तुड़ाई व ग्रेडिंग", "mr": "फळ पक्वता, काढणी व साठवण"},
                "task": {
                    "en": "Harvest mature green fruits in morning with 8mm pedicel using mango harvesters. Hang Methyl Eugenol pheromone traps for fruit flies. Pack in ventilated Corrugated Fibreboard (CFB) boxes wrapped with foam paper. Average yield: 50-225 fruits/tree (19 t/ha).",
                    "hi": "सुबह के समय 8 मिमी डंठल के साथ तुड़ाई करें। फल मक्खी के लिए मिथाइल यूजेनॉल ट्रैप लगाएं। सीएफबी बॉक्स में पैक करें। औसत पैदावार: 50-225 फल प्रति पेड़ (19 टन/हेक्टेयर)।",
                    "mr": "सकाळच्या वेळी ८ मिमी देठासह आंबा हार्वेस्टरने तोडा. फळमाशीसाठी मिथाईल युजेनॉल सापळे लावा. बॉक्समध्ये सुरक्षित पॅकिंग करा. उत्पादन ५०-२२५ फळे प्रति झाड (१९ टन/हेक्टर).",
                },
                "water_advice": {
                    "en": "Stop irrigation 15 days before harvest to enhance fruit sweetness and shelf life.",
                    "hi": "मिठास और भंडारण क्षमता बढ़ाने हेतु तुड़ाई से 15 दिन पहले सिंचाई बंद करें।",
                    "mr": "गोडी व टिकाऊपणा वाढवण्यासाठी काढणीपूर्वी १५ दिवस पाणी बंद करा.",
                },
            },
        ],
        "pests_and_diseases": [
            {
                "name": {"en": "Mango Hopper (Idioscopus spp.)", "hi": "आम का फुदका (हॉपर)", "mr": "आंब्यावरील तुडतुडे (हॉपर)"},
                "symptoms": {
                    "en": "Nymphs and adults suck sap from tender leaves and inflorescence, causing withering, heavy flower drop, and black sooty mould on sticky honeydew secretions.",
                    "hi": "कीट फूलों और कोपलों से रस चूसते हैं जिससे फूल सूखकर गिर जाते हैं और पत्तियों पर काला फफूंद (सूटी मोल्ड) जम जाता है।",
                    "mr": "मोहरातून आणि कोवळ्या पानातून रस शोषतात, ज्यामुळे मोहर जळून गळतो आणि काळी बुरशी (काजळी) पसरते.",
                },
                "organic_remedy": {
                    "en": "Spray 5% Neem seed kernel extract (NSKE) or Neem oil 1500 ppm @ 3ml/L before flowering.",
                    "hi": "फूल आने से पूर्व 5% नीम बीज अर्क या नीम तेल 1500 ppm 3 मिली/ली. छिड़कें।",
                    "mr": "मोहर येण्यापूर्वी ५% निंबोळी अर्क किंवा कडुलिंब तेल १५०० ppm ३ मिली/ली. फवारा.",
                },
                "chemical_remedy": {
                    "en": "Spray Acetamiprid 20% SP @ 0.2g/L or Thiamethoxam 25% WG @ 0.2g/L at bud burst stage.",
                    "hi": "कली खिलते समय एसिटामिप्रिड 20% SP 0.2 ग्राम/ली. या थायमेथोक्सम 0.2 ग्राम/ली. पानी में मिलाकर छिड़कें।",
                    "mr": "मोहर फुटताना ॲसिटामिप्रिड २०% SP ०.२ ग्रॅम/ली. किंवा थायमेथोक्साम ०.२ ग्रॅम/ली. फवारा.",
                },
            },
            {
                "name": {"en": "Mango Powdery Mildew", "hi": "आम का चूर्णिल आसिता (पाउडरी मिल्ड्यू)", "mr": "आंब्यावरील भुरी रोग"},
                "symptoms": {
                    "en": "White powdery fungal growth covering flower panicles, tender leaves and small fruits; unfertilized flowers drop off.",
                    "hi": "फूलों के गुच्छों और नई पत्तियों पर सफेद पाउडर जैसी फफूंद, फूल झड़ जाना और फल न बनना।",
                    "mr": "मोहरावर आणि कोवळ्या पानांवर पांढरी भुकटी पसरते, मोहर जळून गळून पडतो.",
                },
                "organic_remedy": {
                    "en": "Dust Sulphur (350 mesh) in early morning or spray Cow urine (10%) + Fermented buttermilk.",
                    "hi": "सुबह के समय सल्फर डस्ट (350 मेश) बुरकें या 10% गोमूत्र खट्टी छाछ के साथ छिड़कें।",
                    "mr": "सकाळी गंधक भुकटी (३५० मेश) धुरळा किंवा १०% गोमूत्र आंबट ताकासह फवारा.",
                },
                "chemical_remedy": {
                    "en": "Spray Wettable Sulphur 80% WDG @ 2g/L or Hexaconazole 5% EC @ 1ml/L or Bayleton @ 0.5g/L.",
                    "hi": "घुलनशील सल्फर 80% WDG 2 ग्राम/ली. या हेक्साकोनाजोल 1 मिली/ली. छिड़कें।",
                    "mr": "पाण्यात विरघळणारे गंधक २ ग्रॅम/ली. किंवा हेक्झाकोनाझोल १ मिली/ली. फवारा.",
                },
            },
        ],
    },

    "citrus": {
        "id": "citrus",
        "category": "fruits",
        "names": {"en": "Nagpur Mandarin (Citrus)", "hi": "नागपुर संतरा", "mr": "नागपूर संत्रा"},
        "scientific_name": "Citrus reticulata",
        "season": {"en": "Ambia Bahar / Mrig Bahar", "hi": "अंबिया बहार / मृग बहार", "mr": "आंबिया बहार / मृग बहार"},
        "duration_days": 365,
        "optimal_temp": "20°C - 35°C",
        "rainfall_mm": "750 - 1200 mm",
        "soil": {
            "en": "Well-drained light to medium loamy soil (depth 1-1.5m, avoid heavy clay >60% clay contents)",
            "hi": "अच्छी जल निकासी वाली मध्यम दोमट मिट्टी (60% से अधिक चिकनी मिट्टी वाली भूमि में न लगाएं)",
            "mr": "पाण्याचा उत्तम निचरा होणारी हलकी ते मध्यम पोयटा जमीन (६०% पेक्षा जास्त चिकणमाती असलेली जमीन अयोग्य)",
        },
        "sowing_months": {
            "en": "July - August (Budded graft planting)",
            "hi": "जुलाई - अगस्त",
            "mr": "जुलै - ऑगस्ट",
        },
        "expected_yield_per_acre": "6 - 10 Tonnes (15-20 t/ha)",
        "fertilizer_per_acre_kg": {
            "urea": 150,
            "dap": 65,
            "mop": 90,
            "fym_tonnes": 8,
        },
        "growth_stages": [
            {
                "day_start": 0,
                "day_end": 60,
                "stage": {"en": "Rootstock & Planting", "hi": "मूलवृंत चयन व गड्ढा रोपाई", "mr": "रंगपूर रूटस्टॉक व लागवड"},
                "task": {
                    "en": "Use certified budlings on Rangpur lime rootstock. Dig pits of 75x75x75 cm at 6x6m spacing. Solarize potting mixture in May. Dip roots in Metalaxyl MZ 72 (2.75g/L) for 15 mins. Keep graft union 15cm (6 inches) above ground level.",
                    "hi": "रंगपुर लाइम मूलवृंत पर प्रमाणित कलमें लगाएं। 6x6 मीटर पर 75x75x75 सेमी गड्ढे खोदें। रोपाई से पूर्व जड़ों को मेटालेक्सिल (2.75 ग्राम/ली.) में 15 मिनट डुबोएं। कली का जोड़ जमीन से 15 सेमी ऊपर रखें।",
                    "mr": "रंगपूर लिंबू रूटस्टॉकवरील प्रमाणित कलमे वापरा. ६x६ मीटर अंतरावर ७५x७५x७५ सेमी खड्डे घ्या. मुळे मेटालेक्सिल (२.७५ ग्रॅम/ली.) द्रावणात १५ मिनिटे बुडवून लावा. डोळा जोड जमिनीपासून १५ सेमी वर ठेवा.",
                },
                "water_advice": {
                    "en": "Follow double-ring irrigation system to prevent water from touching tree trunk. Drip: 7-17 L/day in 1st year.",
                    "hi": "डबल रिंग विधि अपनाएं ताकि पानी सीधे तने को न छुए। पहले वर्ष 7-17 लीटर/दिन/पेड़।",
                    "mr": "दुहेरी बांगडी पद्धत वापरा जेणेकरून पाणी थेट खोडाला लागणार नाही. पहिल्या वर्षी ७-१७ लिटर/दिवस/झाड.",
                },
            },
            {
                "day_start": 61,
                "day_end": 180,
                "stage": {"en": "Manuring & Canopy Hygiene", "hi": "खाद प्रबंधन व तना लेप", "mr": "खत व्यवस्थापन व बोर्डो पेस्ट"},
                "task": {
                    "en": "Apply N in 3 splits (Jan, July, Nov), P in 2 splits (Jan, July), and K in Jan. Bearing tree (4th yr+): 600g N, 200g P, 100g K/tree. Apply Bordeaux paste (1kg CuSO4 + 1kg Lime + 10L water) on trunk up to 2.5 feet twice a year (May & Oct) to prevent Gummosis.",
                    "hi": "नाइट्रोजन 3 किस्तों में (जनवरी, जुलाई, नवंबर), फास्फोरस 2 किस्तों में और पोटाश जनवरी में दें। वयस्क पेड़ (4 वर्ष+): 600g N, 200g P, 100g K प्रति पेड़। तने पर गमोसिस रोकने के लिए साल में 2 बार (मई व अक्टूबर) 2.5 फीट तक बोर्डो पेस्ट लगाएं।",
                    "mr": "नत्र ३ हप्त्यांत (जानेवारी, जुलै, नोव्हेंबर), स्फुरद २ हप्त्यांत आणि पालाश जानेवारीत द्या. ४ थ्या वर्षापासून: ६०० ग्रॅम N, २०० ग्रॅम P, १०० ग्रॅम K प्रति झाड. डिंक्या रोग टाळण्यासाठी खोडाला २.५ फुटांपर्यंत वर्षातून २ वेळा (मे व ऑक्टोबर) बोर्डो पेस्ट लावा.",
                },
                "water_advice": {
                    "en": "Drip requirement: 2nd yr (9-34 L), 4th yr (24-74 L), 8th yr (65-188 L), >10 yr (82-235 L/day).",
                    "hi": "ड्रिप मात्रा: 2 वर्ष (9-34 ली.), 4 वर्ष (24-74 ली.), 8 वर्ष (65-188 ली.), 10+ वर्ष (82-235 लीटर/दिन)।",
                    "mr": "ठिबक मात्रा: २ रे वर्ष (९-३४ ली.), ४ थे वर्ष (२४-७४ ली.), ८ वे वर्ष (६५-१८८ ली.), १०+ वर्षे (८२-२३५ लिटर/दिवस).",
                },
            },
            {
                "day_start": 181,
                "day_end": 300,
                "stage": {"en": "Pest Scouting & Fruit Drop Control", "hi": "कीट नियंत्रण व फल गिरना रोकथाम", "mr": "कीड नियंत्रण व फळगळ प्रतिबंध"},
                "task": {
                    "en": "Spray Acetamiprid (0.2g/L) for Citrus Blackfly (Kolshi) and Psylla. For Rust Mites (Lalya on Mrig bahar), spray Fenazaquin 10% EC (4ml/L) + Wettable Sulphur (3g/L). To prevent pre-harvest fruit drop, spray 2,4-D or GA3 (15ppm) + Urea 1% + Copper Oxychloride (0.3%) in April-May & Sept-Oct.",
                    "hi": "कोलशी (काली मक्खी) व सायला के लिए एसिटामिप्रिड 0.2 ग्राम/ली. छिड़कें। लाल्या (माइट्स) के लिए फेनाजाक्विन 4 मिली/ली. + घुलनशील गंधक 3 ग्राम/ली. छिड़कें। फल गिरने से रोकने हेतु 2,4-D या GA3 (15ppm) + 1% यूरिया + कॉपर ऑक्सीक्लोराइड (0.3%) छिड़कें।",
                    "mr": "काळी माशी (कोलशी) व सायलासाठी ॲसिटामिप्रिड ०.२ ग्रॅम/ली. फवारा. लाल्या रोगासाठी फेनाझाक्विन ४ मिली/ली. + गंधक ३ ग्रॅम/ली. फवारा. फळगळ रोखण्यासाठी २,४-D किंवा GA3 (१५ ppm) + १% युरिया + कॉपर ऑक्सिक्लोराईड (०.३%) फवारा.",
                },
                "water_advice": {
                    "en": "Stress water during rest period (Dec-Jan for Ambia, April-May for Mrig); resume irrigation to induce flowering.",
                    "hi": "बहार पकड़ने के लिए विश्राम काल में पानी का तनाव दें; फिर फूल आने के लिए हल्की सिंचाई शुरू करें।",
                    "mr": "बहार धरण्यासाठी विश्रांती काळात पाण्याचा ताण द्या; नंतर मोहर येण्यासाठी हलके पाणी सुरू करा.",
                },
            },
            {
                "day_start": 301,
                "day_end": 365,
                "stage": {"en": "Selective Harvest & Cold Storage", "hi": "तुड़ाई, वैक्सिंग व भंडारण", "mr": "काढणी, वॅक्सिंग व शीतगृह"},
                "task": {
                    "en": "Harvest when 3/4th skin turns yellow (TSS:Acidity ratio >= 14). Do not pull fruits; cut with clippers. Dip fruits in Difenoconazole (2ml/L) for 5 mins to prevent post-harvest rotting. Store at 6-7°C and 90-95% humidity for up to 45 days.",
                    "hi": "जब 3/4 छिलका पीला हो जाए तो कटर से काटें। तुड़ाई बाद सड़न रोकने के लिए डिफेनोकोनाजोल (2 मिली/ली.) में 5 मिनट डुबोएं। 6-7°C तापमान और 90-95% नमी पर 45 दिन तक सुरक्षित रखें।",
                    "mr": "३/४ फळ पिवळे झाल्यावर देठाजवळून कटरने कापा. सड रोखण्यासाठी डायफेनोकोनाझोल (२ मिली/ली.) द्रावणात ५ मिनिटे बुडवा. ६-७°C तापमान व ९०-९५% आर्द्रतेत ४५ दिवस साठवा.",
                },
                "water_advice": {
                    "en": "Maintain consistent soil moisture to prevent fruit cracking.",
                    "hi": "फल फटने से बचाने के लिए एकसमान नमी रखें।",
                    "mr": "फळे तडकणे टाळण्यासाठी जमिनीत समतोल ओलावा ठेवा.",
                },
            },
        ],
        "pests_and_diseases": [
            {
                "name": {"en": "Citrus Blackfly / Kolshi (Aleurocanthus woglumi)", "hi": "संतरे की काली मक्खी (कोलशी)", "mr": "संत्र्यावरील काळी माशी (कोलशी)"},
                "symptoms": {
                    "en": "Nymphs suck sap from tender flush and excrete sticky honeydew, causing thick black sooty mould over leaves, reducing photosynthesis and fruit size.",
                    "hi": "काली मक्खी के बच्चे पत्तियों से रस चूसते हैं और चिपचिपा तरल छोड़ते हैं, जिससे पूरी पत्तियों पर काली फफूंद (कोलशी) जम जाती है और पेड़ कमजोर हो जाता है।",
                    "mr": "पिल्ले पानातून रस शोषतात व गोड डिंक सोडतात, ज्यामुळे संपूर्ण झाडावर काजळी (कोलशी) चढून प्रकाशसंश्लेषण थांबते.",
                },
                "organic_remedy": {
                    "en": "Spray Neem oil 1500 ppm @ 3ml/L or fish oil rosin soap (25g/L). Wash sooty mould with Maida (50g/L) boiled starch solution.",
                    "hi": "नीम तेल 1500 ppm 3 मिली/ली. छिड़कें। काली फफूंद धोने के लिए 1 किग्रा मैदा 20 लीटर पानी में उबालकर छिड़कें।",
                    "mr": "कडुलिंब तेल १५०० ppm ३ मिली/ली. फवारा. काजळी घालवण्यासाठी १ किलो मैदा २० लिटर पाण्यात उकळून फवारा.",
                },
                "chemical_remedy": {
                    "en": "Spray Acetamiprid 20% SP @ 0.2g/L or Thiamethoxam 25% WG @ 0.25g/L in 2nd week of July & Dec directed at underside of leaves.",
                    "hi": "जुलाई के दूसरे हफ्ते और दिसंबर में एसिटामिप्रिड 0.2 ग्राम/ली. या थायमेथोक्सम 0.25 ग्राम/ली. पत्तियों की निचली सतह पर छिड़कें।",
                    "mr": "जुलैच्या दुसऱ्या आठवड्यात व डिसेंबरमध्ये ॲसिटामिप्रिड ०.२ ग्रॅम/ली. किंवा थायमेथोक्साम ०.२५ ग्रॅम/ली. पानाच्या खाली फवारा.",
                },
            },
            {
                "name": {"en": "Gummosis & Foot Rot (Phytophthora nicotianae)", "hi": "गमोसिस व जड़ सड़न (डिंक्या)", "mr": "डिंक्या व मूळकूज (गमोसिस)"},
                "symptoms": {
                    "en": "Profuse gum oozing from cracked bark on tree trunk near soil line, rotting of bark, yellowing and die-back of branches.",
                    "hi": "जमीन की सतह के पास मुख्य तने से गोंद (डिंक) निकलना, छाल का सड़ना और शाखाओं का सूखना।",
                    "mr": "जमिनीलगतच्या खोडातून डिंक वाहणे, साल सडणे, पाने पिवळी पडून झाडाची फांदी सुकणे.",
                },
                "organic_remedy": {
                    "en": "Scrape gum wound with knife, apply Bordeaux paste (1:1:10) on trunk up to 2.5 ft twice a year (May & Oct). Avoid flood irrigation.",
                    "hi": "घाव को चाकू से साफ कर साल में दो बार (मई व अक्टूबर) 2.5 फीट ऊंचाई तक बोर्डो पेस्ट (1:1:10) लगाएं। जलभराव से बचें।",
                    "mr": "चाकूने जखम तासून वर्षातून दोनदा (मे व ऑक्टोबर) खोडावर २.५ फुटांपर्यंत बोर्डो पेस्ट लावा. पाणी साचू देऊ नका.",
                },
                "chemical_remedy": {
                    "en": "Soil drenching and tree spray with Metalaxyl MZ 72 @ 2.75g/L or Fosetyl-Al @ 2.5g/L in May-June and repeat after 40 days.",
                    "hi": "मेटालेक्सिल MZ 72 2.75 ग्राम/ली. या फॉसेटाइल-अल 2.5 ग्राम/ली. का घोल तने व जड़ों के पास मिट्टी में डालें (मई-जून)।",
                    "mr": "मेटालेक्सिल MZ ७२ २.७५ ग्रॅम/ली. किंवा फॉसेटाईल-अल २.५ ग्रॅम/ली. द्रावण मे-जूनमध्ये झाडावर व मुळांत आळवणी करा.",
                },
            },
            {
                "name": {"en": "Citrus Canker (Xanthomonas axonopodis)", "hi": "संतरे का कैंकर रोग", "mr": "संत्र्यावरील खैऱ्या (कँकर)"},
                "symptoms": {
                    "en": "Raised corky brown crater-like lesions with yellow halos on leaves, twigs and fruits, causing premature fruit drop.",
                    "hi": "पत्तियों, टहनियों और फलों पर उभरे हुए भूरे खुरदरे धब्बे जिनके चारों ओर पीला घेरा होता है, फल समय से पहले गिर जाना।",
                    "mr": "पानांवर, फांद्यांवर आणि फळांवर खरखरीत तपकिरी उठावदार डाग, ज्यामुळे फळगळ होते.",
                },
                "organic_remedy": {
                    "en": "Prune and burn infected twigs before monsoon. Spray Copper Hydroxide @ 2g/L.",
                    "hi": "मानसून से पहले संक्रमित टहनियां काटकर जलाएं। कॉपर हाइड्रॉक्साइड 2 ग्राम/ली. छिड़कें।",
                    "mr": "पावसाळ्यापूर्वी रोगट फांद्या छाटून नष्ट करा. कॉपर हायड्रॉक्साईड २ ग्रॅम/ली. फवारा.",
                },
                "chemical_remedy": {
                    "en": "Spray Copper Oxychloride 0.3% (3g/L) + Streptocycline @ 100 ppm (1g in 10L water) at monthly intervals after monsoon onset.",
                    "hi": "कॉपर ऑक्सीक्लोराइड 3 ग्राम/ली. + स्ट्रेप्टोसाइक्लिन 1 ग्राम/10 लीटर पानी में मिलाकर मासिक अंतराल पर छिड़कें।",
                    "mr": "कॉपर ऑक्सिक्लोराईड ३ ग्रॅम/ली. + स्ट्रेप्टोसायक्लिन १ ग्रॅम/१० ली. पाण्यात मिसळून फवारा.",
                },
            },
        ],
    },

    "wheat": {
        "id": "wheat",
        "category": "cereals",
        "names": {"en": "Wheat", "hi": "गेहूं", "mr": "गहू"},
        "scientific_name": "Triticum aestivum",
        "season": {"en": "Rabi", "hi": "रबी", "mr": "रब्बी"},
        "duration_days": 120,
        "optimal_temp": "12°C - 25°C",
        "rainfall_mm": "350 - 600 mm",
        "soil": {
            "en": "Well-drained loam or clay-loam soils (pH 6.0 - 7.5)",
            "hi": "उत्तम जल निकासी वाली दोमट या मटियार दोमट मिट्टी (pH 6.0 - 7.5)",
            "mr": "पाण्याचा चांगला निचरा होणारी पोयटा किंवा मध्यम काळी जमीन (pH ६.० - ७.५)",
        },
        "sowing_months": {
            "en": "October - November",
            "hi": "अक्टूबर - नवंबर",
            "mr": "ऑक्टोबर - नोव्हेंबर",
        },
        "expected_yield_per_acre": "18 - 24 Quintals",
        "fertilizer_per_acre_kg": {
            "urea": 90,
            "dap": 55,
            "mop": 25,
            "zinc_sulphate": 8,
            "fym_tonnes": 3,
        },
        "growth_stages": [
            {
                "day_start": 0,
                "day_end": 20,
                "stage": {"en": "Crown Root Initiation (CRI)", "hi": "मुकुट जड़ अवस्था (CRI)", "mr": "मुकुट मुळे फुटणे (CRI)"},
                "task": {
                    "en": "Seed treatment with Azotobacter + PSB (10g/kg) or Carboxin 75% WP. Apply basal 55kg DAP + 25kg MOP + 8kg Zinc per acre. Give 1st irrigation at Day 20-25 (most critical stage).",
                    "hi": "एजोटोबैक्टर + PSB से बीज उपचार। 55 किग्रा DAP + 25 किग्रा MOP + 8 किग्रा जिंक बेसल दें। 20-25 दिन पर पहली अत्यंत महत्वपूर्ण सिंचाई करें।",
                    "mr": "ॲझोटोबॅक्टर + PSB बीज प्रक्रिया. ५५ किग्रॅ DAP + २५ किग्रॅ MOP + ८ किग्रॅ झिंक बेसल द्या. २०-२५ दिवसांनी पहिली महत्त्वाची पाणीपाळी द्या.",
                },
                "water_advice": {
                    "en": "First irrigation at CRI stage (21 days) is vital for root anchorage.",
                    "hi": "CRI अवस्था में पहली सिंचाई जड़ों के विकास के लिए अनिवार्य है।",
                    "mr": "CRI अवस्थेत पहिली पाणीपाळी मुळांच्या वाढीसाठी अत्यंत गरजेची आहे.",
                },
            },
            {
                "day_start": 21,
                "day_end": 45,
                "stage": {"en": "Tillering & Jointing", "hi": "कल्ले फूटना व गांठ बनना", "mr": "फुटवे व कांडी धरणे"},
                "task": {
                    "en": "Apply 1st top dressing: 45kg Urea per acre after first irrigation. Spray 2,4-D (Fernoxone 80% SS @ 1kg/ha) for broadleaf weed control.",
                    "hi": "पहली सिंचाई के बाद 45 किग्रा यूरिया प्रति एकड़ दें। चौड़ी पत्ती के खरपतवार के लिए 2,4-D (1 किग्रा/हेक्टेयर) का छिड़काव करें।",
                    "mr": "पहिल्या पाण्यानंतर ४५ किग्रॅ युरिया प्रति एकर टाका. रुंद पानाच्या तणासाठी २,४-D फवारा.",
                },
                "water_advice": {
                    "en": "Provide second irrigation at active tillering (40-45 days).",
                    "hi": "40-45 दिन पर दूसरी सिंचाई करें।",
                    "mr": "४०-४५ दिवसांनी दुसरी पाणीपाळी द्या.",
                },
            },
            {
                "day_start": 46,
                "day_end": 75,
                "stage": {"en": "Booting & Heading", "hi": "गोभ व बाली निकलना", "mr": "पोंगा अवस्था व लोंबी बाहेर पडणे"},
                "task": {
                    "en": "Apply 2nd top dressing: 45kg Urea. Spray NPK 19:19:19 (5g/L) to boost earhead size.",
                    "hi": "दूसरा छिड़काव: 45 किग्रा यूरिया। बालियों के अच्छे विकास के लिए NPK 19:19:19 (5 ग्राम/ली.) छिड़कें।",
                    "mr": "दुसरा हप्ता: ४५ किग्रॅ युरिया. लोंब्यांच्या वाढीसाठी NPK १९:१९:१९ (५ ग्रॅम/ली.) फवारा.",
                },
                "water_advice": {
                    "en": "Third irrigation at late boot stage.",
                    "hi": "गोभ अवस्था में तीसरी सिंचाई करें।",
                    "mr": "पोंगा अवस्थेत तिसरी पाणीपाळी द्या.",
                },
            },
            {
                "day_start": 76,
                "day_end": 100,
                "stage": {"en": "Flowering & Milking", "hi": "फूल आना व दुग्ध अवस्था", "mr": "फुलधारणा व दाणे भरणे"},
                "task": {
                    "en": "Spray 0:0:50 (5g/L) + Boron (1g/L) for shining, heavy grains. Check for Yellow/Brown Rust.",
                    "hi": "चमकदार और भारी दानों के लिए 0:0:50 (5 ग्राम/ली.) + बोरॉन (1 ग्राम/ली.) का छिड़काव करें। रतुआ रोग की जांच करें।",
                    "mr": "चमकदार दाण्यांसाठी ०:०:५० (५ ग्रॅम/ली.) + बोरॉन (१ ग्रॅम/ली.) फवारा. तांबेरा रोगाची तपासणी करा.",
                },
                "water_advice": {
                    "en": "Irrigate lightly on calm days to prevent lodging.",
                    "hi": "हवा शांत होने पर हल्की सिंचाई करें ताकि फसल गिरे नहीं।",
                    "mr": "वारा शांत असताना हलके पाणी द्या जेणेकरून पीक लोळणार नाही.",
                },
            },
            {
                "day_start": 101,
                "day_end": 120,
                "stage": {"en": "Dough & Ripening", "hi": "दाना पकना व कटाई", "mr": "दाणे पक्व होणे व कापणी"},
                "task": {
                    "en": "Stop irrigation completely. Harvest when straw turns golden yellow and moisture is below 12%.",
                    "hi": "सिंचाई पूरी तरह बंद करें। जब पौधा सुनहरा पीला हो जाए और नमी 12% से कम हो तो कटाई करें।",
                    "mr": "पाणी देणे पूर्ण बंद करा. झाड पिवळे सोनेरी झाल्यावर आणि ओलावा १२% पेक्षा कमी असताना कापणी करा.",
                },
                "water_advice": {
                    "en": "No irrigation during dough stage.",
                    "hi": "पकने के समय सिंचाई न करें।",
                    "mr": "पक्वतेच्या काळात पाणी देऊ नका.",
                },
            },
        ],
        "pests_and_diseases": [
            {
                "name": {"en": "Yellow / Stripe Rust", "hi": "पीला रतुआ", "mr": "पिवळा तांबेरा"},
                "symptoms": {
                    "en": "Yellow stripes of powder/pustules running along leaf veins.",
                    "hi": "पत्तियों की नसों के समानांतर पीले रंग की धारियां व पाउडर के दाने।",
                    "mr": "पानांच्या शिरांवर पिवळ्या रंगाच्या पट्ट्या आणि भुकटीचे ठिपके दिसणे.",
                },
                "organic_remedy": {
                    "en": "Spray Cow urine (10%) + Fermented buttermilk (5%).",
                    "hi": "गोमूत्र (10%) + खट्टी छाछ (5%) का छिड़काव करें।",
                    "mr": "गोमूत्र (१०%) + आंबट ताक (५%) फवारा.",
                },
                "chemical_remedy": {
                    "en": "Spray Propiconazole 25% EC (Tilt) @ 1ml/L at first appearance.",
                    "hi": "लक्षण दिखते ही प्रोपिकोनाजोल 25% EC (टिल्ट) 1 मिली/ली. का छिड़काव करें।",
                    "mr": "लक्षणे दिसताच प्रोपिकोनाझोल २५% EC (टिल्ट) १ मिली/ली. फवारा.",
                },
            },
        ],
    },

    "cotton": {
        "id": "cotton",
        "category": "cash_crops",
        "names": {"en": "Cotton", "hi": "कपास", "mr": "कापूस"},
        "scientific_name": "Gossypium hirsutum",
        "season": {"en": "Kharif", "hi": "खरीफ", "mr": "खरीप"},
        "duration_days": 160,
        "optimal_temp": "21°C - 35°C",
        "rainfall_mm": "600 - 1000 mm",
        "soil": {
            "en": "Deep black clay soil (Regur) or fertile alluvial loam (pH 6.5 - 8.0)",
            "hi": "गहरी काली मिट्टी (रेगुर) या उपजाऊ जलोढ़ दोमट (pH 6.5 - 8.0)",
            "mr": "खोल काळी कसदार जमीन (रेगूर) किंवा गाळाची पोयटा जमीन (pH ६.५ - ८.०)",
        },
        "sowing_months": {
            "en": "May - June (Pre-monsoon / Monsoon onset)",
            "hi": "मई - जून",
            "mr": "मे - जून",
        },
        "expected_yield_per_acre": "10 - 15 Quintals",
        "fertilizer_per_acre_kg": {
            "urea": 110,
            "dap": 60,
            "mop": 40,
            "magnesium_sulphate": 10,
            "fym_tonnes": 5,
        },
        "growth_stages": [
            {
                "day_start": 0,
                "day_end": 30,
                "stage": {"en": "Emergence & Seedling", "hi": "अंकुरण व प्रारंभिक वृद्धि", "mr": "उगवण व रोप अवस्था"},
                "task": {
                    "en": "Seed treatment with Imidacloprid (5g/kg). Apply basal dose 60kg DAP + 20kg MOP per acre. Intercrop with Black gram / Green gram (6:2).",
                    "hi": "इमिडाक्लोप्रिड से बीज उपचार। 60 किग्रा DAP + 20 किग्रा MOP बेसल दें। उड़द/मूंग के साथ अंतरफसल (6:2) लगाएं।",
                    "mr": "इमिडाक्लोप्रिडने बीज प्रक्रिया. ६० किग्रॅ DAP + २० किग्रॅ MOP बेसल द्या. उडीद/मुगासोबत आंतरपीक (६:२) घ्या.",
                },
                "water_advice": {
                    "en": "Avoid waterlogging; maintain optimal soil moisture.",
                    "hi": "जलभराव से बचें; मिट्टी में पर्याप्त नमी रखें।",
                    "mr": "पाणी साचू देऊ नका; जमिनीत वाफसा ठेवा.",
                },
            },
            {
                "day_start": 31,
                "day_end": 60,
                "stage": {"en": "Square Formation & Branching", "hi": "शाखाएं व कलियां (स्क्वायर) बनना", "mr": "फांद्या व पाते लागणे"},
                "task": {
                    "en": "Apply 1st top dressing: 45kg Urea + 10kg Magnesium Sulphate per acre. Use tractor-operated cotton weeder. Spray Neem oil (3ml/L) against sucking pests (Thrips, Aphids, Jassids, Whitefly ETL: 5-10/leaf).",
                    "hi": "पहला टॉप ड्रेसिंग: 45 किग्रा यूरिया + 10 किग्रा मैग्नीशियम सल्फेट। रस चूसक कीटों (थ्रिप्स, माहू, हरा तेला, सफेद मक्खी) के लिए नीम तेल (3 मिली/ली.) छिड़कें।",
                    "mr": "पहिला हप्ता: ४५ किग्रॅ युरिया + १० किग्रॅ मॅग्नेशियम सल्फेट प्रति एकर. रसशोषक किडींसाठी कडुलिंब तेल (३ मिली/ली.) फवारा.",
                },
                "water_advice": {
                    "en": "Irrigate at 12-15 day intervals in absence of rain. Drip irrigation increases yield by 88%.",
                    "hi": "बारिश न होने पर 12-15 दिनों में सिंचाई करें। ड्रिप से पैदावार 88% बढ़ती है।",
                    "mr": "पाऊस नसल्यास १२-१५ दिवसांनी पाणी द्या. ठिबकमुळे उत्पादन ८८% वाढते.",
                },
            },
            {
                "day_start": 61,
                "day_end": 100,
                "stage": {"en": "Flowering & Boll Formation", "hi": "फूल आना व गूलर (टिंडे) बनना", "mr": "फुलधारणा व बोंड धरणे"},
                "task": {
                    "en": "Apply 2nd top dressing: 40kg Urea + 20kg MOP per acre. Spray Planofix (0.25ml/L) or 13:00:45 (10g/L) to prevent square/boll dropping. Install Pheromone traps @ 8-10/acre for Pink Bollworm.",
                    "hi": "दूसरा टॉप ड्रेसिंग: 40 किग्रा यूरिया + 20 किग्रा MOP। फूल-टिंडे झड़ने से रोकने हेतु प्लानोफिक्स या 13:00:45 छिड़कें। गुलाबी सुंडी के लिए 8-10 फेरोमोन ट्रैप लगाएं।",
                    "mr": "दुसरा हप्ता: ४० किग्रॅ युरिया + २० किग्रॅ MOP प्रति एकर. पातेगळ रोखण्यासाठी प्लॅनोफिक्स किंवा १३:००:४५ फवारा. गुलाबी बोंडअळीसाठी ८-१० कामगंध सापळे लावा.",
                },
                "water_advice": {
                    "en": "Critical moisture stage; water stress causes severe boll shedding.",
                    "hi": "सबसे महत्वपूर्ण नमी अवस्था; पानी की कमी से टिंडे गिर जाते हैं।",
                    "mr": "पाण्याचा अतिशय संवेदनशील काळ; टंचाई झाल्यास बोंडगळ होते.",
                },
            },
            {
                "day_start": 101,
                "day_end": 160,
                "stage": {"en": "Boll Bursting & Picking", "hi": "टिंडे खिलना व चुनाई", "mr": "बोंडे फुटणे व वेचणी"},
                "task": {
                    "en": "Pick fully opened dry cotton in clean cotton bags. Use tractor cotton stalk puller after final harvest. Avoid burning stalks; shred into soil.",
                    "hi": "धूप के समय सूखे खिले कपास की साफ सूती थैलियों में चुनाई करें। कटाई बाद डंठल उखाड़कर मिट्टी में मिलाएं।",
                    "mr": "दुपारच्या उन्हात पूर्ण उमललेला कापूस स्वच्छ सुती पिशवीत वेचा. काड्या जाळू नका; जमिनीत गाडा.",
                },
                "water_advice": {
                    "en": "Stop irrigation completely.",
                    "hi": "सिंचाई पूरी तरह बंद रखें।",
                    "mr": "पाणी पूर्णपणे बंद ठेवा.",
                },
            },
        ],
        "pests_and_diseases": [
            {
                "name": {"en": "Pink Bollworm (PBW)", "hi": "गुलाबी सुंडी", "mr": "गुलाबी बोंडअळी"},
                "symptoms": {
                    "en": "Rosetted flowers, bore holes on bolls sealed with excreta, damaged lint and seeds.",
                    "hi": "गुलाब जैसे मुड़े हुए फूल, टिंडों पर छेद और अंदर रुई व बीज का सड़ना।",
                    "mr": "गुलाबासारखी बंद फुले (रोझेट फ्लॉवर), बोंडांवर छिद्रे आणि आतील सरकीचे नुकसान.",
                },
                "organic_remedy": {
                    "en": "Pheromone traps @ 8-10/acre. Spray Beauveria bassiana @ 5g/L or Neem oil 10000 ppm @ 2ml/L.",
                    "hi": "8-10 फेरोमोन ट्रैप/एकड़ लगाएं। ब्युवेरिया बासियाना 5 ग्राम/ली. या नीम तेल 10000 ppm 2 मिली/ली. छिड़कें।",
                    "mr": "८-१० कामगंध सापळे लावा. बिव्हेरिया बॅसियाना ५ ग्रॅम/ली. किंवा कडुलिंब तेल १०००० ppm २ मिली/ली. फवारा.",
                },
                "chemical_remedy": {
                    "en": "Spray Profenofos 50% EC @ 2ml/L or Emamectin Benzoate 5% SG @ 0.5g/L.",
                    "hi": "प्रोफेनोफॉस 50% EC 2 मिली/ली. या एमामेक्टिन बेंजोएट 5% SG 0.5 ग्राम/ली. छिड़कें।",
                    "mr": "प्रोफेनोफॉस ५०% EC २ मिली/ली. किंवा इमामेक्टिन बेंझोएट ५% SG ०.५ ग्रॅम/ली. फवारा.",
                },
            },
        ],
    },

    "sugarcane": {
        "id": "sugarcane",
        "category": "cash_crops",
        "names": {"en": "Sugarcane", "hi": "गन्ना", "mr": "ऊस"},
        "scientific_name": "Saccharum officinarum",
        "season": {"en": "Annual (Adsali / Pre-seasonal / Suru)", "hi": "वार्षिक (अडसाली / पूर्व मौसमी / सुरू)", "mr": "वार्षिक (अडसाली / पूर्वहंगामी / सुरू)"},
        "duration_days": 360,
        "optimal_temp": "20°C - 38°C",
        "rainfall_mm": "1500 - 2500 mm",
        "soil": {
            "en": "Deep rich well-drained loam or medium black soil (pH 6.5 - 7.5)",
            "hi": "गहरी उपजाऊ दोमट या मध्यम काली मिट्टी (pH 6.5 - 7.5)",
            "mr": "खोल कसदार, पाण्याचा उत्तम निचरा होणारी पोयट्याची किंवा मध्यम काळी जमीन (pH ६.५ - ७.५)",
        },
        "sowing_months": {
            "en": "July - Aug (Adsali), Oct - Nov (Pre-season), Jan - Feb (Suru)",
            "hi": "जुलाई - अगस्त (अडसाली), अक्टूबर - नवंबर (पूर्व मौसमी), जनवरी - फरवरी (सुरू)",
            "mr": "जुलै - ऑगस्ट (अडसाली), ऑक्टोबर - नोव्हेंबर (पूर्वहंगामी), जानेवारी - फेब्रुवारी (सुरू)",
        },
        "expected_yield_per_acre": "40 - 65 Tonnes (Drip yield increase: 133%)",
        "fertilizer_per_acre_kg": {
            "urea": 220,
            "dap": 100,
            "mop": 80,
            "micronutrient_mix": 15,
            "fym_tonnes": 8,
        },
        "growth_stages": [
            {
                "day_start": 0,
                "day_end": 45,
                "stage": {"en": "Planting & Basal Dose", "hi": "बुवाई व आधार खाद", "mr": "लागवड व बेसल डोस"},
                "task": {
                    "en": "Plough to 45cm depth. Make ridges & furrows at 80cm spacing. Apply 375kg SSP in furrows. Select 75,000 two-budded setts/ha. Treat setts for 10 mins with Thiamine + 2.5kg Urea + 2.5kg Lime in 250L water or Trichoderma. Spray Atrataf (2.5kg/ha) on Day 3 for weed control. Spread trash (15cm) on Day 5.",
                    "hi": "45 सेमी गहरी जुताई। 80 सेमी पर मेड़ व नालियां बनाएं। 375 किग्रा सुपर फास्फेट डालें। दो आंख वाले गूलों का उपचार करें। तीसरे दिन खरपतवार के लिए एट्राटाफ 2.5 किग्रा/हे. छिड़कें। 5वें दिन 15 सेमी गन्ने की पत्ती की मल्चिंग करें।",
                    "mr": "४५ सेमी खोल नांगरट. ८० सेमी अंतरावर सऱ्या पाडा. ३७५ किग्रॅ SSP सऱ्यांत टाका. दोन डोळ्यांच्या कांड्यांची प्रक्रिया करा. ३ ऱ्या दिवशी तण नियंत्रणासाठी ॲट्राटाफ फवारा. ५ व्या दिवशी सऱ्यांवर पाचट पसरा.",
                },
                "water_advice": {
                    "en": "Irrigate once in 7-10 days.",
                    "hi": "7-10 दिन में हल्की सिंचाई करें।",
                    "mr": "७-१० दिवसांनी पाणी द्या.",
                },
            },
            {
                "day_start": 46,
                "day_end": 120,
                "stage": {"en": "Tillering & Biofertilizers", "hi": "कल्ले फूटना व बायोफर्टिलाइजर", "mr": "फुटवे फुटणे व बाळबांधणी"},
                "task": {
                    "en": "On Day 30 & 60: Apply 5kg Azospirillum + 5kg Phosphobacteria with 250kg FYM at base. At Day 45: Hand weeding + 110kg N + 60kg K + 35kg neem cake/ha. At Day 90: Earthing up. During drought: Spray Urea 2.5% + Potassium Chloride 2.5%.",
                    "hi": "30वें व 60वें दिन: 5 किग्रा एजोस्पाइरिलम + 5 किग्रा फास्फोबैक्टीरिया 250 किग्रा गोबर खाद में मिलाकर डालें। 45वें दिन 110 किग्रा N + 60 किग्रा पोटाश + 35 किग्रा नीम खली डालें। 90वें दिन मिट्टी चढ़ाएं। सूखे में 2.5% यूरिया + 2.5% पोटाश छिड़कें।",
                    "mr": "३० व ६० व्या दिवशी: ५ किग्रॅ ॲझोस्पिरीलम + ५ किग्रॅ फॉस्फोबॅक्टेरिया २५० किग्रॅ शेणखतात मिसळून द्या. ४५ व्या दिवशी खुरपणी + खताचा डोस द्या. ९० व्या दिवशी बाळबांधणी करा.",
                },
                "water_advice": {
                    "en": "Regular irrigation every 7-10 days; peak tillering phase.",
                    "hi": "हर 7-10 दिन में सिंचाई करें; कल्ले निकलने का मुख्य समय।",
                    "mr": "दर ७-१० दिवसांनी पाणी द्या.",
                },
            },
            {
                "day_start": 121,
                "day_end": 270,
                "stage": {"en": "Grand Growth & Detrashing", "hi": "मुख्य बढ़वार, पत्ती छंटाई व बंधाई", "mr": "पाचट काढणे, मोठी बांधणी व कीड नियंत्रण"},
                "task": {
                    "en": "At Day 150 & 180: Detrash dry lower leaves. Release Trichogramma parasites @ 5cc/ha once in 15 days for internode borer. At Day 210: Tie lodged canes. At Day 225: Spray Acetamiprid (2ml/L) for mealy bugs/scales. At Day 260: Spray Emamectin benzoate (50g/L) for pyrilla.",
                    "hi": "150वें व 180वें दिन: निचली सूखी पत्तियां हटाएं (डीट्रैशिंग)। तना छेदक के लिए ट्राइकोग्रामा 5cc/हे. छोड़ें। 210वें दिन बंधाई करें। मिलीबग व शल्क कीट के लिए एसिटामिप्रिड 2 मिली/ली. छिड़कें।",
                    "mr": "१५० व १८० व्या दिवशी: खालचे वाळलेले पाचट काढा. खोडकिडीसाठी ट्रायकोगामा परोपजीवी कीटक सोडा. २१० व्या दिवशी ऊस बांधणी करा. पिठ्या ढेकूणासाठी ॲसिटामिप्रिड फवारा.",
                },
                "water_advice": {
                    "en": "Peak water requirement. Irrigate every 7 days (surface) or daily drip.",
                    "hi": "पानी की सर्वाधिक आवश्यकता। हर 7 दिन में सिंचाई करें।",
                    "mr": "दर ७ दिवसांनी पाणी द्या.",
                },
            },
            {
                "day_start": 271,
                "day_end": 360,
                "stage": {"en": "Ripening & Harvesting", "hi": "शर्करा संचय व कटाई", "mr": "पक्वता व ऊसतोड"},
                "task": {
                    "en": "Irrigate once in 15 days. Stop irrigation 15 days before harvest. Cut canes at ground level with sharp sickles. Send clean canes without roots/trash to sugar mill. Manage ratoon crop with stubble shaving and 375kg Superphosphate + 135kg N + 35kg neem cake.",
                    "hi": "कटाई से 15 दिन पहले पानी पूरी तरह बंद करें। जमीन की सतह से सटाकर कटाई करें। खोड़वा (रटून) फसल में ठूंठों की छंटाई कर 375 किग्रा सुपर फास्फेट + 135 किग्रा N + 35 किग्रा नीम खली डालें।",
                    "mr": "तोडणीपूर्वी १५ दिवस आधी पाणी बंद करा. जमिनीलगत तोडणी करा. खोडवा पिकासाठी बुडके छाटून ३७५ किग्रॅ सुपर फॉस्फेट + १३५ किग्रॅ N + ३५ किग्रॅ निंबोळी पेंड द्या.",
                },
                "water_advice": {
                    "en": "Stop irrigation 15 days before harvest.",
                    "hi": "कटाई से 15 दिन पहले सिंचाई रोक दें।",
                    "mr": "ऊसतोडीच्या १५ दिवस आधी पाणी पूर्ण बंद करा.",
                },
            },
        ],
        "pests_and_diseases": [
            {
                "name": {"en": "Early Shoot Borer", "hi": "अग्र प्ररोह छेदक", "mr": "खोडकीड"},
                "symptoms": {
                    "en": "Dead heart in young shoots (up to 100 days), foul odor when pulled.",
                    "hi": "शुरुआती 100 दिनों में मृत कल्ले (डेड हार्ट) और खींचने पर दुर्गंध आना।",
                    "mr": "सुरुवातीच्या १०० दिवसांत पोंगा सुकणे आणि ओढल्यास दुर्गंधी येणे.",
                },
                "organic_remedy": {
                    "en": "Soil mulching with trash (15cm) + Release Trichogramma chilonis @ 2.5 cc/acre.",
                    "hi": "गन्ने की सूखी पत्ती की मल्चिंग + ट्राइकोग्रामा चिलोनीस 2.5 सीसी/एकड़ छोड़ें।",
                    "mr": "पाचटाचे आच्छादन + ट्रायकोगामा चिलोनीस २.५ सीसी/एकर सोडा.",
                },
                "chemical_remedy": {
                    "en": "Apply Sulphur on setts or spray Chlorantraniliprole 18.5% SC @ 150ml/acre.",
                    "hi": "गूलों पर सल्फर डालें या क्लोरेंट्रानिलिप्रोल 18.5% SC 150 मिली/एकड़ मिट्टी में डालें।",
                    "mr": "कांड्यांवर गंधक टाका किंवा क्लोरँट्रानिलीप्रोल १८.५% SC १५० मिली/एकर आळवणी करा.",
                },
            },
            {
                "name": {"en": "Red Rot (Fungal)", "hi": "गन्ने का लाल सड़न (रेड रॉट)", "mr": "तांब्या किंवा लाल कूज"},
                "symptoms": {
                    "en": "Yellowing of crown leaves, internal split stalk showing blood red color with white cross patches and alcoholic smell.",
                    "hi": "ऊपरी पत्तियों का पीला पड़कर सूखना, तना चीरने पर अंदर सफेद धब्बों युक्त गहरा लाल रंग दिखना।",
                    "mr": "वरची पाने पिवळी पडून वाळणे, ऊस चिरल्यावर आतून पांढऱ्या पट्ट्यांसह लाल भडक दिसणे व दारूसारखा वास येणे.",
                },
                "organic_remedy": {
                    "en": "Hot water seed treatment at 50°C for 2 hours + Trichoderma harzianum @ 2kg/acre in FYM.",
                    "hi": "50°C गर्म पानी में 2 घंटे बीज उपचार + ट्राइकोडर्मा हरजियानम 2 किग्रा/एकड़ गोबर खाद में मिलाकर डालें।",
                    "mr": "५०°C गरम पाण्यात २ तास बेणे प्रक्रिया + ट्रायकोडर्मा हरझियानम २ किग्रॅ/एकर शेणखतातून द्या.",
                },
                "chemical_remedy": {
                    "en": "Dip setts in Carbendazim 50% WP @ 1g/L for 15 minutes before planting.",
                    "hi": "बुवाई पूर्व गूलों को कार्बेंडाजिम 50% WP (1 ग्राम/ली.) के घोल में 15 मिनट डुबोएं।",
                    "mr": "लागवडीपूर्वी बेणे कार्बेंडाझिम ५०% WP (१ ग्रॅम/ली.) द्रावणात १५ मिनिटे बुडवून घ्या.",
                },
            },
        ],
    },

    "soybean": {
        "id": "soybean",
        "category": "pulses_oilseeds",
        "names": {"en": "Soybean", "hi": "सोयाबीन", "mr": "सोयाबीन"},
        "scientific_name": "Glycine max",
        "season": {"en": "Kharif", "hi": "खरीफ", "mr": "खरीप"},
        "duration_days": 95,
        "optimal_temp": "20°C - 32°C",
        "rainfall_mm": "600 - 800 mm",
        "soil": {
            "en": "Well-drained fertile clay-loam or medium black soil (pH 6.0 - 7.5)",
            "hi": "अच्छी जल निकासी वाली दोमट या मध्यम काली मिट्टी (pH 6.0 - 7.5)",
            "mr": "पाण्याचा निचरा होणारी कसदार मध्यम ते भारी काळी जमीन (pH ६.० - ७.५)",
        },
        "sowing_months": {
            "en": "June - July (After 75-100mm monsoon rain)",
            "hi": "जून - जुलाई (75-100 मिमी बारिश के बाद)",
            "mr": "जून - जुलै (७५-१०० मिमी पाऊस पडल्यानंतर)",
        },
        "expected_yield_per_acre": "8 - 12 Quintals",
        "fertilizer_per_acre_kg": {
            "urea": 25,
            "dap": 60,
            "mop": 30,
            "sulphur": 10,
            "fym_tonnes": 3,
        },
        "growth_stages": [
            {
                "day_start": 0,
                "day_end": 20,
                "stage": {"en": "Sowing & Seedling", "hi": "बुवाई व अंकुरण", "mr": "पेरणी व उगवण"},
                "task": {
                    "en": "Inoculate seed with Bradyrhizobium + PSB culture. Apply full basal: 25kg Urea + 60kg DAP + 30kg MOP + 10kg Sulphur per acre. Sowing depth 3-4 cm.",
                    "hi": "राइजोबियम + PSB कल्चर से बीज उपचार। पूरा बेसल: 25 किग्रा यूरिया + 60 किग्रा DAP + 30 किग्रा MOP + 10 किग्रा सल्फर डालें।",
                    "mr": "रायझोबियम + PSB जिवाणू संवर्धक प्रक्रिया. संपूर्ण बेसल डोस: २५ किग्रॅ युरिया + ६० किग्रॅ DAP + ३० किग्रॅ MOP + १० किग्रॅ गंधक टाका.",
                },
                "water_advice": {
                    "en": "Ensure sufficient moisture during sowing; avoid water stagnation.",
                    "hi": "बुवाई के समय अच्छी नमी हो; जलभराव न होने दें।",
                    "mr": "पेरणीवेळी जमिनीत पुरेसा ओलावा असावा; पाणी साचू नये.",
                },
            },
            {
                "day_start": 21,
                "day_end": 45,
                "stage": {"en": "Vegetative & Flowering", "hi": "वानस्पतिक बढ़वार व फूल आना", "mr": "वाढ व फुलधारणा"},
                "task": {
                    "en": "Weeding at 20-25 days. Spray 19:19:19 (5g/L) + Boron (1g/L) at onset of flowering. Critical period for weed competition is 45 days.",
                    "hi": "20-25 दिन पर निराई। फूल आते समय 19:19:19 (5 ग्राम/ली.) + बोरॉन (1 ग्राम/ली.) छिड़कें।",
                    "mr": "२०-२५ दिवसांनी खुरपणी. फुलधारणेच्या सुरुवातीला १९:१९:१९ (५ ग्रॅम/ली.) + बोरॉन (१ ग्रॅम/ली.) फवारा.",
                },
                "water_advice": {
                    "en": "Critical moisture stage. Do not allow water stress.",
                    "hi": "फूल आने के समय पानी की कमी न होने दें।",
                    "mr": "फुलधारणेचा अत्यंत संवेदनशील काळ. पाण्याचा ताण पडू देऊ नका.",
                },
            },
            {
                "day_start": 46,
                "day_end": 75,
                "stage": {"en": "Pod Formation & Seed Filling", "hi": "फलियां बनना व दाना भराव", "mr": "शेंगा भरणे व दाण्यांची वाढ"},
                "task": {
                    "en": "Spray 0:52:34 (7g/L) for bold seeds. Check for Girdle Beetle and Spodoptera caterpillar.",
                    "hi": "मोटे दानों के लिए 0:52:34 (7 ग्राम/ली.) छिड़कें। चक्र भृंग व तम्बाकू इल्ली की जांच करें।",
                    "mr": "टपोऱ्या दाण्यांसाठी ०:५२:३४ (७ ग्रॅम/ली.) फवारा. चक्रभुंगा व लष्करी अळीवर लक्ष ठेवा.",
                },
                "water_advice": {
                    "en": "Pod filling requires good moisture. Drain excess rainfall.",
                    "hi": "फली भराव के समय अच्छी नमी चाहिए।",
                    "mr": "शेंगा भरताना ओलावा आवश्यक.",
                },
            },
            {
                "day_start": 76,
                "day_end": 95,
                "stage": {"en": "Maturity & Harvest", "hi": "परिपक्वता व कटाई", "mr": "पक्वता व काढणी"},
                "task": {
                    "en": "Harvest when 90% leaves drop and pods turn brown/yellow. Thresh at gentle cylinder speed to avoid split seed coats.",
                    "hi": "जब 90% पत्तियां झड़ जाएं और फलियां भूरी/पीली हो जाएं तो कटाई करें।",
                    "mr": "९०% पाने गळून पडल्यावर आणि शेंगा पिवळसर-तपकिरी झाल्यावर काढणी करा.",
                },
                "water_advice": {
                    "en": "No irrigation needed.",
                    "hi": "सिंचाई की आवश्यकता नहीं।",
                    "mr": "पाण्याची गरज नाही.",
                },
            },
        ],
        "pests_and_diseases": [
            {
                "name": {"en": "Girdle Beetle (Obereopsis brevis)", "hi": "चक्र भृंग (गर्डल बीटल)", "mr": "चक्रभुंगा (गर्डल बीटल)"},
                "symptoms": {
                    "en": "Two ring-like cuts on petiole/stem, wilting and drying of the cut shoot tip.",
                    "hi": "तने या पत्ती की डंठल पर दो गोल छल्ले जैसे कट, ऊपर का भाग मुरझाकर सूख जाना।",
                    "mr": "फांदीवर किंवा देठावर दोन गोल चक्राकार खाचा, पुढचा शेंडा सुकणे.",
                },
                "organic_remedy": {
                    "en": "Handpick and destroy girdled plant parts + Spray Neem oil 1500 ppm @ 3ml/L.",
                    "hi": "प्रभावित भागों को तोड़कर नष्ट करें + नीम तेल 1500 ppm 3 मिली/ली. छिड़कें।",
                    "mr": "अळीग्रस्त शेंडे तोडून नष्ट करा + कडुलिंब तेल १५०० ppm ३ मिली/ली. फवारा.",
                },
                "chemical_remedy": {
                    "en": "Spray Chlorantraniliprole 18.5% SC @ 0.3ml/L or Thiamethoxam + Lambda-cyhalothrin @ 0.5ml/L.",
                    "hi": "क्लोरेंट्रानिलिप्रोल 18.5% SC 0.3 मिली/ली. या थायमेथोक्सम + लैम्ब्डा-साइहैलोथ्रिन 0.5 मिली/ली. छिड़कें।",
                    "mr": "क्लोरँट्रानिलीप्रोल १८.५% SC ०.३ मिली/ली. किंवा थायमेथोक्साम + लॅम्ब्डा-सायहालोथ्रीन ०.५ मिली/ली. फवारा.",
                },
            },
        ],
    },

    "gram": {
        "id": "gram",
        "category": "pulses_oilseeds",
        "names": {"en": "Chickpea / Gram", "hi": "चना", "mr": "हरभरा (चना)"},
        "scientific_name": "Cicer arietinum",
        "season": {"en": "Rabi", "hi": "रबी", "mr": "रब्बी"},
        "duration_days": 105,
        "optimal_temp": "15°C - 25°C",
        "rainfall_mm": "300 - 500 mm",
        "soil": {
            "en": "Well-drained medium to heavy black soils or alluvial loam (pH 6.5 - 8.0)",
            "hi": "उत्तम जल निकासी वाली मध्यम से भारी काली या दोमट मिट्टी (pH 6.5 - 8.0)",
            "mr": "पाण्याचा उत्तम निचरा होणारी मध्यम ते भारी काळी किंवा पोयट्याची जमीन (pH ६.५ - ८.०)",
        },
        "sowing_months": {
            "en": "October - November",
            "hi": "अक्टूबर - नवंबर",
            "mr": "ऑक्टोबर - नोव्हेंबर",
        },
        "expected_yield_per_acre": "8 - 12 Quintals (Sprinkler yield increase: 57%)",
        "fertilizer_per_acre_kg": {
            "urea": 20,
            "dap": 50,
            "mop": 20,
            "sulphur": 10,
            "fym_tonnes": 3,
        },
        "growth_stages": [
            {
                "day_start": 0,
                "day_end": 25,
                "stage": {"en": "Germination & Seedling", "hi": "अंकुरण व प्रारंभिक बढ़वार", "mr": "उगवण व वाढ"},
                "task": {
                    "en": "Seed treatment with Trichoderma (5g/kg) + Rhizobium culture. Apply full basal: 20kg Urea + 50kg DAP + 20kg MOP + 10kg Sulphur.",
                    "hi": "ट्राइकोडर्मा (5 ग्राम/किग्रा) + राइजोबियम से बीज उपचार। बेसल: 20 किग्रा यूरिया + 50 किग्रा DAP + 20 किग्रा MOP + 10 किग्रा सल्फर।",
                    "mr": "ट्रायकोडर्मा (५ ग्रॅम/किग्रॅ) + रायझोबियम जिवाणू संवर्धक प्रक्रिया. बेसल: २० किग्रॅ युरिया + ५० किग्रॅ DAP + २० किग्रॅ MOP + १० किग्रॅ गंधक.",
                },
                "water_advice": {
                    "en": "Pre-sowing irrigation is sufficient for emergence.",
                    "hi": "बुवाई पूर्व पलेवा सिंचाई अंकुरण के लिए पर्याप्त है।",
                    "mr": "पेरणीपूर्वीचे वाफसा पाणी उगवणीसाठी पुरेसे आहे.",
                },
            },
            {
                "day_start": 26,
                "day_end": 45,
                "stage": {"en": "Branching & Nipping", "hi": "शाखाएं फूटना व खुटाई (निपिंग)", "mr": "फांद्या फुटणे व शेंडे खुडणे"},
                "task": {
                    "en": "Nipping (plucking top shoots) at 30-35 days to encourage multiple lateral branches. Spray 19:19:19 (5g/L).",
                    "hi": "30-35 दिन पर ऊपर के शिखाग्र की खुटाई करें ताकि अधिक शाखाएं फूटें। 19:19:19 (5 ग्राम/ली.) का छिड़काव करें।",
                    "mr": "३०-३५ दिवसांनी झाडांचे शेंडे खुडावेत जेणेकरून भरपूर फांद्या फुटतील. १९:१९:१९ (५ ग्रॅम/ली.) फवारा.",
                },
                "water_advice": {
                    "en": "First light irrigation at 35-40 days before flowering.",
                    "hi": "फूल आने से पहले 35-40 दिन पर पहली हल्की सिंचाई करें।",
                    "mr": "फुले येण्यापूर्वी ३५-४० दिवसांनी पहिले हलके पाणी द्या.",
                },
            },
            {
                "day_start": 46,
                "day_end": 75,
                "stage": {"en": "Podding & Grain Filling", "hi": "घाटी (घेंटे) बनना व दाना भराव", "mr": "घाटे धरणे व दाणे भरणे"},
                "task": {
                    "en": "Spray 0:52:34 (5g/L) + 2% Urea for bold grains. Monitor for Helicoverpa Pod Borer; install 'T' perches (20/acre).",
                    "hi": "0:52:34 (5 ग्राम/ली.) + 2% यूरिया घोल छिड़कें। घाटी छेदक इल्ली के लिए खेत में 'T' आकार की खूंटियां (20/एकड़) लगाएं।",
                    "mr": "०:५२:३४ (५ ग्रॅम/ली.) + २% युरिया द्रावण फवारा. घाटेअळीसाठी शेतात 'T' आकाराचे पक्षी थांबे (२०/एकर) लावा.",
                },
                "water_advice": {
                    "en": "Second light irrigation at pod filling (avoid flood irrigation).",
                    "hi": "घाटी भराव अवस्था में दूसरी हल्की सिंचाई (पानी भराव न हो)।",
                    "mr": "घाटे भरताना दुसरी हलकी पाणीपाळी (जास्त पाणी साचू देऊ नका).",
                },
            },
            {
                "day_start": 76,
                "day_end": 105,
                "stage": {"en": "Maturity & Harvesting", "hi": "परिपक्वता व कटाई", "mr": "पक्वता व काढणी"},
                "task": {
                    "en": "Harvest when plants turn yellowish-brown and seeds rattle inside pods. Dry seeds to 10% moisture before storing.",
                    "hi": "जब पौधे पीले-भूरे हो जाएं और हिलाने पर घाटियों में दाने खड़कने लगें तो कटाई करें।",
                    "mr": "झाडे पिवळसर-तपकिरी होऊन घाट्यात दाणे वाजायला लागले की उपटून काढणी करा.",
                },
                "water_advice": {
                    "en": "No irrigation.",
                    "hi": "सिंचाई न करें।",
                    "mr": "पाणी देऊ नका.",
                },
            },
        ],
        "pests_and_diseases": [
            {
                "name": {"en": "Gram Pod Borer (Helicoverpa armigera)", "hi": "चना घाटी छेदक इल्ली", "mr": "हरभरा घाटेअळी"},
                "symptoms": {
                    "en": "Circular bore holes on pods with caterpillar feeding inside, skeletonized leaves.",
                    "hi": "घाटियों पर गोल छेद और अंदर इल्ली द्वारा दानों को खाया जाना।",
                    "mr": "घाट्यांना गोल छिद्रे पाडून आतील दाणे खाणारी हिरवट अळी.",
                },
                "organic_remedy": {
                    "en": "Install Pheromone traps @ 6/acre. Spray HaNPV @ 250 LE/acre or Neem oil 5ml/L.",
                    "hi": "6 फेरोमोन ट्रैप/एकड़ लगाएं। HaNPV 250 LE/एकड़ या नीम तेल 5 मिली/ली. छिड़कें।",
                    "mr": "६ कामगंध सापळे/एकर लावा. HaNPV २५० LE/एकर किंवा कडुलिंब तेल ५ मिली/ली. फवारा.",
                },
                "chemical_remedy": {
                    "en": "Spray Emamectin Benzoate 5% SG @ 0.5g/L or Chlorantraniliprole 18.5% SC @ 0.3ml/L.",
                    "hi": "एमामेक्टिन बेंजोएट 5% SG 0.5 ग्राम/ली. या क्लोरेंट्रानिलिप्रोल 18.5% SC 0.3 मिली/ली. छिड़कें।",
                    "mr": "इमामेक्टिन बेंझोएट ५% SG ०.५ ग्रॅम/ली. किंवा क्लोरँट्रानिलीप्रोल १८.५% SC ०.३ मिली/ली. फवारा.",
                },
            },
        ],
    },

    "mustard": {
        "id": "mustard",
        "category": "pulses_oilseeds",
        "names": {"en": "Mustard / Rapeseed", "hi": "सरसों / राई", "mr": "मोहरी"},
        "scientific_name": "Brassica juncea",
        "season": {"en": "Rabi", "hi": "रबी", "mr": "रब्बी"},
        "duration_days": 115,
        "optimal_temp": "10°C - 25°C",
        "rainfall_mm": "250 - 450 mm",
        "soil": {
            "en": "Light to heavy loam soils with good drainage (pH 6.0 - 7.5)",
            "hi": "हल्की से भारी दोमट मिट्टी जिसमें जल निकास अच्छा हो (pH 6.0 - 7.5)",
            "mr": "पाण्याचा निचरा होणारी हलकी ते मध्यम पोयटा जमीन (pH ६.० - ७.५)",
        },
        "sowing_months": {
            "en": "September - October",
            "hi": "सितंबर - अक्टूबर",
            "mr": "सप्टेंबर - ऑक्टोबर",
        },
        "expected_yield_per_acre": "7 - 10 Quintals",
        "fertilizer_per_acre_kg": {
            "urea": 65,
            "dap": 40,
            "mop": 20,
            "sulphur": 15,
            "fym_tonnes": 3,
        },
        "growth_stages": [
            {
                "day_start": 0,
                "day_end": 25,
                "stage": {"en": "Sowing & Thinning", "hi": "बुवाई व विरलीकरण", "mr": "पेरणी व विरळणी"},
                "task": {
                    "en": "Seed treatment with Thiram (3g/kg). Apply basal: 30kg Urea + 40kg DAP + 20kg MOP + 15kg Bentonite Sulphur per acre. Thin plants to 10-15cm distance at 15-20 days.",
                    "hi": "थायराम (3 ग्राम/किग्रा) से बीज उपचार। 30 किग्रा यूरिया + 40 किग्रा DAP + 20 किग्रा MOP + 15 किग्रा सल्फर बेसल दें। 15-20 दिन पर पौधों की छंटाई कर 10-15 सेमी दूरी रखें।",
                    "mr": "थायरम (३ ग्रॅम/किग्रॅ) ने बीज प्रक्रिया. ३० किग्रॅ युरिया + ४० किग्रॅ DAP + २० किग्रॅ MOP + १५ किग्रॅ गंधक बेसल द्या. १५-२० दिवसांनी विरळणी करून १०-१५ सेमी अंतर ठेवा.",
                },
                "water_advice": {
                    "en": "First irrigation at 25-30 days before flowering.",
                    "hi": "फूल आने से पहले 25-30 दिन पर पहली सिंचाई करें।",
                    "mr": "फुले येण्यापूर्वी २५-३० दिवसांनी पहिले पाणी द्या.",
                },
            },
            {
                "day_start": 26,
                "day_end": 60,
                "stage": {"en": "Flowering & Branching", "hi": "फूल आना व शाखाएं", "mr": "फुलधारणा व फांद्यांची वाढ"},
                "task": {
                    "en": "Apply top dressing of 35kg Urea after 1st irrigation. Monitor for Mustard Aphids (Chetu / Mahu).",
                    "hi": "पहली सिंचाई के बाद 35 किग्रा यूरिया टॉप ड्रेसिंग दें। सरसों के माहू (चेपा) की सख्त निगरानी करें।",
                    "mr": "पहिल्या पाण्यानंतर ३५ किग्रॅ युरिया खताचा हप्ता द्या. मोहरीवरील मावा किडीवर बारीक लक्ष ठेवा.",
                },
                "water_advice": {
                    "en": "Second irrigation at siliqua (pod) formation at 50-60 days.",
                    "hi": "50-60 दिन पर फलियां बनते समय दूसरी सिंचाई करें।",
                    "mr": "५०-६० दिवसांनी शेंगा भरताना दुसरे पाणी द्या.",
                },
            },
            {
                "day_start": 61,
                "day_end": 115,
                "stage": {"en": "Pod Filling & Harvest", "hi": "फली भराव व कटाई", "mr": "शेंगा भरणे व काढणी"},
                "task": {
                    "en": "Spray 0:0:50 (5g/L) + Sulphur 80% WDG (2g/L). Harvest early morning when 75% pods turn yellow to prevent shattering of seeds.",
                    "hi": "0:0:50 (5 ग्राम/ली.) + सल्फर 80% WDG (2 ग्राम/ली.) छिड़कें। 75% फलियां पीली होने पर सुबह कटाई करें।",
                    "mr": "०:०:५० (५ ग्रॅम/ली.) + गंधक ८०% WDG (२ ग्रॅम/ली.) फवारा. ७५% शेंगा पिवळ्या झाल्यावर सकाळी कापणी करा.",
                },
                "water_advice": {
                    "en": "Stop irrigation completely.",
                    "hi": "सिंचाई पूर्णतः बंद करें।",
                    "mr": "पाणी पूर्ण बंद करा.",
                },
            },
        ],
        "pests_and_diseases": [
            {
                "name": {"en": "Mustard Aphid (Lipaphis erysimi)", "hi": "सरसों का माहू (चेपा)", "mr": "मोहरीवरील मावा"},
                "symptoms": {
                    "en": "Dense colonies of small greenish-yellow aphids sucking sap from inflorescence, curling flowers and stunting pods.",
                    "hi": "फूलों और फलियों पर पीले-हरे माहू के झुंड जो रस चूसकर फलियों को बनने नहीं देते।",
                    "mr": "फुलोऱ्यावर व शेंगांवर पिवळसर-हिरव्या मावा किडींचा प्रादुर्भाव, रस शोषून शेंगा वाकड्या होणे.",
                },
                "organic_remedy": {
                    "en": "Yellow sticky cards @ 15/acre + Spray 5% Neem seed kernel extract (NSKE).",
                    "hi": "पीले चिपचिपे कार्ड 15/एकड़ लगाएं + 5% नीम बीज अर्क (NSKE) छिड़कें।",
                    "mr": "१५ पिवळे चिकट सापळे/एकर लावा + ५% निंबोळी अर्क फवारा.",
                },
                "chemical_remedy": {
                    "en": "Spray Dimethoate 30% EC @ 1.5ml/L or Thiamethoxam 25% WG @ 0.3g/L.",
                    "hi": "डायमेथोएट 30% EC 1.5 मिली/ली. या थायमेथोक्सम 25% WG 0.3 ग्राम/ली. छिड़कें।",
                    "mr": "डायमेथोएट ३०% EC १.५ मिली/ली. किंवा थायमेथोक्साम २५% WG ०.३ ग्रॅम/ली. फवारा.",
                },
            },
        ],
    },

    "maize": {
        "id": "maize",
        "category": "cereals",
        "names": {"en": "Maize (Corn)", "hi": "मक्का", "mr": "मका"},
        "scientific_name": "Zea mays",
        "season": {"en": "Kharif / Rabi", "hi": "खरीफ / रबी", "mr": "खरीप / रब्बी"},
        "duration_days": 100,
        "optimal_temp": "18°C - 35°C",
        "rainfall_mm": "500 - 800 mm",
        "soil": {
            "en": "Deep, fertile, well-drained loamy soil (pH 6.0 - 7.5)",
            "hi": "गहरी, उपजाऊ, अच्छी जल निकासी वाली दोमट मिट्टी (pH 6.0 - 7.5)",
            "mr": "पाण्याचा चांगला निचरा होणारी सुपीक पोयटा जमीन (pH ६.० - ७.५)",
        },
        "sowing_months": {
            "en": "June - July (Kharif), Oct - Nov (Rabi)",
            "hi": "जून - जुलाई (खरीफ), अक्टूबर - नवंबर (रबी)",
            "mr": "जून - जुलै (खरीप), ऑक्टोबर - नोव्हेंबर (रब्बी)",
        },
        "expected_yield_per_acre": "22 - 30 Quintals (Sprinkler yield increase: 36%)",
        "fertilizer_per_acre_kg": {
            "urea": 100,
            "dap": 60,
            "mop": 30,
            "zinc_sulphate": 10,
            "fym_tonnes": 4,
        },
        "growth_stages": [
            {
                "day_start": 0,
                "day_end": 20,
                "stage": {"en": "Sowing & Knee-high", "hi": "बुवाई व घुटने तक ऊंचाई", "mr": "पेरणी व गुडघाभर वाढ"},
                "task": {
                    "en": "Seed treatment with Cyantraniliprole (4ml/kg) for Fall Armyworm. Basal: 30kg Urea + 60kg DAP + 30kg MOP + 10kg Zinc Sulphate.",
                    "hi": "फॉल आर्मीवॉर्म से बचाव हेतु सायंस्ट्रानिलिप्रोल (4 मिली/किग्रा) से बीज उपचार। 30 किग्रा यूरिया + 60 किग्रा DAP + 30 किग्रा MOP + 10 किग्रा जिंक बेसल दें।",
                    "mr": "लष्करी अळीपासून संरक्षणासाठी सायंट्रानिलीप्रोल (४ मिली/किग्रॅ) ने बीज प्रक्रिया. ३० किग्रॅ युरिया + ६० किग्रॅ DAP + ३० किग्रॅ MOP + १० किग्रॅ झिंक बेसल डोस द्या.",
                },
                "water_advice": {
                    "en": "Do not allow water stagnation.",
                    "hi": "खेत में पानी जमा न होने दें।",
                    "mr": "शेतात पाणी साचू देऊ नका.",
                },
            },
            {
                "day_start": 21,
                "day_end": 50,
                "stage": {"en": "Tasseling & Silking", "hi": "मंजरी (नर) व भुट्टा (मादा) निकलना", "mr": "तुरा व कणसाचे केस बाहेर पडणे"},
                "task": {
                    "en": "Apply 1st top dressing of 40kg Urea at knee-high and 30kg Urea at tasseling. Monitor whorls for Fall Armyworm.",
                    "hi": "घुटने की ऊंचाई पर 40 किग्रा यूरिया और मंजरी निकलते समय 30 किग्रा यूरिया दें। पत्तों के भंवर में फॉल आर्मीवॉर्म की जांच करें।",
                    "mr": "गुडघाभर उंचीवर ४० किग्रॅ युरिया आणि तुरा येताना ३० किग्रॅ युरिया द्या. पानांच्या पोंग्यात लष्करी अळी तपासा.",
                },
                "water_advice": {
                    "en": "Critical moisture stage. Moisture stress drastically reduces grain setting.",
                    "hi": "अत्यंत महत्वपूर्ण अवस्था। पानी की कमी से भुट्टे में दाने नहीं बनते।",
                    "mr": "अतिसंवेदनशील काळ. पाण्याचा ताण पडल्यास कणसात दाणे भरत नाहीत.",
                },
            },
            {
                "day_start": 51,
                "day_end": 100,
                "stage": {"en": "Grain Filling & Harvest", "hi": "दाना भराव व कटाई", "mr": "दाणे भरणे व काढणी"},
                "task": {
                    "en": "Spray 0:0:50 (5g/L). Harvest when cob sheath dries to straw color and black layer forms at seed base. Dry to 12% moisture.",
                    "hi": "0:0:50 छिड़कें। जब भुट्टे का छिलका सूखकर भूरा हो जाए तो कटाई करें। 12% नमी तक सुखाएं।",
                    "mr": "०:०:५० फवारा. कणसाची पाने वाळल्यावर कणसे तोडा. १२% ओलाव्यापर्यंत सुकवा.",
                },
                "water_advice": {
                    "en": "Stop irrigation.",
                    "hi": "सिंचाई बंद रखें।",
                    "mr": "पाणी देणे बंद करा.",
                },
            },
        ],
        "pests_and_diseases": [
            {
                "name": {"en": "Fall Armyworm (Spodoptera frugiperda)", "hi": "फॉल आर्मीवॉर्म (सैनिक कीट)", "mr": "लष्करी अळी (फॉल आर्मीवॉर्म)"},
                "symptoms": {
                    "en": "Elongated window panes on young leaves, severe defoliation, large holes with abundant sawdust-like fecal matter in the central whorl.",
                    "hi": "पत्तियों पर झिल्लीदार धब्बे, तने के भंवर में बुरादे जैसी विष्ठा और पत्तियों को बुरी तरह काटकर खाना।",
                    "mr": "पानांवर खिडकीसारखे पांढरे डाग, पोंग्यात लाकडाच्या भुशासारखी विष्ठा व पाने खाऊन नष्ट करणे.",
                },
                "organic_remedy": {
                    "en": "Apply sand + wood ash in central leaf whorl or spray Metarhizium anisopliae @ 5g/L.",
                    "hi": "पत्तियों के भंवर में सूखी रेत + राख डालें या मेटाराइजियम एनीसोप्ली 5 ग्राम/ली. छिड़कें।",
                    "mr": "पानांच्या पोंग्यात वाळू + लाकडाची राख टाका किंवा मेटारायझियम अॅनिसोप्ली ५ ग्रॅम/ली. फवारा.",
                },
                "chemical_remedy": {
                    "en": "Spray Chlorantraniliprole 18.5% SC @ 0.4ml/L or Emamectin Benzoate 5% SG @ 0.5g/L directing into whorl.",
                    "hi": "क्लोरेंट्रानिलिप्रोल 18.5% SC 0.4 मिली/ली. या एमामेक्टिन बेंजोएट 5% SG 0.5 ग्राम/ली. सीधे भंवर में छिड़कें।",
                    "mr": "क्लोरँट्रानिलीप्रोल १८.५% SC ०.४ मिली/ली. किंवा इमामेक्टिन बेंझोएट ५% SG ०.५ ग्रॅम/ली. थेट पोंग्यात फवारा.",
                },
            },
        ],
    },

    "tomato": {
        "id": "tomato",
        "category": "vegetables",
        "names": {"en": "Tomato", "hi": "टमाटर", "mr": "टोमॅटो"},
        "scientific_name": "Solanum lycopersicum",
        "season": {"en": "Kharif / Rabi / Summer", "hi": "खरीफ / रबी / जायद", "mr": "खरीप / रब्बी / उन्हाळी"},
        "duration_days": 130,
        "optimal_temp": "18°C - 30°C",
        "rainfall_mm": "600 - 800 mm",
        "soil": {
            "en": "Rich, well-drained sandy loam or clay loam (pH 6.0 - 7.0)",
            "hi": "उपजाऊ, उत्तम जल निकास वाली बलुई दोमट या दोमट मिट्टी (pH 6.0 - 7.0)",
            "mr": "सुपीक, पाण्याचा चांगला निचरा होणारी वाळूयुक्त पोयटा जमीन (pH ६.० - ७.०)",
        },
        "sowing_months": {
            "en": "June - July, Oct - Nov, Jan - Feb",
            "hi": "जून - जुलाई, अक्टूबर - नवंबर, जनवरी - फरवरी",
            "mr": "जून - जुलै, ऑक्टोबर - नोव्हेंबर, जानेवारी - फेब्रुवारी",
        },
        "expected_yield_per_acre": "180 - 250 Quintals (Drip yield increase: 50%)",
        "fertilizer_per_acre_kg": {
            "urea": 80,
            "dap": 70,
            "mop": 60,
            "calcium_nitrate": 15,
            "boron": 5,
            "fym_tonnes": 8,
        },
        "growth_stages": [
            {
                "day_start": 0,
                "day_end": 25,
                "stage": {"en": "Nursery & Transplanting", "hi": "नर्सरी व रोपाई", "mr": "रोपवाटिका व पुनर्लागवड"},
                "task": {
                    "en": "Raise healthy seedlings. Transplant 25-day seedlings. Apply basal: 25kg Urea + 70kg DAP + 30kg MOP + 8 tonnes FYM. Seed treatment with Trichoderma viride (2g/100g seed) or Pseudomonas fluorescens (10g/kg).",
                    "hi": "25 दिन के स्वस्थ पौधों की रोपाई। बेसल: 25 किग्रा यूरिया + 70 किग्रा DAP + 30 किग्रा MOP + 8 टन गोबर खाद। ट्राइकोडर्मा या स्यूडोमोनास से बीज उपचार।",
                    "mr": "२५ दिवसांच्या निरोगी रोपांची पुनर्लागवड. बेसल: २५ किग्रॅ युरिया + ७० किग्रॅ DAP + ३० किग्रॅ MOP + ८ टन शेणखत. ट्रायकोडर्मा किंवा स्यूडोमोनासने बीज प्रक्रिया.",
                },
                "water_advice": {
                    "en": "Light daily watering in nursery; immediate irrigation after transplanting.",
                    "hi": "नर्सरी में रोज हल्का पानी; रोपाई के तुरंत बाद सिंचाई।",
                    "mr": "रोपवाटिकेत रोज हलके पाणी; पुनर्लागवडीनंतर लगेच पाणी द्या.",
                },
            },
            {
                "day_start": 26,
                "day_end": 60,
                "stage": {"en": "Vegetative & Staking", "hi": "वानस्पतिक बढ़वार व सहारा", "mr": "झाडांची वाढ व बांबू आधार"},
                "task": {
                    "en": "Staking with bamboo poles. Apply 30kg Urea + 15kg MOP at 30 days. Spray Boron (1g/L) to prevent flower drop.",
                    "hi": "बांस के सहारे बांधें (स्टेकिंग)। 30 दिन पर 30 किग्रा यूरिया + 15 किग्रा MOP। फूल झड़ने से रोकने हेतु बोरॉन (1 ग्राम/ली.) छिड़कें।",
                    "mr": "बांबूच्या काठ्यांचा आधार (स्टेकिंग) द्या. ३० दिवसांनी ३० किग्रॅ युरिया + १५ किग्रॅ MOP द्या. फूलगळ रोखण्यासाठी बोरॉन (१ ग्रॅम/ली.) फवारा.",
                },
                "water_advice": {
                    "en": "Drip irrigation at 2-3 day intervals. Critical weed competition period is 30 days.",
                    "hi": "ड्रिप से 2-3 दिन में सिंचाई।",
                    "mr": "ठिबक सिंचनाने २-३ दिवसांनी पाणी द्या.",
                },
            },
            {
                "day_start": 61,
                "day_end": 130,
                "stage": {"en": "Fruiting & Harvesting", "hi": "फल विकास व तुड़ाई", "mr": "फळधारणा व तोडणी"},
                "task": {
                    "en": "Apply Calcium Nitrate (15kg/acre) + 0:0:50 (5g/L) for firm cracking-resistant fruit. Pick pink/breaker stage tomatoes every 3-4 days.",
                    "hi": "कैल्शियम नाइट्रेट (15 किग्रा/एकड़) + 0:0:50 (5 ग्राम/ली.) छिड़कें। हर 3-4 दिन में तुड़ाई करें।",
                    "mr": "कॅल्शियम नायट्रेट (१५ किग्रॅ/एकर) + ०:०:५० (५ ग्रॅम/ली.) फवारा. दर ३-४ दिवसांनी तोडणी करा.",
                },
                "water_advice": {
                    "en": "Maintain consistent drip moisture.",
                    "hi": "नियमित ड्रिप सिंचाई जारी रखें।",
                    "mr": "नियमित पाणी सुरू ठेवा.",
                },
            },
        ],
        "pests_and_diseases": [
            {
                "name": {"en": "Early Blight (Alternaria solani)", "hi": "टमाटर का अगेती झुलसा (अर्ली ब्लाइट)", "mr": "टोमॅटोवरील लवकर येणारा करपा"},
                "symptoms": {
                    "en": "Concentric target-board rings of dark brown spots on lower leaves, yellowing and drying upward.",
                    "hi": "निचली पत्तियों पर गहरे भूरे गोल छल्ले जैसे धब्बे (टारगेट बोर्ड), पत्तियां पीली पड़कर सूखना।",
                    "mr": "खालच्या पानांवर गोल रिंगासारखे गडद तपकिरी डाग, पाने पिवळी पडून वाळणे.",
                },
                "organic_remedy": {
                    "en": "Spray Copper Oxychloride 50% WP @ 2.5g/L or Trichoderma viride @ 5g/L.",
                    "hi": "कॉपर ऑक्सीक्लोराइड 50% WP 2.5 ग्राम/ली. या ट्राइकोडर्मा 5 ग्राम/ली. छिड़कें।",
                    "mr": "कॉपर ऑक्सिक्लोराईड ५०% WP २.५ ग्रॅम/ली. किंवा ट्रायकोडर्मा ५ ग्रॅम/ली. फवारा.",
                },
                "chemical_remedy": {
                    "en": "Spray Azoxystrobin + Difenoconazole @ 1ml/L or Mancozeb 75% WP @ 2.5g/L.",
                    "hi": "एजॉक्सीस्ट्रोबिन + डिफेनोकोनाजोल 1 मिली/ली. या मैंकोजेब 75% WP 2.5 ग्राम/ली. छिड़कें।",
                    "mr": "अॅझॉक्सीस्ट्रोबिन + डायफेनोकोनाझोल १ मिली/ली. किंवा मॅन्कोझेब ७५% WP २.५ ग्रॅम/ली. फवारा.",
                },
            },
        ],
    },

    "onion": {
        "id": "onion",
        "category": "vegetables",
        "names": {"en": "Onion", "hi": "प्याज", "mr": "कांदा"},
        "scientific_name": "Allium cepa",
        "season": {"en": "Kharif / Late Kharif / Rabi", "hi": "खरीफ / लेट खरीफ / रबी", "mr": "खरीप / लेट खरीप / रब्बी"},
        "duration_days": 120,
        "optimal_temp": "13°C - 30°C",
        "rainfall_mm": "500 - 750 mm",
        "soil": {
            "en": "Well-drained friable sandy loam or red loam (pH 6.0 - 7.5)",
            "hi": "भुरभुरी, उत्तम जल निकास वाली बलुई दोमट या लाल दोमट मिट्टी (pH 6.0 - 7.5)",
            "mr": "भुसभुशीत, पाण्याचा चांगला निचरा होणारी पोयट्याची जमीन (pH ६.० - ७.५)",
        },
        "sowing_months": {
            "en": "May - June (Kharif), Oct - Nov (Rabi)",
            "hi": "मई - जून (खरीफ), अक्टूबर - नवंबर (रबी)",
            "mr": "मे - जून (खरीप), ऑक्टोबर - नोव्हेंबर (रब्बी)",
        },
        "expected_yield_per_acre": "100 - 160 Quintals (Drip yield increase: 53.8%)",
        "fertilizer_per_acre_kg": {
            "urea": 75,
            "dap": 60,
            "mop": 40,
            "sulphur": 15,
            "fym_tonnes": 8,
        },
        "growth_stages": [
            {
                "day_start": 0,
                "day_end": 20,
                "stage": {"en": "Transplanting & Establishment", "hi": "रोपाई व स्थापना", "mr": "पुनर्लागवड व स्थापना"},
                "task": {
                    "en": "Transplant 45-day sturdy seedlings. Apply basal: 25kg Urea + 60kg DAP + 20kg MOP + 15kg Sulphur per acre. Weed competition critical period is 60 days.",
                    "hi": "45 दिन के पौधों की रोपाई। बेसल: 25 किग्रा यूरिया + 60 किग्रा DAP + 20 किग्रा MOP + 15 किग्रा सल्फर प्रति एकड़।",
                    "mr": "४५ दिवसांच्या रोपांची पुनर्लागवड. बेसल: २५ किग्रॅ युरिया + ६० किग्रॅ DAP + २० किग्रॅ MOP + १५ किग्रॅ गंधक प्रति एकर.",
                },
                "water_advice": {
                    "en": "Give immediate irrigation after transplanting and second on Day 3.",
                    "hi": "रोपाई के तुरंत बाद पहली और तीसरे दिन दूसरी सिंचाई करें।",
                    "mr": "लागवडीनंतर लगेच पहिले पाणी व ३ ऱ्या दिवशी दुसरे पाणी द्या.",
                },
            },
            {
                "day_start": 21,
                "day_end": 50,
                "stage": {"en": "Vegetative & Foliage Growth", "hi": "पत्तियों की बढ़वार", "mr": "पातीची वाढ"},
                "task": {
                    "en": "Apply 1st top dressing of 25kg Urea at 30 days. Spray 19:19:19 (5g/L). Monitor for Onion Thrips.",
                    "hi": "30 दिन पर 25 किग्रा यूरिया का पहला टॉप ड्रेसिंग। 19:19:19 (5 ग्राम/ली.) छिड़कें।",
                    "mr": "३० दिवसांनी २५ किग्रॅ युरिया खताचा हप्ता द्या. १९:१९:१९ (५ ग्रॅम/ली.) फवारा.",
                },
                "water_advice": {
                    "en": "Irrigate at 6-8 day intervals.",
                    "hi": "6-8 दिन के अंतराल पर सिंचाई करें।",
                    "mr": "६-८ दिवसांनी पाणी द्या.",
                },
            },
            {
                "day_start": 51,
                "day_end": 120,
                "stage": {"en": "Bulb Development & Harvesting", "hi": "कंद फुलाव व खुदाई", "mr": "कांदा फुगवण व काढणी"},
                "task": {
                    "en": "Apply 2nd top dressing of 25kg Urea + 20kg MOP at 45-50 days. Spray 0:52:34 (5g/L) + Boron (1g/L). Stop irrigation when 50% tops fall naturally. Cure in shade 10-15 days.",
                    "hi": "बड़े ठोस कंद हेतु 0:52:34 (5 ग्राम/ली.) + बोरॉन (1 ग्राम/ली.) छिड़कें। 50% गर्दन झुकने पर 10-12 दिन पहले सिंचाई बंद करें।",
                    "mr": "कांदा फुगवणीसाठी ०:५२:३४ (५ ग्रॅम/ली.) + बोरॉन (१ ग्रॅम/ली.) फवारा. ५०% माना पडल्यावर पाणी बंद करा.",
                },
                "water_advice": {
                    "en": "Stop irrigation completely 10-12 days before harvest.",
                    "hi": "भंडारण में सड़न से बचने के लिए सिंचाई पूरी तरह रोकें।",
                    "mr": "साठवणुकीत सड होऊ नये म्हणून पाणी पूर्ण बंद ठेवा.",
                },
            },
        ],
        "pests_and_diseases": [
            {
                "name": {"en": "Onion Thrips (Thrips tabaci)", "hi": "प्याज का थ्रिप्स (जूं)", "mr": "कांद्यावरील थ्रिप्स (बोकड्या)"},
                "symptoms": {
                    "en": "Silvery white patches on foliage, leaf curling, tip burning, stunted bulb formation.",
                    "hi": "पत्तियों पर चांदी जैसे सफेद धब्बे, पत्तियों का मुड़ना और ऊपर से सूखना।",
                    "mr": "पातीवर पांढुरके चंदेरी ठिपके, पाती वाकडी होणे व शेंडे जळणे.",
                },
                "organic_remedy": {
                    "en": "Blue/Yellow sticky traps @ 20/acre + Spray Verticillium lecanii @ 5g/L or Neem oil 10000 ppm @ 2ml/L.",
                    "hi": "नीले/पीले चिपचिपे ट्रैप 20/एकड़ लगाएं + वर्टिसिलियम लेकानी 5 ग्राम/ली. या नीम तेल 2 मिली/ली. छिड़कें।",
                    "mr": "२० निळे/पिवळे चिकट सापळे/एकर लावा + व्हर्टिसिलियम लेकानी ५ ग्रॅम/ली. किंवा कडुलिंब तेल २ मिली/ली. फवारा.",
                },
                "chemical_remedy": {
                    "en": "Spray Fipronil 5% SC @ 1.5ml/L or Spinetoram 11.7% SC @ 0.8ml/L with sticking agent.",
                    "hi": "फिप्रोनिल 5% SC 1.5 मिली/ली. या स्पिनेटोरम 0.8 मिली/ली. चिपचिपे पदार्थ के साथ छिड़कें।",
                    "mr": "फिप्रोनिल ५% SC १.५ मिली/ली. किंवा स्पिनेटोरम ०.८ मिली/ली. स्टिकर मिसळून फवारा.",
                },
            },
        ],
    },

    "potato": {
        "id": "potato",
        "category": "vegetables",
        "names": {"en": "Potato", "hi": "आलू", "mr": "बटाटा"},
        "scientific_name": "Solanum tuberosum",
        "season": {"en": "Rabi", "hi": "रबी", "mr": "रब्बी"},
        "duration_days": 100,
        "optimal_temp": "15°C - 24°C",
        "rainfall_mm": "400 - 600 mm",
        "soil": {
            "en": "Loose, friable, well-aerated sandy loam with rich organic matter (pH 5.2 - 6.4)",
            "hi": "भुरभुरी, उपजाऊ बलुई दोमट मिट्टी जिसमें जीवांश प्रचुर हो (pH 5.2 - 6.4)",
            "mr": "भुसभुशीत, सेंद्रिययुक्त पाण्याचा चांगला निचरा होणारी वाळूमिश्रित पोयटा जमीन (pH ५.२ - ६.४)",
        },
        "sowing_months": {
            "en": "October - November",
            "hi": "अक्टूबर - नवंबर",
            "mr": "ऑक्टोबर - नोव्हेंबर",
        },
        "expected_yield_per_acre": "120 - 180 Quintals (Drip yield increase: 79.5%)",
        "fertilizer_per_acre_kg": {
            "urea": 90,
            "dap": 80,
            "mop": 60,
            "fym_tonnes": 8,
        },
        "growth_stages": [
            {
                "day_start": 0,
                "day_end": 25,
                "stage": {"en": "Sprouting & Emergence", "hi": "अंकुरण व पौध निकलना", "mr": "कोंब फुटणे व उगवण"},
                "task": {
                    "en": "Treat cut seed tubers with Mancozeb (2g/L) or Boric acid 3% for 20 mins before storage. Apply basal: 45kg Urea + 80kg DAP + 30kg MOP per acre.",
                    "hi": "कटे आलू कंदों को मैंकोजेब (2 ग्राम/ली.) या 3% बोरिक एसिड से उपचारित करें। बेसल: 45 किग्रा यूरिया + 80 किग्रा DAP + 30 किग्रा MOP।",
                    "mr": "बटाटा बेण्याला मॅन्कोझेब (२ ग्रॅम/ली.) किंवा ३% बोरिक ॲसिडची प्रक्रिया करा. बेसल: ४५ किग्रॅ युरिया + ८० किग्रॅ DAP + ३० किग्रॅ MOP.",
                },
                "water_advice": {
                    "en": "Light irrigation before and after planting.",
                    "hi": "बुवाई से पहले और बाद में हल्की सिंचाई करें।",
                    "mr": "लागवडीपूर्वी व नंतर हलके पाणी द्या.",
                },
            },
            {
                "day_start": 26,
                "day_end": 50,
                "stage": {"en": "Vegetative & Earthing Up", "hi": "वानस्पतिक बढ़वार व मिट्टी चढ़ाना", "mr": "झाडांची वाढ व मातीची भर"},
                "task": {
                    "en": "Earthing up at 30-35 days to cover developing tubers from sunlight. Apply top dressing of 45kg Urea + 30kg MOP.",
                    "hi": "30-35 दिन पर मिट्टी चढ़ाएं ताकि आलू धूप से हरे न हों। 45 किग्रा यूरिया + 30 किग्रा MOP टॉप ड्रेसिंग दें।",
                    "mr": "३०-३५ दिवसांनी बटाट्यावर मातीची भर द्या जेणेकरून बटाटे उघडे पडून हिरवे पडणार नाहीत. ४५ किग्रॅ युरिया + ३० किग्रॅ MOP द्या.",
                },
                "water_advice": {
                    "en": "Maintain consistent moisture at 7-8 day intervals.",
                    "hi": "7-8 दिन के अंतराल पर एकसमान नमी रखें।",
                    "mr": "७-८ दिवसांच्या अंतराने नियमित पाणी द्या.",
                },
            },
            {
                "day_start": 51,
                "day_end": 100,
                "stage": {"en": "Tuber Bulking & Dehaulming", "hi": "कंद विकास, बेल काटना व खुदाई", "mr": "बटाटा फुगवण, छाटणी व काढणी"},
                "task": {
                    "en": "Spray 0:0:50 (5g/L) + Boron (1g/L). Cut aerial foliage (dehaulm) 10 days before digging to harden skin of tubers. Dig carefully in dry soil.",
                    "hi": "0:0:50 (5 ग्राम/ली.) + बोरॉन (1 ग्राम/ली.) छिड़कें। खोदने से 10 दिन पहले ऊपर की बेल काट दें ताकि छिलका कड़ा हो जाए।",
                    "mr": "०:०:५० + बोरॉन फवारा. काढणीपूर्वी १० दिवस आधी वरचा पाला कापून टाका (डिहॉमिंग) जेणेकरून साल टणक बनेल.",
                },
                "water_advice": {
                    "en": "Stop irrigation 10-12 days before digging.",
                    "hi": "खुदाई से 10-12 दिन पहले सिंचाई बंद करें।",
                    "mr": "काढणीच्या १०-१२ दिवस आधी पाणी बंद करा.",
                },
            },
        ],
        "pests_and_diseases": [
            {
                "name": {"en": "Late Blight (Phytophthora infestans)", "hi": "आलू का पछेती झुलसा (लेट ब्लाइट)", "mr": "बटाट्यावरील उशिरा येणारा करपा"},
                "symptoms": {
                    "en": "Water-soaked dark lesions on leaf tips with white mildew on underside during humid weather, rapid plant collapse.",
                    "hi": "पत्तियों के किनारों पर गीले काले धब्बे, निचली सतह पर सफेद फफूंद और फसल का तेजी से झुलस कर नष्ट होना।",
                    "mr": "पानांच्या कडांवर काळपट-तपकिरी जळाल्यासारखे डाग, दमट हवेत पानाच्या खाली पांढरी बुरशी व पीक झपाट्याने करपणे.",
                },
                "organic_remedy": {
                    "en": "Prophylactic spray of Copper Hydroxide 53.8% DF @ 2g/L before foggy cloudy spell.",
                    "hi": "कोहरे व बादलों के मौसम से पहले कॉपर हाइड्रॉक्साइड 2 ग्राम/ली. का छिड़काव करें।",
                    "mr": "ढगाळ व धुक्याच्या हवामानापूर्वी कॉपर हायड्रॉक्साईड २ ग्रॅम/ली. प्रतिबंधक फवारणी करा.",
                },
                "chemical_remedy": {
                    "en": "Spray Cymoxanil 8% + Mancozeb 64% WP @ 2.5g/L or Dimethomorph 50% WP @ 1g/L.",
                    "hi": "साइमोक्सानिल 8% + मैंकोजेब 64% WP 2.5 ग्राम/ली. या डायमेथोमॉर्फ 50% WP 1 ग्राम/ली. छिड़कें।",
                    "mr": "सायमॉक्सॅनिल ८% + मॅन्कोझेब ६४% WP २.५ ग्रॅम/ली. किंवा डायमेथोमॉर्फ ५०% WP १ ग्रॅम/ली. फवारा.",
                },
            },
        ],
    },

    "groundnut": {
        "id": "groundnut",
        "category": "pulses_oilseeds",
        "names": {"en": "Groundnut (Peanut)", "hi": "मूंगफली", "mr": "भुईमूग"},
        "scientific_name": "Arachis hypogaea",
        "season": {"en": "Kharif / Summer", "hi": "खरीफ / जायद", "mr": "खरीप / उन्हाळी"},
        "duration_days": 110,
        "optimal_temp": "22°C - 32°C",
        "rainfall_mm": "500 - 700 mm",
        "soil": {
            "en": "Well-drained loose sandy loam or red sandy soil with good calcium content (pH 6.0 - 7.5)",
            "hi": "अच्छी जल निकासी वाली बलुई दोमट या लाल रेतीली मिट्टी (pH 6.0 - 7.5)",
            "mr": "पाण्याचा चांगला निचरा होणारी भुसभुशीत वाळूमिश्रित किंवा लाल हलकी जमीन (pH ६.० - ७.५)",
        },
        "sowing_months": {
            "en": "June - July (Kharif), Jan - Feb (Summer)",
            "hi": "जून - जुलाई (खरीफ), जनवरी - फरवरी (जायद)",
            "mr": "जून - जुलै (खरीप), जानेवारी - फेब्रुवारी (उन्हाळी)",
        },
        "expected_yield_per_acre": "10 - 15 Quintals (Sprinkler yield increase: 40%)",
        "fertilizer_per_acre_kg": {
            "urea": 25,
            "dap": 50,
            "mop": 30,
            "gypsum": 200,
            "fym_tonnes": 4,
        },
        "growth_stages": [
            {
                "day_start": 0,
                "day_end": 25,
                "stage": {"en": "Sowing & Vegetative", "hi": "बुवाई व प्रारंभिक बढ़वार", "mr": "पेरणी व वाढ"},
                "task": {
                    "en": "Seed treatment with Rhizobium + Trichoderma (5g/kg). Apply basal: 25kg Urea + 50kg DAP + 30kg MOP per acre. Intercrop with Red gram (6:1 or 4:1) or Sunflower (6:2).",
                    "hi": "राइजोबियम + ट्राइकोडर्मा से बीज उपचार। 25 किग्रा यूरिया + 50 किग्रा DAP + 30 किग्रा MOP बेसल दें। अरहर (6:1) या सूरजमुखी (6:2) के साथ अंतरफसल लगाएं।",
                    "mr": "रायझोबियम + ट्रायकोडर्मा ने बीज प्रक्रिया. २५ किग्रॅ युरिया + ५० किग्रॅ DAP + ३० किग्रॅ MOP बेसल डोस द्या. तूर (६:१) किंवा सूर्यफुलासोबत आंतरपीक घ्या.",
                },
                "water_advice": {
                    "en": "Irrigate lightly for uniform germination.",
                    "hi": "अंकुरण के लिए हल्की सिंचाई करें।",
                    "mr": "चांगल्या उगवणीसाठी हलके पाणी द्या.",
                },
            },
            {
                "day_start": 26,
                "day_end": 55,
                "stage": {"en": "Flowering & Pegging", "hi": "फूल आना व सुइयां (पेग) जमीन में जाना", "mr": "फुलधारणा व आऱ्या जमिनीत जाणे"},
                "task": {
                    "en": "Apply 200kg Gypsum per acre at 40-45 days around root zone for calcium supply to developing pods. Avoid weeding after pegging.",
                    "hi": "40-45 दिन पर 200 किग्रा जिप्सम प्रति एकड़ जड़ों के पास डालें। सुइयां जमीन में घुसने के बाद निराई-गुड़ाई न करें।",
                    "mr": "४०-४५ दिवसांनी २०० किग्रॅ जिप्सम प्रति एकर आऱ्यांच्या भागात द्या. आऱ्या सुटल्यानंतर खुरपणी करू नये.",
                },
                "water_advice": {
                    "en": "Crucial moisture stage; soil must be soft for easy peg penetration.",
                    "hi": "अत्यंत महत्वपूर्ण अवस्था; मिट्टी नरम होनी चाहिए ताकि सुइयां आसानी से धंस सकें।",
                    "mr": "अतिसंवेदनशील काळ; आऱ्या जमिनीत सहज शिरण्यासाठी जमीन मऊ असावी.",
                },
            },
            {
                "day_start": 56,
                "day_end": 110,
                "stage": {"en": "Pod Development & Harvest", "hi": "मूंगफली भराव व खुदाई", "mr": "शेंगा भरणे व काढणी"},
                "task": {
                    "en": "Spray 0:52:34 (5g/L) + Boron (1g/L) to prevent 'pops' (empty pods). Harvest when inner shell of pod turns brownish-black. Use groundnut pod stripper.",
                    "hi": "खाली फलियों (पॉप्स) से बचने हेतु 0:52:34 + बोरॉन छिड़कें। छिलके के अंदर भूरा-काला रंग आने पर खुदाई करें।",
                    "mr": "शेंगा पोकळ राहू नयेत म्हणून ०:५२:३४ + बोरॉन फवारा. शेंगेचे आतील आवरण तपकिरी-काळे झाल्यावर काढणी करा.",
                },
                "water_advice": {
                    "en": "Give light irrigation 1-2 days before harvesting for easy pulling without leaving pods in soil.",
                    "hi": "खुदाई से 1-2 दिन पहले हल्का पानी दें ताकि पौधे खींचते समय फलियां जमीन में न टूटें।",
                    "mr": "उपटणी सुलभ व्हावी म्हणून १-२ दिवस आधी हलके पाणी द्या.",
                },
            },
        ],
        "pests_and_diseases": [
            {
                "name": {"en": "Tikka Disease (Cercospora Leaf Spot)", "hi": "टिक्का रोग (पत्ती धब्बा)", "mr": "टिक्का रोग (तांबडे ठिपके)"},
                "symptoms": {
                    "en": "Circular dark brown spots with yellow halos on upper surface, causing premature leaf shedding.",
                    "hi": "पत्तियों पर पीले घेरे वाले गोल गहरे भूरे धब्बे और पत्तियों का तेजी से झड़ना।",
                    "mr": "पानांवर पिवळ्या कडा असलेले गोल काळे-तपकिरी ठिपके व पाने गळणे.",
                },
                "organic_remedy": {
                    "en": "Spray Pseudomonas fluorescens @ 10g/L or Cow urine + Neem oil spray.",
                    "hi": "स्यूडोमोनास फ्लोरोसेंस 10 ग्राम/ली. या गोमूत्र + नीम तेल का छिड़काव करें।",
                    "mr": "स्यूडोमोनास फ्लोरोसन्स १० ग्रॅम/ली. किंवा गोमूत्र + कडुलिंब तेल फवारा.",
                },
                "chemical_remedy": {
                    "en": "Spray Carbendazim 12% + Mancozeb 63% WP (Saaf) @ 2g/L or Hexaconazole 5% EC @ 2ml/L.",
                    "hi": "कार्बेंडाजिम 12% + मैंकोजेब 63% WP (साफ) 2 ग्राम/ली. या हेक्साकोनाजोल 2 मिली/ली. छिड़कें।",
                    "mr": "कार्बेंडाझिम १२% + मॅन्कोझेब ६३% WP (साफ) २ ग्रॅम/ली. किंवा हेक्झाकोनाझोल २ मिली/ली. फवारा.",
                },
            },
        ],
    },
}

CATEGORIES = {
    "cereals": {"en": "Cereals & Grains", "hi": "अनाज व खाद्यान्न", "mr": "तृणधान्ये"},
    "cash_crops": {"en": "Cash & Commercial Crops", "hi": "व्यावसायिक व नकदी फसलें", "mr": "नगदी पिके"},
    "pulses_oilseeds": {"en": "Pulses & Oilseeds", "hi": "दलहन व तिलहन", "mr": "कडधान्ये व गळित धान्ये"},
    "vegetables": {"en": "Vegetables & Horticulture", "hi": "सब्जियां व बागवानी", "mr": "भाजीपाला"},
    "fruits": {"en": "Fruit Crops & Orchards", "hi": "फल एवं बागवानी फसलें", "mr": "फळबाग पिके"},
}

# Critical stages for irrigation from Handbook
CRITICAL_IRRIGATION_STAGES = [
    {
        "crop": {"en": "Rice (Paddy)", "hi": "धान", "mr": "भात"},
        "stages": {"en": "Tillering, Panicle Initiation, Heading and Flowering", "hi": "कल्ले निकलना, बाली बनना, फूल आना", "mr": "फुटवे फुटणे, पोंगा अवस्था, लोंबी बाहेर पडणे, फुलधारणा"}
    },
    {
        "crop": {"en": "Wheat", "hi": "गेहूं", "mr": "गहू"},
        "stages": {"en": "Crown Root Initiation (CRI at 21 days), Tillering to Booting, Flowering, Milking", "hi": "CRI मुकुट जड़ (21 दिन), कल्ले फूटना, गोभ अवस्था, दुग्ध अवस्था", "mr": "CRI मुकुट मुळे (२१ दिवस), फुटवे, पोंगा अवस्था, दाणे भरणे"}
    },
    {
        "crop": {"en": "Maize", "hi": "मक्का", "mr": "मका"},
        "stages": {"en": "Silking and Tasseling to Dough Stage", "hi": "नर मंजरी व भुट्टा (सिल्क) निकलने से दाना बनने तक", "mr": "तुरा येणे व कणसाचे केस बाहेर पडण्यापासून दाणे भरेपर्यंत"}
    },
    {
        "crop": {"en": "Chickpea / Gram", "hi": "चना", "mr": "हरभरा"},
        "stages": {"en": "Late Vegetative Stage and Pod Filling", "hi": "फूल आने से ठीक पहले व घाटी भराव अवस्था", "mr": "फुलधारणेपूर्वी व घाटे भरण्याची अवस्था"}
    },
    {
        "crop": {"en": "Cotton", "hi": "कपास", "mr": "कापूस"},
        "stages": {"en": "Square Formation, Flowering and Boll Development", "hi": "कलियां (स्क्वायर) बनना, फूल आना और टिंडे का विकास", "mr": "पाते लागणे, फुलधारणा व बोंड विकास अवस्था"}
    },
    {
        "crop": {"en": "Groundnut", "hi": "मूंगफली", "mr": "भुईमूग"},
        "stages": {"en": "Flowering, Peg Formation and Pod Development", "hi": "फूल आना, सुइयां (पेग) जमीन में घुसना व फली भराव", "mr": "फुलधारणा, आऱ्या जमिनीत शिरणे व शेंगा भरणे"}
    },
    {
        "crop": {"en": "Soybean", "hi": "सोयाबीन", "mr": "सोयाबीन"},
        "stages": {"en": "Blooming and Seed/Pod Formation", "hi": "फूल खिलना व फली दाना भराव अवस्था", "mr": "फुलधारणा व शेंगांमध्ये दाणे भरणे"}
    },
    {
        "crop": {"en": "Tomato", "hi": "टमाटर", "mr": "टोमॅटो"},
        "stages": {"en": "Flowering, Fruit Setting and Fruit Enlargement", "hi": "फूल आना, फल बनना व फलों का आकार बढ़ना", "mr": "फुलधारणा, फळधारणा व फळांची वाढ"}
    },
    {
        "crop": {"en": "Onion", "hi": "प्याज", "mr": "कांदा"},
        "stages": {"en": "Bulb Formation and Pre-maturity", "hi": "कंद (गांठ) बनना व पकने से पूर्व", "mr": "कांदा फुगवण व काढणीपूर्वीची अवस्था"}
    },
    {
        "crop": {"en": "Potato", "hi": "आलू", "mr": "बटाटा"},
        "stages": {"en": "Tuber Initiation to Tuber Bulking", "hi": "कंद बनना व कंद का आकार बढ़ना", "mr": "बटाटा लागणे व बटाटा फुगवण अवस्था"}
    },
    {
        "crop": {"en": "Banana", "hi": "केला", "mr": "केळी"},
        "stages": {"en": "Shooting, Bunch Emergence and Bunch Development", "hi": "कमल निकलना, घार बाहर आना व घार का विकास", "mr": "केळफूल बाहेर पडणे, घड धरणे व घड भरणे"}
    },
    {
        "crop": {"en": "Nagpur Mandarin (Citrus)", "hi": "नागपुर संतरा", "mr": "नागपूर संत्रा"},
        "stages": {"en": "Flowering, Fruit Setting and Fruit Enlargement", "hi": "फूल आना, फल बनना व फलों का आकार बढ़ना", "mr": "मोहर येणे, फळधारणा व फळांची वाढ"}
    },
    {
        "crop": {"en": "Mango", "hi": "आम", "mr": "आंबा"},
        "stages": {"en": "Fruit Setting and Pea-size Stage", "hi": "फल बनने व मटर के दाने के बराबर होने पर", "mr": "फळधारणा व वाटाण्याच्या आकाराची फळे असताना"}
    }
]

# Sprinkler and Drip response & water savings from Handbook
DRIP_SPRINKLER_BENEFITS = {
    "drip": [
        {"crop": {"en": "Sugarcane", "hi": "गन्ना", "mr": "ऊस"}, "water_saving": "49.3%", "yield_increase": "133.3%"},
        {"crop": {"en": "Pomegranate", "hi": "अनार", "mr": "डाळिंब"}, "water_saving": "45.0%", "yield_increase": "98.0%"},
        {"crop": {"en": "Cotton", "hi": "कपास", "mr": "कापूस"}, "water_saving": "46.6%", "yield_increase": "88.0%"},
        {"crop": {"en": "Mango", "hi": "आम", "mr": "आंबा"}, "water_saving": "34.8%", "yield_increase": "80.0%"},
        {"crop": {"en": "Potato", "hi": "आलू", "mr": "बटाटा"}, "water_saving": "54.1%", "yield_increase": "79.5%"},
        {"crop": {"en": "Banana", "hi": "केला", "mr": "केळी"}, "water_saving": "45.0%", "yield_increase": "52.0%"},
        {"crop": {"en": "Onion", "hi": "प्याज", "mr": "कांदा"}, "water_saving": "46.1%", "yield_increase": "53.8%"},
        {"crop": {"en": "Tomato", "hi": "टमाटर", "mr": "टोमॅटो"}, "water_saving": "39.0%", "yield_increase": "50.0%"},
    ],
    "sprinkler": [
        {"crop": {"en": "Gram / Chickpea", "hi": "चना", "mr": "हरभरा"}, "water_saving": "69.0%", "yield_increase": "57.0%"},
        {"crop": {"en": "Cotton", "hi": "कपास", "mr": "कापूस"}, "water_saving": "36.0%", "yield_increase": "50.0%"},
        {"crop": {"en": "Groundnut", "hi": "मूंगफली", "mr": "भुईमूग"}, "water_saving": "20.0%", "yield_increase": "40.0%"},
        {"crop": {"en": "Maize", "hi": "मक्का", "mr": "मका"}, "water_saving": "41.0%", "yield_increase": "36.0%"},
        {"crop": {"en": "Wheat", "hi": "गेहूं", "mr": "गहू"}, "water_saving": "35.0%", "yield_increase": "24.0%"},
        {"crop": {"en": "Chillies", "hi": "मिर्च", "mr": "मिरची"}, "water_saving": "33.0%", "yield_increase": "24.0%"},
        {"crop": {"en": "Onion", "hi": "प्याज", "mr": "कांदा"}, "water_saving": "33.0%", "yield_increase": "23.0%"},
    ]
}

# Seed types and purity standards from Handbook
SEED_CLASSES = [
    {"type": {"en": "Nucleus Seed", "hi": "नाभिकीय बीज (न्यूक्लियस)", "mr": "केंद्रक बियाणे"}, "purity": "100%", "tag": {"en": "None (Breeder maintain)", "hi": "कोई टैग नहीं", "mr": "टॅग नाही"}},
    {"type": {"en": "Breeder Seed", "hi": "प्रजनक बीज (ब्रीडर)", "mr": "प्रजनक बियाणे"}, "purity": "100%", "tag": {"en": "Golden Yellow Tag", "hi": "सुनहरा पीला टैग", "mr": "सोनेरी पिवळा टॅग"}},
    {"type": {"en": "Foundation Seed", "hi": "आधार बीज (फाउंडेशन)", "mr": "पायाभूत बियाणे"}, "purity": "99.5%", "tag": {"en": "White Tag", "hi": "सफेद टैग", "mr": "पांढरा टॅग"}},
    {"type": {"en": "Certified Seed", "hi": "प्रमाणित बीज (सर्टिफाइड)", "mr": "प्रमाणित बियाणे"}, "purity": "99.0%", "tag": {"en": "Azure Blue Tag", "hi": "आसमानी नीला टैग (Azar Blue)", "mr": "आकाशी निळा टॅग"}}
]


def calculate_crop_plan(crop_id, sowing_date_str="2026-06-01", land_size_val=1.0, unit="acre", yield_per_acre=None, price_per_quintal=None, cost_per_acre=None):
    """
    Calculate comprehensive agronomic timeline, fertilizer requirements, and Farm Profitability Economics (B:C Ratio).
    Supported units: acre, hectare (1 ha = 2.471 acres), guntha (40 guntha = 1 acre), bigha (1.6 bigha = 1 acre approx).
    """
    crop = CROPS.get(crop_id, CROPS["wheat"])

    try:
        sowing_date = datetime.strptime(sowing_date_str, "%Y-%m-%d")
    except (ValueError, TypeError):
        sowing_date = datetime.now()

    try:
        size = float(land_size_val)
        if size <= 0:
            size = 1.0
    except (ValueError, TypeError):
        size = 1.0

    # Convert land unit to acres
    unit_lower = str(unit).lower()
    if "hect" in unit_lower or unit_lower == "ha":
        acres = size * 2.471
    elif "guntha" in unit_lower:
        acres = size / 40.0
    elif "bigha" in unit_lower:
        acres = size / 1.6
    else:
        acres = size

    # Scale fertilizers
    scaled_fertilizers = {}
    for fert_key, fert_amount in crop.get("fertilizer_per_acre_kg", {}).items():
        scaled_fertilizers[fert_key] = round(fert_amount * acres, 1)

    # Compute timeline dates
    milestones = []
    for stage_info in crop.get("growth_stages", []):
        start_day = stage_info["day_start"]
        end_day = stage_info["day_end"]
        target_start_date = sowing_date + timedelta(days=start_day)
        target_end_date = sowing_date + timedelta(days=end_day)

        milestones.append({
            "stage": stage_info["stage"],
            "day_range": f"Day {start_day} - {end_day}",
            "start_date": target_start_date.strftime("%d %b %Y"),
            "end_date": target_end_date.strftime("%d %b %Y"),
            "task": stage_info["task"],
            "water_advice": stage_info.get("water_advice", {}),
        })

    harvest_date = sowing_date + timedelta(days=crop.get("duration_days", 120))

    # Economics & Profitability Calculator (B:C Ratio)
    crop_defaults = {
        "rice": {"yield": 24.0, "price": 2300, "cost": 28000},
        "wheat": {"yield": 20.0, "price": 2275, "cost": 22000},
        "cotton": {"yield": 12.0, "price": 7121, "cost": 35000},
        "sugarcane": {"yield": 400.0, "price": 315, "cost": 55000},
        "onion": {"yield": 100.0, "price": 1800, "cost": 45000},
        "soybean": {"yield": 10.0, "price": 4892, "cost": 18000},
        "banana": {"yield": 280.0, "price": 1400, "cost": 65000},
        "maize": {"yield": 25.0, "price": 2090, "cost": 20000},
        "gram": {"yield": 9.0, "price": 5440, "cost": 16000},
        "groundnut": {"yield": 11.0, "price": 6377, "cost": 24000},
    }

    c_def = crop_defaults.get(crop_id, {"yield": 20.0, "price": 2500, "cost": 25000})

    try:
        y_acre = float(yield_per_acre) if yield_per_acre is not None and float(yield_per_acre) > 0 else c_def["yield"]
    except (ValueError, TypeError):
        y_acre = c_def["yield"]

    try:
        p_quintal = float(price_per_quintal) if price_per_quintal is not None and float(price_per_quintal) > 0 else c_def["price"]
    except (ValueError, TypeError):
        p_quintal = c_def["price"]

    try:
        c_acre = float(cost_per_acre) if cost_per_acre is not None and float(cost_per_acre) > 0 else c_def["cost"]
    except (ValueError, TypeError):
        c_acre = c_def["cost"]

    total_yield = y_acre * acres
    gross_revenue = total_yield * p_quintal
    total_cost = c_acre * acres
    net_profit = gross_revenue - total_cost
    net_profit_per_acre = net_profit / acres if acres > 0 else net_profit

    bc_ratio = round(gross_revenue / total_cost, 2) if total_cost > 0 else 1.0
    if bc_ratio >= 1.25:
        bc_status = "healthy"
    elif bc_ratio >= 1.0:
        bc_status = "low_margin"
    else:
        bc_status = "loss_risk"

    return {
        "crop": crop,
        "sowing_date": sowing_date.strftime("%d %b %Y"),
        "harvest_date": harvest_date.strftime("%d %b %Y"),
        "land_size": size,
        "unit": unit,
        "acres_calculated": round(acres, 2),
        "fertilizers": scaled_fertilizers,
        "milestones": milestones,
        "economics": {
            "yield_per_acre": y_acre,
            "price_per_quintal": p_quintal,
            "cost_per_acre": c_acre,
            "total_yield": round(total_yield, 1),
            "gross_revenue": round(gross_revenue),
            "total_cost": round(total_cost),
            "net_profit": round(net_profit),
            "net_profit_per_acre": round(net_profit_per_acre),
            "bc_ratio": bc_ratio,
            "bc_status": bc_status,
        }
    }
