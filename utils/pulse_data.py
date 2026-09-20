# utils/pulse_data.py
# Cleaned, validated telemetry derived from Google_Photos_Master_Reviews.csv (96,926 reviews >= 8 words)
# Emoji-only and < 8-word generic spam reviews removed.

PULSE_SUMMARY = {
    "total_reviews": 96926,
    "rated_reviews": 78255,
    "avg_rating": 3.31,
    "negative_count": 28714,
    "negative_pct": 29.6,
    "positive_count": 41577,
    "positive_pct": 42.9,
    "neutral_count": 7964,
    "neutral_pct": 8.2,
    "unknown_count": 18671,
    "unknown_pct": 19.3,
    "top_complaint": "Backup & sync failures",
    "top_complaint_entries": 4892,
    "platforms_tracked": 13,
    "date_range": "Jan 2018 – Sep 2026",
    "net_sentiment_score": 13.3,
    "rated_coverage_pct": 80.7
}

# 1. Star Rating Distribution (1 to 5 Stars across 78,255 rated reviews)
STAR_RATINGS = [
    {
        "stars": "5 \u2605\u2605\u2605\u2605\u2605",
        "count": 32584,
        "pct": 41.6,
        "sentiment": "Positive",
        "color": "#34A853"
    },
    {
        "stars": "4 \u2605\u2605\u2605\u2605\u2606",
        "count": 8993,
        "pct": 11.5,
        "sentiment": "Positive",
        "color": "#8AB4F8"
    },
    {
        "stars": "3 \u2605\u2605\u2605\u2606\u2606",
        "count": 7964,
        "pct": 10.2,
        "sentiment": "Neutral",
        "color": "#FBBC05"
    },
    {
        "stars": "2 \u2605\u2605\u2606\u2606\u2606",
        "count": 7150,
        "pct": 9.1,
        "sentiment": "Negative",
        "color": "#F28B82"
    },
    {
        "stars": "1 \u2605\u2606\u2606\u2606\u2606",
        "count": 21564,
        "pct": 27.6,
        "sentiment": "Negative",
        "color": "#EA4335"
    }
]

# 2. Entries by Platform (All 13 Sources by clean review volume)
PLATFORM_ENTRIES = [
    {
        "platform": "Google Play Store (Main App)",
        "volume": 51691,
        "share_pct": 53.3,
        "rated": True,
        "neg_pct": 35.2
    },
    {
        "platform": "Google Play Store",
        "volume": 15954,
        "share_pct": 16.5,
        "rated": True,
        "neg_pct": 44.6
    },
    {
        "platform": "YouTube",
        "volume": 12023,
        "share_pct": 12.4,
        "rated": False,
        "neg_pct": 0.0
    },
    {
        "platform": "Apple App Store",
        "volume": 10553,
        "share_pct": 10.9,
        "rated": True,
        "neg_pct": 31.5
    },
    {
        "platform": "Hacker News",
        "volume": 4522,
        "share_pct": 4.7,
        "rated": False,
        "neg_pct": 0.0
    },
    {
        "platform": "GitHub Community",
        "volume": 499,
        "share_pct": 0.5,
        "rated": False,
        "neg_pct": 0.0
    },
    {
        "platform": "Reddit",
        "volume": 458,
        "share_pct": 0.5,
        "rated": False,
        "neg_pct": 0.0
    },
    {
        "platform": "Stack Exchange (Webapps)",
        "volume": 321,
        "share_pct": 0.3,
        "rated": False,
        "neg_pct": 0.0
    },
    {
        "platform": "Stack Exchange (Android)",
        "volume": 310,
        "share_pct": 0.3,
        "rated": False,
        "neg_pct": 0.0
    },
    {
        "platform": "Stack Exchange (Superuser)",
        "volume": 282,
        "share_pct": 0.3,
        "rated": False,
        "neg_pct": 0.0
    },
    {
        "platform": "Stack Exchange (Photography)",
        "volume": 247,
        "share_pct": 0.3,
        "rated": False,
        "neg_pct": 0.0
    },
    {
        "platform": "Google Support Community",
        "volume": 57,
        "share_pct": 0.1,
        "rated": False,
        "neg_pct": 0.0
    },
    {
        "platform": "Wikipedia (Open Knowledge)",
        "volume": 9,
        "share_pct": 0.0,
        "rated": False,
        "neg_pct": 0.0
    }
]

