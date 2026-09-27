import math
import streamlit as st
import pandas as pd
from components.styles import render_html

CATEGORY_ICONS = {
    "Health & Medical": "💊",
    "Travel & Nature": "🏖️",
    "Food & Dining": "🍕",
    "Documents & Receipts": "🧾",
    "Automotive & Parking": "🚗",
    "Family & Celebrations": "🎉",
    "Home & Personal": "🏡"
}

MEMORIES = [
    {
        "id": "mem_1",
        "title": "1 Year Ago",
        "subtitle": "Winter 2025 Highlights",
        "badge": "Rewind",
        "query": "2025",
        "image_url": "https://images.unsplash.com/photo-1517824806704-9040b037703b?w=600&auto=format&fit=crop&q=80"
    },
    {
        "id": "mem_2",
        "title": "Goa Beachside",
        "subtitle": "Coastal Sunsets & Cafes",
        "badge": "Trip",
        "query": "Goa",
        "image_url": "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=600&auto=format&fit=crop&q=80"
    },
    {
        "id": "mem_3",
        "title": "Food & Cafes",
        "subtitle": "Artisan Brews & Dining",
        "badge": "Culinary",
        "query": "Food & Dining",
        "image_url": "https://images.unsplash.com/photo-1555396273-367ea4eb4db5?w=600&auto=format&fit=crop&q=80"
    },
    {
        "id": "mem_4",
        "title": "Document Vault",
        "subtitle": "Receipts & Paperwork",
        "badge": "Records",
        "query": "Documents & Receipts",
        "image_url": "https://images.unsplash.com/photo-1450133064473-71024230f91b?w=600&auto=format&fit=crop&q=80"
    },
    {
        "id": "mem_5",
        "title": "Winter Moments",
        "subtitle": "Snow & Fireside Evenings",
        "badge": "Seasonal",
        "query": "Winter",
        "image_url": "https://images.unsplash.com/photo-1483921020237-2ff51e8e4b22?w=600&auto=format&fit=crop&q=80"
    }
]

DEFAULT_FALLBACK_IMAGE = "https://images.unsplash.com/photo-1506744038136-46273834b3fb?w=600&auto=format&fit=crop&q=80"

