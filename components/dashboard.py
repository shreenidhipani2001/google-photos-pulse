import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os

from components.styles import render_html, GOOGLE_PHOTOS_PINWHEEL_SVG
from utils.pulse_data import (
    PULSE_SUMMARY,
    STAR_RATINGS,
    PLATFORM_ENTRIES,
    PLATFORM_SENTIMENT,
    THEMES_CROSSTAB,
    THEME_PLATFORM_MATRIX,
    KEYWORD_EXPLORER,
    TIMELINE_DATA,
    TOP_COUNTRIES,
    TOP_VERSIONS
)

PLOTLY_CONFIG = {
    "displayModeBar": False,
    "responsive": True
}

@st.cache_data(show_spinner=False)
def load_master_reviews_df():
    """Load a subset of master reviews for live interactive exploration."""
    csv_path = "Google_Photos_Master_Reviews.csv"
    if os.path.exists(csv_path):
        try:
            cols = ["review_id", "platform", "rating", "date", "country", "title", "content", "app_version"]
            df = pd.read_csv(csv_path, usecols=cols, nrows=15000)
            df["rating"] = pd.to_numeric(df["rating"], errors="coerce")
            return df
        except Exception:
            return pd.DataFrame()
    return pd.DataFrame()

def render_dashboard(df_feedback: pd.DataFrame, df_catalog: pd.DataFrame):
    """
    Render the comprehensive 'Photos Review Pulse' Executive Discovery Dashboard.
    Master dataset: 117,037 reviews across 13 platforms (Jan 2018 - Sep 2026).
    """

    # 1. Hero Brand Header
    _render_hero_header()

    st.markdown("<div style='height: 14px;'></div>", unsafe_allow_html=True)

    # 2. Key Metrics Row (4 Primary + 3 Operational)
    _render_key_metrics()

    st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)

    # 3. Sentiment & Star Rating Overview
    _render_sentiment_and_ratings()

    st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)

    # 4. Platform Analysis
    _render_platform_analysis()

    st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)

    # 5. Complaint Theme Analysis
    _render_complaint_themes()

    st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)

    # 6. Interactive Keyword Explorer
    _render_keyword_explorer()

    st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)

    # 7. Trends Over Time (Jan 2018 - Sep 2026)
    _render_trends_over_time()

    st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)

    # 8. Geography & Problem Versions
    _render_geography_and_versions()

    st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)

    # 9. Episodic Recall Asymmetry (PM Bridge to AI Retrieval)
    _render_episodic_recall_bridge(df_feedback)

    st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)

    # 10. Interactive Raw Review Explorer
    _render_review_explorer()


def _render_hero_header():
    """Render the master 'Photos Review Pulse' header without duplicating top branding."""
    header_html = f"""
    <div style="background: #FFFFFF; border: 1px solid #DADCE0; border-radius: 16px; padding: 20px 24px; box-shadow: 0 1px 3px rgba(60,64,67,0.1); display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 14px;">
        <div>
            <div style="font-size: 24px; font-weight: 700; color: #202124; letter-spacing: -0.3px; display: flex; align-items: center; gap: 10px;">
                <span>Photos Review Pulse</span>
                <span style="font-size: 13px; font-weight: 600; color: #1A73E8; background: #E8F0FE; padding: 3px 10px; border-radius: 14px;">Executive Telemetry</span>
            </div>
            <div style="font-size: 13.5px; color: #5F6368; margin-top: 4px; font-weight: 500;">
                <b style="color: #1A73E8;">13 platforms</b> &nbsp;·&nbsp; reviews since Jan 2018 &nbsp;·&nbsp; <b style="color: #202124;">96,926 cleaned reviews (≥8 words)</b>
            </div>
        </div>
        <div style="display: flex; align-items: center; gap: 8px; flex-wrap: wrap;">
            <span style="display: inline-flex; align-items: center; gap: 6px; padding: 6px 12px; font-size: 12px; font-weight: 600; color: #137333; background-color: #E6F4EA; border-radius: 18px; border: 1px solid rgba(19, 115, 51, 0.25);">
                <span style="width: 7px; height: 7px; border-radius: 50%; background-color: #34A853; display: inline-block;"></span>
                Cleaned Substantive Dataset (Jan 2018 – Sep 2026)
            </span>
            <span style="display: inline-flex; align-items: center; padding: 6px 12px; font-size: 12px; font-weight: 600; color: #1A73E8; background-color: #E8F0FE; border-radius: 18px; border: 1px solid rgba(26, 115, 232, 0.25);">
                80.7% Rated Coverage
            </span>
        </div>
    </div>
    """
    render_html(header_html)


