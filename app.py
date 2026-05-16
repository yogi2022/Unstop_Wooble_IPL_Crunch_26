"""
IPL CRUNCH '26 — Data Analytics Dashboard
Author: Built for Wooble IPL Crunch '26 Challenge
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import warnings
warnings.filterwarnings("ignore")

from utils.data_loader import load_and_preprocess
from utils.analysis import (
    toss_analysis,
    phase_analysis,
    top_batters,
    top_bowlers,
    surprise_insights,
    season_trends,
    venue_analysis,
    partnership_analysis,
)

# ── PAGE CONFIG ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="IPL CRUNCH '26 | Wooble Analytics",
    page_icon="🏏",
    layout="wide",
    initial_sidebar_state="expanded",
)



# css1

st.markdown("""
<style>

/* ─── TAB CONTAINER ───────────────────── */
.stTabs [data-baseweb="tab-list"] {
    gap: 10px;
    background: rgba(20, 20, 20, 0.25);
    padding: 8px;
    border-radius: 14px;
    backdrop-filter: blur(10px);
}

/* ─── EACH TAB ────────────────────────── */
.stTabs [data-baseweb="tab"] {
    height: 44px;
    padding: 0px 16px;
    border-radius: 10px;
    background: rgba(255, 255, 255, 0.05);
    color: #aaa;
    font-weight: 500;
    transition: all 0.2s ease-in-out;
}

/* ─── HOVER EFFECT ────────────────────── */
.stTabs [data-baseweb="tab"]:hover {
    background: rgba(255, 255, 255, 0.12);
    color: white;
    transform: translateY(-1px);
}

