import streamlit as st
from components.styles import render_html, GEMINI_SPARK_SVG, ROBOT_ICON_SVG
from utils.rag_engine import PhotosRAGEngine

def render_ask_photos(rag_engine: PhotosRAGEngine):
    """Render the Google Photos 'Ask Photos' Gemini-powered conversational assistant."""

    # Header Card
    render_html(f"""
    <div style="background: #FFFFFF; border: 1px solid #DADCE0; border-radius: 16px; padding: 20px 24px; margin-bottom: 20px; box-shadow: 0 1px 3px rgba(60,64,67,0.1); display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 12px;">
        <div style="display: flex; align-items: center; gap: 12px;">
            {GEMINI_SPARK_SVG}
            <div>
                <h2 style="font-size: 22px; font-weight: 700; color: #202124; margin: 0;">
                    Ask Photos <span style="font-size: 13px; font-weight: 600; color: #1A73E8; background: #E8F0FE; padding: 3px 10px; border-radius: 14px; margin-left: 6px;">Gemini Powered</span>
                </h2>
                <div style="font-size: 13.5px; color: #5F6368; margin-top: 3px;">
                    Search your visual library using natural language, vague memories, and episodic context.
                </div>
            </div>
        </div>
        <div style="font-size: 12.5px; color: #137333; background: #E6F4EA; padding: 6px 14px; border-radius: 20px; font-weight: 600;">
            Multimodal OCR + Vision Match
        </div>
    </div>
    """)

    # Interactive Clue Chips
    render_html("""
    <div style="font-size: 13px; font-weight: 700; color: #202124; margin-bottom: 8px;">
        ✨ Try searching with these episodic memory cues:
    </div>
    """)

    clue_chips = [
        ("💊 Medicine box when I had fever", "medicine box for fever"),
        ("🏖️ Beach cafe with blue chairs in Goa", "beach cafe with blue chairs Goa"),
        ("🧾 Italian dinner receipt downtown", "Italian restaurant receipt total"),
        ("🍪 Grandma's chocolate cookie recipe", "handwritten chocolate chip cookie recipe"),
        ("🚗 Where did I park on level 3?", "car parking ticket level 3")
    ]

    chip_cols = st.columns(len(clue_chips))
    selected_chip_query = None
    for i, (label, query) in enumerate(clue_chips):
        with chip_cols[i]:
            if st.button(label, key=f"chip_{i}", use_container_width=True):
                selected_chip_query = query

    # Chat history state
    if "ask_photos_messages" not in st.session_state:
        st.session_state.ask_photos_messages = []

    # Display Chat History
    for msg in st.session_state.ask_photos_messages:
        if msg["role"] == "user":
            render_html(f"""
            <div style="display: flex; justify-content: flex-end; margin-bottom: 14px;">
                <div style="background-color: #E8F0FE; border: 1px solid #D2E3FC; border-radius: 18px 18px 4px 18px; padding: 12px 18px; max-width: 80%; color: #174EA6; font-weight: 600; font-size: 14.5px;">
                    {msg["content"]}
                </div>
            </div>
            """)
        else:
            _render_ai_response(msg["response_data"])

    # User Input Field
    user_query = st.chat_input("Ask about your memories... e.g. 'yellow box on nightstand when I was sick'")

    # Handle trigger from chip or chat input
    active_query = selected_chip_query or user_query

    if active_query:
        # Add user message
        st.session_state.ask_photos_messages.append({"role": "user", "content": active_query})
        
        # Generate response using RAG Engine
        with st.spinner("🧠 Expanding episodic cues & searching multimodal index..."):
            response_data = rag_engine.answer_query(active_query)
            st.session_state.ask_photos_messages.append({
                "role": "assistant",
                "response_data": response_data
            })
        st.rerun()

    # Clear chat button
    if st.session_state.ask_photos_messages:
        st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)
        if st.button("🗑️ Clear Search Conversation", key="clear_ask_photos"):
            st.session_state.ask_photos_messages = []
            st.rerun()