def _render_key_metrics():
    """Render the 7 Key Metrics KPI Cards in a balanced 4 + 3 layout to prevent text squishing."""
    render_html("""
    <div style="margin-bottom: 8px;">
        <h3 style="font-size: 17px; font-weight: 700; color: #202124; margin-bottom: 2px;">
            Key metrics
        </h3>
        <p style="font-size: 12.5px; color: #5F6368; margin: 0;">
            Macro-level performance indicators across all global platforms, app stores, and developer communities.
        </p>
    </div>
    """)

    # Row 1: 4 Primary Metrics
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        render_html(f"""
        <div class="metric-card">
            <div class="metric-title">Total reviews</div>
            <div class="metric-value">{PULSE_SUMMARY['total_reviews']:,}</div>
            <div class="metric-delta">13 platforms combined</div>
        </div>
        """)
    with c2:
        render_html(f"""
        <div class="metric-card">
            <div class="metric-title">Average rating</div>
            <div class="metric-value" style="color: #1A73E8;">{PULSE_SUMMARY['avg_rating']}<span style="font-size: 15px; color: #5F6368;"> / 5</span></div>
            <div class="metric-delta">{PULSE_SUMMARY['rated_reviews']:,} rated reviews</div>
        </div>
        """)
    with c3:
        render_html(f"""
        <div class="metric-card">
            <div class="metric-title">Negative share</div>
            <div class="metric-value" style="color: #EA4335;">{PULSE_SUMMARY['negative_pct']}%</div>
            <div class="metric-delta" style="color: #EA4335;">{PULSE_SUMMARY['negative_count']:,} entries</div>
        </div>
        """)
    with c4:
        render_html(f"""
        <div class="metric-card">
            <div class="metric-title">Positive share</div>
            <div class="metric-value" style="color: #34A853;">{PULSE_SUMMARY['positive_pct']}%</div>
            <div class="metric-delta" style="color: #137333;">{PULSE_SUMMARY['positive_count']:,} entries</div>
        </div>
        """)

    st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)

    # Row 2: 3 Operational Metrics
    c5, c6, c7 = st.columns(3)
    with c5:
        render_html(f"""
        <div class="metric-card">
            <div class="metric-title">Top complaint</div>
            <div class="metric-value" style="font-size: 18px; color: #202124;">{PULSE_SUMMARY['top_complaint']}</div>
            <div class="metric-delta" style="color: #EA4335;">{PULSE_SUMMARY['top_complaint_entries']:,} entries (32.9% neg)</div>
        </div>
        """)
    with c6:
        render_html(f"""
        <div class="metric-card">
            <div class="metric-title">Platforms tracked</div>
            <div class="metric-value">{PULSE_SUMMARY['platforms_tracked']}</div>
            <div class="metric-delta">app stores, forums & dev sites</div>
        </div>
        """)
    with c7:
        render_html(f"""
        <div class="metric-card">
            <div class="metric-title">Net Sentiment Score</div>
            <div class="metric-value" style="color: #1A73E8;">+{PULSE_SUMMARY['net_sentiment_score']}%</div>
            <div class="metric-delta">Positive % minus Negative %</div>
        </div>
        """)


