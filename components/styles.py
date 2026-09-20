import streamlit as st

def render_html(html_str: str):
    """
    Safely render HTML without Markdown 4-space code block interpretation.
    Strips leading whitespace on each line so CommonMark never treats HTML as <pre><code>.
    """
    cleaned = "\n".join(line.strip() for line in html_str.strip().splitlines())
    st.markdown(cleaned, unsafe_allow_html=True)

GOOGLE_PHOTOS_PINWHEEL_SVG = """
<svg width="40" height="40" viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg" style="vertical-align: middle; flex-shrink: 0;">
  <path d="M24 4C24 15.0457 15.0457 24 4 24H24V4Z" fill="#EA4335"/>
  <path d="M44 24C32.9543 24 24 15.0457 24 4V24H44Z" fill="#FBBC05"/>
  <path d="M24 44C24 32.9543 32.9543 24 44 24H24V44Z" fill="#34A853"/>
  <path d="M4 24C15.0457 24 24 32.9543 24 44V24H4Z" fill="#4285F4"/>
</svg>
"""

ROBOT_ICON_SVG = """
<svg width="22" height="22" viewBox="0 0 24 24" fill="currentColor" xmlns="http://www.w3.org/2000/svg">
  <path d="M12 2a2 2 0 0 1 2 2c0 .74-.4 1.38-1 1.72V7h4a3 3 0 0 1 3 3v8a3 3 0 0 1-3 3H7a3 3 0 0 1-3-3v-8a3 3 0 0 1 3-3h4V5.72c-.6-.34-1-.98-1-1.72a2 2 0 0 1 2-2zM7.5 13a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3zm9 0a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3zm-7 3a.5.5 0 0 0 0 1h5a.5.5 0 0 0 0-1h-5z"/>
</svg>
"""

