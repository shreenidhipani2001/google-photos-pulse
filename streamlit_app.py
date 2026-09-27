import streamlit as st
import pandas as pd
from components.styles import (
    apply_custom_styles,
    render_html,
    GOOGLE_PHOTOS_PINWHEEL_SVG,
    GEMINI_SPARK_SVG
)
from components.photo_grid import render_photo_grid
from components.ask_photos import render_ask_photos
from components.evaluator_mode import render_evaluator_mode
from components.dashboard import render_dashboard
from utils.data_loader import load_all_data
from utils.rag_engine import PhotosRAGEngine

# 1. Streamlit Page Configuration
st.set_page_config(
    page_title="Google Photos - Ask Photos & Episodic Search MVP",
    page_icon="📸",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Inject Material Design 3 Expressive Styles
apply_custom_styles()

# 3. Load Datasets & RAG Engine (Cached)
@st.cache_resource(show_spinner=False)
def get_engine():
    df_feedback, df_catalog = load_all_data()
    engine = PhotosRAGEngine(df_catalog=df_catalog, df_feedback=df_feedback)
    return df_feedback, df_catalog, engine

df_feedback, df_catalog, rag_engine = get_engine()

# 4. Google Photos Left Sidebar Navigation & Storage Quota
view_options = [
    "📸 Photos",
    "✨ Ask Photos",
    "⚖️ Before vs After",
    "📊 Review Pulse"
]

if "current_view" not in st.session_state or st.session_state.current_view not in view_options:
    st.session_state.current_view = "✨ Ask Photos"

with st.sidebar:
    # Google Photos Sidebar Header
    render_html(f"""
    <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 20px; padding: 4px 0;">
        {GOOGLE_PHOTOS_PINWHEEL_SVG}
        <div>
            <div style="font-weight: 700; font-size: 19px; color: #202124; letter-spacing: -0.2px;">Google Photos</div>
            <div style="font-size: 12px; color: #5F6368; display: flex; align-items: center; gap: 4px;">
                <span>Ask Photos MVP</span>
                {GEMINI_SPARK_SVG}
            </div>
        </div>
    </div>
    """)

    st.markdown("<div style='font-size: 11.5px; font-weight: 700; color: #5F6368; text-transform: uppercase; letter-spacing: 0.8px; margin-bottom: 8px;'>Navigation</div>", unsafe_allow_html=True)
    
    selected_view = st.radio(
        "Navigation",
        options=view_options,
        index=view_options.index(st.session_state.current_view),
        label_visibility="collapsed"
    )

    if selected_view != st.session_state.current_view:
        st.session_state.current_view = selected_view
        st.rerun()

    # Google One Storage Quota Meter
    render_html("""
    <div class="storage-meter-box">
        <div style="display: flex; justify-content: space-between; align-items: center; font-size: 12.5px; font-weight: 600; color: #202124;">
            <span>☁️ Google One Storage</span>
            <span style="color: #1A73E8; font-size: 11.5px;">18%</span>
        </div>
        <div class="storage-bar-bg">
            <div class="storage-bar-fill" style="width: 18.4%;"></div>
        </div>
        <div style="font-size: 11.5px; color: #5F6368; display: flex; justify-content: space-between;">
            <span>18.4 GB of 100 GB used</span>
        </div>
    </div>
    """)

    st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)
    st.markdown("<div style='font-size: 11.5px; font-weight: 700; color: #5F6368; text-transform: uppercase; letter-spacing: 0.8px; margin-bottom: 8px;'>Active Repositories</div>", unsafe_allow_html=True)

    catalog_count = len(df_catalog)
    st.metric(label="Photos Catalog", value=f"{catalog_count:,}", delta="Multimodal vision + OCR")
    st.metric(label="Cleaned User Reviews", value="96,926", delta="13 platforms (≥8 words)")
    st.metric(label="Episodic Test Benchmarks", value=f"{len(df_feedback)} cases", delta="Failure taxonomy")

    if st.button("🔄 Reload & Re-index Datasets", use_container_width=True):
        st.cache_resource.clear()
        st.cache_data.clear()
        st.success("Datasets re-indexed successfully!")
        st.rerun()

    st.markdown("---")
    with st.expander("📖 Graduation Project Scope", expanded=False):
        st.markdown("""
        **Problem Statement**:
        Traditional photo search relies on exact EXIF timestamps and filenames. When users have vague or episodic memories (*"medicine when I had fever"*, *"beach cafe with blue chairs"*), search fails completely.

        **The Solution**:
        An AI-powered episodic search assistant that expands subjective memory anchors and matches them to multimodal visual descriptors and OCR tokens.
        """)

# 5. Top App Bar for Main Pane
top_bar_html = f"""
<div class="gp-app-bar" style="margin-bottom: 16px;">
    <div style="display: flex; align-items: center; gap: 12px;">
        <span style="font-size: 16px; font-weight: 700; color: #202124;">
            {st.session_state.current_view}
        </span>
    </div>
    <div style="display: flex; align-items: center; gap: 12px;">
        <span style="font-size: 12px; font-weight: 600; color: #137333; background: #E6F4EA; padding: 5px 12px; border-radius: 16px; border: 1px solid rgba(19,115,51,0.25);">
            ● Gemini Multimodal Active
        </span>
        <div class="gp-user-avatar">S</div>
    </div>
</div>
"""
render_html(top_bar_html)

# 6. View Router
if st.session_state.current_view == "📸 Photos":
    render_photo_grid(df_catalog=df_catalog)

elif st.session_state.current_view == "✨ Ask Photos":
    render_ask_photos(rag_engine=rag_engine)

elif st.session_state.current_view == "⚖️ Before vs After":
    render_evaluator_mode(rag_engine=rag_engine, df_catalog=df_catalog)

elif st.session_state.current_view == "📊 Review Pulse":
    render_dashboard(df_feedback=df_feedback, df_catalog=df_catalog)
