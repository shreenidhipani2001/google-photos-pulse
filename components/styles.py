import streamlit as st

def render_html(html_str: str):
    """
    Safely render HTML without Markdown 4-space code block interpretation.
    Strips leading whitespace on each line so CommonMark never treats HTML as <pre><code>.
    """
    cleaned = "\n".join(line.strip() for line in html_str.strip().splitlines())
    st.markdown(cleaned, unsafe_allow_html=True)

GOOGLE_PHOTOS_PINWHEEL_SVG = """
<svg width="38" height="38" viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg" style="vertical-align: middle; flex-shrink: 0;">
  <path d="M24 4C24 15.0457 15.0457 24 4 24H24V4Z" fill="#EA4335"/>
  <path d="M44 24C32.9543 24 24 15.0457 24 4V24H44Z" fill="#FBBC05"/>
  <path d="M24 44C24 32.9543 32.9543 24 44 24H24V44Z" fill="#34A853"/>
  <path d="M4 24C15.0457 24 24 32.9543 24 44V24H4Z" fill="#4285F4"/>
</svg>
"""

GEMINI_SPARK_SVG = """
<svg width="22" height="22" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" style="vertical-align: middle;">
  <path d="M12 2L14.5 9.5L22 12L14.5 14.5L12 22L9.5 14.5L2 12L9.5 9.5L12 2Z" fill="url(#gemini_grad)"/>
  <defs>
    <linearGradient id="gemini_grad" x1="2" y1="2" x2="22" y2="22" gradientUnits="userSpaceOnUse">
      <stop stop-color="#1A73E8"/>
      <stop offset="0.5" stop-color="#8AB4F8"/>
      <stop offset="1" stop-color="#EA4335"/>
    </linearGradient>
  </defs>
</svg>
"""

ROBOT_ICON_SVG = """
<svg width="22" height="22" viewBox="0 0 24 24" fill="currentColor" xmlns="http://www.w3.org/2000/svg">
  <path d="M12 2a2 2 0 0 1 2 2c0 .74-.4 1.38-1 1.72V7h4a3 3 0 0 1 3 3v8a3 3 0 0 1-3 3H7a3 3 0 0 1-3-3v-8a3 3 0 0 1 3-3h4V5.72c-.6-.34-1-.98-1-1.72a2 2 0 0 1 2-2zM7.5 13a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3zm9 0a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3zm-7 3a.5.5 0 0 0 0 1h5a.5.5 0 0 0 0-1h-5z"/>
</svg>
"""