/* ─── ACTIVE TAB ───────────────────────── */
.stTabs [aria-selected="true"] {
    background: linear-gradient(90deg, #f5a623, #ffcc66);
    color: black !important;
    font-weight: 700;
    box-shadow: 0px 4px 20px rgba(245, 166, 35, 0.25);
}

/* ─── TAB TEXT CLEANUP ────────────────── */
.stTabs button {
    letter-spacing: 0.2px;
}

</style>
""", unsafe_allow_html=True)

# ── CUSTOM CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=DM+Sans:wght@300;400;500;600&family=JetBrains+Mono:wght@400;600&display=swap');

:root {
    --bg:         #0a0c10;
    --bg2:        #111520;
    --bg3:        #181d2a;
    --accent:     #f5a623;
    --accent2:    #e84c4c;
    --accent3:    #3ecf8e;
    --text:       #e8eaf0;
    --muted:      #6b7280;
    --border:     #1e2535;
}

html, body, [data-testid="stAppViewContainer"] {
    background: var(--bg) !important;
    color: var(--text) !important;
    font-family: 'DM Sans', sans-serif;
}

[data-testid="stSidebar"] {
    background: var(--bg2) !important;
    border-right: 1px solid var(--border);
}

[data-testid="stSidebar"] * { color: var(--text) !important; }

h1, h2, h3 {
    font-family: 'Bebas Neue', sans-serif !important;
    letter-spacing: 2px;
    color: var(--accent) !important;
}

.metric-card {
    background: var(--bg3);
    border: 1px solid var(--border);
    border-left: 4px solid var(--accent);
    border-radius: 8px;
    padding: 20px 24px;
    margin: 8px 0;
}
.metric-card .label {
    font-size: 11px;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: var(--muted);
    font-family: 'JetBrains Mono', monospace;
}
.metric-card .value {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 42px;
    color: var(--accent);
    line-height: 1.1;
}
.metric-card .sub {
    font-size: 12px;
    color: var(--muted);
    margin-top: 4px;
}

.section-header {
    border-bottom: 1px solid var(--border);
    margin: 32px 0 20px 0;
    padding-bottom: 8px;
    display: flex;
    align-items: center;
    gap: 10px;
}

.insight-box {
    background: linear-gradient(135deg, #1a1f30 0%, #0f1420 100%);
    border: 1px solid var(--accent);
    border-radius: 12px;
    padding: 24px 28px;
    margin: 16px 0;
    position: relative;
    overflow: hidden;
}
.insight-box::before {
    content: '"';
    font-family: 'Bebas Neue', sans-serif;
    font-size: 120px;
    color: var(--accent);
    opacity: 0.08;
    position: absolute;
    top: -20px;
    left: 10px;
    line-height: 1;
}
.insight-box .insight-text {
    font-size: 16px;
    line-height: 1.7;
    color: var(--text);
    position: relative;
    z-index: 1;
}
.insight-box .insight-label {
    font-family: 'JetBrains Mono', monospace;
    font-size: 10px;
    letter-spacing: 3px;
    color: var(--accent);
    text-transform: uppercase;
    margin-bottom: 10px;
}

.pill {
    display: inline-block;
    padding: 3px 12px;
    border-radius: 20px;
    font-size: 11px;
    font-family: 'JetBrains Mono', monospace;
    letter-spacing: 1px;
    font-weight: 600;
}
.pill-gold  { background: #f5a62322; color: #f5a623; border: 1px solid #f5a62355; }
.pill-red   { background: #e84c4c22; color: #e84c4c; border: 1px solid #e84c4c55; }
.pill-green { background: #3ecf8e22; color: #3ecf8e; border: 1px solid #3ecf8e55; }

.stTabs [data-baseweb="tab-list"] {
    background: var(--bg2);
    border-radius: 8px;
    gap: 4px;
}
.stTabs [data-baseweb="tab"] {
    color: var(--muted) !important;
    font-family: 'DM Sans', sans-serif;
    font-weight: 500;
}
.stTabs [aria-selected="true"] {
    background: var(--accent) !important;
    color: #000 !important;
    border-radius: 6px;
}

div[data-testid="metric-container"] {
    background: var(--bg3);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 16px;
}
div[data-testid="metric-container"] label { color: var(--muted) !important; }
div[data-testid="metric-container"] [data-testid="stMetricValue"] { color: var(--accent) !important; font-family: 'Bebas Neue', sans-serif; font-size: 32px !important; }

.stSelectbox > div, .stMultiSelect > div {
    background: var(--bg3) !important;
    border-color: var(--border) !important;
    color: var(--text) !important;
}

footer, [data-testid="stToolbar"] { display: none !important; }

.hero-banner {
    background: linear-gradient(135deg, #0f1420 0%, #1a0f05 50%, #0a0c10 100%);
    border: 1px solid #f5a62333;
    border-radius: 16px;
    padding: 40px 48px;
    margin-bottom: 32px;
    position: relative;
    overflow: hidden;
}
.hero-banner::after {
    content: '🏏';
    position: absolute;
    right: 48px;
    top: 50%;
    transform: translateY(-50%);
    font-size: 80px;
    opacity: 0.15;
}
.hero-title {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 52px;
    letter-spacing: 4px;
    color: var(--accent);
    line-height: 1;
    margin: 0;
}
.hero-sub {
    color: var(--muted);
    font-size: 14px;
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-top: 8px;
    font-family: 'JetBrains Mono', monospace;
}

.table-styled { width: 100%; border-collapse: collapse; font-size: 13px; }
.table-styled th {
    background: var(--bg3);
    color: var(--accent);
    font-family: 'JetBrains Mono', monospace;
    font-size: 10px;
    letter-spacing: 2px;
    text-transform: uppercase;
    padding: 10px 14px;
    border-bottom: 2px solid var(--accent);
    text-align: left;
}
.table-styled td {
    padding: 10px 14px;
    border-bottom: 1px solid var(--border);
    color: var(--text);
}
.table-styled tr:hover td { background: var(--bg3); }
.rank-badge {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 24px; height: 24px;
    border-radius: 50%;
    font-family: 'Bebas Neue', sans-serif;
    font-size: 13px;
}
.rank-1 { background: #f5a623; color: #000; }
.rank-2 { background: #9ca3af; color: #000; }
.rank-3 { background: #b45309; color: #fff; }
.rank-n { background: var(--bg3); color: var(--muted); border: 1px solid var(--border); }

[data-testid="stDataFrame"] { background: var(--bg3) !important; }
</style>
""", unsafe_allow_html=True)


# ── SIDEBAR ────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='text-align:center; padding: 16px 0 24px 0;'>
        <div style='font-family: Bebas Neue, sans-serif; font-size: 28px; color: #f5a623; letter-spacing: 3px;'>🏏 IPL CRUNCH</div>
        <div style='font-family: JetBrains Mono, monospace; font-size: 10px; color: #6b7280; letter-spacing: 2px;'>WOOBLE · 2026</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### 📂 Upload Dataset")
    uploaded = st.file_uploader(
        "Drop your ipl_matches.csv here",
        type=["csv"],
        help="Ball-by-ball IPL match data CSV"
    )

    st.markdown("---")
    st.markdown("### 🎛️ Filters")


# ── DATA LOADING ───────────────────────────────────────────────────────────────
@st.cache_data(show_spinner=False)
def get_data(file_bytes):
    return load_and_preprocess(file_bytes)