def render_photo_grid(df_catalog: pd.DataFrame):
    """
    Render the authentic Google Photos visual library with:
    - Real photographic imagery for all cards & memories
    - Top Google Photos Memories Carousel
    - Timeline groupings with count badges
    - Category pills & live library search
    - Responsive 36-photo pagination for smooth rendering across 10,000+ items
    - Rich detail drawer modal with OCR tokens
    """

    if df_catalog.empty:
        st.info("No photo catalog data found.")
        return

    # Normalize safe column retrieval
    cat_col = "category" if "category" in df_catalog.columns else ("album_name" if "album_name" in df_catalog.columns else None)
    loc_col = "location" if "location" in df_catalog.columns else ("location_tag" if "location_tag" in df_catalog.columns else None)
    ocr_col = "detected_ocr" if "detected_ocr" in df_catalog.columns else ("ocr_text" if "ocr_text" in df_catalog.columns else None)
    desc_col = "visual_description" if "visual_description" in df_catalog.columns else ("ai_visual_description" if "ai_visual_description" in df_catalog.columns else None)
    img_col = "image_url" if "image_url" in df_catalog.columns else None

    # Top Header
    total_photos = len(df_catalog)
    render_html(f"""
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px; flex-wrap: wrap; gap: 10px;">
        <div>
            <h2 style="font-size: 22px; font-weight: 700; color: #202124; margin: 0; display: flex; align-items: center; gap: 8px;">
                <span>📸 Photo Library</span>
            </h2>
            <div style="font-size: 13.5px; color: #5F6368; margin-top: 3px;">
                Explore your personal timeline with AI scene descriptions, object tags, and extracted OCR tokens.
            </div>
        </div>
        <div style="font-size: 12.5px; color: #1A73E8; background: #E8F0FE; padding: 6px 14px; border-radius: 20px; font-weight: 600;">
            ⚡ {total_photos:,} Multimodal Assets Indexed
        </div>
    </div>
    """)

    # 1. Google Photos Memories Carousel with Real Photography
    st.markdown("<div style='font-size: 14px; font-weight: 700; color: #202124; margin: 8px 0 10px 0;'>✨ Highlights & Memories</div>", unsafe_allow_html=True)
    mem_cols = st.columns(len(MEMORIES))
    for idx, mem in enumerate(MEMORIES):
        with mem_cols[idx]:
            render_html(f"""
            <div class="memory-card" style="background: linear-gradient(180deg, rgba(0,0,0,0.15) 0%, rgba(0,0,0,0.75) 100%), url('{mem['image_url']}') center/cover no-repeat;">
                <span class="memory-card-badge">{mem['badge']}</span>
                <div>
                    <div class="memory-card-title">{mem['title']}</div>
                    <div class="memory-card-subtitle">{mem['subtitle']}</div>
                </div>
            </div>
            """)
            if st.button(f"View {mem['title']}", key=f"btn_mem_{mem['id']}", use_container_width=True):
                st.session_state.catalog_search = mem["query"]
                st.rerun()

    st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)

    # 2. Search & Category Filters
    col_search, col_cat = st.columns([3, 2])
    with col_search:
        search_default = st.session_state.get("catalog_search", "")
        search_query = st.text_input(
            "Search Photos",
            value=search_default,
            placeholder="🔍 Search catalog by keyword, place, or OCR text (e.g. 'Goa', 'receipt', 'medicine', '2024')...",
            label_visibility="collapsed"
        )
        if search_query != search_default:
            st.session_state.catalog_search = search_query
            st.session_state.photo_page = 1

    # Standard high-level categories
    base_cats = [
        "All Photos",
        "Travel & Nature",
        "Food & Dining",
        "Documents & Receipts",
        "Health & Medical",
        "Automotive & Parking",
        "Family & Celebrations",
        "Home & Personal"
    ]

    with col_cat:
        selected_cat = st.selectbox("Filter by Category", base_cats, index=0, label_visibility="collapsed")

    # Apply Filters
    filtered_df = df_catalog.copy()

    if selected_cat != "All Photos":
        filtered_df = filtered_df[
            filtered_df[cat_col].str.contains(selected_cat, case=False, na=False) |
            filtered_df.get("album_name", pd.Series()).str.contains(selected_cat, case=False, na=False)
        ]

    if search_query.strip():
        q = search_query.strip().lower()
        mask = (
            filtered_df["photo_id"].str.lower().str.contains(q, na=False) |
            filtered_df[loc_col].str.lower().str.contains(q, na=False) |
            filtered_df[desc_col].str.lower().str.contains(q, na=False) |
            filtered_df[ocr_col].str.lower().str.contains(q, na=False) |
            filtered_df["timestamp"].str.lower().str.contains(q, na=False)
        )
        filtered_df = filtered_df[mask]

    # Reset search clear button if active
    if search_query.strip() or selected_cat != "All Photos":
        col_info, col_clear = st.columns([4, 1])
        with col_info:
            st.caption(f"Filtered results: **{len(filtered_df):,} photos** matching '{search_query or selected_cat}'")
        with col_clear:
            if st.button("✕ Clear Filter", key="btn_clear_filter", use_container_width=True):
                st.session_state.catalog_search = ""
                st.rerun()

    if filtered_df.empty:
        st.warning("No photos match your current search or category filter. Try a broader search term.")
        return

    # 3. Pagination Controls (36 photos per page)
    PAGE_SIZE = 36
    total_pages = max(1, math.ceil(len(filtered_df) / PAGE_SIZE))

    if "photo_page" not in st.session_state or st.session_state.photo_page > total_pages:
        st.session_state.photo_page = 1

    current_page = st.session_state.photo_page
    start_idx = (current_page - 1) * PAGE_SIZE
    end_idx = min(start_idx + PAGE_SIZE, len(filtered_df))
    page_df = filtered_df.iloc[start_idx:end_idx]

    # Pagination header
    col_p1, col_p2, col_p3 = st.columns([1, 2, 1])
    with col_p1:
        if current_page > 1:
            if st.button("⬅️ Previous Page", key="btn_prev_page", use_container_width=True):
                st.session_state.photo_page -= 1
                st.rerun()
    with col_p2:
        st.markdown(
            f"<div style='text-align: center; font-size: 13.5px; color: #5F6368; padding-top: 6px;'>"
            f"Showing photos <b>{start_idx + 1:,} - {end_idx:,}</b> of <b>{len(filtered_df):,}</b> (Page {current_page} of {total_pages})"
            f"</div>",
            unsafe_allow_html=True
        )
    with col_p3:
        if current_page < total_pages:
            if st.button("Next Page ➡️", key="btn_next_page", use_container_width=True):
                st.session_state.photo_page += 1
                st.rerun()

    # 4. Render Photo Grid (3 per row) with Real Photography
    if "selected_photo_id" not in st.session_state:
        st.session_state.selected_photo_id = None

    cols_per_row = 3
    rows = [page_df.iloc[i:i + cols_per_row] for i in range(0, len(page_df), cols_per_row)]

    for row in rows:
        grid_cols = st.columns(cols_per_row)
        for idx, (_, photo) in enumerate(row.iterrows()):
            with grid_cols[idx]:
                cat = str(photo.get(cat_col, "General"))
                photo_id = str(photo.get("photo_id", f"PHOTO_{idx}"))
                loc = str(photo.get(loc_col, "Unknown Location"))
                ts = str(photo.get("timestamp", ""))
                ocr = str(photo.get(ocr_col, ""))
                desc = str(photo.get(desc_col, ""))
                img_url = str(photo.get("image_url", DEFAULT_FALLBACK_IMAGE)) if img_col else DEFAULT_FALLBACK_IMAGE
                if not img_url or img_url == "None" or not img_url.startswith("http"):
                    img_url = DEFAULT_FALLBACK_IMAGE
                has_ocr = bool(ocr and ocr.lower() != "nan" and ocr.lower() != "none" and ocr.strip())

                # Card HTML with Real Photograph
                render_html(f"""
                <div class="photo-tile-card">
                    <div style="position: relative; width: 100%; height: 185px; overflow: hidden; background-color: #E8EAED;">
                        <img src="{img_url}" alt="{desc}" style="width: 100%; height: 100%; object-fit: cover; transition: transform 0.25s ease;" loading="lazy" />
                        <div style="position: absolute; bottom: 8px; right: 8px; background: rgba(0,0,0,0.7); backdrop-filter: blur(4px); color: #fff; font-size: 11px; padding: 2px 8px; border-radius: 10px; font-weight: 600;">
                            {'📝 OCR Detected' if has_ocr else '🖼️ Visual Match'}
                        </div>
                    </div>
                    <div class="photo-tile-body">
                        <span class="photo-category-pill">{cat}</span>
                        <div style="font-weight: 700; font-size: 13.5px; color: #202124; margin-bottom: 3px; font-family: monospace;">
                            {photo_id}
                        </div>
                        <div style="font-size: 12px; color: #5F6368; margin-bottom: 4px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">
                            📍 {loc}
                        </div>
                        <div style="font-size: 11.5px; color: #80868B;">
                            🗓️ {ts}
                        </div>
                    </div>
                </div>
                """)

                # Inspect Button
                if st.button(f"🔍 Inspect Photo Details", key=f"btn_inspect_{photo_id}", use_container_width=True):
                    st.session_state.selected_photo_id = photo_id
                    st.rerun()

    # 5. Inspection Drawer Modal with High-Res Image Preview
    if st.session_state.selected_photo_id:
        selected_row = df_catalog[df_catalog["photo_id"] == st.session_state.selected_photo_id]
        if not selected_row.empty:
            p = selected_row.iloc[0]
            cat = str(p.get(cat_col, "General"))
            icon = CATEGORY_ICONS.get(cat, "📷")
            loc = str(p.get(loc_col, "Unknown Location"))
            ts = str(p.get("timestamp", ""))
            desc = str(p.get(desc_col, "No description available"))
            objs = str(p.get("detected_objects", "None"))
            ocr = str(p.get(ocr_col, "None"))
            img_url = str(p.get("image_url", DEFAULT_FALLBACK_IMAGE))
            if not img_url or img_url == "None" or not img_url.startswith("http"):
                img_url = DEFAULT_FALLBACK_IMAGE
            if ocr.lower() in ["nan", "none"]:
                ocr = "No printed or handwritten text detected in this image."

            st.markdown("---")
            render_html(f"""
            <div style="background: #FFFFFF; border: 2px solid #1A73E8; border-radius: 16px; padding: 22px 24px; box-shadow: 0 6px 20px rgba(26,115,232,0.18); margin-top: 14px;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 14px; flex-wrap: wrap; gap: 10px;">
                    <div style="display: flex; align-items: center; gap: 10px;">
                        <span style="font-size: 26px;">{icon}</span>
                        <div>
                            <span style="font-size: 18px; font-weight: 700; color: #1A73E8; font-family: monospace;">{p.get('photo_id')}</span>
                            <span class="photo-category-pill" style="margin-left: 8px;">{cat}</span>
                        </div>
                    </div>
                    <span style="font-size: 13px; color: #5F6368;">🗓️ {ts} &nbsp;·&nbsp; 📍 {loc}</span>
                </div>

                <div style="display: flex; gap: 20px; flex-wrap: wrap; margin-bottom: 14px;">
                    <div style="flex: 0 0 280px; height: 210px; border-radius: 12px; overflow: hidden; box-shadow: 0 2px 8px rgba(0,0,0,0.12); background-color: #E8EAED;">
                        <img src="{img_url}" alt="{desc}" style="width: 100%; height: 100%; object-fit: cover;" />
                    </div>
                    <div style="flex: 1; min-width: 260px;">
                        <div style="background: #F8F9FA; border-radius: 10px; padding: 12px 16px; margin-bottom: 10px;">
                            <div style="font-weight: 700; font-size: 13px; color: #202124; margin-bottom: 4px;">🧠 AI Visual Scene Description:</div>
                            <div style="font-size: 13.5px; color: #3C4043; line-height: 1.5;">{desc}</div>
                        </div>
                        <div style="background: #E8F0FE; border-radius: 10px; padding: 12px 14px; margin-bottom: 8px;">
                            <div style="font-weight: 700; font-size: 12.5px; color: #1A73E8; margin-bottom: 4px;">📦 Detected Objects:</div>
                            <div style="font-size: 13px; color: #3C4043;">{objs}</div>
                        </div>
                        <div style="background: #FEF7E0; border-radius: 10px; padding: 12px 14px;">
                            <div style="font-weight: 700; font-size: 12.5px; color: #B06000; margin-bottom: 4px;">📝 Extracted OCR Text:</div>
                            <div style="font-size: 13px; color: #3C4043; font-style: italic;">{ocr}</div>
                        </div>
                    </div>
                </div>
            </div>
            """)
            if st.button("✕ Close Inspector Drawer", key="btn_close_drawer"):
                st.session_state.selected_photo_id = None
                st.rerun()
