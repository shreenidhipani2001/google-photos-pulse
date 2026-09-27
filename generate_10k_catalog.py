import os
import random
import datetime
import hashlib
import pandas as pd
from utils.data_loader import generate_sample_photo_catalog, normalize_catalog_dataframe

# Context-perfect real images for all 35 ground-truth benchmark photos
BENCHMARK_IMAGES = {
    "IMG_20250114_091522": "https://images.unsplash.com/photo-1584308666744-24d5c474f2ae?w=600&auto=format&fit=crop&q=80", # Paracetamol medicine box & pills
    "IMG_20241108_164530": "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=600&auto=format&fit=crop&q=80", # Beach cafe & blue sunset chairs Goa
    "IMG_20231224_173010": "https://images.unsplash.com/photo-1556910103-1c02745aae4d?w=600&auto=format&fit=crop&q=80", # Handwritten recipe card & pasta
    "IMG_20240905_131045": "https://images.unsplash.com/photo-1436491865332-7a61a109cc05?w=600&auto=format&fit=crop&q=80", # Airport boarding pass to Paris
    "IMG_20240120_112204": "https://images.unsplash.com/photo-1552053831-71594a27632d?w=600&auto=format&fit=crop&q=80", # Golden retriever in snow
    "IMG_20240618_211550": "https://images.unsplash.com/photo-1554415707-9e44667664d8?w=600&auto=format&fit=crop&q=80", # Trattoria dinner receipt
    "IMG_20241012_084012": "https://images.unsplash.com/photo-1506521781263-d8422e82f27a?w=600&auto=format&fit=crop&q=80", # Level 3 Blue Pillar parking garage
    "IMG_20240722_190415": "https://images.unsplash.com/photo-1570168007204-dfb528c6958f?w=600&auto=format&fit=crop&q=80", # Marine Drive Mumbai sunset
    "IMG_20240315_142010": "https://images.unsplash.com/photo-1544197150-b99a580bb7a8?w=600&auto=format&fit=crop&q=80", # Wi-Fi router password barcode
    "IMG_20240504_154022": "https://images.unsplash.com/photo-1535141192574-5d4897c13136?w=600&auto=format&fit=crop&q=80", # 5th Birthday Dinosaur cake
    "IMG_20230819_161545": "https://images.unsplash.com/photo-1541899481282-d53bffe3c35d?w=600&auto=format&fit=crop&q=80", # Turquoise vintage Beetle car
    "IMG_20240402_105500": "https://images.unsplash.com/photo-1628009368231-7bb7cfcb0def?w=600&auto=format&fit=crop&q=80", # Dog rabies vaccination certificate
    "IMG_20240810_134015": "https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?w=600&auto=format&fit=crop&q=80", # Mount Rainier trail signpost
    "IMG_20240211_170530": "https://images.unsplash.com/photo-1496181133206-80ce9b88a853?w=600&auto=format&fit=crop&q=80", # Laptop barcode sticker
    "IMG_20240630_221015": "https://images.unsplash.com/photo-1563245372-f21724e3856d?w=600&auto=format&fit=crop&q=80", # Neon wings art exhibition
    "IMG_20230914_194510": "https://images.unsplash.com/photo-1510812431401-41d2bd2722f3?w=600&auto=format&fit=crop&q=80", # Chateau Margaux wine bottle
    "IMG_20241025_213045": "https://images.unsplash.com/photo-1470225620780-dba8ba36b745?w=600&auto=format&fit=crop&q=80", # Concert crowd yellow coat
    "IMG_20240329_152010": "https://images.unsplash.com/photo-1501339847302-ac426a4a7cbb?w=600&auto=format&fit=crop&q=80", # Coffee napkin guitar chords
    "IMG_20240516_114520": "https://images.unsplash.com/photo-1586528116311-ad8dd3c8310d?w=600&auto=format&fit=crop&q=80", # USPS thermal tracking receipt
    "IMG_20230715_231500": "https://images.unsplash.com/photo-1510312305653-8ed496efae75?w=600&auto=format&fit=crop&q=80", # Desert camping tent Milky Way
    "IMG_20230521_143000": "https://images.unsplash.com/photo-1523050854058-8df90110c9f1?w=600&auto=format&fit=crop&q=80", # University graduation diploma
    "IMG_20240804_111030": "https://images.unsplash.com/photo-1581783342308-f792dbdd27c5?w=600&auto=format&fit=crop&q=80", # Stanley tape measure drawer
    "IMG_20240428_085012": "https://images.unsplash.com/photo-1502602898657-3e91760cbb34?w=600&auto=format&fit=crop&q=80", # Paris balcony Eiffel tower
    "IMG_20240918_102040": "https://images.unsplash.com/photo-1579684385127-1ef15d508118?w=600&auto=format&fit=crop&q=80", # LabCorp blood test report
    "IMG_20240218_153022": "https://images.unsplash.com/photo-1555252333-9f8e92e65df9?w=600&auto=format&fit=crop&q=80", # Baby sleeping with plush elephant
    "IMG_20241005_164510": "https://images.unsplash.com/photo-1503376780353-7e6692767b70?w=600&auto=format&fit=crop&q=80", # Rental car bumper scratch
    "IMG_20240612_101500": "https://images.unsplash.com/photo-1534778101976-62847782c213?w=600&auto=format&fit=crop&q=80", # Swan latte art flat white
    "IMG_20231014_204015": "https://images.unsplash.com/photo-1519741497674-611481863552?w=600&auto=format&fit=crop&q=80", # Wedding champagne toast flutes
    "IMG_20240118_093045": "https://images.unsplash.com/photo-1617788138017-80ad40651399?w=600&auto=format&fit=crop&q=80", # Car door tire pressure decal
    "IMG_20240308_221530": "https://images.unsplash.com/photo-1565299585323-38d6b0865b47?w=600&auto=format&fit=crop&q=80", # Mexico City taco truck neon
    "IMG_20241215_141020": "https://images.unsplash.com/photo-1542990253-0d0f5be5f0ed?w=600&auto=format&fit=crop&q=80", # Aspen hot cocoa marshmallows
    "IMG_20240530_164010": "https://images.unsplash.com/photo-1525310072745-f49212b5ac6d?w=600&auto=format&fit=crop&q=80", # Purple moth orchid macro
    "IMG_20231128_185030": "https://images.unsplash.com/photo-1507842229450-782124d4e0e3?w=600&auto=format&fit=crop&q=80", # Independent bookstore bookshelves
    "IMG_20240704_214500": "https://images.unsplash.com/photo-1498931299472-f7a63a5a1cfa?w=600&auto=format&fit=crop&q=80", # 4th July lake fireworks
    "IMG_20250210_123015": "https://images.unsplash.com/photo-1471864190281-a93a3070b6de?w=600&auto=format&fit=crop&q=80"  # CVS pharmacy prescription vial
}

