import streamlit as st
import time
from typing import Dict, Any
from utils.rag_engine import PhotosRAGEngine
from components.styles import render_html

def render_confidence_badge(score: int) -> str:
    """Render a Google Material styled confidence percentage badge."""
    if score >= 80:
        return f'<span class="badge-confidence-high">🟢 {score}% Match Confidence</span>'
    elif score >= 60:
        return f'<span class="badge-confidence-med">🟡 {score}% Match Confidence</span>'
    else:
        return f'<span class="badge-confidence-low">🔴 {score}% Match Confidence</span>'

def render_photo_card(photo: Dict[str, Any]):
    """Render an individual candidate photo result card."""
    badge_html = render_confidence_badge(photo.get("confidence_score", 0))
    ocr_text = photo.get("ocr_text", "None")
    ocr_display = f'<div style="font-size: 12px; color: #444746; background: #F1F3F4; padding: 5px 9px; border-radius: 6px; font-family: monospace; margin-top: 6px;"><b>Detected OCR:</b> "{ocr_text}"</div>' if ocr_text and ocr_text != "None" else ""

    card_html = f"""
    <div class="photo-card">
    <div class="photo-header">
    <span class="photo-id-tag">📷 {photo.get('photo_id', 'PHOTO')}</span>
    {badge_html}
    </div>
    <div style="font-size: 13.5px; font-weight: 600; color: #1F1F1F; margin-bottom: 4px;">
    📍 {photo.get('location_tag', 'Unknown Location')} &nbsp;•&nbsp; 🗓️ {photo.get('timestamp', 'Date unknown')} &nbsp;•&nbsp; 📁 {photo.get('album_name', 'General')}
    </div>
    <div style="font-size: 13px; color: #3C4043; line-height: 1.45; margin-bottom: 6px;">
    <b>AI Visual Description:</b> {photo.get('ai_visual_description', '')}
    </div>
    <div style="font-size: 12px; color: #5F6368; margin-top: 4px;">
    <b>Detected Objects:</b> {photo.get('detected_objects', 'None')}
    </div>
    {ocr_display}
    </div>
    """
    render_html(card_html)

def render_bot_message_content(response: Dict[str, Any]):
    """Render the structured RAG response with paragraph, point-wise breakdown, reasoning, and photo cards."""
    # 1. Conversational Paragraph Summary
    para = response.get("paragraph_response")
    if para:
        paragraph_html = f"""
        <div class="bot-paragraph-card">
        {para}
        </div>
        """
        render_html(paragraph_html)

    # 2. Point-Wise Breakdown Card
    points = response.get("point_wise_response", [])
    if points:
        points_html_list = []
        for title, desc in points:
            points_html_list.append(f'<div class="bot-point-item"><b>{title}:</b> {desc}</div>')
        all_points = "".join(points_html_list)
        
        header_text = "Key Product Management Findings & Evidence" if response.get("is_conceptual") else "Episodic Retrieval & Match Breakdown"
        points_card_html = f"""
        <div class="bot-points-card">
        <div class="bot-points-header">📌 {header_text}</div>
        {all_points}
        </div>
        """
        render_html(points_card_html)

    # 3. Episodic Reasoning Summary Box
    reasoning = response.get("reasoning")
    if reasoning:
        reasoning_html = f"""
        <div class="reasoning-box">
        <div class="reasoning-title">
        <span>🧠 Episodic Reasoning Summary</span>
        </div>
        <div class="reasoning-text">
        {reasoning}
        </div>
        </div>
        """
        render_html(reasoning_html)

    # 4. Related Historical Failure Context Drawer
    hist = response.get("historical_feedback_context", [])
    if hist:
        with st.expander("📌 Related Historical Search Failure Context from User Reviews", expanded=False):
            for h in hist:
                item_html = f"""
                <div style="font-size: 12.5px; margin-bottom: 6px;">
                • Similar past complaint: <i>"{h.get('query')}"</i><br>
                &nbsp;&nbsp;<b>Failure Reason:</b> <span style="color:#C5221F;">{h.get('failure_reason')}</span> | <b>Root Cause:</b> User forgot {h.get('forgotten')}
                </div>
                """
                render_html(item_html)

    # 5. Retrieved Candidate Photos (only for photo queries)
    show_photos = response.get("show_photos", True)
    matches = response.get("matches", [])
    if show_photos and matches:
        title_html = f"""
        <div style="font-size: 14.5px; font-weight: 700; color: #202124; margin: 14px 0 8px 0;">
        🎯 Retrieved Candidate Photos ({len(matches)} matches found):
        </div>
        """
        render_html(title_html)
        for photo in matches:
            render_photo_card(photo)

    # 6. Clarifying Follow-up Question if confidence < 70%
    clarifying = response.get("clarifying_question")
    if show_photos and clarifying:
        clarifying_html = f"""
        <div class="clarification-card">
        <div class="clarification-title">
        ❓ Clarifying Follow-up Question (Confidence &lt; 70%)
        </div>
        <div class="clarification-body">
        {clarifying}
        </div>
        </div>
        """
        render_html(clarifying_html)