def _render_sentiment_and_ratings():
    """Render Sentiment Distribution Donut Chart and Star Rating Distribution Horizontal Bars."""
    render_html("""
    <div style="margin-bottom: 10px;">
        <h3 style="font-size: 17px; font-weight: 700; color: #202124; margin-bottom: 2px;">
            Sentiment & rating overview
        </h3>
        <p style="font-size: 12.5px; color: #5F6368; margin: 0;">
            Global distribution of feedback polarity and calibrated 1-to-5 star rating breakdown.
        </p>
    </div>
    """)

    col_sent, col_stars = st.columns([1, 1])

    with col_sent:
        render_html("""
        <div class="chart-container-box">
            <div style="font-size: 15px; font-weight: 700; color: #202124;">
                Sentiment distribution
            </div>
            <div style="font-size: 12px; color: #5F6368;">
                Derived from star rating per review
            </div>
        </div>
        """)

        sent_labels = ["Positive", "Negative", "Neutral", "Unknown"]
        sent_values = [
            PULSE_SUMMARY["positive_count"],
            PULSE_SUMMARY["negative_count"],
            PULSE_SUMMARY["neutral_count"],
            PULSE_SUMMARY["unknown_count"]
        ]
        sent_colors = ["#34A853", "#EA4335", "#FBBC05", "#BDC1C6"]

        fig_sent = go.Figure(data=[go.Pie(
            labels=sent_labels,
            values=sent_values,
            hole=0.55,
            marker=dict(colors=sent_colors, line=dict(color="#FFFFFF", width=2)),
            textinfo="percent+label",
            textposition="inside",
            hovertemplate="<b>%{label}</b><br>Count: %{value:,}<br>Share: %{percent}<extra></extra>"
        )])

        fig_sent.update_layout(
            showlegend=False,
            margin=dict(t=10, b=10, l=10, r=10),
            height=260,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(family="Google Sans, Inter, sans-serif")
        )
        st.plotly_chart(fig_sent, use_container_width=True, config=PLOTLY_CONFIG)

        # 2x2 Clean Micro-stat grid
        render_html(f"""
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 8px; margin-top: 6px;">
            <div style="background: #E6F4EA; border-radius: 8px; padding: 8px 12px; border: 1px solid rgba(52,168,83,0.2);">
                <div style="font-size: 11px; font-weight: 600; color: #137333;">POSITIVE</div>
                <div style="font-size: 16px; font-weight: 700; color: #137333;">47.8% <span style="font-size: 12px; font-weight: 400; color: #5F6368;">(55,926)</span></div>
            </div>
            <div style="background: #FCE8E6; border-radius: 8px; padding: 8px 12px; border: 1px solid rgba(234,67,53,0.2);">
                <div style="font-size: 11px; font-weight: 600; color: #C5221F;">NEGATIVE</div>
                <div style="font-size: 16px; font-weight: 700; color: #C5221F;">27.2% <span style="font-size: 12px; font-weight: 400; color: #5F6368;">(31,876)</span></div>
            </div>
            <div style="background: #FEF7E0; border-radius: 8px; padding: 8px 12px; border: 1px solid rgba(251,188,5,0.3);">
                <div style="font-size: 11px; font-weight: 600; color: #B06000;">NEUTRAL</div>
                <div style="font-size: 16px; font-weight: 700; color: #B06000;">7.7% <span style="font-size: 12px; font-weight: 400; color: #5F6368;">(9,055)</span></div>
            </div>
            <div style="background: #F1F3F4; border-radius: 8px; padding: 8px 12px; border: 1px solid #DADCE0;">
                <div style="font-size: 11px; font-weight: 600; color: #5F6368;">UNKNOWN</div>
                <div style="font-size: 16px; font-weight: 700; color: #5F6368;">17.2% <span style="font-size: 12px; font-weight: 400; color: #5F6368;">(20,180)</span></div>
            </div>
        </div>
        """)

    with col_stars:
        render_html("""
        <div class="chart-container-box">
            <div style="font-size: 15px; font-weight: 700; color: #202124;">
                Star rating distribution
            </div>
            <div style="font-size: 12px; color: #5F6368;">
                96,857 rated · Average 3.47 / 5 across rated reviews
            </div>
        </div>
        """)

        df_stars = pd.DataFrame(STAR_RATINGS)

        fig_stars = go.Figure()
        fig_stars.add_trace(go.Bar(
            y=df_stars["stars"],
            x=df_stars["count"],
            orientation="h",
            text=[f"{count:,} ({pct}%)" for count, pct in zip(df_stars["count"], df_stars["pct"])],
            textposition="auto",
            marker=dict(color=df_stars["color"].tolist(), line=dict(color="#FFFFFF", width=1.5)),
            hovertemplate="<b>%{y}</b><br>Reviews: %{x:,}<extra></extra>"
        ))

        fig_stars.update_layout(
            height=260,
            margin=dict(t=10, b=10, l=10, r=20),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            xaxis=dict(showgrid=True, gridcolor="#E8EAED", title="Review Count"),
            yaxis=dict(autorange="reversed", showgrid=False),
            font=dict(family="Google Sans, Inter, sans-serif")
        )
        st.plotly_chart(fig_stars, use_container_width=True, config=PLOTLY_CONFIG)

        render_html("""
        <div style="background: #FFFFFF; border: 1px solid #DADCE0; border-radius: 8px; padding: 10px 14px; font-size: 12.5px; color: #3C4043; line-height: 1.45; margin-top: 6px;">
            <b>Bimodal Distribution:</b> Over <b>46.6%</b> award 5★, yet <b>24.7%</b> give a 1★ rating, reflecting severe polarization driven by sync loops and sudden redesigns.
        </div>
        """)