def _render_ai_response(resp: dict):
    """Render structured AI response with paragraph, bullet points, reasoning, and photo cards."""

    # 1. Conversational Paragraph Card
    summary_text = resp.get("paragraph_summary", "No summary generated.")
    render_html(f"""
    <div style="background-color: #FFFFFF; border: 1px solid #DADCE0; border-left: 5px solid #1A73E8; border-radius: 12px; padding: 16px 20px; margin-bottom: 14px; font-size: 14.5px; line-height: 1.65; color: #202124; box-shadow: 0 1px 3px rgba(60,64,67,0.1);">
        <div style="display: flex; align-items: center; gap: 8px; font-weight: 700; color: #1A73E8; margin-bottom: 6px; font-size: 13.5px;">
            {GEMINI_SPARK_SVG} Ask Photos Response
        </div>
        {summary_text}
    </div>
    """)

    # 2. Point-wise Takeaways
    points = resp.get("point_takeaways", [])
    if points:
        items_html = "".join([f"<li style='margin-bottom: 6px;'>{p}</li>" for p in points])
        render_html(f"""
        <div style="background-color: #FFFFFF; border: 1px solid #DADCE0; border-radius: 14px; padding: 16px 20px; margin-bottom: 14px; box-shadow: 0 1px 3px rgba(60,64,67,0.1);">
            <div style="font-size: 14px; font-weight: 700; color: #1A73E8; margin-bottom: 8px;">
                📌 Key Memory Anchors Identified:
            </div>
            <ul style="margin: 0; padding-left: 20px; font-size: 13.5px; color: #3C4043; line-height: 1.6;">
                {items_html}
            </ul>
        </div>
        """)

    # 3. Episodic Reasoning Card
    reasoning = resp.get("reasoning", "")
    if reasoning:
        render_html(f"""
        <div class="reasoning-box">
            <div class="reasoning-title">
                🧠 Episodic Reasoning Summary:
            </div>
            <div class="reasoning-text">
                {reasoning}
            </div>
        </div>
        """)

    # 4. Retrieved Photo Cards
    photos = resp.get("photos", [])
    if photos:
        render_html(f"""
        <div style="font-size: 14.5px; font-weight: 700; color: #202124; margin: 14px 0 8px 0;">
            🎯 Retrieved Candidate Photos ({len(photos)} matches found):
        </div>
        """)

        for p in photos:
            conf_pct = int(p.get("confidence", 0) * 100)
            if conf_pct >= 65:
                badge_class = "badge-confidence-high"
                badge_text = f"🟢 {conf_pct}% High Match"
            elif conf_pct >= 35:
                badge_class = "badge-confidence-med"
                badge_text = f"🟡 {conf_pct}% Likely Match"
            else:
                badge_class = "badge-confidence-low"
                badge_text = f"🔴 {conf_pct}% Low Match"

            photo_id = p.get("photo_id", "")
            loc = p.get("location", "Unknown Location")
            ts = p.get("timestamp", "")
            cat = p.get("category", "General")
            desc = p.get("visual_description", "")
            objs = p.get("detected_objects", "")
            ocr = p.get("detected_ocr", "")
            img_url = str(p.get("image_url", "https://images.unsplash.com/photo-1506744038136-46273834b3fb?w=600&auto=format&fit=crop&q=80"))
            if not img_url or img_url == "None" or not img_url.startswith("http"):
                img_url = "https://images.unsplash.com/photo-1506744038136-46273834b3fb?w=600&auto=format&fit=crop&q=80"

            ocr_snippet = f"<div style='margin-top: 4px; font-size: 12.5px; color: #3C4043;'><b style='color: #B06000;'>Detected OCR:</b> &ldquo;{ocr}&rdquo;</div>" if ocr and ocr.lower() != "nan" and ocr.lower() != "none" else ""

            render_html(f"""
            <div class="photo-card" style="display: flex; gap: 16px; align-items: flex-start; padding: 16px;">
                <div style="flex: 0 0 150px; height: 135px; border-radius: 10px; overflow: hidden; background-color: #E8EAED; box-shadow: 0 1px 4px rgba(0,0,0,0.12);">
                    <img src="{img_url}" alt="{desc}" style="width: 100%; height: 100%; object-fit: cover;" loading="lazy" />
                </div>
                <div style="flex: 1; min-width: 0;">
                    <div class="photo-header" style="margin-bottom: 6px;">
                        <span class="photo-id-tag">📷 {photo_id}</span>
                        <span class="{badge_class}">{badge_text}</span>
                    </div>
                    <div style="font-size: 12.5px; color: #5F6368; margin-bottom: 6px;">
                        📍 {loc} &nbsp;•&nbsp; 🗓️ {ts} &nbsp;•&nbsp; 📁 {cat}
                    </div>
                    <div style="font-size: 13px; color: #202124; line-height: 1.5; margin-bottom: 4px;">
                        <b>AI Visual Description:</b> {desc}
                    </div>
                    <div style="font-size: 12.5px; color: #1A73E8;">
                        <b>Detected Objects:</b> {objs}
                    </div>
                    {ocr_snippet}
                </div>
            </div>
            """)

    # 5. Clarifying Follow-up Loop
    clarifying_q = resp.get("clarifying_question")
    if clarifying_q:
        render_html(f"""
        <div style="background-color: #FEF7E0; border: 1px solid #F9AB00; border-radius: 12px; padding: 14px 18px; margin-top: 14px;">
            <div style="color: #B06000; font-weight: 700; font-size: 13.5px; margin-bottom: 4px;">
                ❓ Clarifying Question (Narrow Your Memory):
            </div>
            <div style="color: #3C4043; font-size: 13px;">
                {clarifying_q}
            </div>
        </div>
        """)
