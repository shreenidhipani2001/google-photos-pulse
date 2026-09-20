import streamlit as st
import pandas as pd
from components.styles import (
    apply_custom_styles,
    render_html,
    GOOGLE_PHOTOS_PINWHEEL_SVG,
    ROBOT_ICON_SVG
)
from components.dashboard import render_dashboard
from components.rag_bot import render_rag_bot
from utils.data_loader import load_all_data, init_datasets_on_disk
from utils.rag_engine import PhotosRAGEngine

# 1. Page Configuration
st.set_page_config(
    page_title="Google Photos - Discovery Analytics & Search Assistant",
    page_icon="📸",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Inject Google Material Design 3 Styling
apply_custom_styles()

# 3. Session State for Navigation
view_options = ["📊 Photos Review Pulse", "🤖 AI Search Assistant"]
if "active_view" not in st.session_state or st.session_state.active_view not in view_options:
    st.session_state.active_view = "📊 Photos Review Pulse"

def switch_to_bot():
    st.session_state.active_view = "🤖 AI Search Assistant"

def switch_to_dashboard():
    st.session_state.active_view = "📊 Photos Review Pulse"

# 4. Load Datasets & RAG Engine
@st.cache_resource
def get_engine():
    df_feedback, df_catalog = load_all_data()
    engine = PhotosRAGEngine(df_catalog=df_catalog, df_feedback=df_feedback)
    return df_feedback, df_catalog, engine

df_feedback, df_catalog, rag_engine = get_engine()

# 5. Top Material Brand Header (Zero-indentation safe HTML)
header_html = f"""
<div class="gp-header-card">
<div style="display: flex; align-items: center; gap: 14px;">
{GOOGLE_PHOTOS_PINWHEEL_SVG}
<div>
<div class="gp-brand-title">Google Photos <span style="font-weight: 400; color: #5F6368; font-size: 18px; margin-left: 6px;">| Search Intelligence</span></div>
<div class="gp-brand-subtitle">Product Management Case Study & Episodic Retrieval Engine</div>
</div>
</div>
<div style="display: flex; gap: 8px; align-items: center;">
<span class="gp-tag">Case Study Prototype</span>
<span class="gp-tag" style="background-color: #E6F4EA; color: #137333; border-color: rgba(19, 115, 51, 0.25);">MD3 Active</span>
</div>
</div>
"""
render_html(header_html)

# 6. Material Segmented Navigation Bar
selected_view = st.radio(
    "Navigation Switcher",
    options=view_options,
    index=view_options.index(st.session_state.active_view),
    horizontal=True,
    label_visibility="collapsed"
)

if selected_view != st.session_state.active_view:
    st.session_state.active_view = selected_view
    st.rerun()

# 7. Sidebar Controls & Datasets
with st.sidebar:
    st.markdown("### ⚙️ System Controls")
    
    st.markdown("#### 📁 Active Datasets")
    st.metric(label="Cleaned Reviews Pulse", value="96,926", delta="≥8 words, spam removed")
    st.metric(label="Photo Catalog Items", value=f"{len(df_catalog):,} indexed photos")
    st.metric(label="Episodic Feedback Cases", value=f"{len(df_feedback):,} failure reports")

    if st.button("🔄 Reload & Re-index Datasets", use_container_width=True):
        st.cache_resource.clear()
        st.cache_data.clear()
        st.success("Datasets re-indexed successfully!")
        st.rerun()

    st.markdown("---")
    st.markdown("#### 🔀 Quick View Switcher")
    if st.session_state.active_view == "📊 Photos Review Pulse":
        if st.button("🤖 Jump to AI Search Assistant", use_container_width=True, type="primary"):
            switch_to_bot()
            st.rerun()
    else:
        if st.button("📊 Return to Review Pulse", use_container_width=True):
            switch_to_dashboard()
            st.rerun()

    st.markdown("---")
    with st.expander("📖 Case Study Background", expanded=False):
        st.markdown("""
        **Problem Statement:**
        Users frequently struggle to retrieve specific photos using traditional search because human episodic memory stores subjective cues (emotions, seasons, visual colors) rather than technical metadata (EXIF dates, filenames).

        **Proposed Solution:**
        An Episodic Semantic RAG system that bridges the recall gap via:
        1. Query Expansion (synonyms, relative timeframes, visual clues)
        2. Multi-modal Vector Matching (OCR text + AI visual descriptions)
        3. Clarifying Context Loop for ambiguous queries.
        """)

    with st.expander("🔑 Optional LLM API Key", expanded=False):
        st.markdown("The RAG engine is fully self-contained and operates offline with zero API key dependencies. Optionally provide a key for live generation.")
        gemini_key = st.text_input("Gemini API Key", type="password", placeholder="AIzaSy...")
        if gemini_key:
            st.info("Gemini API Key saved for extended synthesis.")

# 8. Main Application Views
if st.session_state.active_view == "📊 Photos Review Pulse":
    render_dashboard(df_feedback=df_feedback, df_catalog=df_catalog)
    
    st.markdown("<div style='height: 24px;'></div>", unsafe_allow_html=True)
    f_c1, f_c2, f_c3 = st.columns([1, 2, 1])
    with f_c2:
        if st.button("🤖 Launch Google Photos AI Search Assistant →", use_container_width=True, type="primary"):
            switch_to_bot()
            st.rerun()

else:
    render_rag_bot(rag_engine=rag_engine)
    
    st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
    b_c1, b_c2, b_c3 = st.columns([1, 2, 1])
    with b_c2:
        if st.button("← Back to Photos Review Pulse Dashboard", use_container_width=True, type="primary"):
            switch_to_dashboard()
            st.rerun()
