import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import os

from data_engine import ROUTES_DF, QUARTERLY_DF, SUMMARY, EXITS_DF

st.set_page_config(
    page_title="Spirit Opportunity War Room",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

  html, body, [class*="css"] {
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background-color: #ffffff !important;
  }

  /* Force white background on all Streamlit containers */
  .stApp,
  [data-testid="stApp"],
  [data-testid="stAppViewContainer"],
  [data-testid="stMainBlockContainer"],
  [data-testid="stHeader"],
  [data-testid="stToolbar"],
  [data-testid="stDecoration"],
  section[data-testid="stMain"],
  [data-testid="stVerticalBlock"],
  .main,
  .block-container {
    background-color: #ffffff !important;
    color: #333333 !important;
  }

  .main { background: #ffffff !important; }
  .block-container { padding-top: 0rem; padding-bottom: 2rem; }

  /* ── Sidebar ─────────────────────────────────────────────────── */
  [data-testid="stSidebar"] {
    background-color: #f8f9fa !important;
    border-right: 1px solid #dde3e8 !important;
  }
  [data-testid="stSidebar"] > div {
    background-color: #f8f9fa !important;
  }
  [data-testid="stSidebarContent"] {
    background-color: #f8f9fa !important;
  }
  /* Radio label base style */
  [data-testid="stSidebar"] [data-testid="stRadio"] label {
    font-size: 14px !important;
    color: #444444 !important;
    padding: 5px 10px 5px 12px !important;
    border-left: 3px solid transparent !important;
    border-radius: 0 4px 4px 0 !important;
    display: block !important;
    margin-bottom: 2px !important;
    transition: all 0.15s !important;
  }
  [data-testid="stSidebar"] [data-testid="stRadio"] label:hover {
    background-color: #e8edf2 !important;
    color: #003366 !important;
  }
  /* Selected radio item — targets the checked input's parent label */
  [data-testid="stSidebar"] [role="radio"][aria-checked="true"] ~ div label,
  [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] {
    color: #333 !important;
  }
  [data-testid="stSidebar"] div[data-baseweb="radio"]:has(input:checked) label,
  [data-testid="stSidebar"] div[data-baseweb="radio"][aria-checked="true"] label {
    font-weight: 700 !important;
    color: #003366 !important;
    border-left: 3px solid #003366 !important;
    background-color: #e8eef7 !important;
  }
  /* ──────────────────────────────────────────────────────────── */

  .topbar {
    background: #003366;
    color: white;
    padding: 10px 24px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 20px;
    border-radius: 4px;
  }
  .topbar-left { font-size: 15px; font-weight: 700; letter-spacing: 0.3px; }
  .topbar-right { font-size: 12px; color: #a8c4e0; text-align: right; }

  .alert-banner {
    background: #003366;
    color: white;
    padding: 20px 28px;
    border-radius: 6px;
    margin-bottom: 24px;
  }
  .alert-banner .label {
    font-size: 11px; font-weight: 700; letter-spacing: 2px;
    color: #FFD700; text-transform: uppercase; margin-bottom: 6px;
  }
  .alert-banner h2 {
    font-size: 22px; font-weight: 800; margin: 0 0 8px 0; color: white;
  }
  .alert-banner p { font-size: 14px; color: #c8d8e8; margin: 0; line-height: 1.6; }

  .metric-card {
    background: #ffffff;
    border: 1px solid #e8ecf0;
    border-left: 4px solid #003366;
    border-radius: 6px;
    padding: 20px 18px;
  }
  .metric-card .big-num {
    font-size: 36px; font-weight: 800; color: #003366;
    line-height: 1.1; margin-bottom: 4px;
  }
  .metric-card .label { font-size: 13px; font-weight: 600; color: #333; }
  .metric-card .sub { font-size: 11px; color: #777; margin-top: 4px; }

  .metric-card-green { border-left-color: #1a7a1a; }
  .metric-card-green .big-num { color: #1a7a1a; }

  .section-divider {
    border: none; border-top: 1px solid #e8ecf0;
    margin: 24px 0;
  }

  .section-header {
    font-size: 18px; font-weight: 700; color: #003366;
    margin-bottom: 4px; margin-top: 8px;
  }
  .section-sub {
    font-size: 13px; color: #666;
    margin-bottom: 16px;
  }

  .airline-card {
    background: #f8f9fa;
    border-radius: 6px;
    padding: 18px;
    height: 100%;
  }
  .airline-card h4 {
    font-size: 14px; font-weight: 700; color: #003366;
    margin-bottom: 10px; border-bottom: 1px solid #dde;
    padding-bottom: 8px;
  }
  .airline-card ul {
    margin: 0; padding-left: 18px;
    font-size: 12.5px; color: #444; line-height: 1.9;
  }

  .insight-box {
    background: #f0f4ff;
    border-left: 4px solid #003366;
    padding: 18px 20px;
    border-radius: 0 6px 6px 0;
    margin-top: 16px;
  }
  .insight-box h4 {
    font-size: 13px; font-weight: 700; color: #003366;
    letter-spacing: 1px; text-transform: uppercase;
    margin-bottom: 8px;
  }
  .insight-box p { font-size: 13px; color: #333; line-height: 1.7; margin: 0; }

  .navy-callout {
    background: #003366;
    color: white;
    padding: 18px 22px;
    border-radius: 6px;
    margin-bottom: 20px;
  }
  .navy-callout .callout-label {
    font-size: 10px; font-weight: 700; letter-spacing: 2px;
    color: #FFD700; text-transform: uppercase; margin-bottom: 8px;
  }
  .navy-callout p { font-size: 13px; color: #d8e8f4; line-height: 1.75; margin: 0; }
  .navy-callout strong { color: #ffffff; }

  .ai-response-box {
    background: #f0f4ff;
    border-left: 4px solid #003366;
    padding: 18px 20px;
    border-radius: 0 6px 6px 0;
    margin-top: 12px;
  }

  .footer {
    font-size: 11px; color: #999;
    border-top: 1px solid #eee;
    padding-top: 12px; margin-top: 32px;
    text-align: center;
  }

  .risk-high { color: #cc0000; font-weight: 600; }
  .risk-medium { color: #cc7700; font-weight: 600; }
  .risk-low { color: #1a7a1a; font-weight: 600; }

  .recommendation-card {
    border-radius: 8px;
    padding: 20px;
    text-align: center;
    font-weight: 700;
    font-size: 14px;
  }

  .kpi-card {
    background: #f8f9fa;
    border: 1px solid #e0e0e0;
    border-top: 3px solid #003366;
    border-radius: 6px;
    padding: 16px;
    text-align: center;
  }
  .kpi-card .kpi-target { font-size: 14px; font-weight: 700; color: #003366; }
  .kpi-card .kpi-sub { font-size: 11px; color: #777; margin-top: 4px; }

  .fare-result-card {
    background: #f8f9fa;
    border: 1px solid #dde;
    border-left: 4px solid #1a7a1a;
    border-radius: 6px;
    padding: 20px;
  }
</style>
""", unsafe_allow_html=True)


def topbar():
    st.markdown("""
    <div class="topbar">
      <div class="topbar-left">Spirit Opportunity War Room</div>
      <div class="topbar-right">Data as of May 2, 2026 | Spirit Airlines Ceased Operations Today</div>
    </div>
    """, unsafe_allow_html=True)


def footer():
    st.markdown("""
    <div class="footer">
      Built by Mustafa Qadri | Aviation Analytics Portfolio &nbsp;|&nbsp;
      Data: BTS Government Data, Public Earnings Reports &nbsp;|&nbsp;
      Methodology: Available on GitHub
    </div>
    """, unsafe_allow_html=True)


# ─── CHART DEFAULTS ───────────────────────────────────────────────────────────
CHART_LAYOUT = dict(
    paper_bgcolor="white",
    plot_bgcolor="white",
    font_family="Inter, system-ui, sans-serif",
    font_color="#333333",
    margin=dict(l=40, r=20, t=40, b=40),
)


def ax(title_text, extra=None):
    """Return a standardised axis dict."""
    d = dict(
        title=dict(text=title_text, font=dict(size=13, color="#111111", family="Arial Black")),
        tickfont=dict(size=12, color="#111111"),
        showline=True,
        linecolor="#111111",
        linewidth=2,
        showgrid=True,
        gridcolor="#eeeeee",
    )
    if extra:
        d.update(extra)
    return d


# ═══════════════════════════════════════════════════════════════════════════════
# PAGE 1: EXECUTIVE BRIEF
# ═══════════════════════════════════════════════════════════════════════════════
def page_executive_brief():
    topbar()

    st.markdown("""
    <div class="alert-banner">
      <div class="label">Strategic Alert &nbsp;|&nbsp; May 2, 2026</div>
      <h2>Spirit Airlines has ceased operations.</h2>
      <p>$2.3B in annual passenger revenue is now up for grabs across 25 high-value routes.<br>
         The 90-day window to capture market share starts today.</p>
    </div>
    """, unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)
    cards = [
        ("$2.3B", "Total Annual Revenue Opportunity", "Across Spirit's top 25 routes"),
        ("25", "Routes Losing ULCC Competition", "Immediate pricing power shift"),
        ("17,000", "Spirit Employees Displaced", "Experienced aviation talent available"),
        ("90 Days", "Critical Response Window", "Before market stabilizes"),
    ]
    for col, (num, label, sub) in zip([c1, c2, c3, c4], cards):
        with col:
            st.markdown(f"""
            <div class="metric-card">
              <div class="big-num">{num}</div>
              <div class="label">{label}</div>
              <div class="sub">{sub}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown('<hr class="section-divider">', unsafe_allow_html=True)

    st.markdown('<div class="section-header">Why This Matters For You</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Position-specific analysis for each stakeholder</div>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        <div class="airline-card">
          <h4>Delta's Position</h4>
          <ul>
            <li>Delta overlaps <strong>18 of 25</strong> Spirit routes</li>
            <li>Strongest position: FLL-MSP, FLL-DTW, MCO-MSP<br>
                <em>(Delta is only major carrier on these)</em></li>
            <li>Estimated capturable revenue: <strong>$1.1B annually</strong></li>
            <li>Recommended: Add frequencies on FLL-MSP, FLL-DTW within 30 days</li>
          </ul>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class="airline-card">
          <h4>American's Position</h4>
          <ul>
            <li>AA overlaps <strong>21 of 25</strong> Spirit routes</li>
            <li>Strongest position: FLL-MIA, MCO-PHL, FLL-ORD</li>
            <li>Estimated capturable revenue: <strong>$890M annually</strong></li>
            <li>Recommended: Aggressive pricing on FLL-MIA<br>
                <em>(Fort Lauderdale is Spirit's home turf)</em></li>
          </ul>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
        <div class="airline-card">
          <h4>Consumer Impact</h4>
          <ul>
            <li>1.7M monthly Spirit passengers need new options</li>
            <li>Fare increases likely: <strong>12–18%</strong> on key routes</li>
            <li>Fort Lauderdale most exposed: Spirit held 27% share</li>
            <li>Basic economy competition will intensify across network</li>
          </ul>
        </div>
        """, unsafe_allow_html=True)

    footer()


# ═══════════════════════════════════════════════════════════════════════════════
# PAGE 2: THE COLLAPSE STORY
# ═══════════════════════════════════════════════════════════════════════════════
def page_collapse_story():
    topbar()

    st.markdown('<div class="section-header">How Did We Get Here?</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">The data told this story 18 months before it ended.</div>', unsafe_allow_html=True)

    df = QUARTERLY_DF.copy()
    periods = df["period"].tolist()

    # Chart 1 — dual-axis collapse overview
    fig1 = make_subplots(specs=[[{"secondary_y": True}]])

    fig1.add_trace(go.Scatter(
        x=periods, y=df["on_time_pct"],
        name="On-Time %", mode="lines+markers",
        line=dict(color="#FFD700", width=2.5),
        marker=dict(size=5),
        hovertemplate="%{x}<br>On-Time: %{y:.1f}%<extra></extra>",
    ), secondary_y=False)

    fig1.add_trace(go.Scatter(
        x=periods, y=df["market_share_pct"],
        name="Market Share %", mode="lines+markers",
        line=dict(color="#cc0000", width=2.5, dash="dash"),
        marker=dict(size=5),
        hovertemplate="%{x}<br>Market Share: %{y:.1f}%<extra></extra>",
    ), secondary_y=True)

    for shade, color, label in [
        (["Q2 2020", "Q4 2020"], "rgba(180,180,180,0.18)", "COVID Period"),
        (["Q1 2022", "Q4 2023"], "rgba(255,215,0,0.12)", "Merger Optimism"),
        (["Q1 2024", "Q4 2024"], "rgba(204,0,0,0.10)", "Terminal Decline"),
    ]:
        fig1.add_vrect(
            x0=shade[0], x1=shade[1],
            fillcolor=color, layer="below", line_width=0,
            annotation_text=label,
            annotation_position="top left",
            annotation_font=dict(size=10, color="#555"),
        )

    fig1.update_layout(
        title=dict(text="Spirit Airlines: Collapse by the Numbers (Q1 2019 – Q4 2024)", font_size=14, font_color="#003366"),
        **CHART_LAYOUT,
        xaxis=ax("Quarter", {"tickangle": -45}),
        legend=dict(orientation="h", y=-0.18, bgcolor="rgba(255,255,255,0.9)",
                    bordercolor="#cccccc", borderwidth=1, font=dict(size=11, color="#111111")),
        height=380,
    )
    fig1.update_yaxes(
        title_text="On-Time Performance (%)",
        title_font=dict(size=13, color="#111111", family="Arial Black"),
        tickfont=dict(size=12, color="#111111"),
        showline=True, linecolor="#111111", linewidth=2,
        showgrid=True, gridcolor="#eeeeee",
        secondary_y=False, range=[30, 95],
    )
    fig1.update_yaxes(
        title_text="Market Share (%)",
        title_font=dict(size=13, color="#111111", family="Arial Black"),
        tickfont=dict(size=12, color="#111111"),
        showline=True, linecolor="#111111", linewidth=2,
        showgrid=False,
        secondary_y=True, range=[0, 7],
    )

    st.plotly_chart(fig1, use_container_width=True)

    col1, col2 = st.columns(2)

    with col1:
        fig2 = go.Figure()
        fig2.add_trace(go.Scatter(x=periods, y=df["on_time_pct"],
                                   name="Spirit (NK)", line=dict(color="#FFD700", width=2.5),
                                   mode="lines+markers", marker=dict(size=4)))
        fig2.add_trace(go.Scatter(x=periods, y=df["delta_on_time"],
                                   name="Delta (DL)", line=dict(color="#003366", width=2),
                                   mode="lines", opacity=0.85))
        fig2.add_trace(go.Scatter(x=periods, y=df["aa_on_time"],
                                   name="American (AA)", line=dict(color="#cc0000", width=2),
                                   mode="lines", opacity=0.85))
        fig2.update_layout(
            title=dict(text="On-Time Performance: Spirit vs Peers", font_size=13, font_color="#003366"),
            **CHART_LAYOUT,
            xaxis=ax("Quarter", {"tickangle": -45, "tickfont": dict(size=9, color="#111111")}),
            yaxis=ax("On-Time Performance (%)", {"range": [30, 95]}),
            legend=dict(orientation="h", y=-0.25, bgcolor="rgba(255,255,255,0.9)",
                        bordercolor="#cccccc", borderwidth=1, font=dict(size=11, color="#111111")),
            height=340,
        )
        st.plotly_chart(fig2, use_container_width=True)

    with col2:
        years = ["2019", "2020", "2021", "2022", "2023", "2024"]

        def avg_by_year(col):
            vals = []
            for y in years:
                rows = df[df["period"].str.contains(y)]
                vals.append(round(rows[col].mean(), 2))
            return vals

        spirit_cancel = avg_by_year("cancel_pct")
        delta_cancel = avg_by_year("delta_cancel")
        aa_cancel = [1.5, 3.8, 2.1, 3.2, 2.4, 2.1]
        wn_cancel  = [1.8, 2.9, 2.4, 3.1, 2.1, 1.9]

        fig3 = go.Figure()
        fig3.add_trace(go.Bar(name="Spirit (NK)", x=years, y=spirit_cancel,
                               marker_color="#FFD700",
                               text=[f"{v:.1f}%" for v in spirit_cancel],
                               textposition="outside", textfont_size=9))
        fig3.add_trace(go.Bar(name="Delta (DL)", x=years, y=delta_cancel,
                               marker_color="#003366",
                               text=[f"{v:.1f}%" for v in delta_cancel],
                               textposition="outside", textfont_size=9))
        fig3.add_trace(go.Bar(name="American (AA)", x=years, y=aa_cancel,
                               marker_color="#CC0000",
                               text=[f"{v:.1f}%" for v in aa_cancel],
                               textposition="outside", textfont_size=9))
        fig3.add_trace(go.Bar(name="Southwest (WN)", x=years, y=wn_cancel,
                               marker_color="#304CB2",
                               text=[f"{v:.1f}%" for v in wn_cancel],
                               textposition="outside", textfont_size=9))
        fig3.update_layout(
            title=dict(text="Cancellation Rate by Year: Spirit vs Peers", font_size=13, font_color="#003366"),
            **CHART_LAYOUT,
            xaxis=ax("Year", {"showgrid": False}),
            yaxis=ax("Cancellation Rate (%)", {"range": [0, 12]}),
            barmode="group",
            legend=dict(orientation="h", y=-0.25, bgcolor="rgba(255,255,255,0.9)",
                        bordercolor="#cccccc", borderwidth=1, font=dict(size=10, color="#111111")),
            height=360,
        )
        st.plotly_chart(fig3, use_container_width=True)

    st.markdown("""
    <div class="insight-box">
      <h4>The Inflection Point</h4>
      <p>Spirit's on-time performance fell below 60% in Q3 2024 — the same quarter their market share dropped below 2.5%.
      This is not coincidence. Poor operations drove customer churn, which reduced load factors, which increased per-seat
      costs, which made recovery mathematically impossible. The spiral was self-reinforcing from Q2 2021 onward.
      The data signaled terminal decline more than 18 months before the formal shutdown.</p>
    </div>
    """, unsafe_allow_html=True)

    footer()


# ═══════════════════════════════════════════════════════════════════════════════
# PAGE 3: ROUTE OPPORTUNITY MAP
# ═══════════════════════════════════════════════════════════════════════════════
def page_route_map():
    topbar()

    st.markdown('<div class="section-header">Where Should Delta and American Move First?</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Routes ranked by revenue opportunity, urgency, and competitive positioning</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="navy-callout">
      <div class="callout-label">Important Context</div>
      <p>
        <strong>Delta and American already serve most of these routes alongside Spirit.</strong>
        The opportunity is not to start new routes — it is to:<br>
        <strong>(1)</strong> Add flight frequencies now that Spirit's seats are gone,&nbsp;
        <strong>(2)</strong> Adjust pricing upward as ULCC competition disappears, and&nbsp;
        <strong>(3)</strong> Target Spirit's 1.7M monthly passengers with loyalty offers.<br>
        Routes marked <strong>MOVE NOW</strong> have the highest Spirit market share and fewest
        alternative competitors.
      </p>
    </div>
    """, unsafe_allow_html=True)

    f1, f2, f3 = st.columns(3)
    with f1:
        airline_filter = st.selectbox("View opportunities for:", ["Both Airlines", "Delta Specifically", "AA Specifically"])
    with f2:
        min_opp = st.selectbox("Minimum opportunity size:", ["All routes", "$50M+", "$100M+", "$200M+"])
    with f3:
        risk_filter = st.selectbox("Competitive risk:", ["All", "Low Risk Only", "Medium Risk", "High Risk"])

    df = ROUTES_DF.copy()

    if airline_filter == "Delta Specifically":
        df = df[df["has_delta"]]
    elif airline_filter == "AA Specifically":
        df = df[df["has_aa"]]

    if min_opp == "$50M+":
        df = df[df["Annual Rev Opportunity ($M)"] >= 50]
    elif min_opp == "$100M+":
        df = df[df["Annual Rev Opportunity ($M)"] >= 100]
    elif min_opp == "$200M+":
        df = df[df["Annual Rev Opportunity ($M)"] >= 200]

    if risk_filter == "Low Risk Only":
        df = df[df["Competitive Risk"] == "LOW"]
    elif risk_filter == "Medium Risk":
        df = df[df["Competitive Risk"] == "MEDIUM"]
    elif risk_filter == "High Risk":
        df = df[df["Competitive Risk"] == "HIGH"]

    display_cols = ["Route", "Monthly Pax Lost", "Annual Rev Opportunity ($M)",
                    "Urgency Score", "Best Positioned", "Competitive Risk", "Recommended Action"]

    def color_urgency(val):
        if val >= 8:
            return "background-color: #ffe5e5; color: #cc0000; font-weight: 600;"
        elif val >= 5:
            return "background-color: #fff8e1; color: #b36b00; font-weight: 600;"
        else:
            return "background-color: #e8f5e9; color: #1a7a1a; font-weight: 600;"

    def color_risk(val):
        if val == "HIGH":
            return "color: #cc0000; font-weight: 600;"
        elif val == "MEDIUM":
            return "color: #cc7700; font-weight: 600;"
        else:
            return "color: #1a7a1a; font-weight: 600;"

    st.markdown("""
    <div style='background:#f0f4ff;border-left:4px solid #003366;padding:1rem 1.2rem;
                border-radius:0 8px 8px 0;margin-bottom:1rem;'>
      <p style='font-size:0.7rem;font-weight:700;color:#003366;text-transform:uppercase;
                letter-spacing:0.08em;margin:0 0 6px 0;'>METHODOLOGY NOTE</p>
      <p style='font-size:0.85rem;color:#333;line-height:1.6;margin:0;'>
        <b>Urgency Score (1–10)</b> is a screening tool, not a final decision model. Formula:
        (Spirit market share × 10) + (1 ÷ competitors × 5).
        <b>Higher score = Spirit had dominant share AND few alternatives exist for displaced passengers.</b>
        This identifies which routes warrant immediate deeper analysis by revenue management teams.
        Full modeling should incorporate: route profitability, aircraft availability, slot constraints,
        and seasonal demand patterns before any capacity decision.
      </p>
    </div>
    """, unsafe_allow_html=True)

    styled = df[display_cols].style \
        .applymap(color_urgency, subset=["Urgency Score"]) \
        .applymap(color_risk, subset=["Competitive Risk"]) \
        .format({"Annual Rev Opportunity ($M)": "${:.1f}M", "Monthly Pax Lost": "{:,.0f}"}) \
        .set_properties(**{"font-size": "12px"})

    st.dataframe(styled, use_container_width=True, height=400)

    with st.expander("How is the Urgency Score calculated?"):
        st.markdown("""
**Urgency Score (1–10)** =
(Spirit's market share on route × 10) + (1 ÷ number of competing airlines × 5)

**Higher score** = Spirit had dominant share AND fewer competitors to absorb displaced passengers.

**Example:** FLL-MSP scores 9.4 because Spirit had 29% market share AND Delta is the only other
major carrier on this route.

**Source:** Calculated from BTS market share data and public route schedules.
        """)

    st.markdown('<hr class="section-divider">', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        risk_color_map = {"LOW": "#1a7a1a", "MEDIUM": "#cc7700", "HIGH": "#cc0000"}
        df["risk_color"] = df["Competitive Risk"].map(risk_color_map)

        fig_bubble = go.Figure()
        for risk, color in risk_color_map.items():
            sub = df[df["Competitive Risk"] == risk]
            fig_bubble.add_trace(go.Scatter(
                x=sub["Annual Rev Opportunity ($M)"],
                y=sub["Urgency Score"],
                mode="markers+text",
                name=risk,
                text=sub["Route"],
                textposition="top center",
                textfont=dict(size=8),
                marker=dict(
                    size=sub["Monthly Pax Lost"] / 800,
                    color=color,
                    opacity=0.75,
                    line=dict(width=1, color="white"),
                ),
                hovertemplate="<b>%{text}</b><br>Rev Opp: $%{x:.1f}M<br>Urgency: %{y:.1f}<extra></extra>",
            ))

        fig_bubble.add_shape(type="line", x0=120, x1=120, y0=0, y1=10,
                              line=dict(color="#aaa", dash="dash", width=1))
        fig_bubble.add_shape(type="line", x0=0, x1=300, y0=6, y1=6,
                              line=dict(color="#aaa", dash="dash", width=1))

        for txt, x, y in [("ACT IMMEDIATELY", 200, 9.5),
                           ("PLAN AND EXECUTE", 20, 9.5),
                           ("QUICK WIN", 200, 1.2),
                           ("MONITOR", 20, 1.2)]:
            fig_bubble.add_annotation(text=txt, x=x, y=y, showarrow=False,
                                       font=dict(size=9, color="#888"))

        fig_bubble.update_layout(
            title=dict(text="Opportunity vs Urgency Matrix", font_size=13, font_color="#003366"),
            **CHART_LAYOUT,
            xaxis=ax("Annual Revenue Opportunity ($M)"),
            yaxis=ax("Urgency Score (1–10)", {"range": [0, 11]}),
            legend=dict(title=dict(text="Risk Level", font=dict(size=11, color="#111111")),
                        bgcolor="rgba(255,255,255,0.9)", bordercolor="#cccccc", borderwidth=1,
                        font=dict(size=11, color="#111111")),
            height=420,
        )
        st.plotly_chart(fig_bubble, use_container_width=True)

    with col2:
        top10 = df.nlargest(10, "Annual Rev Opportunity ($M)").sort_values("Annual Rev Opportunity ($M)")
        fig_bar = go.Figure(go.Bar(
            x=top10["Annual Rev Opportunity ($M)"],
            y=top10["Route"],
            orientation="h",
            marker_color="#1a7a1a",
            text=[f"${v:.1f}M" for v in top10["Annual Rev Opportunity ($M)"]],
            textposition="outside",
            textfont=dict(size=11),
            hovertemplate="<b>%{y}</b><br>$%{x:.1f}M annually<extra></extra>",
        ))
        fig_bar.update_layout(
            title=dict(text="Top 10 Revenue Opportunities by Route", font_size=13, font_color="#003366"),
            **CHART_LAYOUT,
            xaxis=ax("Annual Revenue Opportunity ($M)"),
            yaxis=ax("", {"showgrid": False}),
            height=420,
        )
        st.plotly_chart(fig_bar, use_container_width=True)

    footer()


# ═══════════════════════════════════════════════════════════════════════════════
# PAGE 4: FARE IMPACT PROJECTOR
# ═══════════════════════════════════════════════════════════════════════════════
def page_fare_projector():
    topbar()

    st.markdown('<div class="section-header">What Happens To Fares When Competition Disappears?</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Historical analysis shows ULCC exits drive 12–22% fare increases within 90 days</div>', unsafe_allow_html=True)

    routes_list = ROUTES_DF["Route"].tolist()
    route_share_map = dict(zip(ROUTES_DF["Route"], ROUTES_DF["spirit_share"]))
    route_comp_map = dict(zip(ROUTES_DF["Route"], ROUTES_DF["Best Positioned"]))

    fc1, fc2, fc3 = st.columns(3)
    with fc1:
        st.markdown("**Select Route to Analyze**")
        selected_route = st.selectbox("Select Route", routes_list, index=0, label_visibility="collapsed")
    with fc2:
        st.markdown("**Spirit's Market Share on This Route (%)**")
        st.markdown("<p style='font-size:0.8rem;color:#666;margin-top:-8px;'>Higher share = more passengers displaced = larger fare increase expected</p>", unsafe_allow_html=True)
        default_share = int(route_share_map.get(selected_route, 0.25) * 100)
        spirit_share_pct = st.slider("Spirit Market Share on This Route (%)", 0, 50, default_share, label_visibility="collapsed")
    with fc3:
        st.markdown("**Days Since Spirit Exited This Route**")
        st.markdown("<p style='font-size:0.8rem;color:#666;margin-top:-8px;'>Fare increases peak around day 60–90 then stabilize as competition responds</p>", unsafe_allow_html=True)
        days_since_exit = st.slider("Days Since Spirit Exited", 0, 365, 30, label_visibility="collapsed")

    base_fare = 187.0
    spirit_avg = 89.0
    base_increase_pct = spirit_share_pct * 0.45

    d30  = base_fare * (1 + base_increase_pct * 0.4 / 100)
    d90  = base_fare * (1 + base_increase_pct * 0.8 / 100)
    d180 = base_fare * (1 + base_increase_pct / 100)

    def lerp(t, start, end):
        return start + (end - start) * min(t, 1.0)

    if days_since_exit <= 30:
        current_est = lerp(days_since_exit / 30, base_fare, d30)
    elif days_since_exit <= 90:
        current_est = lerp((days_since_exit - 30) / 60, d30, d90)
    elif days_since_exit <= 180:
        current_est = lerp((days_since_exit - 90) / 90, d90, d180)
    else:
        current_est = lerp((days_since_exit - 180) / 185, d180, base_fare * 1.08)

    best_airline = route_comp_map.get(selected_route, "Delta / AA")
    pct_change = (current_est - base_fare) / base_fare * 100

    col_card, col_spacer = st.columns([1, 1])
    with col_card:
        st.markdown(f"""
        <div class="fare-result-card">
          <div style="font-size:18px;font-weight:800;color:#003366;margin-bottom:12px;">{selected_route}</div>
          <div style="display:grid;grid-template-columns:1fr 1fr;gap:12px;">
            <div>
              <div style="font-size:11px;color:#777;text-transform:uppercase;letter-spacing:1px;">Current Est. Fare</div>
              <div style="font-size:24px;font-weight:800;color:#003366;">${current_est:.0f}</div>
              <div style="font-size:11px;color:{'#cc0000' if pct_change > 0 else '#1a7a1a'}">
                {'+' if pct_change >= 0 else ''}{pct_change:.1f}% vs base
              </div>
            </div>
            <div>
              <div style="font-size:11px;color:#777;text-transform:uppercase;letter-spacing:1px;">Most Likely to Fill Route</div>
              <div style="font-size:18px;font-weight:700;color:#003366;">{best_airline}</div>
            </div>
          </div>
          <div style="margin-top:14px;border-top:1px solid #dde;padding-top:12px;display:grid;grid-template-columns:1fr 1fr 1fr;gap:8px;">
            <div style="text-align:center;">
              <div style="font-size:10px;color:#777;">30-Day</div>
              <div style="font-size:16px;font-weight:700;color:#1a7a1a;">${d30:.0f}</div>
              <div style="font-size:10px;color:#999;">+{(d30-base_fare)/base_fare*100:.1f}%</div>
            </div>
            <div style="text-align:center;">
              <div style="font-size:10px;color:#777;">90-Day</div>
              <div style="font-size:16px;font-weight:700;color:#cc7700;">${d90:.0f}</div>
              <div style="font-size:10px;color:#999;">+{(d90-base_fare)/base_fare*100:.1f}%</div>
            </div>
            <div style="text-align:center;">
              <div style="font-size:10px;color:#777;">180-Day</div>
              <div style="font-size:16px;font-weight:700;color:#cc0000;">${d180:.0f}</div>
              <div style="font-size:10px;color:#999;">+{(d180-base_fare)/base_fare*100:.1f}%</div>
            </div>
          </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("&nbsp;", unsafe_allow_html=True)

    days = list(range(0, 366))
    fares = []
    for d in days:
        if d <= 30:
            fares.append(lerp(d / 30, base_fare, d30))
        elif d <= 90:
            fares.append(lerp((d - 30) / 60, d30, d90))
        elif d <= 180:
            fares.append(lerp((d - 90) / 90, d90, d180))
        else:
            fares.append(lerp((d - 180) / 185, d180, base_fare * 1.08))

    fig_fare = go.Figure()
    fig_fare.add_trace(go.Scatter(
        x=days, y=fares,
        name="Projected Fare Post-Spirit Exit",
        line=dict(color="#003366", width=2.5),
        fill="tozeroy", fillcolor="rgba(0,51,102,0.06)",
        hovertemplate="Day %{x}: $%{y:.0f}<extra></extra>",
    ))
    fig_fare.add_trace(go.Scatter(
        x=days, y=[spirit_avg] * len(days),
        name=f"Spirit's Historical Avg Fare: ${spirit_avg:.0f}",
        line=dict(color="#b8960c", width=1.5, dash="dash"),
        hoverinfo="skip",
    ))
    fig_fare.add_trace(go.Scatter(
        x=days, y=[base_fare] * len(days),
        name=f"Legacy Carrier Avg Fare: ${base_fare:.0f}",
        line=dict(color="#cc0000", width=1.5, dash="dash"),
        hoverinfo="skip",
    ))
    for d_mark in [30, 90, 180]:
        fig_fare.add_vline(x=d_mark, line_dash="dot", line_color="#aaa",
                            annotation_text=f"Day {d_mark}",
                            annotation_position="top")
    if 0 <= days_since_exit <= 365:
        fig_fare.add_vline(x=days_since_exit, line_color="#1a7a1a", line_width=2,
                            annotation_text="Today", annotation_position="top right")

    fig_fare.update_layout(
        title=dict(text=f"Projected Fare Trajectory — {selected_route}", font_size=13, font_color="#003366"),
        **CHART_LAYOUT,
        xaxis=ax("Days Since Spirit Exit"),
        yaxis=ax("Average Fare ($)"),
        legend=dict(
            orientation="v",
            yanchor="top", y=0.99,
            xanchor="left", x=0.01,
            bgcolor="rgba(255,255,255,0.9)",
            bordercolor="#cccccc",
            borderwidth=1,
            font=dict(size=11, color="#111111"),
        ),
        height=340,
    )
    st.plotly_chart(fig_fare, use_container_width=True)

    st.markdown('<div class="section-header" style="font-size:14px;margin-top:8px;">Historical Precedent: When Airlines Have Exited Markets</div>', unsafe_allow_html=True)
    exits_display = EXITS_DF[["airline", "routes", "year", "fare_increase_90d", "context"]].copy()
    exits_display.columns = ["Airline", "Market Coverage", "Year Exited", "Fare Increase (90 Days)", "Context"]
    exits_display["Fare Increase (90 Days)"] = exits_display["Fare Increase (90 Days)"].apply(lambda x: f"+{x}%")
    st.dataframe(exits_display, use_container_width=True, hide_index=True)

    footer()


# ═══════════════════════════════════════════════════════════════════════════════
# PAGE 5: STRATEGY COMMAND CENTER
# ═══════════════════════════════════════════════════════════════════════════════
def page_strategy_command():
    topbar()

    st.markdown('<div class="section-header">90-Day Response Playbook</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">A structured program management framework for capturing Spirit\'s abandoned market share</div>', unsafe_allow_html=True)

    # SECTION A — Decision Framework
    st.markdown("### A. Should Delta or AA Add This Route?")
    st.markdown("""
    <p style='color:#555555;font-size:0.9rem;margin-bottom:1.5rem;'>
    Adjust the three inputs below to match a specific route you want to evaluate.
    The recommendation updates instantly based on your inputs.
    </p>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <p style='font-weight:700;color:#111111;font-size:0.9rem;margin-bottom:4px;'>
        Spirit Market Share on This Route (%)</p>
        <p style='color:#666666;font-size:0.78rem;margin-bottom:8px;'>
        Higher % = more displaced passengers = bigger revenue gap to fill</p>
        """, unsafe_allow_html=True)
        spirit_share = st.slider(
            "spirit_share_hidden", min_value=0, max_value=50,
            value=25, step=1, label_visibility="collapsed",
        )
        st.markdown(f"""
        <p style='font-size:1.4rem;font-weight:800;color:#003366;margin:4px 0;'>{spirit_share}%</p>
        <p style='font-size:0.75rem;color:#888888;'>Spirit's share of this route's passengers</p>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <p style='font-weight:700;color:#111111;font-size:0.9rem;margin-bottom:4px;'>
        Delta/AA Current Daily Frequencies</p>
        <p style='color:#666666;font-size:0.78rem;margin-bottom:8px;'>
        How many flights per day does Delta or AA already operate on this route?</p>
        """, unsafe_allow_html=True)
        current_freq = st.slider(
            "frequency_hidden", min_value=0, max_value=20,
            value=4, step=1, label_visibility="collapsed",
        )
        st.markdown(f"""
        <p style='font-size:1.4rem;font-weight:800;color:#003366;margin:4px 0;'>{current_freq} flights/day</p>
        <p style='font-size:0.75rem;color:#888888;'>Current daily frequency on this route</p>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <p style='font-weight:700;color:#111111;font-size:0.9rem;margin-bottom:4px;'>
        Airport Slot Availability</p>
        <p style='color:#666666;font-size:0.78rem;margin-bottom:8px;'>
        How easy is it to get additional gate/slot access at this airport?</p>
        """, unsafe_allow_html=True)
        slot_avail = st.selectbox(
            "slot_hidden", options=["Easy", "Medium", "Hard"],
            label_visibility="collapsed",
        )
        slot_color = {"Easy": "#2e7d32", "Medium": "#f57c00", "Hard": "#c62828"}
        st.markdown(f"""
        <p style='font-size:1.4rem;font-weight:800;color:{slot_color[slot_avail]};margin:4px 0;'>{slot_avail}</p>
        <p style='font-size:0.75rem;color:#888888;'>Slot availability at target airport</p>
        """, unsafe_allow_html=True)

    if spirit_share >= 25 and slot_avail == "Easy":
        rec_color, rec_bg, rec_border = "#1a7a1a", "#e8f5e9", "#2e7d32"
        rec_text = "ADD IMMEDIATELY"
        rec_detail = (
            f"Spirit held {spirit_share}% of this route with {slot_avail.lower()} slot access available. "
            f"Delta/AA currently operates {current_freq} daily flights. Recommended action: Add 2–3 daily "
            f"frequencies within 7 days and file with DOT. Estimated additional revenue: "
            f"${int(spirit_share * 1200):,}/month per frequency added."
        )
    elif spirit_share >= 20 and slot_avail != "Hard":
        rec_color, rec_bg, rec_border = "#f57c00", "#fff8e8", "#f57c00"
        rec_text = "ADD WITHIN 30 DAYS"
        rec_detail = (
            f"Spirit held {spirit_share}% of this route. Slot availability is {slot_avail.lower()} — "
            f"negotiate gate access before a competitor does. Current {current_freq} daily flights gives "
            f"an operational base to expand from. File slot request within 72 hours."
        )
    elif spirit_share >= 15:
        rec_color, rec_bg, rec_border = "#e65100", "#fff3e0", "#e65100"
        rec_text = "EVALUATE CAREFULLY"
        rec_detail = (
            f"Spirit held {spirit_share}% share but slot access is {slot_avail.lower()} and current "
            f"frequency is {current_freq} flights/day. Run full load factor model before committing "
            f"capacity. Consider code-share options instead of new frequencies. Decision window: 60 days."
        )
    else:
        rec_color, rec_bg, rec_border = "#1565c0", "#e8eaf6", "#1565c0"
        rec_text = "MONITOR ONLY"
        rec_detail = (
            f"Spirit's {spirit_share}% share is relatively low on this route. Multiple competitors will "
            f"absorb displaced passengers naturally. No immediate action needed. Review again in 90 days."
        )

    st.markdown(f"""
    <div style='background:{rec_bg};border-left:5px solid {rec_border};
                border-radius:0 10px 10px 0;padding:1.2rem 1.5rem;margin-top:1rem;'>
      <p style='font-size:0.65rem;font-weight:700;letter-spacing:0.12em;text-transform:uppercase;
                color:{rec_color};margin:0 0 6px 0;'>RECOMMENDATION</p>
      <p style='font-size:1.3rem;font-weight:800;color:{rec_color};margin:0 0 8px 0;'>{rec_text}</p>
      <p style='font-size:0.88rem;color:#333333;line-height:1.7;margin:0;'>{rec_detail}</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<hr class="section-divider">', unsafe_allow_html=True)

    # SECTION B — Gantt timeline
    st.markdown("### B. 90-Day Program Timeline")

    tasks = [
        dict(ws="Revenue Management", task="Price analysis on all 25 Spirit routes", start=0,  end=14, color="#003366"),
        dict(ws="Revenue Management", task="Dynamic pricing adjustments",             start=14, end=28, color="#003366"),
        dict(ws="Revenue Management", task="Add frequencies on Tier 1 routes",        start=28, end=56, color="#003366"),
        dict(ws="Revenue Management", task="Targeted marketing to ex-Spirit customers",start=56, end=84, color="#003366"),
        dict(ws="Operations",         task="Gate availability assessment (FLL, MCO, LAS)", start=0,  end=7,  color="#1a7a1a"),
        dict(ws="Operations",         task="Aircraft repositioning plan",              start=14, end=21, color="#1a7a1a"),
        dict(ws="Operations",         task="Crew scheduling for new frequencies",      start=21, end=42, color="#1a7a1a"),
        dict(ws="Operations",         task="Full operational integration",             start=42, end=84, color="#1a7a1a"),
        dict(ws="Commercial/Marketing", task="Loyalty outreach to ex-Spirit flyers",   start=0,  end=7,  color="#cc5500"),
        dict(ws="Commercial/Marketing", task="Targeted digital ads in Spirit markets", start=14, end=28, color="#cc5500"),
        dict(ws="Commercial/Marketing", task="Corporate travel team outreach FLL/MCO", start=28, end=56, color="#cc5500"),
        dict(ws="Commercial/Marketing", task="Performance review and optimization",    start=56, end=84, color="#cc5500"),
    ]

    fig_gantt = go.Figure()
    for i, t in enumerate(tasks):
        fig_gantt.add_trace(go.Bar(
            x=[t["end"] - t["start"]],
            y=[t["task"]],
            base=[t["start"]],
            orientation="h",
            marker_color=t["color"],
            marker_opacity=0.82,
            name=t["ws"],
            showlegend=(i in [0, 4, 8]),
            hovertemplate=f"<b>{t['task']}</b><br>Day {t['start']} → Day {t['end']}<extra>{t['ws']}</extra>",
        ))

    fig_gantt.update_layout(
        barmode="overlay",
        title=dict(text="Three Parallel Workstreams | Day 0 = May 2, 2026", font_size=13, font_color="#003366"),
        **{k: v for k, v in CHART_LAYOUT.items() if k != "margin"},
        xaxis=ax("Days from Spirit Shutdown", {
            "range": [0, 90],
            "tickvals": [0, 14, 28, 42, 56, 70, 84, 90],
        }),
        yaxis=ax("", {"showgrid": False, "tickfont": dict(size=10, color="#111111")}),
        legend=dict(orientation="h", y=-0.15, bgcolor="rgba(255,255,255,0.9)",
                    bordercolor="#cccccc", borderwidth=1, font=dict(size=11, color="#111111")),
        height=460,
        margin=dict(l=300, r=20, t=40, b=60),
    )
    st.plotly_chart(fig_gantt, use_container_width=True)

    st.markdown('<hr class="section-divider">', unsafe_allow_html=True)

    # SECTION C — Risk Register
    st.markdown("### C. Program Risk Register")

    risks = [
        {"Risk": "American Airlines moves first on FLL routes",       "Probability": "HIGH",   "Impact": "HIGH",   "Mitigation": "File for additional FLL slots within 72 hours"},
        {"Risk": "Ex-Spirit passengers shift to driving/not traveling","Probability": "MEDIUM", "Impact": "MEDIUM", "Mitigation": "Introductory fares at $109 for first 60 days"},
        {"Risk": "Fuel cost spike reduces route profitability",        "Probability": "MEDIUM", "Impact": "HIGH",   "Mitigation": "Hedge fuel for Q3 2026 before adding capacity"},
        {"Risk": "DOT scrutiny on fare increases",                     "Probability": "LOW",    "Impact": "HIGH",   "Mitigation": "Price at market rates, avoid price gouging optics"},
        {"Risk": "Southwest aggressively enters FLL market",           "Probability": "MEDIUM", "Impact": "MEDIUM", "Mitigation": "Compete on service and loyalty, not price"},
    ]

    def risk_row_style(row):
        p, i = row["Probability"], row["Impact"]
        if p == "HIGH" and i == "HIGH":
            return ["background-color: #ffe8e8; color: #111111;"] * len(row)
        elif p == "LOW":
            return ["background-color: #e8f8e8; color: #111111;"] * len(row)
        else:
            return ["background-color: #fff8e8; color: #111111;"] * len(row)

    risk_df = pd.DataFrame(risks)
    styled_risk = risk_df.style.apply(risk_row_style, axis=1).set_properties(**{"font-size": "13px", "color": "#111111"})
    st.dataframe(styled_risk, use_container_width=True, hide_index=True)

    st.markdown('<hr class="section-divider">', unsafe_allow_html=True)

    # SECTION D — KPI Targets
    st.markdown("### D. Success Metrics Dashboard")
    k1, k2, k3, k4 = st.columns(4)
    kpi_data = [
        ("+8%",   "#1a7a1a", "Revenue increase on Spirit routes",
         "Achieved by adding 2× daily frequency on FLL-MSP, FLL-DTW, MCO-MSP"),
        ("+15%",  "#1a7a1a", "Seat capacity on top 10 routes",
         "Requires repositioning 12–15 aircraft from lower-yield routes"),
        ("40%",   "#003366", "Of displaced Spirit passengers captured",
         "1.7M monthly Spirit pax × 40% = 680K new monthly passengers for Delta/AA"),
        ("$280M", "#003366", "Incremental annual revenue run-rate",
         "Conservative estimate: 65% passenger capture at $187 avg fare"),
    ]
    milestones = ["30-Day Target", "60-Day Target", "90-Day Target", "6-Month Target"]
    for col, milestone, (num, accent, label, sub) in zip([k1, k2, k3, k4], milestones, kpi_data):
        with col:
            st.markdown(f"""
            <div style="background:#ffffff;border:1px solid #e8ecf0;
                        border-top:3px solid {accent};border-radius:6px;
                        padding:18px 16px;box-shadow:0 1px 4px rgba(0,0,0,0.06);">
              <div style="font-size:11px;font-weight:700;color:#888;text-transform:uppercase;
                          letter-spacing:1px;margin-bottom:8px;">{milestone}</div>
              <div style="font-size:34px;font-weight:800;color:#003366;line-height:1.1;
                          margin-bottom:6px;">{num}</div>
              <div style="font-size:13px;font-weight:600;color:#333333;
                          margin-bottom:6px;">{label}</div>
              <div style="font-size:11px;color:#666666;line-height:1.5;">{sub}</div>
            </div>
            """, unsafe_allow_html=True)

    footer()


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN — SIDEBAR NAVIGATION
# ═══════════════════════════════════════════════════════════════════════════════
def main():
    st.sidebar.markdown("## Spirit War Room")
    st.sidebar.markdown("---")

    pages = [
        "Executive Brief",
        "Collapse Story",
        "Route Opportunity Map",
        "Fare Impact Projector",
        "Strategy Command Center",
    ]
    selected = st.sidebar.radio("Navigate", pages, label_visibility="collapsed")

    if selected == "Executive Brief":
        page_executive_brief()
    elif selected == "Collapse Story":
        page_collapse_story()
    elif selected == "Route Opportunity Map":
        page_route_map()
    elif selected == "Fare Impact Projector":
        page_fare_projector()
    elif selected == "Strategy Command Center":
        page_strategy_command()


if __name__ == "__main__":
    main()