def apply_custom_styles():
    """Inject comprehensive Google Material Design 3 theme overrides into Streamlit."""
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
        --radius-bubble: 24px;
        --shadow-elevation-1: 0 1px 3px rgba(60,64,67,0.12), 0 1px 2px rgba(60,64,67,0.18);
        --shadow-elevation-2: 0 4px 10px rgba(60,64,67,0.15), 0 1px 3px rgba(60,64,67,0.25);
    }

    /* Enforce Light Theme Surface on the entire app container */
    [data-testid="stAppViewContainer"], .stApp {
        font-family: 'Google Sans', 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
        background-color: var(--google-bg) !important;
        color: var(--google-text) !important;
    }

    /* Top Streamlit Header */
    header[data-testid="stHeader"] {
        background-color: transparent !important;
    }

    /* Main Container Padding */
    .block-container {
        padding-top: 1.25rem !important;
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
    [data-testid="stSidebar"] [data-testid="stMetricValue"] {
        font-size: 22px !important;
        font-weight: 700 !important;
        color: var(--google-blue) !important;
    }
    [data-testid="stSidebar"] [data-testid="stMetricLabel"] {
        color: var(--google-subtext) !important;
        font-size: 13px !important;
        font-weight: 600 !important;
    }

    /* Top Brand Header Box */
    .gp-header-card {
        display: flex;
        align-items: center;
        justify-content: space-between;
        background: #FFFFFF !important;
        border: 1px solid var(--google-border) !important;
        border-radius: var(--radius-card) !important;
        padding: 14px 22px !important;
        margin-bottom: 18px !important;
        box-shadow: var(--shadow-elevation-1) !important;
    }

    .gp-brand-title {
        font-size: 21px !important;
        font-weight: 700 !important;
        color: var(--google-text) !important;
        line-height: 1.2 !important;
    }

    .gp-brand-subtitle {
        font-size: 13px !important;
        color: var(--google-subtext) !important;
        margin-top: 3px !important;
    }

    .gp-tag {
        display: inline-block !important;
        padding: 4px 12px !important;
        font-size: 12px !important;
        font-weight: 600 !important;
        color: var(--google-blue) !important;
        background-color: var(--google-blue-surface) !important;
        border-radius: 20px !important;
        border: 1px solid rgba(26, 115, 232, 0.25) !important;
    }

    /* Segmented Navigation Tab Switcher */
    div[data-testid="stRadio"] {
        margin-bottom: 18px !important;
    }
    div[data-testid="stRadio"] div[role="radiogroup"] {
        display: inline-flex !important;
        flex-direction: row !important;
        background-color: #EDF2FA !important;
        padding: 4px !important;
        border-radius: 30px !important;
        border: 1px solid #D3E3FD !important;
        gap: 6px !important;
    }
    div[data-testid="stRadio"] div[role="radiogroup"] > label {
        display: flex !important;
        align-items: center !important;
        padding: 8px 20px !important;
        border-radius: 24px !important;
        cursor: pointer !important;
        font-family: 'Google Sans', sans-serif !important;
        font-size: 14px !important;
        font-weight: 600 !important;
        color: #444746 !important;
        background-color: transparent !important;
        transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1) !important;
        margin: 0 !important;
        border: none !important;
    }
    div[data-testid="stRadio"] div[role="radiogroup"] > label > div:first-child {
        display: none !important; /* Hide ugly radio dot */
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
        transition: transform 0.2s ease, box-shadow 0.2s ease !important;
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

    /* Section Card Container */
    .section-card {
        background: #FFFFFF !important;
        border: 1px solid var(--google-border) !important;
        border-radius: var(--radius-card) !important;
        padding: 22px 24px !important;
        box-shadow: var(--shadow-elevation-1) !important;
        margin-bottom: 20px !important;
    }
    .section-header-title {
        font-size: 18px !important;
        font-weight: 700 !important;
        color: var(--google-text) !important;
        margin-bottom: 3px !important;
    }
    .section-header-subtitle {
        font-size: 13px !important;
        color: var(--google-subtext) !important;
        margin-bottom: 16px !important;
    }

    /* Chart Containers */
    .chart-container-box {
        background: #FFFFFF !important;
        border: 1px solid var(--google-border) !important;
        border-radius: var(--radius-card) !important;
        padding: 16px 18px !important;
        box-shadow: var(--shadow-elevation-1) !important;
        margin-bottom: 12px !important;
    }

    /* Conversational Paragraph Card */
    .bot-paragraph-card {
        background-color: #FFFFFF !important;
        border: 1px solid var(--google-border) !important;
        border-left: 5px solid var(--google-blue) !important;
        border-radius: 12px !important;
        padding: 16px 20px !important;
        margin-bottom: 14px !important;
        font-size: 14.5px !important;
        line-height: 1.65 !important;
        color: #202124 !important;
        box-shadow: var(--shadow-elevation-1) !important;
    }

    /* Point-wise Analysis Card */
    .bot-points-card {
        background-color: #FFFFFF !important;
        border: 1px solid var(--google-border) !important;
        border-radius: 14px !important;
        padding: 16px 20px !important;
        margin-bottom: 16px !important;
        box-shadow: var(--shadow-elevation-1) !important;
    }
    .bot-points-header {
        font-size: 15px !important;
        font-weight: 700 !important;
        color: var(--google-blue) !important;
        margin-bottom: 10px !important;
        display: flex !important;
        align-items: center !important;
        gap: 6px !important;
    }
    .bot-point-item {
        font-size: 13.5px !important;
        line-height: 1.6 !important;
        color: #3C4043 !important;
        margin-bottom: 8px !important;
        padding-left: 6px !important;
    }

    /* Reasoning Card */
    .reasoning-box {
        background-color: #F8FAFD !important;
        border-left: 4px solid var(--google-blue) !important;
        border-radius: 8px 16px 16px 8px !important;
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
        line-height: 1.5 !important;
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

    /* Clarifying Alert */
    .clarification-card {
        background-color: #FEF7E0 !important;
        border: 1px solid #F9AB00 !important;
        border-radius: var(--radius-card) !important;
        padding: 14px 18px !important;
        margin-top: 14px !important;
        margin-bottom: 8px !important;
    }
    .clarification-title {
        color: #B06000 !important;
        font-weight: 700 !important;
        font-size: 13.5px !important;
        margin-bottom: 4px !important;
    }
    .clarification-body {
        color: #3C4043 !important;
        font-size: 13px !important;
    }

    /* Prompt Chips Styling */
    .chip-button-row button {
        border-radius: 20px !important;
        border: 1px solid var(--google-border) !important;
        background-color: #FFFFFF !important;
        color: var(--google-text) !important;
        font-size: 12.5px !important;
        font-weight: 500 !important;
        padding: 6px 12px !important;
        transition: all 0.2s ease !important;
    }
    .chip-button-row button:hover {
        background-color: var(--google-blue-surface) !important;
        color: var(--google-blue) !important;
        border-color: var(--google-blue) !important;
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
        box-shadow: 0 2px 8px rgba(26, 115, 232, 0.16), 0 1px 3px rgba(60, 64, 67, 0.1) !important;
        transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1) !important;
    }
    button[kind="primary"]:hover, 
    button[data-testid="stBaseButton-primary"]:hover,
    .stButton > button[kind="primary"]:hover {
        background-color: #E8F0FE !important;
        color: #1557B0 !important;
        border-color: #1557B0 !important;
        box-shadow: 0 4px 14px rgba(26, 115, 232, 0.28) !important;
        transform: translateY(-2px) !important;
    }
    button[kind="primary"] p, 
    button[kind="primary"] span, 
    button[kind="primary"] div,
    button[data-testid="stBaseButton-primary"] p,
    button[data-testid="stBaseButton-primary"] span {
        color: #1A73E8 !important;
        font-weight: 700 !important;
        font-size: 15px !important;
    }
    button[kind="primary"]:hover p,
    button[kind="primary"]:hover span,
    button[data-testid="stBaseButton-primary"]:hover p,
    button[data-testid="stBaseButton-primary"]:hover span {
        color: #1557B0 !important;
    }

    /* Headings and General Text */
    h1, h2, h3, h4, p, span {
        color: var(--google-text);
    }
    </style>
    """
    st.markdown(md3_css, unsafe_allow_html=True)