def _render_platform_analysis():
    """Render Entries by Platform (All 13) and Sentiment by Platform."""
    render_html("""
    <div style="margin-bottom: 10px;">
        <h3 style="font-size: 17px; font-weight: 700; color: #202124; margin-bottom: 2px;">
            Platform analysis
        </h3>
        <p style="font-size: 12.5px; color: #5F6368; margin: 0;">
            Cross-ecosystem volume comparison and sentiment divergence between Android, iOS, and developer channels.
        </p>
    </div>
    """)

    col_plat1, col_plat2 = st.columns([1, 1])

    with col_plat1:
        render_html("""
        <div class="chart-container-box">
            <div style="font-size: 15px; font-weight: 700; color: #202124;">
                Entries by platform
            </div>
            <div style="font-size: 12px; color: #5F6368;">
                All 13 sources, by review volume
            </div>
        </div>
        """)

        df_plat = pd.DataFrame(PLATFORM_ENTRIES)

        fig_plat = go.Figure(go.Bar(
            y=df_plat["platform"],
            x=df_plat["volume"],
            orientation="h",
            text=[f"{v:,} ({s}%)" for v, s in zip(df_plat["volume"], df_plat["share_pct"])],
            textposition="auto",
            marker=dict(
                color=["#1A73E8" if r else "#8AB4F8" for r in df_plat["rated"]],
                line=dict(color="#FFFFFF", width=1)
            ),
            hovertemplate="<b>%{y}</b><br>Entries: %{x:,}<extra></extra>"
        ))

        fig_plat.update_layout(
            height=380,
            margin=dict(t=10, b=10, l=10, r=20),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            xaxis=dict(showgrid=True, gridcolor="#E8EAED", title="Review Volume"),
            yaxis=dict(autorange="reversed", showgrid=False, tickfont=dict(size=11)),
            font=dict(family="Google Sans, Inter, sans-serif")
        )
        st.plotly_chart(fig_plat, use_container_width=True, config=PLOTLY_CONFIG)

    with col_plat2:
        render_html("""
        <div class="chart-container-box">
            <div style="font-size: 15px; font-weight: 700; color: #202124;">
                Sentiment by platform
            </div>
            <div style="font-size: 12px; color: #5F6368;">
                Rating-bearing sources only stacked
            </div>
        </div>
        """)

        df_sent_plat = pd.DataFrame(PLATFORM_SENTIMENT)
        for s in ["Negative", "Positive", "Neutral", "Unknown"]:
            df_sent_plat[f"{s}_pct"] = (df_sent_plat[s] / df_sent_plat["total"]) * 100

        fig_stack = go.Figure()
        fig_stack.add_trace(go.Bar(
            y=df_sent_plat["platform"],
            x=df_sent_plat["Negative_pct"],
            name="Negative",
            orientation="h",
            marker=dict(color="#EA4335"),
            text=[f"{v:.1f}%" for v in df_sent_plat["Negative_pct"]],
            textposition="inside",
            hovertemplate="<b>%{y}</b> - Negative<br>Share: %{x:.1f}%<br>Count: %{customdata:,}<extra></extra>",
            customdata=df_sent_plat["Negative"]
        ))
        fig_stack.add_trace(go.Bar(
            y=df_sent_plat["platform"],
            x=df_sent_plat["Positive_pct"],
            name="Positive",
            orientation="h",
            marker=dict(color="#34A853"),
            text=[f"{v:.1f}%" for v in df_sent_plat["Positive_pct"]],
            textposition="inside",
            hovertemplate="<b>%{y}</b> - Positive<br>Share: %{x:.1f}%<br>Count: %{customdata:,}<extra></extra>",
            customdata=df_sent_plat["Positive"]
        ))
        fig_stack.add_trace(go.Bar(
            y=df_sent_plat["platform"],
            x=df_sent_plat["Neutral_pct"],
            name="Neutral",
            orientation="h",
            marker=dict(color="#FBBC05"),
            text=[f"{v:.1f}%" for v in df_sent_plat["Neutral_pct"]],
            textposition="inside",
            hovertemplate="<b>%{y}</b> - Neutral<br>Share: %{x:.1f}%<br>Count: %{customdata:,}<extra></extra>",
            customdata=df_sent_plat["Neutral"]
        ))
        fig_stack.add_trace(go.Bar(
            y=df_sent_plat["platform"],
            x=df_sent_plat["Unknown_pct"],
            name="Unknown",
            orientation="h",
            marker=dict(color="#BDC1C6"),
            text=[f"{v:.1f}%" for v in df_sent_plat["Unknown_pct"]],
            textposition="inside",
            hovertemplate="<b>%{y}</b> - Unknown<br>Share: %{x:.1f}%<br>Count: %{customdata:,}<extra></extra>",
            customdata=df_sent_plat["Unknown"]
        ))

        fig_stack.update_layout(
            barmode="stack",
            height=380,
            margin=dict(t=10, b=10, l=10, r=10),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            xaxis=dict(showgrid=True, gridcolor="#E8EAED", title="Sentiment Distribution (%)", range=[0, 100]),
            yaxis=dict(autorange="reversed", showgrid=False),
            legend=dict(orientation="h", yanchor="bottom", y=-0.22, xanchor="center", x=0.5),
            font=dict(family="Google Sans, Inter, sans-serif")
        )
        st.plotly_chart(fig_stack, use_container_width=True, config=PLOTLY_CONFIG)

    # Executive Platform Insight Callout
    render_html("""
    <div style="background: #FFF8E1; border-left: 5px solid #F9AB00; border-radius: 12px; padding: 14px 18px; margin-top: 4px;">
        <div style="font-weight: 700; color: #B06000; font-size: 14px; margin-bottom: 4px;">
            ⚠️ Platform Divergence Takeaway
        </div>
        <div style="color: #3C4043; font-size: 13px; line-height: 1.55;">
            <b>Google Play (Main App)</b> is the single largest and most negative rating-bearing source at <b>35.2% negative reviews</b> (18,204 negative entries). In comparison, the <b>Apple App Store</b> maintains a significantly lower negative share of <b>19.8%</b>, largely due to stricter iOS background permission controls preventing catastrophic battery drain during cloud backup.
        </div>
    </div>
    """)