if uploaded is None:
    st.markdown("""
    <div class='hero-banner'>
        <div class='hero-title'>IPL CRUNCH '26</div>
        <div class='hero-sub'>Wooble Analytics Challenge · Ball-by-Ball Intelligence</div>
    </div>
    """, unsafe_allow_html=True)

    st.info("👈  Upload your **ipl_matches.csv** in the sidebar to begin the analysis.")

    with st.expander("📋 What this dashboard analyses"):
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("""
            **🎲 Toss Impact**
            - Win rate: toss winners vs losers
            - Decision (bat/field) effectiveness
            - Season-wise toss leverage
            """)
        with col2:
            st.markdown("""
            **⚡ Phase Analysis**
            - Powerplay (0–5 overs)
            - Middle overs (6–14)
            - Death overs (15–19)
            - Which phase predicts victory?
            """)
        with col3:
            st.markdown("""
            **🏆 Hall of Fame**
            - Top 5 batters by runs
            - Top 5 bowlers by wickets
            - Season-wise performance
            - Surprise insights
            """)
    st.stop()


# ── LOAD ───────────────────────────────────────────────────────────────────────
with st.spinner("⚙️  Crunching ball-by-ball data…"):
    df, matches = get_data(uploaded)

seasons = sorted(df["season"].unique())

with st.sidebar:
    selected_seasons = st.multiselect(
        "Seasons", seasons, default=seasons,
        help="Filter analysis to specific seasons"
    )
    if not selected_seasons:
        selected_seasons = seasons

df_f    = df[df["season"].isin(selected_seasons)]
matches_f = matches[matches["season"].isin(selected_seasons)]

total_matches  = matches_f["match_id"].nunique()
total_balls    = len(df_f)
total_runs     = df_f["runs_total"].sum()
total_wickets  = df_f["wicket_player_out"].notna().sum()

# ── HERO ───────────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class='hero-banner'>
    <div class='hero-title'>IPL CRUNCH '26</div>
    <div class='hero-sub'>Wooble Analytics · {len(selected_seasons)} Season{"s" if len(selected_seasons)!=1 else ""} · {total_matches:,} Matches · Ball-by-Ball Intelligence</div>