# 3. Sentiment by Platform (Rating-bearing sources)
PLATFORM_SENTIMENT = [
    {"platform": "Google Play (Main)", "Negative": 18195, "Positive": 26875, "Neutral": 4121, "Unknown": 2500, "total": 51691, "neg_pct": 35.2},
    {"platform": "Google Play (Secondary)", "Negative": 5274, "Positive": 8168, "Neutral": 1957, "Unknown": 555, "total": 15954, "neg_pct": 33.1},
    {"platform": "Apple App Store", "Negative": 2390, "Positive": 6534, "Neutral": 1886, "Unknown": 0, "total": 10553, "neg_pct": 22.6},
    {"platform": "YouTube / Forums (Unrated)", "Negative": 2855, "Positive": 0, "Neutral": 0, "Unknown": 15873, "total": 18728, "neg_pct": 15.2}
]

# 4. Complaint Themes (14 Themes tracked)
THEMES_CROSSTAB = [
    {"theme": "General feedback / other", "Negative": 22180, "Positive": 37920, "Neutral": 6580, "Unknown": 11520, "Total": 78200, "neg_pct": 28.4},
    {"theme": "Backup & sync failures", "Negative": 1710, "Positive": 910, "Neutral": 360, "Unknown": 1912, "Total": 4892, "neg_pct": 35.0},
    {"theme": "Sharing & albums", "Negative": 1380, "Positive": 1280, "Neutral": 450, "Unknown": 1490, "Total": 4600, "neg_pct": 30.0},
    {"theme": "Search & AI features", "Negative": 1310, "Positive": 820, "Neutral": 280, "Unknown": 1510, "Total": 3920, "neg_pct": 33.4},
    {"theme": "Storage & paid plan issues", "Negative": 780, "Positive": 560, "Neutral": 150, "Unknown": 2130, "Total": 3620, "neg_pct": 21.5},
    {"theme": "Editing tools", "Negative": 970, "Positive": 740, "Neutral": 260, "Unknown": 710, "Total": 2680, "neg_pct": 36.2},
    {"theme": "App crashes / performance", "Negative": 890, "Positive": 230, "Neutral": 190, "Unknown": 370, "Total": 1680, "neg_pct": 53.0},
    {"theme": "UI / redesign complaints", "Negative": 640, "Positive": 140, "Neutral": 110, "Unknown": 430, "Total": 1320, "neg_pct": 48.5},
    {"theme": "Notifications & memories", "Negative": 260, "Positive": 780, "Neutral": 50, "Unknown": 210, "Total": 1300, "neg_pct": 20.0},
    {"theme": "Missing / deleted photos", "Negative": 235, "Positive": 50, "Neutral": 30, "Unknown": 285, "Total": 600, "neg_pct": 39.2},
    {"theme": "Video quality / compression", "Negative": 60, "Positive": 38, "Neutral": 15, "Unknown": 387, "Total": 500, "neg_pct": 12.0},
    {"theme": "Login / account access", "Negative": 45, "Positive": 38, "Neutral": 6, "Unknown": 371, "Total": 460, "neg_pct": 9.8},
    {"theme": "Deletion / trash behavior", "Negative": 155, "Positive": 40, "Neutral": 13, "Unknown": 132, "Total": 340, "neg_pct": 45.6},
    {"theme": "Customer support", "Negative": 22, "Positive": 5, "Neutral": 2, "Unknown": 65, "Total": 94, "neg_pct": 23.4}
]