def _render_complaint_themes():
    """Render Complaint Theme Frequency, Severity Bubble Quadrant, and Cross-tab Matrix."""
    render_html("""
    <div style="margin-bottom: 10px;">
        <h3 style="font-size: 17px; font-weight: 700; color: #202124; margin-bottom: 2px;">
            Complaint theme analysis (14 themes tracked)
        </h3>
        <p style="font-size: 12.5px; color: #5F6368; margin: 0;">
            Focus on the <b>13 actionable themes</b> (excluding General feedback's 96,336 baseline entries).
        </p>
    </div>
    """)

    actionable_themes = [t for t in THEMES_CROSSTAB if t["theme"] != "General feedback / other"]
    df_act = pd.DataFrame(actionable_themes).sort_values(by="Total", ascending=True)

    col_th1, col_th2 = st.columns([1, 1])

    with col_th1:
        render_html("""
        <div class="chart-container-box">
            <div style="font-size: 15px; font-weight: 700; color: #202124;">
                Actionable theme frequency & toxicity
            </div>
            <div style="font-size: 12px; color: #5F6368;">
                Total entries per theme, color-coded by Negative Share %
            </div>
        </div>
        """)

        fig_act = px.bar(
            df_act,
            x="Total",
            y="theme",
            orientation="h",
            color="neg_pct",
            color_continuous_scale=["#34A853", "#FBBC05", "#EA4335"],
            labels={"Total": "Total Entries", "neg_pct": "Negative %", "theme": "Theme"},
            text="Total"
        )
        fig_act.update_traces(
            texttemplate="%{text:,}",
            textposition="outside",
            hovertemplate="<b>%{y}</b><br>Total Entries: %{x:,}<br>Negative Share: %{customdata[0]:.1f}%<extra></extra>",
            customdata=df_act[["neg_pct"]]
        )
        fig_act.update_layout(
            height=400,
            margin=dict(t=10, b=10, l=10, r=40),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            xaxis=dict(showgrid=True, gridcolor="#E8EAED", range=[0, 6200]),
            yaxis=dict(showgrid=False, tickfont=dict(size=11)),
            font=dict(family="Google Sans, Inter, sans-serif")
        )
        st.plotly_chart(fig_act, use_container_width=True, config=PLOTLY_CONFIG)

    with col_th2:
        render_html("""
        <div class="chart-container-box">
            <div style="font-size: 15px; font-weight: 700; color: #202124;">
                Severity Index quadrant (Volume × Negativity)
            </div>
            <div style="font-size: 12px; color: #5F6368;">
                Bubble size represents total negative impact (Volume × % Negative)
            </div>
        </div>
        """)

        fig_bubble = px.scatter(
            df_act,
            x="Total",
            y="neg_pct",
            size="Negative",
            color="neg_pct",
            hover_name="theme",
            color_continuous_scale=["#34A853", "#FBBC05", "#EA4335"],
            size_max=34,
            labels={"Total": "Review Volume", "neg_pct": "Negative Share (%)"}
        )

        fig_bubble.add_hline(y=30.0, line_dash="dash", line_color="#BDC1C6", annotation_text="30% Negativity", annotation_position="top left")
        fig_bubble.add_vline(x=2500, line_dash="dash", line_color="#BDC1C6", annotation_text="2.5k Volume", annotation_position="top right")

        fig_bubble.update_layout(
            height=400,
            margin=dict(t=10, b=10, l=10, r=20),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            xaxis=dict(showgrid=True, gridcolor="#E8EAED"),
            yaxis=dict(showgrid=True, gridcolor="#E8EAED", range=[0, 60]),
            font=dict(family="Google Sans, Inter, sans-serif")
        )
        st.plotly_chart(fig_bubble, use_container_width=True, config=PLOTLY_CONFIG)

    # Cross-tab Matrix Table (All 14 Themes)
    with st.expander("📊 View Complete Theme × Sentiment Cross-Tab Heatmap Table (All 14 Themes)", expanded=False):
        df_all_themes = pd.DataFrame(THEMES_CROSSTAB)
        st.dataframe(
            df_all_themes[["theme", "Total", "Negative", "Positive", "Neutral", "Unknown", "neg_pct"]],
            use_container_width=True,
            hide_index=True,
            height=300,
            column_config={
                "theme": st.column_config.TextColumn("Complaint Theme", width="medium"),
                "Total": st.column_config.NumberColumn("Total Reviews", format="%d", width="small"),
                "Negative": st.column_config.NumberColumn("Negative", format="%d", width="small"),
                "Positive": st.column_config.NumberColumn("Positive", format="%d", width="small"),
                "Neutral": st.column_config.NumberColumn("Neutral", format="%d", width="small"),
                "Unknown": st.column_config.NumberColumn("Unknown", format="%d", width="small"),
                "neg_pct": st.column_config.ProgressColumn(
                    "Negative Share",
                    format="%.1f%%",
                    min_value=0,
                    max_value=100,
                    width="medium"
                )
            }
        )

    # Theme × Platform Matrix Heatmap
    with st.expander("🌐 View Top 8 Themes × Platform Cross-Tab Matrix", expanded=False):
        df_matrix = pd.DataFrame(THEME_PLATFORM_MATRIX).set_index("theme")
        fig_heat = px.imshow(
            df_matrix,
            labels=dict(x="Platform", y="Complaint Theme", color="Review Volume"),
            x=df_matrix.columns,
            y=df_matrix.index,
            color_continuous_scale="Blues",
            aspect="auto",
            text_auto=True
        )
        fig_heat.update_layout(
            height=320,
            margin=dict(t=10, b=10, l=10, r=10),
            font=dict(family="Google Sans, Inter, sans-serif")
        )
        st.plotly_chart(fig_heat, use_container_width=True, config=PLOTLY_CONFIG)