</div>
""", unsafe_allow_html=True)

# ── KPI ROW ────────────────────────────────────────────────────────────────────
k1, k2, k3, k4 = st.columns(4)
for col, label, val, sub in [
    (k1, "Total Matches",  f"{total_matches:,}",    f"{len(selected_seasons)} seasons"),
    (k2, "Balls Bowled",   f"{total_balls:,}",      "ball-by-ball records"),
    (k3, "Total Runs",     f"{total_runs:,}",       "across all innings"),
    (k4, "Wickets Taken",  f"{total_wickets:,}",    "dismissals recorded"),
]:
    col.markdown(f"""
    <div class='metric-card'>
        <div class='label'>{label}</div>
        <div class='value'>{val}</div>
        <div class='sub'>{sub}</div>
    </div>""", unsafe_allow_html=True)


# ── TABS ───────────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🎲  Toss Impact",
    "⚡  Phase Analysis",
    "🏆  Hall of Fame",
    "📈  Season Trends",
    "💡  Surprise Insights",
])


# ══════════════════════════════════════════════════════════════════════════════
# TAB 1 — TOSS IMPACT
# ══════════════════════════════════════════════════════════════════════════════
with tab1:
    st.markdown("<h2>🎲 Does Winning The Toss Actually Matter?</h2>", unsafe_allow_html=True)

    toss_data = toss_analysis(matches_f)

    col_a, col_b = st.columns([3, 2])

    with col_a:
        # Main bar chart
        fig = go.Figure()
        categories = ["Toss Winners", "Toss Losers"]
        values     = [toss_data["toss_win_rate"], toss_data["toss_lose_rate"]]
        colors     = ["#f5a623", "#3a3f55"]

        fig.add_trace(go.Bar(
            x=categories, y=values,
            marker_color=colors,
            marker_line_width=0,
            text=[f"{v:.1f}%" for v in values],
            textposition="inside",
            textfont=dict(family="Bebas Neue", size=22, color="white"),
            width=0.55,
        ))
        fig.add_hline(y=50, line_dash="dash", line_color="#6b7280",
                      annotation_text="  50% baseline", annotation_font_color="#6b7280",
                      annotation_font_size=11)

        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font_color="#e8eaf0", font_family="DM Sans",
            title=dict(text="Win Rate: Toss Winners vs Losers", font_size=16,
                       font_family="Bebas Neue", font_color="#f5a623", x=0),
            yaxis=dict(title="Win Rate (%)", range=[0, 80],
                       gridcolor="#1e2535", tickfont_size=11),
            xaxis=dict(tickfont=dict(family="Bebas Neue", size=14)),
            showlegend=False,
            height=380,
            margin=dict(l=20, r=20, t=50, b=20),
        )
        st.plotly_chart(fig, use_container_width=True)

    with col_b:
        st.markdown("<br>", unsafe_allow_html=True)
        for label, val, sub, pill_cls in [
            ("Toss-Win Rate",     f"{toss_data['toss_win_rate']:.1f}%",
             "of toss winners win match", "pill-gold"),
            ("Toss-Lose Rate",    f"{toss_data['toss_lose_rate']:.1f}%",
             "of toss losers still win", "pill-red"),
            ("Advantage Margin",  f"{toss_data['toss_win_rate'] - toss_data['toss_lose_rate']:.1f}pp",
             "percentage point edge", "pill-green"),
        ]:
            st.markdown(f"""
            <div class='metric-card'>
                <div class='label'>{label}</div>
                <div class='value'>{val}</div>
                <div class='sub'>{sub}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Decision breakdown
    col_c, col_d = st.columns(2)

    with col_c:
        dec = toss_data["decision_wins"]
        fig2 = go.Figure()
        fig2.add_trace(go.Bar(
            x=list(dec.keys()), y=list(dec.values()),
            marker_color=["#3ecf8e", "#e84c4c"],
            text=[f"{v:.1f}%" for v in dec.values()],
            textposition="inside",
            textfont=dict(family="Bebas Neue", size=18, color="white"),
            marker_line_width=0, width=0.45,
        ))
        fig2.add_hline(y=50, line_dash="dash", line_color="#6b7280")
        fig2.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font_color="#e8eaf0",
            title=dict(text="Win Rate by Toss Decision", font_size=15,
                       font_family="Bebas Neue", font_color="#f5a623", x=0),
            yaxis=dict(title="Win Rate (%)", range=[0,80], gridcolor="#1e2535"),
            xaxis=dict(tickfont=dict(family="Bebas Neue", size=13)),
            showlegend=False, height=320,
            margin=dict(l=20, r=20, t=50, b=20),
        )
        st.plotly_chart(fig2, use_container_width=True)

    with col_d:
        # Season-wise toss advantage line
        season_toss = toss_data["season_toss_rates"]
        fig3 = go.Figure()
        fig3.add_trace(go.Scatter(
            x=season_toss["season"], y=season_toss["win_rate"],
            mode="lines+markers+text",
            line=dict(color="#f5a623", width=2.5),
            marker=dict(size=9, color="#f5a623", line=dict(color="#0a0c10", width=2)),
            text=[f"{v:.0f}%" for v in season_toss["win_rate"]],
            textposition="top center",
            textfont=dict(family="JetBrains Mono", size=10, color="#f5a623"),
        ))
        fig3.add_hline(y=50, line_dash="dot", line_color="#6b7280",
                       annotation_text="  50%", annotation_font_color="#6b7280",
                       annotation_font_size=10)
        fig3.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font_color="#e8eaf0",
            title=dict(text="Toss-Win Rate by Season", font_size=15,
                       font_family="Bebas Neue", font_color="#f5a623", x=0),
            yaxis=dict(title="Win Rate (%)", range=[30,80], gridcolor="#1e2535"),
            xaxis=dict(tickfont=dict(family="JetBrains Mono", size=10)),
            showlegend=False, height=320,
            margin=dict(l=20, r=20, t=50, b=20),
        )
        st.plotly_chart(fig3, use_container_width=True)

    # Insight callout
    delta = toss_data["toss_win_rate"] - 50
    direction = "higher" if delta > 0 else "lower"
    st.markdown(f"""
    <div class='insight-box'>
        <div class='insight-label'>📊 Data Verdict</div>
        <div class='insight-text'>
            Toss winners convert at <strong style='color:#f5a623'>{toss_data['toss_win_rate']:.1f}%</strong>
            — {abs(delta):.1f} percentage points {direction} than pure chance (50%).
            Teams electing to <strong>field first</strong> win at
            <strong style='color:#3ecf8e'>{toss_data["decision_wins"].get("field", 0):.1f}%</strong>,
            while those choosing to bat win at
            <strong style='color:#e84c4c'>{toss_data["decision_wins"].get("bat", 0):.1f}%</strong>.
            {"The toss advantage is real but modest — form & execution still dominate." if abs(delta) < 10 else "The toss confers a meaningful edge in this dataset."}
        </div>
    </div>
    """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# TAB 2 — PHASE ANALYSIS
# ══════════════════════════════════════════════════════════════════════════════
with tab2:
    st.markdown("<h2>⚡ Which Phase Wins Matches?</h2>", unsafe_allow_html=True)

    phase_data = phase_analysis(df_f, matches_f)

    col_a, col_b = st.columns([3, 2])

    with col_a:
        phases  = ["Powerplay (0–5)", "Middle Overs (6–14)", "Death Overs (15–19)"]
        w_runs  = [phase_data["winners"]["powerplay"],
                   phase_data["winners"]["middle"],
                   phase_data["winners"]["death"]]
        l_runs  = [phase_data["losers"]["powerplay"],
                   phase_data["losers"]["middle"],
                   phase_data["losers"]["death"]]

        fig = go.Figure()
        fig.add_trace(go.Bar(
            name="Match Winners", x=phases, y=w_runs,
            marker_color="#f5a623", marker_line_width=0,
            text=[f"{v:.1f}" for v in w_runs],
            textposition="outside",
            textfont=dict(family="JetBrains Mono", size=11, color="#f5a623"),
        ))
        fig.add_trace(go.Bar(
            name="Match Losers", x=phases, y=l_runs,
            marker_color="#3a3f55", marker_line_width=0,
            text=[f"{v:.1f}" for v in l_runs],
            textposition="outside",
            textfont=dict(family="JetBrains Mono", size=11, color="#9ca3af"),
        ))
        fig.update_layout(
            barmode="group",
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font_color="#e8eaf0",
            title=dict(text="Avg Runs Per Phase — Winners vs Losers", font_size=16,
                       font_family="Bebas Neue", font_color="#f5a623", x=0),
            yaxis=dict(title="Average Runs", gridcolor="#1e2535"),
            legend=dict(bgcolor="rgba(0,0,0,0)", font_size=12),
            height=400,
            margin=dict(l=20, r=20, t=50, b=20),
        )
        st.plotly_chart(fig, use_container_width=True)

    with col_b:
        st.markdown("<br>", unsafe_allow_html=True)
        diffs = {
            "Powerplay":   w_runs[0] - l_runs[0],
            "Middle Overs": w_runs[1] - l_runs[1],
            "Death Overs":  w_runs[2] - l_runs[2],
        }
        max_phase = max(diffs, key=diffs.get)
        for ph, diff in diffs.items():
            pill_cls = "pill-gold" if ph == max_phase else "pill-green" if diff > 0 else "pill-red"
            st.markdown(f"""
            <div class='metric-card'>
                <div class='label'>{ph}</div>
                <div class='value'>+{diff:.1f}</div>
                <div class='sub'>avg run advantage (winners over losers)
                <br><span class='pill {pill_cls}'>{"★ KEY PHASE" if ph==max_phase else "CONTRIBUTES"}</span></div>
            </div>""", unsafe_allow_html=True)

    # Run-rate heatmap by over
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<h3>🔥 Run Rate by Over — Winners vs Losers</h3>", unsafe_allow_html=True)

    over_data = phase_data["over_rr"]
    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(
        x=over_data["over"], y=over_data["winner_rr"],
        name="Winners", mode="lines",
        line=dict(color="#f5a623", width=2.5),
        fill="tozeroy", fillcolor="rgba(245,166,35,0.08)",
    ))
    fig2.add_trace(go.Scatter(
        x=over_data["over"], y=over_data["loser_rr"],
        name="Losers", mode="lines",
        line=dict(color="#e84c4c", width=2, dash="dot"),
        fill="tozeroy", fillcolor="rgba(232,76,76,0.05)",
    ))
    fig2.add_vrect(x0=-0.5, x1=5.5, fillcolor="rgba(245, 166, 35, 0.03)",
                   layer="below", line_width=0,
                   annotation_text="POWERPLAY", annotation_position="top left",
                   annotation_font_color="#f5a623", annotation_font_size=10)
    fig2.add_vrect(x0=5.5, x1=14.5, fillcolor="rgba(62, 207, 142, 0.02)",
                   layer="below", line_width=0,
                   annotation_text="MIDDLE", annotation_position="top left",
                   annotation_font_color="#3ecf8e", annotation_font_size=10)
    fig2.add_vrect(x0=14.5, x1=19.5, fillcolor="rgba(232, 76, 76, 0.03)",
                   layer="below", line_width=0,
                   annotation_text="DEATH", annotation_position="top left",
                   annotation_font_color="#e84c4c", annotation_font_size=10)
    fig2.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font_color="#e8eaf0",
        yaxis=dict(title="Run Rate (runs/over)", gridcolor="#1e2535"),
        xaxis=dict(title="Over Number", tickvals=list(range(0,20)),
                   gridcolor="#1e2535"),
        legend=dict(bgcolor="rgba(0,0,0,0)"),
        height=360,
        margin=dict(l=20, r=20, t=20, b=40),
    )
    st.plotly_chart(fig2, use_container_width=True)

    st.markdown(f"""
    <div class='insight-box'>
        <div class='insight-label'>📊 Phase Verdict</div>
        <div class='insight-text'>
            The <strong style='color:#f5a623'>{max_phase}</strong> shows the largest run-scoring
            gap between winners and losers (+{diffs[max_phase]:.1f} runs), making it the
            most decisive phase. Teams that dominate the Death Overs especially tend to swing
            close matches — the run-rate divergence is sharpest in the final 5 overs.
        </div>
    </div>
    """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# TAB 3 — HALL OF FAME
# ══════════════════════════════════════════════════════════════════════════════
with tab3:
    st.markdown("<h2>🏆 Hall of Fame — Top Performers</h2>", unsafe_allow_html=True)

    batters = top_batters(df_f, n=5)
    bowlers = top_bowlers(df_f, n=5)

    col_bat, col_bowl = st.columns(2)

    def rank_badge(i):
        cls = ["rank-1","rank-2","rank-3","rank-n","rank-n"][i]
        return f"<span class='rank-badge {cls}'>{i+1}</span>"

    with col_bat:
        st.markdown("<h3>🏏 Top 5 Batters</h3>", unsafe_allow_html=True)

        # Bar chart
        fig = go.Figure()
        fig.add_trace(go.Bar(
            y=batters["batter"][::-1], x=batters["runs"][::-1],
            orientation="h",
            marker=dict(
                color=batters["runs"][::-1],
                colorscale=[[0,"#3a3f55"],[0.5,"#b45309"],[1,"#f5a623"]],
                showscale=False,
            ),
            text=batters["runs"][::-1],
            textposition="inside",
            textfont=dict(family="Bebas Neue", size=14, color="white"),
            marker_line_width=0,
        ))
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font_color="#e8eaf0",
            xaxis=dict(title="Total Runs", gridcolor="#1e2535"),
            yaxis=dict(tickfont=dict(family="DM Sans", size=12)),
            showlegend=False, height=280,
            margin=dict(l=20, r=20, t=10, b=30),
        )
        st.plotly_chart(fig, use_container_width=True)

        # Table
        rows = ""
        for i, row in batters.iterrows():
            rows += f"""
            <tr>
                <td>{rank_badge(i)}</td>
                <td><strong>{row['batter']}</strong></td>
                <td><span style='color:#f5a623;font-family:JetBrains Mono'>{row['runs']:,}</span></td>
                <td>{row['innings']}</td>
                <td><span style='color:#3ecf8e;font-family:JetBrains Mono'>{row['avg']:.1f}</span></td>
                <td><span style='color:#e84c4c;font-family:JetBrains Mono'>{row['sr']:.1f}</span></td>
            </tr>"""
        st.markdown(f"""
        <table class='table-styled'>
        <thead><tr>
            <th>#</th><th>Batter</th><th>Runs</th><th>Inn</th><th>Avg</th><th>SR</th>
        </tr></thead>
        <tbody>{rows}</tbody>
        </table>""", unsafe_allow_html=True)

    with col_bowl:
        st.markdown("<h3>🎯 Top 5 Bowlers</h3>", unsafe_allow_html=True)

        fig2 = go.Figure()
        fig2.add_trace(go.Bar(
            y=bowlers["bowler"][::-1], x=bowlers["wickets"][::-1],
            orientation="h",
            marker=dict(
                color=bowlers["wickets"][::-1],
                colorscale=[[0,"#1a2535"],[0.5,"#1d4e8f"],[1,"#3ecf8e"]],
                showscale=False,
            ),
            text=bowlers["wickets"][::-1],
            textposition="inside",
            textfont=dict(family="Bebas Neue", size=14, color="white"),
            marker_line_width=0,
        ))
        fig2.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font_color="#e8eaf0",
            xaxis=dict(title="Total Wickets", gridcolor="#1e2535"),
            yaxis=dict(tickfont=dict(family="DM Sans", size=12)),
            showlegend=False, height=280,
            margin=dict(l=20, r=20, t=10, b=30),
        )
        st.plotly_chart(fig2, use_container_width=True)

        rows2 = ""
        for i, row in bowlers.iterrows():
            rows2 += f"""
            <tr>
                <td>{rank_badge(i)}</td>
                <td><strong>{row['bowler']}</strong></td>
                <td><span style='color:#3ecf8e;font-family:JetBrains Mono'>{row['wickets']}</span></td>
                <td>{row['innings']}</td>
                <td><span style='color:#f5a623;font-family:JetBrains Mono'>{row['economy']:.2f}</span></td>
                <td><span style='color:#e84c4c;font-family:JetBrains Mono'>{row['avg']:.1f}</span></td>
            </tr>"""
        st.markdown(f"""
        <table class='table-styled'>
        <thead><tr>
            <th>#</th><th>Bowler</th><th>Wkts</th><th>Inn</th><th>Eco</th><th>Avg</th>
        </tr></thead>
        <tbody>{rows2}</tbody>
        </table>""", unsafe_allow_html=True)

    # Season-wise top scorers
    st.markdown("<br><h3>📅 Top Scorer Per Season</h3>", unsafe_allow_html=True)
    season_top = (
        df_f.groupby(["season","batter"])["runs_batter"].sum()
        .reset_index()
        .sort_values(["season","runs_batter"], ascending=[True,False])
        .groupby("season").first().reset_index()
        .rename(columns={"batter":"Player","runs_batter":"Runs"})
    )
    fig3 = go.Figure()
    fig3.add_trace(go.Bar(
        x=season_top["season"].astype(str), y=season_top["Runs"],
        text=season_top["Player"],
        textposition="inside",
        textfont=dict(family="DM Sans", size=10, color="white"),
        marker=dict(
            color=season_top["Runs"],
            colorscale=[[0,"#1a2535"],[1,"#f5a623"]],
            showscale=False,
        ),
        marker_line_width=0,
        customdata=season_top["Player"],
        hovertemplate="<b>%{customdata}</b><br>Season: %{x}<br>Runs: %{y:,}<extra></extra>",
    ))
    fig3.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font_color="#e8eaf0",
        yaxis=dict(title="Total Runs", gridcolor="#1e2535"),
        xaxis=dict(tickfont=dict(family="JetBrains Mono", size=11)),
        showlegend=False, height=300,
        margin=dict(l=20, r=20, t=10, b=20),
    )
    st.plotly_chart(fig3, use_container_width=True)