def render_rag_bot(rag_engine: PhotosRAGEngine):
    """Render the interactive Google Photos Search Assistant Chatbot interface."""
    
    header_html = """
    <div style="margin-bottom: 16px;">
    <h2 style="font-size: 24px; font-weight: 700; color: #202124; margin-bottom: 4px;">
    🤖 Google Photos Search Assistant
    </h2>
    <p style="color: #5F6368; font-size: 14px; margin: 0;">
    Ask questions the way humans remember them. The assistant translates episodic memory clues (time, color, feeling, location) into photographic matches.
    </p>
    </div>
    """
    render_html(header_html)

    # Initialize chat memory in session state
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {
                "role": "assistant",
                "type": "welcome",
                "content": (
                    "👋 **Hi! I'm your Google Photos Search Assistant.**\n\n"
                    "I can find photos even if you don't remember the exact date, album, or file name! "
                    "Tell me what you remember—like *\"the medicine photo I took when sick last year\"*, "
                    "*\"small cafe in Goa with blue chairs\"*, or *\"dog running in snow\"*."
                )
            }
        ]

    # Pre-built example prompt chips (formatted in 2 rows of 3 columns)
    render_html("<div style='font-size: 13px; font-weight: 600; color: #5F6368; margin-bottom: 8px;'>✨ Try an episodic memory search:</div>")
    
    chips_row1 = [
        ("💊 Yellow medicine box last year", "the medicine photo I took when sick last year"),
        ("☕ Goa trip small cafe", "small cafe in Goa with blue chairs"),
        ("📝 Handwritten recipe card", "handwritten recipe card for pasta bake")
    ]
    chips_row2 = [
        ("🐕 Dog playing in snow", "my dog running in heavy snow with red collar"),
        ("✈️ Boarding pass to Paris", "boarding pass flight to Paris terminal 3"),
        ("🎂 Dinosaur birthday cake", "kids birthday cake with dinosaur toy on top")
    ]

    selected_chip_query = None

    row1_cols = st.columns(3)
    for i, (label, prompt_text) in enumerate(chips_row1):
        with row1_cols[i]:
            if st.button(label, key=f"chip_r1_{i}", use_container_width=True):
                selected_chip_query = prompt_text

    row2_cols = st.columns(3)
    for i, (label, prompt_text) in enumerate(chips_row2):
        with row2_cols[i]:
            if st.button(label, key=f"chip_r2_{i}", use_container_width=True):
                selected_chip_query = prompt_text

    st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)

    # Conversation control actions
    c_col1, c_col2 = st.columns([6, 1])
    with c_col2:
        if st.button("🗑️ Clear Chat", use_container_width=True):
            st.session_state.messages = [
                {
                    "role": "assistant",
                    "type": "welcome",
                    "content": "Chat history cleared. How can I help you find your memories?"
                }
            ]
            st.rerun()

    # Display conversation messages
    for msg in st.session_state.messages:
        role = msg["role"]
        avatar = "🤖" if role == "assistant" else "👤"
        with st.chat_message(role, avatar=avatar):
            if msg.get("type") == "rag_result":
                render_bot_message_content(msg["response_data"])
            else:
                st.markdown(msg["content"])

    # Chat Input handler
    user_input = st.chat_input("Describe the memory you want to find (e.g. 'romantic dinner receipt last month')...")

    # If chip was clicked, treat it as input
    active_query = selected_chip_query or user_input

    if active_query:
        # Display user message
        st.session_state.messages.append({"role": "user", "type": "text", "content": active_query})
        with st.chat_message("user", avatar="👤"):
            st.markdown(active_query)

        # Generate RAG response
        with st.chat_message("assistant", avatar="🤖"):
            with st.spinner("Analyzing episodic memory clues & vector indexing catalog..."):
                rag_result = rag_engine.search(active_query)
                time.sleep(0.3)
                render_bot_message_content(rag_result)

            # Store in session state
            st.session_state.messages.append({
                "role": "assistant",
                "type": "rag_result",
                "response_data": rag_result,
                "content": rag_result["reasoning"]
            })
            st.rerun()