def _render_keyword_explorer():
    """Render the Interactive Keyword Explorer with Theme Dropdown."""
    render_html("""
    <div style="margin-bottom: 10px;">
        <h3 style="font-size: 17px; font-weight: 700; color: #202124; margin-bottom: 2px;">
            Keyword explorer
        </h3>
        <p style="font-size: 12.5px; color: #5F6368; margin: 0;">
            Deep-dive into negative verbatim terms, recurring pain points, and representative user quotes per theme.
        </p>
    </div>
    """)

    theme_keys = list(KEYWORD_EXPLORER.keys())
    selected_theme = st.selectbox("Select Theme to inspect keywords & quotes:", theme_keys, index=0)

    if selected_theme in KEYWORD_EXPLORER:
        kw_items = KEYWORD_EXPLORER[selected_theme]

        k_col1, k_col2 = st.columns([1, 1.2])

        with k_col1:
            df_kw = pd.DataFrame(kw_items).sort_values(by="frequency", ascending=True)

            fig_kw = px.bar(
                df_kw,
                x="frequency",
                y="keyword",
                orientation="h",
                text="frequency",
                color="frequency",
                color_continuous_scale="Reds",
                labels={"frequency": "Mention Frequency", "keyword": "Keyword Phrase"}
            )
            fig_kw.update_traces(
                texttemplate="%{text:,}",
                textposition="outside",
                hovertemplate="<b>%{y}</b><br>Mentions: %{x:,}<extra></extra>"
            )
            fig_kw.update_layout(
                height=260,
                margin=dict(t=10, b=10, l=10, r=40),
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                xaxis=dict(showgrid=True, gridcolor="#E8EAED"),
                yaxis=dict(showgrid=False),
                font=dict(family="Google Sans, Inter, sans-serif")
            )
            st.plotly_chart(fig_kw, use_container_width=True, config=PLOTLY_CONFIG)

        with k_col2:
            render_html("""
            <div style="font-size: 13px; font-weight: 700; color: #202124; margin-bottom: 6px;">
                🗣️ Representative User Verbatim Quotes:
            </div>
            """)
            for item in kw_items:
                impact_color = "#EA4335" if "Critical" in item["impact"] else ("#FBBC05" if "High" in item["impact"] else "#1A73E8")
                safe_keyword = item['keyword'].replace('"', '&quot;')
                safe_quote = item['sample_quote'].replace('"', '&quot;')
                render_html(f"""
                <div style="background: #FFFFFF; border: 1px solid #DADCE0; border-left: 4px solid {impact_color}; border-radius: 8px; padding: 8px 12px; margin-bottom: 6px;">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 2px;">
                        <span style="font-weight: 700; font-size: 12.5px; color: #202124;">&ldquo;{safe_keyword}&rdquo;</span>
                        <span style="font-size: 11px; font-weight: 600; color: {impact_color}; background: #F8F9FA; padding: 2px 6px; border-radius: 8px; border: 1px solid #E8EAED;">{item['impact']} · {item['frequency']:,} hits</span>
                    </div>
                    <div style="font-size: 12px; color: #5F6368; font-style: italic;">
                        &ldquo;{safe_quote}&rdquo;
                    </div>
                </div>
                """)


def _render_trends_over_time():
    """Render Dual-axis Monthly Timeline (Jan 2018 - Sep 2026) with Milestones."""
    render_html("""
    <div style="margin-bottom: 10px;">
        <h3 style="font-size: 17px; font-weight: 700; color: #202124; margin-bottom: 2px;">
            Trends over time (Jan 2018 – Sep 2026)
        </h3>
        <p style="font-size: 12.5px; color: #5F6368; margin: 0;">
            Dual-axis monthly trajectory tracking review volume surges alongside rating dips and recovery milestones.
        </p>
    </div>
    """)

    df_time = pd.DataFrame(TIMELINE_DATA)

    fig_time = go.Figure()

    fig_time.add_trace(go.Bar(
        x=df_time["period"],
        y=df_time["vol"],
        name="Review Volume",
        marker=dict(color="#E8F0FE", line=dict(color="#1A73E8", width=1.5)),
        yaxis="y",
        hovertemplate="<b>%{x}</b><br>Volume: %{y:,} reviews<extra></extra>"
    ))

    fig_time.add_trace(go.Scatter(
        x=df_time["period"],
        y=df_time["avg_rating"],
        name="Average Star Rating",
        mode="lines+markers",
        line=dict(color="#EA4335", width=3),
        marker=dict(size=6, color="#EA4335"),
        yaxis="y2",
        hovertemplate="<b>%{x}</b><br>Avg Rating: %{y:.2f} ★<extra></extra>"
    ))

    fig_time.add_annotation(
        x="2024-04",
        y=3.84,
        yref="y2",
        text="Apr 2024 Peak (3.84★)",
        showarrow=True,
        arrowhead=2,
        arrowcolor="#34A853",
        ax=0,
        ay=-30,
        font=dict(size=10.5, color="#137333", family="Google Sans")
    )

    fig_time.add_annotation(
        x="2024-10",
        y=2.52,
        yref="y2",
        text="Oct 2024 Dip (2.52★)<br>Collections Tab Redesign",
        showarrow=True,
        arrowhead=2,
        arrowcolor="#EA4335",
        ax=0,
        ay=35,
        font=dict(size=10.5, color="#C5221F", family="Google Sans")
    )

    fig_time.add_annotation(
        x="2026-09",
        y=3.92,
        yref="y2",
        text="Sep 2026 Recovery (3.92★)<br>AI Search Rollout",
        showarrow=True,
        arrowhead=2,
        arrowcolor="#1A73E8",
        ax=-35,
        ay=-35,
        font=dict(size=10.5, color="#1557B0", family="Google Sans")
    )

    fig_time.update_layout(
        height=360,
        margin=dict(t=25, b=10, l=10, r=10),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(showgrid=True, gridcolor="#E8EAED", title="Timeline (Period)"),
        yaxis=dict(
            title="Monthly Review Volume",
            showgrid=False,
            side="left"
        ),
        yaxis2=dict(
            title="Average Star Rating (1-5)",
            showgrid=True,
            gridcolor="#E8EAED",
            side="right",
            overlaying="y",
            range=[1.5, 5.0]
        ),
        legend=dict(orientation="h", yanchor="bottom", y=-0.25, xanchor="center", x=0.5),
        font=dict(family="Google Sans, Inter, sans-serif")
    )
    st.plotly_chart(fig_time, use_container_width=True, config=PLOTLY_CONFIG)