# ══════════════════════════════════════════════════════════════════════════════
# TAB 4 — SEASON TRENDS
# ══════════════════════════════════════════════════════════════════════════════
with tab4:
    st.markdown("<h2>📈 Season-by-Season Trends</h2>", unsafe_allow_html=True)

    s_data = season_trends(df_f, matches_f)

    col_a, col_b = st.columns(2)

    with col_a:
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=s_data["season"], y=s_data["avg_total_score"],
            mode="lines+markers",
            name="Avg Match Score",
            line=dict(color="#f5a623", width=2.5),
            marker=dict(size=8, color="#f5a623"),
            fill="tozeroy", fillcolor="rgba(245,166,35,0.07)",
        ))
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font_color="#e8eaf0",
            title=dict(text="Average 1st Innings Score by Season", font_size=15,
                       font_family="Bebas Neue", font_color="#f5a623", x=0),
            yaxis=dict(title="Avg Runs", gridcolor="#1e2535"),
            xaxis=dict(tickfont=dict(family="JetBrains Mono", size=10)),
            showlegend=False, height=300,
            margin=dict(l=20, r=20, t=50, b=20),
        )
        st.plotly_chart(fig, use_container_width=True)

    with col_b:
        fig2 = go.Figure()
        fig2.add_trace(go.Scatter(
            x=s_data["season"], y=s_data["avg_wickets"],
            mode="lines+markers",
            name="Avg Wickets",
            line=dict(color="#e84c4c", width=2.5),
            marker=dict(size=8, color="#e84c4c"),
            fill="tozeroy", fillcolor="rgba(232,76,76,0.07)",
        ))
        fig2.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font_color="#e8eaf0",
            title=dict(text="Avg Wickets Per Innings by Season", font_size=15,
                       font_family="Bebas Neue", font_color="#f5a623", x=0),
            yaxis=dict(title="Avg Wickets", gridcolor="#1e2535"),
            xaxis=dict(tickfont=dict(family="JetBrains Mono", size=10)),
            showlegend=False, height=300,
            margin=dict(l=20, r=20, t=50, b=20),
        )
        st.plotly_chart(fig2, use_container_width=True)

    # Matches per season + boundary %
    col_c, col_d = st.columns(2)

    with col_c:
        fig3 = go.Figure()
        fig3.add_trace(go.Bar(
            x=s_data["season"].astype(str), y=s_data["matches"],
            marker_color="#3ecf8e", marker_line_width=0,
            text=s_data["matches"], textposition="outside",
            textfont=dict(family="JetBrains Mono", size=10, color="#3ecf8e"),
        ))
        fig3.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font_color="#e8eaf0",
            title=dict(text="Matches Played Per Season", font_size=15,
                       font_family="Bebas Neue", font_color="#f5a623", x=0),
            yaxis=dict(gridcolor="#1e2535"),
            showlegend=False, height=300,
            margin=dict(l=20, r=20, t=50, b=20),
        )
        st.plotly_chart(fig3, use_container_width=True)

    with col_d:
        fig4 = go.Figure()
        fig4.add_trace(go.Bar(
            x=s_data["season"].astype(str), y=s_data["boundary_pct"],
            marker=dict(
                color=s_data["boundary_pct"],
                colorscale=[[0,"#1a2535"],[1,"#f5a623"]],
                showscale=False,
            ),
            marker_line_width=0,
            text=[f"{v:.1f}%" for v in s_data["boundary_pct"]],
            textposition="outside",
            textfont=dict(family="JetBrains Mono", size=10, color="#f5a623"),
        ))
        fig4.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font_color="#e8eaf0",
            title=dict(text="Boundary % of Total Runs by Season", font_size=15,
                       font_family="Bebas Neue", font_color="#f5a623", x=0),
            yaxis=dict(title="%", gridcolor="#1e2535"),
            showlegend=False, height=300,
            margin=dict(l=20, r=20, t=50, b=20),
        )
        st.plotly_chart(fig4, use_container_width=True)