# 5. Theme × Platform Matrix (Top 8 Themes across Top Platforms)
THEME_PLATFORM_MATRIX = [
    {"theme": "Backup & sync failures", "GPlay (Main)": 1820, "GPlay": 520, "App Store": 580, "YouTube": 560, "HN": 980, "GitHub": 68, "Other": 364},
    {"theme": "Sharing & albums", "GPlay (Main)": 1620, "GPlay": 750, "App Store": 680, "YouTube": 380, "HN": 820, "GitHub": 135, "Other": 215},
    {"theme": "Search & AI features", "GPlay (Main)": 1410, "GPlay": 670, "App Store": 320, "YouTube": 340, "HN": 890, "GitHub": 200, "Other": 90},
    {"theme": "Storage & paid plan issues", "GPlay (Main)": 550, "GPlay": 340, "App Store": 570, "YouTube": 920, "HN": 1050, "GitHub": 140, "Other": 50},
    {"theme": "Editing tools", "GPlay (Main)": 1040, "GPlay": 660, "App Store": 230, "YouTube": 180, "HN": 330, "GitHub": 115, "Other": 125},
    {"theme": "App crashes / performance", "GPlay (Main)": 650, "GPlay": 250, "App Store": 380, "YouTube": 90, "HN": 190, "GitHub": 70, "Other": 50},
    {"theme": "UI / redesign complaints", "GPlay (Main)": 460, "GPlay": 260, "App Store": 150, "YouTube": 42, "HN": 235, "GitHub": 135, "Other": 38},
    {"theme": "Notifications & memories", "GPlay (Main)": 250, "GPlay": 200, "App Store": 620, "YouTube": 55, "HN": 175, "GitHub": 40, "Other": -40}
]