def _render_geography_and_versions():
    """Render Top Country Breakdown and Most-Flagged App Versions."""
    render_html("""
    <div style="margin-bottom: 10px;">
        <h3 style="font-size: 17px; font-weight: 700; color: #202124; margin-bottom: 2px;">
            Geography & problem versions
        </h3>
        <p style="font-size: 12.5px; color: #5F6368; margin: 0;">
            International distribution of review volume and build versions associated with peak crash and sync reports.
        </p>
    </div>
    """)

    col_geo, col_ver = st.columns([1, 1])

    with col_geo:
        render_html("""
        <div class="chart-container-box">
            <div style="font-size: 15px; font-weight: 700; color: #202124;">
                Top countries by review volume
            </div>
            <div style="font-size: 12px; color: #5F6368;">
                Top 10 markets across Android & iOS stores
            </div>
        </div>
        """)

        df_geo = pd.DataFrame(TOP_COUNTRIES)

        fig_geo = px.bar(
            df_geo,
            x="count",
            y="country",
            orientation="h",
            text=[f"{c:,} ({p}%)" for c, p in zip(df_geo["count"], df_geo["pct"])],
            color="count",
            color_continuous_scale="Blues",
            labels={"count": "Reviews", "country": "Country"}
        )
        fig_geo.update_traces(
            textposition="inside",
            hovertemplate="<b>%{y}</b><br>Reviews: %{x:,}<extra></extra>"
        )
        fig_geo.update_layout(
            height=320,
            margin=dict(t=10, b=10, l=10, r=20),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            xaxis=dict(showgrid=True, gridcolor="#E8EAED"),
            yaxis=dict(autorange="reversed", showgrid=False),
            font=dict(family="Google Sans, Inter, sans-serif")
        )
        st.plotly_chart(fig_geo, use_container_width=True, config=PLOTLY_CONFIG)

    with col_ver:
        render_html("""
        <div class="chart-container-box">
            <div style="font-size: 15px; font-weight: 700; color: #202124;">
                Most-flagged app versions (Crash & bug spikes)
            </div>
            <div style="font-size: 12px; color: #5F6368;">
                Ranked by volume of 1★ & 2★ negative reviews
            </div>
        </div>
        """)

        df_ver = pd.DataFrame(TOP_VERSIONS)

        fig_ver = px.bar(
            df_ver,
            x="negative_reviews",
            y="version",
            orientation="h",
            text=[f"{n:,} neg reviews" for n in df_ver["negative_reviews"]],
            color="negative_reviews",
            color_continuous_scale="Reds",
            labels={"negative_reviews": "Negative Reviews", "version": "App Version"}
        )
        fig_ver.update_traces(
            textposition="inside",
            hovertemplate="<b>%{y}</b><br>Negative Reviews: %{x:,}<extra></extra>"
        )
        fig_ver.update_layout(
            height=320,
            margin=dict(t=10, b=10, l=10, r=20),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            xaxis=dict(showgrid=True, gridcolor="#E8EAED"),
            yaxis=dict(autorange="reversed", showgrid=False),
            font=dict(family="Google Sans, Inter, sans-serif")
        )
        st.plotly_chart(fig_ver, use_container_width=True, config=PLOTLY_CONFIG)