def apply_custom_styles():
    """Inject comprehensive Google Material Design 3 Expressive theme overrides into Streamlit."""
    md3_css = """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Google+Sans:wght@400;500;600;700&family=Inter:wght@400;500;600;700&display=swap');

    :root {
        --google-blue: #1A73E8;
        --google-blue-hover: #1557B0;
        --google-blue-surface: #E8F0FE;
        --google-text: #202124;
        --google-subtext: #5F6368;
        --google-bg: #F8F9FA;
        --google-surface: #FFFFFF;
        --google-border: #DADCE0;
        --google-red: #EA4335;
        --google-green: #34A853;
        --google-yellow: #FBBC05;
        --radius-card: 16px;
        --radius-pill: 28px;
        --shadow-elevation-1: 0 1px 3px rgba(60,64,67,0.12), 0 1px 2px rgba(60,64,67,0.18);
        --shadow-elevation-2: 0 4px 12px rgba(60,64,67,0.15), 0 1px 3px rgba(60,64,67,0.25);
    }

    [data-testid="stAppViewContainer"], .stApp {
        font-family: 'Google Sans', 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
        background-color: var(--google-bg) !important;
        color: var(--google-text) !important;
    }

    header[data-testid="stHeader"] {
        background-color: transparent !important;
    }

    .block-container {
        padding-top: 1rem !important;
        padding-bottom: 5rem !important;
        max-width: 1380px !important;
    }

    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: #FFFFFF !important;
        border-right: 1px solid var(--google-border) !important;
    }
    [data-testid="stSidebar"] h1, 
    [data-testid="stSidebar"] h2, 
    [data-testid="stSidebar"] h3,
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] span,
    [data-testid="stSidebar"] label {
        color: var(--google-text) !important;
    }

    /* Top Google Photos Brand & Search Pill Bar */
    .gp-app-bar {
        display: flex;
        align-items: center;
        justify-content: space-between;
        background: #FFFFFF !important;
        border: 1px solid var(--google-border) !important;
        border-radius: var(--radius-card) !important;
        padding: 12px 24px !important;
        margin-bottom: 16px !important;
        box-shadow: var(--shadow-elevation-1) !important;
        gap: 16px;
    }
    .gp-app-brand {
        display: flex;
        align-items: center;
        gap: 12px;
        font-size: 22px;
        font-weight: 700;
        color: #202124;
    }
    .gp-app-brand span {
        color: #5F6368;
        font-weight: 400;
        font-size: 16px;
    }
    .gp-user-avatar {
        width: 36px;
        height: 36px;
        border-radius: 50%;
        background: #1A73E8;
        color: #FFFFFF;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 700;
        font-size: 15px;
    }

    /* Navigation Radio Switcher */
    div[data-testid="stRadio"] {
        margin-bottom: 20px !important;
    }
    div[data-testid="stRadio"] div[role="radiogroup"] {
        display: flex !important;
        flex-direction: row !important;
        background-color: #EDF2FA !important;
        padding: 5px !important;
        border-radius: 32px !important;
        border: 1px solid #D3E3FD !important;
        gap: 6px !important;
        justify-content: center !important;
    }
    div[data-testid="stRadio"] div[role="radiogroup"] > label {
        display: flex !important;
        align-items: center !important;
        padding: 9px 22px !important;
        border-radius: 26px !important;
        cursor: pointer !important;
        font-family: 'Google Sans', sans-serif !important;
        font-size: 14.5px !important;
        font-weight: 600 !important;
        color: #444746 !important;
        background-color: transparent !important;
        transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1) !important;
        margin: 0 !important;
        border: none !important;
    }
    div[data-testid="stRadio"] div[role="radiogroup"] > label > div:first-child {
        display: none !important;
    }
    div[data-testid="stRadio"] div[role="radiogroup"] > label:hover {
        background-color: rgba(255, 255, 255, 0.7) !important;
        color: var(--google-blue) !important;
    }
    div[data-testid="stRadio"] div[role="radiogroup"] > label:has(input:checked) {
        background-color: #FFFFFF !important;
        color: var(--google-blue) !important;
        box-shadow: 0 1px 4px rgba(60,64,67,0.18) !important;
    }

    /* KPI Metrics Cards */
    .metric-card {
        background: #FFFFFF !important;
        border: 1px solid var(--google-border) !important;
        border-radius: var(--radius-card) !important;
        padding: 16px 18px !important;
        box-shadow: var(--shadow-elevation-1) !important;
        display: flex !important;
        flex-direction: column !important;
        justify-content: space-between !important;
        min-height: 110px !important;
        height: 100% !important;
    }
    .metric-card:hover {
        transform: translateY(-2px) !important;
        box-shadow: var(--shadow-elevation-2) !important;
    }
    .metric-title {
        font-size: 12px !important;
        font-weight: 600 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.6px !important;
        color: var(--google-subtext) !important;
        margin-bottom: 4px !important;
    }
    .metric-value {
        font-size: 24px !important;
        font-weight: 700 !important;
        color: var(--google-text) !important;
        line-height: 1.2 !important;
    }
    .metric-delta {
        font-size: 12px !important;
        font-weight: 500 !important;
        margin-top: 5px !important;
        color: var(--google-blue) !important;
    }

    /* Section & Chart Containers */
    .chart-container-box {
        background: #FFFFFF !important;
        border: 1px solid var(--google-border) !important;
        border-radius: var(--radius-card) !important;
        padding: 16px 18px !important;
        box-shadow: var(--shadow-elevation-1) !important;
        margin-bottom: 12px !important;
    }

    /* Primary Action Buttons (White BG, Blue Text, More Height) */
    button[kind="primary"], 
    button[data-testid="stBaseButton-primary"],
    .stButton > button[kind="primary"] {
        background-color: #FFFFFF !important;
        color: #1A73E8 !important;
        border: 1.5px solid #1A73E8 !important;
        border-radius: 30px !important;
        padding: 14px 28px !important;
        min-height: 52px !important;
        font-family: 'Google Sans', 'Inter', sans-serif !important;
        font-size: 15px !important;
        font-weight: 700 !important;
        box-shadow: 0 2px 8px rgba(26, 115, 232, 0.16) !important;
        transition: all 0.25s ease !important;
    }
    button[kind="primary"]:hover, 
    button[data-testid="stBaseButton-primary"]:hover,
    .stButton > button[kind="primary"]:hover {
        background-color: #E8F0FE !important;
        color: #1557B0 !important;
        border-color: #1557B0 !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 4px 14px rgba(26, 115, 232, 0.28) !important;
    }
    button[kind="primary"] p,
    button[data-testid="stBaseButton-primary"] p {
        color: #1A73E8 !important;
        font-weight: 700 !important;
    }
    button[kind="primary"]:hover p,
    button[data-testid="stBaseButton-primary"]:hover p {
        color: #1557B0 !important;
    }

    /* Photo Library Tile Card */
    .photo-tile-card {
        background: #FFFFFF;
        border: 1px solid var(--google-border);
        border-radius: 14px;
        overflow: hidden;
        box-shadow: var(--shadow-elevation-1);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
        margin-bottom: 16px;
        cursor: pointer;
    }
    .photo-tile-card:hover {
        transform: translateY(-3px);
        box-shadow: var(--shadow-elevation-2);
        border-color: #AECBFA;
    }
    .photo-tile-thumb {
        height: 180px;
        background: linear-gradient(135deg, #E8F0FE 0%, #D2E3FC 100%);
        display: flex;
        align-items: center;
        justify-content: center;
        position: relative;
        font-size: 48px;
    }
    .photo-tile-body {
        padding: 12px 14px;
    }
    .photo-category-pill {
        display: inline-block;
        font-size: 11px;
        font-weight: 700;
        padding: 2px 8px;
        border-radius: 12px;
        background-color: #E8F0FE;
        color: #1A73E8;
        margin-bottom: 6px;
    }

    /* Comparison Split Screen Cards */
    .comp-col-legacy {
        background: #FFF8F8;
        border: 1.5px solid #F28B82;
        border-radius: 16px;
        padding: 20px;
        height: 100%;
    }
    .comp-col-solution {
        background: #F8FCF8;
        border: 1.5px solid #81C995;
        border-radius: 16px;
        padding: 20px;
        height: 100%;
    }
    .comp-header-legacy {
        color: #C5221F;
        font-weight: 700;
        font-size: 16px;
        margin-bottom: 10px;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    .comp-header-solution {
        color: #137333;
        font-weight: 700;
        font-size: 16px;
        margin-bottom: 10px;
        display: flex;
        align-items: center;
        gap: 8px;
    }

    /* AI Reasoning Box */
    .reasoning-box {
        background-color: #F8FAFD !important;
        border-left: 4px solid var(--google-blue) !important;
        border-radius: 8px 14px 14px 8px !important;
        padding: 14px 18px !important;
        margin: 12px 0 16px 0 !important;
        box-shadow: 0 1px 2px rgba(0,0,0,0.05) !important;
    }
    .reasoning-title {
        font-size: 14px !important;
        font-weight: 700 !important;
        color: var(--google-blue) !important;
        margin-bottom: 6px !important;
        display: flex !important;
        align-items: center !important;
        gap: 6px !important;
    }
    .reasoning-text {
        font-size: 13.5px !important;
        color: #3C4043 !important;
        line-height: 1.55 !important;
    }

    /* Candidate Photo Card */
    .photo-card {
        background: #FFFFFF !important;
        border: 1px solid var(--google-border) !important;
        border-radius: var(--radius-card) !important;
        padding: 16px 18px !important;
        margin-bottom: 12px !important;
        box-shadow: var(--shadow-elevation-1) !important;
        transition: all 0.2s ease !important;
    }
    .photo-card:hover {
        box-shadow: var(--shadow-elevation-2) !important;
        border-color: #B4D5FE !important;
    }
    .photo-header {
        display: flex !important;
        justify-content: space-between !important;
        align-items: center !important;
        margin-bottom: 8px !important;
    }
    .photo-id-tag {
        font-family: monospace !important;
        font-size: 13px !important;
        font-weight: 600 !important;
        color: var(--google-blue) !important;
    }

    /* Match Confidence Badges */
    .badge-confidence-high {
        background-color: #E6F4EA !important;
        color: #137333 !important;
        font-weight: 700 !important;
        font-size: 12px !important;
        padding: 3px 10px !important;
        border-radius: 12px !important;
        border: 1px solid rgba(19, 115, 51, 0.25) !important;
    }
    .badge-confidence-med {
        background-color: #FEF7E0 !important;
        color: #B06000 !important;
        font-weight: 700 !important;
        font-size: 12px !important;
        padding: 3px 10px !important;
        border-radius: 12px !important;
        border: 1px solid rgba(176, 96, 0, 0.25) !important;
    }
    .badge-confidence-low {
        background-color: #FCE8E6 !important;
        color: #C5221F !important;
        font-weight: 700 !important;
        font-size: 12px !important;
        padding: 3px 10px !important;
        border-radius: 12px !important;
        border: 1px solid rgba(197, 34, 31, 0.25) !important;
    }

    /* Google Photos Memories Carousel */
    .memories-container {
        display: flex;
        gap: 14px;
        overflow-x: auto;
        padding: 4px 2px 14px 2px;
        margin-bottom: 20px;
        scrollbar-width: thin;
    }
    .memory-card {
        flex: 0 0 165px;
        height: 220px;
        border-radius: 18px;
        overflow: hidden;
        position: relative;
        cursor: pointer;
        box-shadow: var(--shadow-elevation-1);
        transition: transform 0.25s ease, box-shadow 0.25s ease;
        border: 2px solid transparent;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        padding: 12px;
        text-decoration: none;
        color: #FFFFFF !important;
    }
    .memory-card:hover {
        transform: translateY(-4px) scale(1.02);
        box-shadow: var(--shadow-elevation-2);
        border-color: #1A73E8;
    }
    .memory-card-title {
        font-weight: 700;
        font-size: 13.5px;
        line-height: 1.3;
        text-shadow: 0 1px 4px rgba(0,0,0,0.65);
        z-index: 2;
    }
    .memory-card-subtitle {
        font-size: 11px;
        opacity: 0.9;
        text-shadow: 0 1px 3px rgba(0,0,0,0.6);
        margin-top: 2px;
        z-index: 2;
    }
    .memory-card-badge {
        align-self: flex-start;
        background: rgba(0, 0, 0, 0.45);
        backdrop-filter: blur(4px);
        font-size: 10px;
        font-weight: 600;
        padding: 2px 8px;
        border-radius: 12px;
        z-index: 2;
    }

    /* Timeline Section Header */
    .timeline-header {
        display: flex;
        align-items: baseline;
        gap: 12px;
        margin: 24px 0 12px 0;
        padding-bottom: 8px;
        border-bottom: 1px solid var(--google-border);
    }
    .timeline-title {
        font-size: 18px;
        font-weight: 700;
        color: var(--google-text);
        letter-spacing: -0.2px;
    }
    .timeline-count {
        font-size: 12.5px;
        color: var(--google-subtext);
        font-weight: 500;
    }

    /* Google One Storage Meter */
    .storage-meter-box {
        background: #F8F9FA;
        border: 1px solid var(--google-border);
        border-radius: 14px;
        padding: 14px 16px;
        margin-top: 14px;
    }
    .storage-bar-bg {
        width: 100%;
        height: 6px;
        background-color: #E8EAED;
        border-radius: 3px;
        overflow: hidden;
        margin: 8px 0 6px 0;
    }
    .storage-bar-fill {
        height: 100%;
        background-color: var(--google-blue);
        border-radius: 3px;
    }

    h1, h2, h3, h4, p, span {
        color: var(--google-text);
    }
    </style>
    """
    st.markdown(md3_css, unsafe_allow_html=True)