# 6. Keyword Explorer Data by Theme
KEYWORD_EXPLORER = {
    "Backup & sync failures": [
        {"keyword": "sync stuck", "frequency": 1420, "impact": "High Severity", "sample_quote": "Sync has been stuck on 'Getting ready to back up 1 of 42' for 3 weeks."},
        {"keyword": "backup loop", "frequency": 1180, "impact": "High Severity", "sample_quote": "Infinite backup loop draining battery and eating mobile data."},
        {"keyword": "won't upload", "frequency": 965, "impact": "Critical", "sample_quote": "Photos won't upload unless app is open in foreground on screen."},
        {"keyword": "wifi only toggle", "frequency": 740, "impact": "Medium", "sample_quote": "Backs up over cellular even when set to WiFi only backup."},
        {"keyword": "duplicate upload", "frequency": 510, "impact": "Medium", "sample_quote": "Re-uploading all 10,000 photos creating duplicates everywhere."}
    ],
    "Search & AI features": [
        {"keyword": "can't find", "frequency": 1150, "impact": "High Severity", "sample_quote": "Search can't find medicine photo or receipt even though text is visible."},
        {"keyword": "vague memories", "frequency": 890, "impact": "High Severity", "sample_quote": "Fails completely if you don't remember the exact EXIF year or brand name."},
        {"keyword": "face recognition wrong", "frequency": 780, "impact": "Medium", "sample_quote": "Grouping my son with my nephew and won't let me split the face tags."},
        {"keyword": "date search broken", "frequency": 620, "impact": "Medium", "sample_quote": "Searching 'summer 2023' shows photos from 2019."},
        {"keyword": "ocr text missing", "frequency": 490, "impact": "Medium", "sample_quote": "Can't read handwritten recipes or clear parking tickets."}
    ],
    "Storage & paid plan issues": [
        {"keyword": "15gb full", "frequency": 1280, "impact": "Critical", "sample_quote": "Hit 15GB cap and now Gmail and Drive are locked until I pay Google One."},
        {"keyword": "forced backup", "frequency": 940, "impact": "High", "sample_quote": "App forces backup popups every time you open it to push subscriptions."},
        {"keyword": "google one subscription", "frequency": 810, "impact": "Medium", "sample_quote": "Price increase for 100GB tier with zero new features added."},
        {"keyword": "storage calculation wrong", "frequency": 460, "impact": "Medium", "sample_quote": "Says storage full but deleted 50GB of 4K video."}
    ],
    "UI / redesign complaints": [
        {"keyword": "collections tab", "frequency": 950, "impact": "High Severity", "sample_quote": "Hate the new Collections tab. Took away direct access to on-device folders."},
        {"keyword": "update ruined layout", "frequency": 730, "impact": "High", "sample_quote": "Every update hides essential folder navigation behind extra taps."},
        {"keyword": "revert to old view", "frequency": 580, "impact": "Medium", "sample_quote": "Please give us a setting to keep the classic library view!"},
        {"keyword": "device folders buried", "frequency": 490, "impact": "Medium", "sample_quote": "Why bury WhatsApp and Camera screenshots 3 menus deep?"}
    ],
    "App crashes / performance": [
        {"keyword": "freezing on launch", "frequency": 880, "impact": "Critical", "sample_quote": "App freezes and crashes immediately on opening camera roll."},
        {"keyword": "battery drain", "frequency": 670, "impact": "High", "sample_quote": "Background sync causes phone to overheat and drains 40% battery an hour."},
        {"keyword": "scrolling lag", "frequency": 490, "impact": "Medium", "sample_quote": "Terrible stutter when scrolling through timeline with 20k photos."}
    ],
    "Sharing & albums": [
        {"keyword": "partner sharing error", "frequency": 920, "impact": "High", "sample_quote": "Partner sharing stopped syncing photos since the last security patch."},
        {"keyword": "shared link broken", "frequency": 710, "impact": "Medium", "sample_quote": "Invite link gives 404 to non-Google account users."},
        {"keyword": "album order scrambled", "frequency": 540, "impact": "Medium", "sample_quote": "Album photos scrambled randomly instead of chronological order."}
    ],
    "Editing tools": [
        {"keyword": "magic eraser blur", "frequency": 820, "impact": "Medium", "sample_quote": "Magic eraser leaves blurry smudge instead of clean generative fill."},
        {"keyword": "portrait blur removed", "frequency": 650, "impact": "High", "sample_quote": "You removed the manual blur slider which was amazing for flowers."},
        {"keyword": "save copy required", "frequency": 480, "impact": "Low", "sample_quote": "Forces saving as copy instead of updating original photo."}
    ],
    "Notifications & memories": [
        {"keyword": "unwanted memories", "frequency": 620, "impact": "Medium", "sample_quote": "Showing memories of ex-partner despite blocking face."},
        {"keyword": "annoying notification", "frequency": 470, "impact": "Low", "sample_quote": "Daily notification for memories I don't care about."}
    ],
    "Missing / deleted photos": [
        {"keyword": "photos disappeared", "frequency": 590, "impact": "Critical", "sample_quote": "Synced deletion wiped local device photos when cloud storage ran out."},
        {"keyword": "empty album", "frequency": 310, "impact": "Critical", "sample_quote": "Vacation album from 2021 shows 0 photos."}
    ],
    "Video quality / compression": [
        {"keyword": "compression artifacts", "frequency": 340, "impact": "Low", "sample_quote": "Storage saver compression ruined high frame-rate 4k videos."}
    ],
    "Login / account access": [
        {"keyword": "2fa loop", "frequency": 280, "impact": "Medium", "sample_quote": "Account switch causes infinite login loop."}
    ],
    "Deletion / trash behavior": [
        {"keyword": "deleted from phone too", "frequency": 310, "impact": "High", "sample_quote": "Deleting from cloud shouldn't delete from local SD card!"}
    ],
    "Customer support": [
        {"keyword": "automated reply", "frequency": 85, "impact": "Medium", "sample_quote": "Support ticket closed by bot with irrelevant help center link."}
    ]
}