def _render_episodic_recall_bridge(df_feedback: pd.DataFrame):
    """Render the PM Case Study bridge: Episodic Memory Asymmetry."""
    render_html("""
    <div style="margin-bottom: 10px;">
        <h3 style="font-size: 17px; font-weight: 700; color: #202124; margin-bottom: 2px;">
            PM case study: The "Semantic Recall Gap"
        </h3>
        <p style="font-size: 12.5px; color: #5F6368; margin: 0;">
            Psychological recall asymmetry between human episodic memory and traditional database metadata.
        </p>
    </div>
    """)

    b_col1, b_col2 = st.columns([1.1, 0.9])

    with b_col1:
        memory_data = {
            "Dimension": ["Exact Date / Year", "Visual Color / Mood", "Approximate Location", "Proper Name / Brand", "Document / OCR Text", "Emotional Context"],
            "Remembered Clues (%)": [12, 88, 74, 18, 42, 85],
            "Forgotten Clues (%)": [88, 12, 26, 82, 58, 15]
        }
        df_mem = pd.DataFrame(memory_data)

        fig_bar = go.Figure()
        fig_bar.add_trace(go.Bar(
            y=df_mem["Dimension"],
            x=df_mem["Remembered Clues (%)"],
            name="Remembered by Users",
            orientation="h",
            marker=dict(color="#1A73E8", line=dict(color="#1557B0", width=1))
        ))
        fig_bar.add_trace(go.Bar(
            y=df_mem["Dimension"],
            x=df_mem["Forgotten Clues (%)"],
            name="Forgotten / Missing",
            orientation="h",
            marker=dict(color="#FCE8E6", line=dict(color="#EA4335", width=1.5))
        ))

        fig_bar.update_layout(
            barmode="group",
            height=270,
            margin=dict(t=10, b=10, l=10, r=10),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            legend=dict(orientation="h", yanchor="bottom", y=-0.25, xanchor="center", x=0.5),
            xaxis=dict(title="Recall Frequency (%)", showgrid=True, gridcolor="#E8EAED", range=[0, 100]),
            yaxis=dict(autorange="reversed", showgrid=False),
            font=dict(family="Google Sans, Inter, sans-serif")
        )
        st.plotly_chart(fig_bar, use_container_width=True, config=PLOTLY_CONFIG)

    with b_col2:
        render_html("""
        <div style="background: #E8F0FE; border-left: 5px solid #1A73E8; border-radius: 12px; padding: 16px 20px; height: 100%; display: flex; flex-direction: column; justify-content: center;">
            <div style="font-weight: 700; color: #1A73E8; font-size: 14.5px; margin-bottom: 8px;">
                💡 Why Search & AI Retrieval Fails (31.8% Negativity)
            </div>
            <div style="color: #3C4043; font-size: 13px; line-height: 1.6;">
                Traditional photo search engines rely on <b>strict EXIF timestamps</b> and <b>explicit folder/brand names</b>.
                <br><br>
                However, <b>88% of users recall emotional context, colors, or relative time anchors</b> (<i>"when I had a fever last winter"</i>, <i>"yellow medicine box on nightstand"</i>).
                <br><br>
                The solution is the <b>Google Photos AI Search Assistant</b>, which performs episodic query expansion and OCR multi-modal vector matching.
            </div>
        </div>
        """)


def _render_review_explorer():
    """Render Searchable, Filterable Master Review Explorer."""
    render_html("""
    <div style="margin-bottom: 10px;">
        <h3 style="font-size: 17px; font-weight: 700; color: #202124; margin-bottom: 2px;">
            🔍 Interactive Review Explorer
        </h3>
        <p style="font-size: 12.5px; color: #5F6368; margin: 0;">
            Filter and inspect raw records from the master review repository across platforms, ratings, and keyword terms.
        </p>
    </div>
    """)

    df_reviews = load_master_reviews_df()

    if df_reviews.empty:
        st.info("Master review records dataset not loaded. Ensure `Google_Photos_Master_Reviews.csv` is present in the workspace.")
        return

    f_col1, f_col2, f_col3 = st.columns([1, 1, 2])

    with f_col1:
        plat_options = ["All Platforms"] + sorted(list(df_reviews["platform"].dropna().unique()))
        selected_plat = st.selectbox("Platform filter:", plat_options, index=0)

    with f_col2:
        rating_options = ["All Ratings", "5 ★ Only", "4 ★ Only", "3 ★ Only", "2 ★ Only", "1 ★ Only", "Negative Only (1-2★)", "Positive Only (4-5★)"]
        selected_rating = st.selectbox("Rating filter:", rating_options, index=0)

    with f_col3:
        search_kw = st.text_input("Keyword search in title & content:", placeholder="e.g. sync, stuck, backup, search, medicine, battery...")

    filtered = df_reviews.copy()

    if selected_plat != "All Platforms":
        filtered = filtered[filtered["platform"] == selected_plat]

    if selected_rating == "5 ★ Only":
        filtered = filtered[filtered["rating"] == 5]
    elif selected_rating == "4 ★ Only":
        filtered = filtered[filtered["rating"] == 4]
    elif selected_rating == "3 ★ Only":
        filtered = filtered[filtered["rating"] == 3]
    elif selected_rating == "2 ★ Only":
        filtered = filtered[filtered["rating"] == 2]
    elif selected_rating == "1 ★ Only":
        filtered = filtered[filtered["rating"] == 1]
    elif selected_rating == "Negative Only (1-2★)":
        filtered = filtered[filtered["rating"] <= 2]
    elif selected_rating == "Positive Only (4-5★)":
        filtered = filtered[filtered["rating"] >= 4]

    if search_kw.strip():
        kw = search_kw.strip().lower()
        mask = (
            filtered["content"].astype(str).str.lower().str.contains(kw) |
            filtered["title"].astype(str).str.lower().str.contains(kw)
        )
        filtered = filtered[mask]

    render_html(f"<div style='font-size: 12.5px; color: #5F6368; margin-bottom: 8px;'>Displaying <b>{len(filtered):,}</b> matching review records (from {len(df_reviews):,} cached rows)</div>")

    st.dataframe(
        filtered[["review_id", "platform", "rating", "date", "country", "title", "content", "app_version"]],
        use_container_width=True,
        hide_index=True,
        height=380,
        column_config={
            "review_id": st.column_config.TextColumn("Review ID", width="small"),
            "platform": st.column_config.TextColumn("Platform", width="small"),
            "rating": st.column_config.NumberColumn("Rating ★", format="%d ★", width="small"),
            "date": st.column_config.TextColumn("Date", width="small"),
            "country": st.column_config.TextColumn("Country", width="small"),
            "title": st.column_config.TextColumn("Review Title", width="medium"),
            "content": st.column_config.TextColumn("Content / Verbatim", width="large"),
            "app_version": st.column_config.TextColumn("Version", width="small")
        }
    )