# Curated pools of real high-resolution Unsplash photography by category
CATEGORY_IMAGE_POOLS = {
    "Travel & Nature": [
        "https://images.unsplash.com/photo-1506744038136-46273834b3fb?w=600&auto=format&fit=crop&q=80", # Yosemite valley
        "https://images.unsplash.com/photo-1469474968028-56623f02e42e?w=600&auto=format&fit=crop&q=80", # Mountain nature
        "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=600&auto=format&fit=crop&q=80", # Tropical beach
        "https://images.unsplash.com/photo-1476514525535-07fb3b4ae5f1?w=600&auto=format&fit=crop&q=80", # Lake boat
        "https://images.unsplash.com/photo-1502602898657-3e91760cbb34?w=600&auto=format&fit=crop&q=80", # Paris street
        "https://images.unsplash.com/photo-1512453979798-5ea266f8880c?w=600&auto=format&fit=crop&q=80", # Dubai skyline
        "https://images.unsplash.com/photo-1493976040374-85c8e12f0c0e?w=600&auto=format&fit=crop&q=80", # Kyoto bamboo
        "https://images.unsplash.com/photo-1488646953014-85cb44e25828?w=600&auto=format&fit=crop&q=80", # Travel map
        "https://images.unsplash.com/photo-1470071459604-3b5ec3a7fe05?w=600&auto=format&fit=crop&q=80", # Foggy mountain
        "https://images.unsplash.com/photo-1447752875215-b2761acb3c5d?w=600&auto=format&fit=crop&q=80"  # Forest sunlight
    ],
    "Food & Dining": [
        "https://images.unsplash.com/photo-1555396273-367ea4eb4db5?w=600&auto=format&fit=crop&q=80", # Restaurant interior
        "https://images.unsplash.com/photo-1565299624946-b28f40a0ae38?w=600&auto=format&fit=crop&q=80", # Artisan pizza
        "https://images.unsplash.com/photo-1568901346375-23c9450c58cd?w=600&auto=format&fit=crop&q=80", # Gourmet burger
        "https://images.unsplash.com/photo-1546069901-ba9599a7e63c?w=600&auto=format&fit=crop&q=80", # Fresh salad bowl
        "https://images.unsplash.com/photo-1567620905732-2d1ec7ab7445?w=600&auto=format&fit=crop&q=80", # Pancakes breakfast
        "https://images.unsplash.com/photo-1501339847302-ac426a4a7cbb?w=600&auto=format&fit=crop&q=80", # Coffee shop brew
        "https://images.unsplash.com/photo-1551024709-8f23befc6f87?w=600&auto=format&fit=crop&q=80", # Sweet dessert
        "https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?w=600&auto=format&fit=crop&q=80", # Trattoria dining table
        "https://images.unsplash.com/photo-1565299585323-38d6b0865b47?w=600&auto=format&fit=crop&q=80", # Mexican tacos
        "https://images.unsplash.com/photo-1534778101976-62847782c213?w=600&auto=format&fit=crop&q=80"  # Latte art
    ],
    "Family & Celebrations": [
        "https://images.unsplash.com/photo-1511632765486-a01980e01a18?w=600&auto=format&fit=crop&q=80", # Family gathering
        "https://images.unsplash.com/photo-1535141192574-5d4897c13136?w=600&auto=format&fit=crop&q=80", # Birthday cake candles
        "https://images.unsplash.com/photo-1519741497674-611481863552?w=600&auto=format&fit=crop&q=80", # Wedding celebration
        "https://images.unsplash.com/photo-1523050854058-8df90110c9f1?w=600&auto=format&fit=crop&q=80", # Graduation ceremony
        "https://images.unsplash.com/photo-1555252333-9f8e92e65df9?w=600&auto=format&fit=crop&q=80", # Baby smiling
        "https://images.unsplash.com/photo-1548199973-03cce0bbc87b?w=600&auto=format&fit=crop&q=80", # Pets playing in park
        "https://images.unsplash.com/photo-1513151233558-d860c5398176?w=600&auto=format&fit=crop&q=80", # Holiday party lights
        "https://images.unsplash.com/photo-1464349095431-e9a21285b5f3?w=600&auto=format&fit=crop&q=80", # Birthday balloons
        "https://images.unsplash.com/photo-1530103862676-de8c9debad1d?w=600&auto=format&fit=crop&q=80", # Celebration confetti
        "https://images.unsplash.com/photo-1527529482837-4698179dc6ce?w=600&auto=format&fit=crop&q=80"  # Friends toast
    ],
    "Documents & Receipts": [
        "https://images.unsplash.com/photo-1554415707-9e44667664d8?w=600&auto=format&fit=crop&q=80", # Receipt & calculator
        "https://images.unsplash.com/photo-1450133064473-71024230f91b?w=600&auto=format&fit=crop&q=80", # Documents & paperwork
        "https://images.unsplash.com/photo-1436491865332-7a61a109cc05?w=600&auto=format&fit=crop&q=80", # Airline boarding pass
        "https://images.unsplash.com/photo-1455390582262-044cdead277a?w=600&auto=format&fit=crop&q=80", # Handwritten cursive notes
        "https://images.unsplash.com/photo-1586528116311-ad8dd3c8310d?w=600&auto=format&fit=crop&q=80", # Shipping label & tracking
        "https://images.unsplash.com/photo-1568667256549-094345857637?w=600&auto=format&fit=crop&q=80", # Stamp and document
        "https://images.unsplash.com/photo-1607344645866-009c320c5ab8?w=600&auto=format&fit=crop&q=80", # Official paperwork
        "https://images.unsplash.com/photo-1589829545856-d10d557cf95f?w=600&auto=format&fit=crop&q=80"  # Legal contract paper
    ],
    "Health & Medical": [
        "https://images.unsplash.com/photo-1584308666744-24d5c474f2ae?w=600&auto=format&fit=crop&q=80", # Pill blister pack & box
        "https://images.unsplash.com/photo-1471864190281-a93a3070b6de?w=600&auto=format&fit=crop&q=80", # Medicine bottles
        "https://images.unsplash.com/photo-1579684385127-1ef15d508118?w=600&auto=format&fit=crop&q=80", # Medical laboratory test
        "https://images.unsplash.com/photo-1584515979956-d9f6e5d09982?w=600&auto=format&fit=crop&q=80", # Healthcare thermometer
        "https://images.unsplash.com/photo-1583912267670-6575ad4736f8?w=600&auto=format&fit=crop&q=80", # First aid kit supplies
        "https://images.unsplash.com/photo-1505751172876-fa1923c5c528?w=600&auto=format&fit=crop&q=80", # Medical stethoscope
        "https://images.unsplash.com/photo-1584017911766-d451b3d0e843?w=600&auto=format&fit=crop&q=80"  # Pharmacy counter capsules
    ],
    "Automotive & Parking": [
        "https://images.unsplash.com/photo-1506521781263-d8422e82f27a?w=600&auto=format&fit=crop&q=80", # Parking garage pillars
        "https://images.unsplash.com/photo-1590674899484-d5640e854abe?w=600&auto=format&fit=crop&q=80", # Multi-story parking lot
        "https://images.unsplash.com/photo-1541899481282-d53bffe3c35d?w=600&auto=format&fit=crop&q=80", # Classic vintage car
        "https://images.unsplash.com/photo-1503376780353-7e6692767b70?w=600&auto=format&fit=crop&q=80", # Modern sports car
        "https://images.unsplash.com/photo-1617788138017-80ad40651399?w=600&auto=format&fit=crop&q=80", # Automobile interior
        "https://images.unsplash.com/photo-1492144534655-ae79c964c9d7?w=600&auto=format&fit=crop&q=80", # Highway night road
        "https://images.unsplash.com/photo-1568605117036-5fe5e7bab0b7?w=600&auto=format&fit=crop&q=80"  # Vehicle on coastal road
    ],
    "Home & Personal": [
        "https://images.unsplash.com/photo-1544197150-b99a580bb7a8?w=600&auto=format&fit=crop&q=80", # Wi-Fi router setup
        "https://images.unsplash.com/photo-1496181133206-80ce9b88a853?w=600&auto=format&fit=crop&q=80", # Home office laptop
        "https://images.unsplash.com/photo-1507842229450-782124d4e0e3?w=600&auto=format&fit=crop&q=80", # Bookshelf reading nook
        "https://images.unsplash.com/photo-1484154218962-a197022b5858?w=600&auto=format&fit=crop&q=80", # Modern kitchen
        "https://images.unsplash.com/photo-1581783342308-f792dbdd27c5?w=600&auto=format&fit=crop&q=80", # DIY wood workshop
        "https://images.unsplash.com/photo-1525310072745-f49212b5ac6d?w=600&auto=format&fit=crop&q=80", # Indoor potted plants
        "https://images.unsplash.com/photo-1513694203232-719a280e022f?w=600&auto=format&fit=crop&q=80"  # Cozy bedroom corner
    ]
}