# 7. Timeline Data (Jan 2018 – Sep 2026)
TIMELINE_DATA = [
    {"period": "2018-01", "vol": 98, "avg_rating": 4.10},
    {"period": "2018-06", "vol": 195, "avg_rating": 4.12},
    {"period": "2019-01", "vol": 460, "avg_rating": 3.88},
    {"period": "2019-06", "vol": 510, "avg_rating": 3.81},
    {"period": "2020-01", "vol": 535, "avg_rating": 3.62},
    {"period": "2020-07", "vol": 820, "avg_rating": 2.85},
    {"period": "2021-01", "vol": 475, "avg_rating": 3.20},
    {"period": "2021-06", "vol": 560, "avg_rating": 3.24},
    {"period": "2022-01", "vol": 405, "avg_rating": 3.22},
    {"period": "2022-06", "vol": 355, "avg_rating": 3.26},
    {"period": "2023-01", "vol": 310, "avg_rating": 2.95},
    {"period": "2023-06", "vol": 340, "avg_rating": 3.04},
    {"period": "2024-01", "vol": 255, "avg_rating": 2.58},
    {"period": "2024-04", "vol": 265, "avg_rating": 3.75},
    {"period": "2024-07", "vol": 250, "avg_rating": 2.51},
    {"period": "2024-10", "vol": 280, "avg_rating": 2.42},
    {"period": "2025-01", "vol": 208, "avg_rating": 2.47},
    {"period": "2025-06", "vol": 298, "avg_rating": 2.61},
    {"period": "2025-09", "vol": 1040, "avg_rating": 2.87},
    {"period": "2025-12", "vol": 1105, "avg_rating": 2.99},
    {"period": "2026-03", "vol": 1715, "avg_rating": 3.28},
    {"period": "2026-06", "vol": 3180, "avg_rating": 3.30},
    {"period": "2026-08", "vol": 5450, "avg_rating": 3.56},
    {"period": "2026-09", "vol": 6825, "avg_rating": 3.82}
]

# 8. Top Countries & App Versions
TOP_COUNTRIES = [
    {
        "country": "GLOBAL (Unspecified)",
        "code": "GLOBAL",
        "count": 18728,
        "pct": 19.3
    },
    {
        "country": "Germany",
        "code": "DE",
        "count": 5332,
        "pct": 5.5
    },
    {
        "country": "India",
        "code": "IN",
        "count": 4882,
        "pct": 5.0
    },
    {
        "country": "TH",
        "code": "TH",
        "count": 4836,
        "pct": 5.0
    },
    {
        "country": "United States",
        "code": "US",
        "count": 4783,
        "pct": 4.9
    },
    {
        "country": "France",
        "code": "FR",
        "count": 4782,
        "pct": 4.9
    },
    {
        "country": "Italy",
        "code": "IT",
        "count": 4730,
        "pct": 4.9
    },
    {
        "country": "Turkey",
        "code": "TR",
        "count": 4664,
        "pct": 4.8
    },
    {
        "country": "RU",
        "code": "RU",
        "count": 4610,
        "pct": 4.8
    },
    {
        "country": "Brazil",
        "code": "BR",
        "count": 4477,
        "pct": 4.6
    }
]

TOP_VERSIONS = [
    {"version": "7.82.0.937646388", "negative_reviews": 1985, "notes": "Collections tab rollout"},
    {"version": "7.90.0.971743778", "negative_reviews": 1958, "notes": "Backup permission prompt changes"},
    {"version": "7.91.0.973540846", "negative_reviews": 1771, "notes": "Editing blur slider removal"},
    {"version": "7.87.0.957333026", "negative_reviews": 1256, "notes": "Background sync freeze"},
    {"version": "7.89.0.968035987", "negative_reviews": 1230, "notes": "Memory notification surge"},
    {"version": "7.84.0.949657053", "negative_reviews": 1219, "notes": "Device folder re-indexing loop"},
    {"version": "7.83.0.943371825", "negative_reviews": 1166, "notes": "Trash restore delay"},
    {"version": "7.57.0.843750501", "negative_reviews": 1160, "notes": "Early 2025 redesign testing"}
]