# ══════════════════════════════════════════════════════════════════════════════
# TAB 5 — SURPRISE INSIGHTS
# ══════════════════════════════════════════════════════════════════════════════
with tab5:
    st.markdown("<h2>💡 What The Data Revealed</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color:#6b7280'>Beyond the obvious — patterns most analysts miss.</p>",
                unsafe_allow_html=True)

    surprises = surprise_insights(df_f, matches_f)

    for i, s in enumerate(surprises):
        icon = ["🎲","🏏","💣","🔄","📊","🎯"][i % 6]
        st.markdown(f"""
        <div class='insight-box' style='margin-bottom: 16px;'>
            <div class='insight-label'>{icon} Insight #{i+1} — {s["title"]}</div>
            <div class='insight-text'>{s["body"]}</div>
        </div>
        """, unsafe_allow_html=True)

    # Dot-ball pressure chart
    # st.markdown("<br><h3>🎯 Dot Ball Economy — Impact On Winning</h3>", unsafe_allow_html=True)
    dot_data = surprises[-1].get("dot_chart_data")
    if dot_data is not None:
        fig = go.Figure()
        fig.add_trace(go.Box(
            y=dot_data["winner_dots"], name="Winners",
            marker_color="#3ecf8e", line_color="#3ecf8e",
            fillcolor="rgba(62,207,142,0.1)",
        ))
        fig.add_trace(go.Box(
            y=dot_data["loser_dots"], name="Losers",
            marker_color="#e84c4c", line_color="#e84c4c",
            fillcolor="rgba(232,76,76,0.1)",
        ))
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font_color="#e8eaf0",
            title=dict(text="Dot Ball % — Bowling Teams (Winners vs Losers)",
                       font_size=15, font_family="Bebas Neue", font_color="#f5a623", x=0),
            yaxis=dict(title="Dot Ball %", gridcolor="#1e2535"),
            showlegend=True,
            legend=dict(bgcolor="rgba(0,0,0,0)"),
            height=360,
            margin=dict(l=20, r=20, t=50, b=20),
        )
        st.plotly_chart(fig, use_container_width=True)

    # # THE one surprising sentence
    # st.markdown("""
    # <div style='background: linear-gradient(135deg, #1a1000 0%, #0a0c10 100%);
    #      border: 2px solid #f5a623; border-radius: 16px; padding: 32px 36px; margin-top: 24px;'>
    #     <div style='font-family: JetBrains Mono, monospace; font-size: 11px;
    #          letter-spacing: 3px; color: #f5a623; text-transform: uppercase; margin-bottom: 12px;'>
    #         ★ THE ONE SENTENCE THAT SURPRISED ME MOST
    #     </div>
    #     <div style='font-family: Bebas Neue, sans-serif; font-size: 28px;
    #          color: #e8eaf0; letter-spacing: 1px; line-height: 1.3;'>
    #         Dot-ball percentage by the bowling team is a stronger predictor of match outcome
    #         than any single batter's score — silence beats sixes.
    #     </div>
    # </div>
    # """, unsafe_allow_html=True)


# ── FOOTER ─────────────────────────────────────────────────────────────────────
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("""
<div style='text-align:center; color:#2d3446; font-family: JetBrains Mono, monospace;
     font-size: 10px; letter-spacing: 2px; padding: 20px 0;'>
    IPL CRUNCH '26 · WOOBLE ANALYTICS CHALLENGE · BALL-BY-BALL INTELLIGENCE
</div>
""", unsafe_allow_html=True)