def get_image_for_photo(photo_id: str, category: str) -> str:
    """Deterministically assign a real photographic image URL."""
    if photo_id in BENCHMARK_IMAGES:
        return BENCHMARK_IMAGES[photo_id]

    pool = CATEGORY_IMAGE_POOLS.get(category, CATEGORY_IMAGE_POOLS["Travel & Nature"])
    # Deterministic hash to guarantee stable photo URL per photo_id
    h = int(hashlib.md5(photo_id.encode('utf-8')).hexdigest(), 16)
    return pool[h % len(pool)]


def generate_10k_photo_catalog():
    print("[10k Generator] Loading ground-truth benchmark photos...")
    df_benchmark = generate_sample_photo_catalog()
    num_benchmark = len(df_benchmark)
    print(f"[10k Generator] Preserved {num_benchmark} benchmark test photos at indices 0-{num_benchmark - 1}.")

    # Add real image URLs to benchmark photos
    benchmark_urls = []
    for idx, row in df_benchmark.iterrows():
        pid = row["photo_id"]
        cat = row.get("category") or row.get("album_name") or "General"
        benchmark_urls.append(get_image_for_photo(pid, cat))
    df_benchmark["image_url"] = benchmark_urls

    num_needed = 10000 - num_benchmark
    print(f"[10k Generator] Procedurally generating {num_needed} realistic multimodal photo records with real images...")

    random.seed(42)

    categories_and_albums = [
        ("Travel & Nature", [
            "Summer Road Trip", "Weekend Hikes", "Beach Vacations", "National Parks", 
            "Mountain Summits", "Desert Trails", "European Holiday", "Tropical Getaways", "Winter Landscapes"
        ]),
        ("Food & Dining", [
            "Culinary Adventures", "Artisan Coffee & Cafes", "Street Food Markets", "Home Cooked Feasts",
            "Baking & Pastries", "Fine Dining & Anniversaries", "Cocktails & Lounges", "Farmers Market"
        ]),
        ("Family & Celebrations", [
            "Family Reunions", "Birthday Parties", "Holiday Gatherings", "Weddings & Receptions",
            "Baby Milestones", "Graduation Days", "Weekend Barbecues", "Pets & Playtime"
        ]),
        ("Documents & Receipts", [
            "Tax & Financial Records", "Travel Tickets & Itineraries", "Warranty Cards & Manuals",
            "Medical & Lab Slips", "Store Receipts & Invoices", "Handwritten Notes & Recipes", "Official IDs"
        ]),
        ("Health & Medical", [
            "Prescriptions & Medicines", "Vaccination Records", "Fitness & Gym Progress", 
            "Doctor Consultation Summaries", "Dental & Vision Records", "First Aid & Wellness"
        ]),
        ("Automotive & Parking", [
            "Vehicle Maintenance", "Parking Garages & Levels", "Road Trips & Mileage",
            "Classic Cars & Meets", "Rental Car Inspections", "Garage Utilities"
        ]),
        ("Home & Personal", [
            "Home Remodel & Interior", "Garden & Botany", "Electronics & Setup",
            "Books & Reading Corners", "Art & Craft Projects", "Closet & Fashion", "DIY Workshop"
        ])
    ]

    locations = [
        ("Goa, India", ["Calangute Beach", "Panjim Latin Quarter", "Anjuna Cliff", "Vagator Fort"]),
        ("Mumbai, India", ["Marine Drive", "Bandra Bandstand", "Colaba Causeway", "Juhu Beach"]),
        ("Tokyo, Japan", ["Shinjuku Golden Gai", "Shibuya Crossing", "Asakusa Sensoji", "Ueno Park"]),
        ("Kyoto, Japan", ["Arashiyama Bamboo Grove", "Fushimi Inari", "Gion District", "Kinkaku-ji"]),
        ("Paris, France", ["Montmartre Steps", "Eiffel Tower Champ de Mars", "Louvre Courtyard", "Le Marais Cafe"]),
        ("Rome, Italy", ["Trastevere Piazza", "Colosseum Promenade", "Trevi Fountain", "Pantheon Steps"]),
        ("Florence, Italy", ["Ponte Vecchio", "Piazza del Duomo", "Boboli Gardens", "Piazzale Michelangelo"]),
        ("New York, USA", ["Central Park Bethesda Terrace", "Times Square", "Brooklyn Bridge Walkway", "SoHo Cobblestones"]),
        ("San Francisco, USA", ["Golden Gate Vista Point", "Fisherman's Wharf", "Mission Dolores Park", "Twin Peaks"]),
        ("Seattle, USA", ["Pike Place Market", "Chihuly Garden", "Kerry Park", "Alki Beach"]),
        ("Austin, USA", ["South Congress Ave", "Zilker Metropolitan Park", "Lady Bird Lake Trail", "East Austin Patio"]),
        ("Denver, USA", ["Red Rocks Amphitheater", "LoDo Historic District", "Larimer Square", "Union Station"]),
        ("Boston, USA", ["Beacon Hill Acorn St", "Boston Common", "Faneuil Hall Marketplace", "North End Italian Alley"]),
        ("Chicago, USA", ["Millennium Park Cloud Gate", "Navy Pier", "Riverwalk Promenade", "Lincoln Park Zoo"]),
        ("London, UK", ["Borough Market", "Covent Garden Plaza", "Hyde Park Serpentine", "Tower Bridge Walk"]),
        ("Zurich, Switzerland", ["Lake Zurich Promenade", "Altstadt Old Town", "Lindenhof Hill", "Bahnhofstrasse"]),
        ("Barcelona, Spain", ["Park Guell", "Gothic Quarter Alley", "Barceloneta Beach Promenade", "Sagrada Familia Plaza"]),
        ("Amsterdam, Netherlands", ["Jordaan Canal Bridge", "Vondelpark Meadow", "Rijksmuseum Courtyard", "Prinsengracht"]),
        ("Sydney, Australia", ["Bondi to Coogee Coastal Walk", "Sydney Opera House Forecourt", "Circular Quay", "The Rocks"]),
        ("Singapore", ["Gardens by the Bay Supertrees", "Marina Bay Sands Promenade", "Chinatown Heritage Street", "Sentosa Beach"]),
        ("Honolulu, Hawaii", ["Waikiki Beachfront", "Diamond Head Summit Trail", "North Shore Surf Break", "Hanauma Bay"]),
        ("Reykjavik, Iceland", ["Hallgrimskirkja Plaza", "Harpa Concert Hall Waterfront", "Old Harbour Walk", "Laugavegur Street"]),
        ("Aspen, Colorado", ["Aspen Snowmass Base", "Downtown Aspen Pedestrian Mall", "Maroon Bells Lake", "Silver Queen Gondola"]),
        ("Vancouver, Canada", ["Stanley Park Seawall", "Granville Island Public Market", "Gastown Steam Clock", "Capilano Suspension Bridge"]),
        ("Seoul, South Korea", ["Bukchon Hanok Village", "Myeongdong Night Market", "Hongdae Arts Street", "N Seoul Tower Vista"])
    ]

    objects_pool = {
        "Travel & Nature": [
            "mountain ridge", "crystal alpine lake", "sandy beach shore", "sunset horizon", "pine forest trail",
            "hiking boots", "wooden bridge", "granite boulders", "waterfall cascade", "ocean waves", "camping backpack",
            "wildflowers", "coastal cliffs", "scenic lookout", "blue sky", "passing clouds", "sunglasses", "map"
        ],
        "Food & Dining": [
            "steaming espresso cup", "latte art rosette", "artisan sourdough bread", "ceramic bowl of ramen",
            "wood-fired neapolitan pizza", "fresh pasta noodles", "cutting board", "wine glass with pinot noir",
            "colorful street tacos with cilantro", "glazed fruit tart", "cast iron skillet", "chopsticks", "menu card"
        ],
        "Family & Celebrations": [
            "celebration birthday cake", "lit candles", "colorful party streamers", "champagne flutes", "family dining table",
            "laughing child", "golden retriever dog", "holiday gift boxes with ribbon", "wrapped presents", "indoor fairy lights",
            "graduation mortarboard cap", "toast clinking glasses", "outdoor backyard grill"
        ],
        "Documents & Receipts": [
            "thermal printed paper receipt", "credit card transaction slip", "printed boarding pass ticket", "airline logo",
            "passport book cover", "printed barcode label", "itemized invoice sheet", "cursive handwritten note card",
            "official stamp seal", "table breakdown numbers", "tax filing document", "warranty certificate"
        ],
        "Health & Medical": [
            "prescription medicine box", "amber pill bottle with label", "pill blister pack", "digital thermometer display",
            "blood pressure monitor cuff", "medical laboratory test report sheet", "official clinic stamp", "first aid kit box",
            "pharmacy receipt", "vitamin supplement bottle", "doctor handwritten note"
        ],
        "Automotive & Parking": [
            "concrete parking garage pillar", "blue parking section marker", "stall number floor stencil", "vehicle windshield",
            "dashboard speedometer gauge", "driver door jamb sticker", "tire pressure specification decal", "classic vintage automobile",
            "parking meter ticket slip", "car key fob on counter", "underground garage lighting"
        ],
        "Home & Personal": [
            "wifi internet router", "specification barcode sticker", "model serial number label", "wooden bookshelf rows",
            "hardcover books", "indoor potted monstera plant", "terracotta flower pot", "laptop keyboard", "measuring tape",
            "reading armchair", "ceramic coffee mug", "desk workspace setup", "craft knitting needles"
        ]
    }

    start_date = datetime.datetime(2018, 1, 15)
    end_date = datetime.datetime(2026, 2, 28)
    time_span_seconds = int((end_date - start_date).total_seconds())

    generated_records = []

    for i in range(num_needed):
        idx = num_benchmark + i + 1
        random_seconds = random.randint(0, time_span_seconds)
        dt = start_date + datetime.timedelta(seconds=random_seconds)
        timestamp_str = dt.strftime("%Y-%m-%d %H:%M:%S")
        date_tag = dt.strftime("%Y%m%d_%H%M%S")
        photo_id = f"IMG_{date_tag}_{i:04d}"

        cat_info = random.choice(categories_and_albums)
        category = cat_info[0]
        album = random.choice(cat_info[1])

        loc_city, loc_landmarks = random.choice(locations)
        landmark = random.choice(loc_landmarks)
        location_tag = f"{landmark}, {loc_city}"

        cat_objs = objects_pool.get(category, ["scene", "lighting", "outdoors", "daylight"])
        num_objs = random.randint(4, 7)
        chosen_objs = random.sample(cat_objs, min(num_objs, len(cat_objs)))
        detected_objects = ", ".join(chosen_objs)

        has_ocr = False
        ocr_text = "None"

        if category == "Documents & Receipts":
            has_ocr = random.random() < 0.90
            merchant = random.choice(["Target", "Costco Wholesale", "Whole Foods Market", "Trader Joe's", "Air France", "Delta Airlines", "Starbucks", "Home Depot", "Apple Store"])
            amount = f"${random.randint(12, 350)}.{random.randint(10, 99)}"
            tax_id = f"TX-{random.randint(100000, 999999)}"
            order_no = f"ORD#{random.randint(10000, 99999)}"
            if has_ocr:
                ocr_text = f"{merchant.upper()} - {order_no} - {tax_id} - SUBTOTAL: {amount} - APPROVED VIA VISA - THANK YOU"
            ai_visual_description = f"Clear document photograph of a printed {merchant} transaction receipt with itemized charges totaling {amount} resting on a flat neutral desk surface."

        elif category == "Health & Medical":
            has_ocr = random.random() < 0.85
            med_name = random.choice(["Ibuprofen 400mg", "Amoxicillin 500mg", "Cetirizine 10mg", "Paracetamol 650mg", "Metformin 500mg", "Omeprazole 20mg", "Vitamin D3 2000IU", "Azithromycin 250mg"])
            rx_num = f"RX-{random.randint(1000000, 9999999)}"
            clinic = random.choice(["CityHealth Urgent Care", "Walgreens Pharmacy", "CVS Caremark", "Metro Health Clinic"])
            if has_ocr:
                ocr_text = f"{clinic.upper()} - {rx_num} - {med_name.upper()} - TAKE AS DIRECTED BY PHYSICIAN - EXP: 2027/06"
            ai_visual_description = f"Close up shot of a medicine packaging box and prescription vial of {med_name} from {clinic} next to a bedside table lamp."

        elif category == "Automotive & Parking":
            has_ocr = random.random() < 0.75
            level_num = random.choice(["P1", "P2", "P3", "Level 2B", "Level 3 Blue", "Level 4 Yellow", "Section 5A", "Zone C"])
            lot_name = random.choice(["Airport Terminal Parking", "Metro Center Garage", "City Hall Underground", "Westfield Parking Plaza"])
            if has_ocr:
                ocr_text = f"{lot_name.upper()} - {level_num.upper()} - STALL #{random.randint(101, 899)} - KEEP TICKET WITH YOU"
            ai_visual_description = f"Photograph of an underground multi-story parking garage concrete pillar marked in bold blue stenciling with {level_num} in {lot_name}."

        elif category == "Food & Dining":
            has_ocr = random.random() < 0.50
            dish = random.choice(["truffle pasta", "wood-fired margherita pizza", "oat milk matcha latte", "acai breakfast bowl", "pan-seared salmon", "artisan burger with brioche bun", "fresh berry crepe"])
            cafe_name = random.choice(["Blue Wave Roasters", "Artisan Bakery & Cafe", "Trattoria Romana", "Bistro de Paris", "Corner Stone Kitchen", "Sweet Bloom Coffee"])
            if has_ocr:
                ocr_text = f"{cafe_name.upper()} - SPECIALTY MENU - {dish.upper()} - ORGANIC & LOCALLY SOURCED"
            ai_visual_description = f"A mouth-watering overhead food photograph of a freshly plated {dish} at {cafe_name} in {loc_city}, garnished with fresh herbs and served on rustic ceramics."

        elif category == "Home & Personal":
            has_ocr = random.random() < 0.60
            device = random.choice(["TP-Link Archer AX55", "ASUS RT-AX88U Router", "Samsung Smart TV 55", "Sony Soundbar HT-S350", "Dyson V11 Vacuum", "Breville Espresso Maker"])
            serial = f"SN-{random.randint(10000, 99999)}-{chr(random.randint(65, 90))}{chr(random.randint(65, 90))}"
            if has_ocr:
                ocr_text = f"{device.upper()} - MODEL: REV-B - S/N: {serial} - INPUT 100-240V ~ 50/60Hz - MADE IN TAIWAN"
            ai_visual_description = f"High resolution photograph of the manufacturer technical label and barcode sticker on the rear casing of a {device} in the home office."

        elif category == "Family & Celebrations":
            has_ocr = random.random() < 0.30
            event = random.choice(["5th birthday celebration", "annual summer family barbecue", "golden wedding anniversary toast", "college graduation celebration", "Christmas eve dinner with cousins"])
            if has_ocr:
                ocr_text = f"CONGRATULATIONS & BEST WISHES - {dt.year} CELEBRATION"
            ai_visual_description = f"Heartwarming family celebration photo capturing a candid moment of laughter during an {event} with sparkling lights and dinner toasts."

        else: # Travel & Nature
            has_ocr = random.random() < 0.35
            trail = random.choice(["Panorama Point Trail", "Coastal Rim Walkway", "Alpine Summit Loop", "Sunset Ridge Overlook", "Emerald Cove Trail"])
            elev = f"{random.randint(2000, 9500)} FT"
            if has_ocr:
                ocr_text = f"{trail.upper()} - ELEV: {elev} - SCENIC PRESERVE - PACK IN PACK OUT"
            ai_visual_description = f"Panoramic scenic travel photograph captured at {location_tag} showcasing vibrant colors, dramatic natural light, and breathtaking vistas."

        # Assign real image URL
        img_url = get_image_for_photo(photo_id, category)

        record = {
            "photo_id": photo_id,
            "timestamp": timestamp_str,
            "location_tag": location_tag,
            "location": location_tag,
            "album_name": album,
            "category": category,
            "detected_objects": detected_objects,
            "ocr_text": ocr_text,
            "detected_ocr": ocr_text,
            "ai_visual_description": ai_visual_description,
            "visual_description": ai_visual_description,
            "image_url": img_url
        }
        generated_records.append(record)

    df_generated = pd.DataFrame(generated_records)

    # Combine benchmark photos (0..34) and generated photos (35..9999)
    df_combined = pd.concat([df_benchmark, df_generated], ignore_index=True)
    df_combined = normalize_catalog_dataframe(df_combined)

    # Ensure image_url has no NaNs
    if "image_url" in df_combined.columns:
        for i, row in df_combined.iterrows():
            if pd.isna(row["image_url"]) or not str(row["image_url"]).startswith("http"):
                df_combined.at[i, "image_url"] = get_image_for_photo(str(row["photo_id"]), str(row["category"]))

    print(f"[10k Generator] Total catalog size: {len(df_combined)} rows.")

    # Paths
    data_dir = os.path.join(os.path.dirname(__file__), "data")
    os.makedirs(data_dir, exist_ok=True)
    csv_path = os.path.join(data_dir, "photo_metadata_catalog.csv")
    xlsx_path = os.path.join(data_dir, "photo_metadata_catalog.xlsx")

    print(f"[10k Generator] Saving fast CSV to {csv_path}...")
    df_combined.to_csv(csv_path, index=False, encoding="utf-8")
    print(f"[10k Generator] CSV saved successfully ({os.path.getsize(csv_path) / (1024*1024):.2f} MB).")

    print(f"[10k Generator] Saving Excel workbook to {xlsx_path}...")
    try:
        df_combined.to_excel(xlsx_path, index=False)
        print(f"[10k Generator] Excel workbook saved successfully.")
    except Exception as e:
        print(f"[10k Generator] Notice: Excel save warning: {e}")

    print("[10k Generator] Verification:")
    print(f" - Row count: {len(df_combined)}")
    print(f" - Top photo (Index 0): {df_combined.iloc[0]['photo_id']} | Image: {df_combined.iloc[0]['image_url']}")
    print(f" - Image coverage: {df_combined['image_url'].notna().sum()} / {len(df_combined)} photos have real image URLs")
    print("[10k Generator] Done!")

if __name__ == "__main__":
    generate_10k_photo_catalog()
