# 📸 Google Photos Product Management Case Study: Master Project Summary (`Summary.md`)

---

## 1. 🎯 Executive Project Overview & Case Study Objective

- **Product Problem Statement**: As Google Photos users accumulate tens of thousands of media assets over years, search experience severely breaks down when memory is incomplete or episodic.
- **The Cognitive Breakdown ("Semantic Recall Gap")**:
  - *What users remember (88% of memory anchors)*: Visual colors, emotional states, weather, ambient surroundings, and relative occasions (*"that yellow medicine box when I was sick last winter"*).
  - *What users forget (88% of database tags)*: Exact EXIF calendar dates, timestamps, GPS coordinates, exact filenames, or album titles.
- **Strategic Goal**: Analyze user feedback across 13 global platforms and build an intelligent episodic search assistant that bridges this semantic gap through automated query expansion and multimodal vector retrieval.

---

## 2. 🧹 Data Assets & Cleaning Pipeline

### Master Review Telemetry
- **Source Files**:
  - [`Google_Photos_Master_Reviews.csv`](file:///c:/Users/shree/OneDrive/Desktop/Google%20Photos/Google_Photos_Master_Reviews.csv) (`49.3 MB`, UTF-8)
  - [`Google_Photos_Master_Reviews.xlsx`](file:///c:/Users/shree/OneDrive/Desktop/Google%20Photos/Google_Photos_Master_Reviews.xlsx) (`20.3 MB`, Excel openpyxl)
- **Safety Backups Created**:
  - `Google_Photos_Master_Reviews_backup_raw.csv` (`56.7 MB`, 117,037 raw rows)
  - `Google_Photos_Master_Reviews_backup_raw.xlsx` (`24.1 MB`, 117,037 raw rows)

### Cleaning & Quality Filtering (Jan 2018 – Sep 2026)
- **Total Raw Reviews**: `117,037`
- **Filtered Out (< 8 words & emoji-only spam)**: `20,111` entries (17.18%)
- **Cleaned Substantive Dataset (≥ 8 words)**: **`96,926` entries (82.82%)**

### Recalibrated Macro Telemetry (Cleaned vs. Raw)
- **Total Reviews**: `96,926`
- **Rated Reviews**: `78,255` (80.7% rated coverage)
- **Average Star Rating**: `3.31 / 5` *(calibrated from 3.47 by filtering out generic 5★ spam like "Good" and "Nice")*
- **Negative Share**: `29.6%` (`28,714` entries)
- **Positive Share**: `42.9%` (`41,577` entries)
- **Neutral Share**: `8.2%` (`7,964` entries)
- **Unknown Share (Unrated Forums)**: `19.3%` (`18,671` entries)
- **Net Sentiment Score**: `+13.3%` (Positive % minus Negative %)
- **Top Actionable Complaint**: `Backup & sync failures` (`4,892` entries, 35.0% negativity)

### Cleaned Star Rating Breakdown
- **5 ★★★★★**: `32,584` (41.6%)
- **4 ★★★★☆**: `8,993` (11.5%)
- **3 ★★★☆☆**: `7,964` (10.2%)
- **2 ★★☆☆☆**: `7,150` (9.1%)
- **1 ★☆☆☆☆**: `21,564` (27.6%)

### Curated Benchmark Datasets
- [`data/user_feedback_dataset.csv`](file:///c:/Users/shree/OneDrive/Desktop/Google%20Photos/data/user_feedback_dataset.csv): 30 curated episodic failure cases across Play Store, Reddit, and Google Support.
- [`data/photo_metadata_catalog.xlsx`](file:///c:/Users/shree/OneDrive/Desktop/Google%20Photos/data/photo_metadata_catalog.xlsx): 35 multi-modal photo records containing visual scene descriptions, detected objects, and extracted OCR text.

---

## 3. 📊 Dashboard Architecture: "Photos Review Pulse"

The Executive Discovery Dashboard ([`components/dashboard.py`](file:///c:/Users/shree/OneDrive/Desktop/Google%20Photos/components/dashboard.py)) features 10 comprehensive analytical sections:

1. **Hero Brand Header**: Title, metadata chips (`13 platforms · 96,926 cleaned reviews`), and status badges (`Cleaned Substantive Dataset`, `80.7% Rated Coverage`).
2. **Key Metrics Row**: Tiered 4 + 3 card layout preventing text compression:
   - Row 1: Total Reviews (`96,926`), Average Rating (`3.31 / 5`), Negative Share (`29.6%`), Positive Share (`42.9%`).
   - Row 2: Top Complaint (`Backup & sync failures`), Platforms Tracked (`13`), Net Sentiment Score (`+13.3%`).
3. **Sentiment & Rating Overview**: Plotly Donut chart + 2x2 micro-summary pills + Horizontal 1★–5★ distribution bar chart illustrating bimodal user polarization.
4. **Platform Analysis**: All 13 sources ranked by review volume (Google Play Main at 51,691, Google Play Secondary at 15,954, YouTube at 12,023, Apple App Store at 10,553, Hacker News at 4,522) + 100% stacked sentiment bars + Executive divergence callout (Google Play at 35.2% negativity vs. Apple App Store at 22.6%).
5. **Complaint Theme Analysis (14 Themes)**:
   - Ranked horizontal bar chart for the 13 actionable themes, colored by Negative Share %.
   - Severity Index Quadrant bubble scatter chart (`Volume × Negativity %`).
   - Expandable Complete Cross-Tab Heatmap Table (all 14 themes).
   - Top 8 Themes × Platform Matrix Heatmap.
6. **Interactive Keyword Explorer**: Dropdown theme selector displaying phrase frequency bars (`sync stuck`, `backup loop`, `can't find`, `15gb full`) with severity tags and authentic user quotes.
7. **Trends Over Time (Jan 2018 – Sep 2026)**: Dual-axis monthly timeline (Monthly Review Volume on primary Y; Average Star Rating on secondary Y) with milestone annotations:
   - *Apr 2024 Peak (3.75★)*: Post-pandemic stability.
   - *Oct 2024 Dip (2.42★)*: Collections tab redesign backlash.
   - *Sep 2026 Recovery (3.82★)*: AI Search rollout.
8. **Geography & Problem Versions**: Top 10 countries (GLOBAL, Germany, Japan, France, Turkey, India, US, Italy, Brazil, UK) + build versions ranked by 1★/2★ negative spikes.
9. **PM Case Study: Semantic Recall Gap**: Interactive visual comparison of what users remember vs. what they forget.
10. **Interactive Review Explorer**: Searchable and filterable data table with platform filter, star rating filter, and live text search across 96,926 cleaned review records.

---

## 4. 🤖 AI Search Assistant & Retrieval Engine

- **Pure-Python Vector Engine ([`utils/rag_engine.py`](file:///c:/Users/shree/OneDrive/Desktop/Google%20Photos/utils/rag_engine.py))**: Built with `PureTfidfVectorizer` in standard library Python, eliminating all C-extension / DLL loading issues under Windows AppLocker / WDAC.
- **Multimodal Field Indexing**: Simultaneously matches queries across:
  - AI Visual Scene Descriptions (lighting, atmosphere, colors, setting).
  - Detected Object Labels (items, vehicles, furniture).
  - Detected OCR Text (printed words, labels, receipts, prescriptions).
- **Episodic Query Expander**: Automatically enriches vague terms with semantic synonyms and co-occurring clues (e.g., query *"when I was sick with fever"* expands to *Paracetamol, thermometer, medicine box, bedside nightstand*).
- **Dual-Mode Structured Output**:
  - 📝 **Conversational Paragraph Summary**: Human-readable synthesis of what was retrieved and why.
  - 📌 **Point-wise Analytical Takeaways**: Bulleted breakdown of matched cues, visual context, and temporal anchors.
  - 🧠 **Episodic Reasoning Card**: Explains how the assistant connected user clues to the metadata.
  - 📷 **Candidate Photo Cards**: Highlighting photo ID, category, location, timestamp, confidence badge (`High`, `Medium`, `Low`), scene description, detected objects, and detected OCR text.
  - ❓ **Clarifying Dialogue Loop**: Renders clickable prompt chips when a query is ambiguous.

---

## 5. 🎨 Google Material Design 3 Styling System

- Implemented in [`components/styles.py`](file:///c:/Users/shree/OneDrive/Desktop/Google%20Photos/components/styles.py) and [`.streamlit/config.toml`](file:///c:/Users/shree/OneDrive/Desktop/Google%20Photos/.streamlit/config.toml).
- Google Brand Colors: Google Blue (`#1A73E8`), Red (`#EA4335`), Yellow (`#FBBC05`), Green (`#34A853`), Light Blue Surface (`#E8F0FE`), Background (`#F8F9FA`).
- Typography: Google Sans / Inter with MD3 elevation card shadows.
- Zero-Indentation Pipeline: `render_html()` strips all leading line indentation to prevent Streamlit's Markdown parser from converting HTML into `<pre><code>` blocks.
- Action Buttons: Styled with solid white backgrounds, bold Google Blue text (`#1A73E8`), and a 52px height.
- Clean Charts: Plotly modebars disabled (`displayModeBar: False`) to prevent floating toolbars from overlapping titles.

---

## 6. 📁 Complete Codebase Structure

```
c:\Users\shree\OneDrive\Desktop\Google Photos\
├── app.py                             # Main entry point & segmented navigation
├── requirements.txt                   # Minimal deployment dependencies
├── run.bat                            # 1-click Windows CMD launcher
├── run.ps1                            # 1-click PowerShell launcher
├── .gitignore                         # Excludes venv, pycache, backups
├── .streamlit/
│   └── config.toml                    # MD3 light theme & headless configuration
├── components/
│   ├── __init__.py
│   ├── dashboard.py                   # 10-section Review Pulse dashboard
│   ├── rag_bot.py                     # AI Search Assistant chat interface
│   └── styles.py                      # MD3 CSS, SVG icons & render_html()
├── utils/
│   ├── __init__.py
│   ├── data_loader.py                 # Multi-format data loader & metrics
│   ├── pulse_data.py                  # Pre-aggregated clean telemetry (96k reviews)
│   └── rag_engine.py                  # Pure-Python TF-IDF vector retrieval engine
├── data/
│   ├── user_feedback_dataset.csv      # 30 episodic failure cases
│   └── photo_metadata_catalog.xlsx    # 35 indexed multimodal photos
├── Google_Photos_Master_Reviews.csv   # Cleaned master dataset (49.3 MB, 96,926 rows)
├── Google_Photos_Master_Reviews.xlsx  # Cleaned master Excel (20.3 MB, 96,926 rows)
├── Google_Photos_Master_Reviews_backup_raw.csv   # Raw backup (117,037 rows)
├── Google_Photos_Master_Reviews_backup_raw.xlsx  # Raw backup (117,037 rows)
├── left.md                            # Comprehensive remaining scope roadmap
└── Summary.md                         # Complete project single source of truth
```

---

## 7. 🚀 Deployment & Execution Summary

- **Local Execution**: Running on `http://localhost:8501`.
- **Public Cloud Deployment**: Ready for 1-click deployment via **GitHub + Streamlit Community Cloud** (`share.streamlit.io`).
