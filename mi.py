import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Mumbai Indians Dashboard",
    page_icon="🏏",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─────────────────────────────────────────────
# THEME CONSTANTS
# ─────────────────────────────────────────────
MI_BLUE   = "#004BA0"
MI_GOLD   = "#D4AF37"
MI_DARK   = "#002D6B"
MI_LIGHT  = "#E8F0FC"
TITLE_YEARS = {"2013", "2015", "2017", "2019", "2020"}

# ─────────────────────────────────────────────
# CUSTOM CSS
# ─────────────────────────────────────────────
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=DM+Sans:wght@400;500;600&display=swap');

html, body, [class*="css"] {{
    font-family: 'DM Sans', sans-serif;
}}

/* Hide default Streamlit header/footer */
#MainMenu, footer, header {{ visibility: hidden; }}

/* Main background */
.stApp {{ background: #f0f3fa; }}

/* Metric cards */
[data-testid="metric-container"] {{
    background: white;
    border: 0.5px solid rgba(0,0,0,0.08);
    border-radius: 12px;
    padding: 1rem !important;
    box-shadow: 0 1px 4px rgba(0,75,160,0.06);
}}
[data-testid="metric-container"] label {{
    font-size: 11px !important;
    text-transform: uppercase;
    letter-spacing: 0.6px;
    color: #6b7280 !important;
}}
[data-testid="metric-container"] [data-testid="stMetricValue"] {{
    font-family: 'Bebas Neue', sans-serif !important;
    font-size: 2rem !important;
    color: {MI_BLUE} !important;
}}

/* Tab styling */
[data-baseweb="tab-list"] {{
    gap: 6px;
    background: transparent !important;
    border-bottom: none !important;
}}
[data-baseweb="tab"] {{
    border-radius: 22px !important;
    border: 1.5px solid #d1d5db !important;
    padding: 6px 20px !important;
    font-size: 13px !important;
    font-weight: 500 !important;
    background: white !important;
    color: #6b7280 !important;
}}
[aria-selected="true"][data-baseweb="tab"] {{
    background: {MI_BLUE} !important;
    color: white !important;
    border-color: {MI_BLUE} !important;
}}
[data-baseweb="tab-highlight"] {{ display: none !important; }}
[data-baseweb="tab-border"]    {{ display: none !important; }}

/* Section titles */
.section-title {{
    font-family: 'Bebas Neue', sans-serif;
    font-size: 22px;
    color: #1a1a2e;
    letter-spacing: 0.5px;
    margin: 0.5rem 0 0.75rem;
}}

/* Player cards */
.player-card {{
    background: white;
    border: 0.5px solid rgba(0,0,0,0.08);
    border-radius: 12px;
    padding: 1rem;
    position: relative;
    overflow: hidden;
    height: 100%;
}}
.player-card::before {{
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 4px;
    background: {MI_GOLD};
}}
.player-badge {{
    width: 44px; height: 44px;
    border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-family: 'Bebas Neue', sans-serif;
    font-size: 15px;
    margin-bottom: 8px;
}}
.badge-bat  {{ background: #E8F0FC; color: {MI_BLUE}; }}
.badge-bowl {{ background: #FFF3E0; color: #E65100; }}
.badge-all  {{ background: #E8F5E9; color: #2E7D32; }}
.player-name {{ font-size: 14px; font-weight: 600; color: #1a1a2e; margin-bottom: 2px; }}
.player-role {{ font-size: 11px; color: #6b7280; margin-bottom: 10px; }}
.stat-row   {{ display: flex; gap: 14px; }}
.stat-val   {{ font-size: 17px; font-weight: 600; color: {MI_BLUE}; }}
.stat-key   {{ font-size: 10px; color: #6b7280; text-transform: uppercase; }}

/* Venue bars */
.venue-row {{
    display: flex; align-items: center; gap: 12px;
    margin-bottom: 10px;
}}
.venue-name {{ font-size: 13px; color: #1a1a2e; width: 185px; flex-shrink: 0; }}
.venue-bar-wrap {{ flex: 1; background: #f0f3fa; border-radius: 4px; height: 22px; overflow: hidden; }}
.venue-bar {{ height: 100%; border-radius: 4px; display: flex; align-items: center; padding-left: 8px; }}
.venue-bar span {{ font-size: 11px; font-weight: 600; color: white; white-space: nowrap; }}
.venue-stat {{ font-size: 12px; color: #6b7280; width: 50px; text-align: right; flex-shrink: 0; }}

/* Rival cards */
.rival-card {{
    background: white;
    border: 0.5px solid rgba(0,0,0,0.08);
    border-radius: 10px;
    padding: 1rem;
    margin-bottom: 8px;
}}
.rival-name {{ font-size: 14px; font-weight: 600; color: #1a1a2e; margin-bottom: 8px; }}
.rival-bar-wrap {{ display: flex; border-radius: 4px; overflow: hidden; height: 8px; margin-bottom: 6px; }}
.rival-labels {{ display: flex; justify-content: space-between; font-size: 11px; color: #6b7280; }}

/* Key player rows */
.kp-row {{
    display: flex; align-items: center; gap: 12px;
    background: white;
    border: 0.5px solid rgba(0,0,0,0.08);
    border-radius: 10px;
    padding: 0.75rem 1rem;
    margin-bottom: 8px;
}}
.kp-num {{ font-family: 'Bebas Neue', sans-serif; font-size: 26px; color: {MI_GOLD}; width: 30px; text-align: center; }}
.kp-name {{ font-size: 14px; font-weight: 600; color: #1a1a2e; }}
.kp-desc {{ font-size: 12px; color: #6b7280; }}
.kp-tag {{ font-size: 11px; padding: 3px 11px; border-radius: 12px; font-weight: 500; white-space: nowrap; }}
.kp-bat  {{ background: #E8F0FC; color: {MI_BLUE}; }}
.kp-bowl {{ background: #FFF3E0; color: #E65100; }}
.kp-all  {{ background: #E8F5E9; color: #2E7D32; }}

/* Chart containers */
.chart-box {{
    background: white;
    border: 0.5px solid rgba(0,0,0,0.08);
    border-radius: 12px;
    padding: 1.25rem;
    margin-bottom: 1rem;
}}
.chart-box-title {{
    font-size: 12px;
    font-weight: 500;
    color: #6b7280;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    margin-bottom: 0.5rem;
}}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# DATA
# ─────────────────────────────────────────────
SEASONS = [
    ("2008",7),("2009",6),("2010",8),("2011",6),("2012",10),
    ("2013",12),("2014",7),("2015",12),("2016",8),("2017",10),
    ("2018",6),("2019",9),("2020",9),("2021",12),("2022",5),
    ("2023",8),("2024",7),
]

BATTERS = [
    {"initials":"RS",  "name":"Rohit Sharma",    "role":"Right-hand Bat · Captain","badge":"bat","runs":5611,"avg":45.3,"stat3":4,   "s3l":"100s"},
    {"initials":"SRT", "name":"Sachin Tendulkar", "role":"Right-hand Bat",          "badge":"bat","runs":2334,"avg":34.8,"stat3":1,   "s3l":"100s"},
    {"initials":"SR",  "name":"Suryakumar Yadav", "role":"Right-hand Bat",          "badge":"bat","runs":2644,"avg":31.9,"stat3":148, "s3l":"SR"},
    {"initials":"KP",  "name":"Kieron Pollard",   "role":"All-rounder",             "badge":"all","runs":3412,"avg":27.5,"stat3":191, "s3l":"SR"},
]
BOWLERS = [
    {"initials":"LB","name":"Lasith Malinga",  "role":"Right-arm Fast","badge":"bowl","wkts":170,"eco":7.14,"avg":17.0},
    {"initials":"JB","name":"Jasprit Bumrah",  "role":"Right-arm Fast","badge":"bowl","wkts":145,"eco":7.39,"avg":21.7},
    {"initials":"HH","name":"Harbhajan Singh", "role":"Off-spin",       "badge":"bowl","wkts":127,"eco":6.97,"avg":24.6},
    {"initials":"HP","name":"Hardik Pandya",   "role":"All-rounder",    "badge":"all", "wkts":42, "eco":8.89,"avg":None,"extra_label":"Runs","extra_val":1476},
]
TOP_SCORERS = [
    ("Rohit Sharma",5611),("K Pollard",3412),("SKY",2644),
    ("R Agarwal",2400),("Tendulkar",2334),("JP Duminy",2000),
]
VENUES = [
    {"name":"Wankhede Stadium",    "wins":52,"total":70,"home":True},
    {"name":"DY Patil Stadium",    "wins":14,"total":18,"home":True},
    {"name":"Eden Gardens",        "wins":12,"total":19,"home":False},
    {"name":"Chinnaswamy Stadium", "wins":11,"total":17,"home":False},
    {"name":"Chepauk Stadium",     "wins":9, "total":17,"home":False},
    {"name":"Arun Jaitley Stadium","wins":10,"total":16,"home":False},
    {"name":"Sawai Mansingh",      "wins":8, "total":14,"home":False},
]
WANKHEDE = {
    "labels":["2010","2012","2013","2015","2017","2019","2020","2021","2022","2023"],
    "data":  [60,67,80,78,72,75,71,82,60,74],
}
RIVALS = [
    {"name":"Chennai Super Kings",   "short":"CSK", "wins":18,"losses":15},
    {"name":"Kolkata Knight Riders", "short":"KKR", "wins":20,"losses":12},
    {"name":"Royal Challengers",     "short":"RCB", "wins":19,"losses":11},
    {"name":"Delhi Capitals",        "short":"DC",  "wins":18,"losses":13},
    {"name":"Rajasthan Royals",      "short":"RR",  "wins":17,"losses":11},
    {"name":"Sunrisers Hyderabad",   "short":"SRH", "wins":16,"losses":10},
    {"name":"Punjab Kings",          "short":"PBKS","wins":18,"losses":10},
    {"name":"Gujarat Titans",        "short":"GT",  "wins":5, "losses":6},
]
KEY_PLAYERS = [
    (1,"Rohit Sharma",    "5611 runs · Most runs for MI · 4 centuries · Captain for 5 title wins","bat"),
    (2,"Lasith Malinga",  "170 wickets · All-time leading wicket-taker · 4 hat-tricks in IPL",   "bowl"),
    (3,"Kieron Pollard",  "3412 runs + crucial wickets · Finisher extraordinaire · 13 seasons",  "all"),
    (4,"Jasprit Bumrah",  "145 wickets · Best death bowler in IPL history · 7.39 economy",       "bowl"),
    (5,"Suryakumar Yadav","2644 runs · SR 148 · T20 World No.1 batsman · MI's modern anchor",   "bat"),
    (6,"Sachin Tendulkar","2334 runs · MI's iconic figure · First owner-player in IPL history",  "bat"),
    (7,"Hardik Pandya",   "1476 runs + 42 wickets · Match-winning all-rounder in title years",   "all"),
]
RADAR = {
    "labels":["Runs","Wickets","Strike Rate","Economy","Consistency","Match Wins"],
    "datasets":[
        {"label":"Rohit Sharma","data":[95,40,72,50,90,98],"color":MI_BLUE},
        {"label":"Malinga",     "data":[20,98,30,85,88,95],"color":MI_GOLD},
        {"label":"Bumrah",      "data":[15,90,25,92,85,90],"color":"#E65100"},
    ],
}

# ─────────────────────────────────────────────
# PLOTLY HELPERS
# ─────────────────────────────────────────────
PLOTLY_LAYOUT = dict(
    paper_bgcolor="white",
    plot_bgcolor="white",
    font=dict(family="DM Sans, sans-serif", color="#1a1a2e"),
    margin=dict(l=10, r=10, t=30, b=10),
    showlegend=False,
)

def season_bar_chart():
    years  = [y for y, _ in SEASONS]
    wins   = [w for _, w in SEASONS]
    colors = [MI_GOLD if y in TITLE_YEARS else MI_BLUE for y in years]
    labels = [f"{y} 🏆" if y in TITLE_YEARS else y for y in years]

    fig = go.Figure(go.Bar(
        x=labels, y=wins,
        marker_color=colors,
        marker_line_color=[("#B8960C" if y in TITLE_YEARS else "#003580") for y in years],
        marker_line_width=1,
        text=wins, textposition="outside",
        textfont=dict(size=11, color="#6b7280"),
    ))
    fig.update_layout(
        **PLOTLY_LAYOUT,
        xaxis=dict(tickfont=dict(size=11), gridcolor="rgba(0,0,0,0)"),
        yaxis=dict(gridcolor="rgba(0,0,0,0.05)", zeroline=False),
        bargap=0.35,
        height=300,
    )
    return fig

def donut_chart():
    fig = go.Figure(go.Pie(
        labels=["Home","Away","Neutral","Playoffs"],
        values=[63, 52, 55, 68],
        hole=0.65,
        marker_colors=[MI_BLUE,"#378ADD",MI_GOLD,"#BA7517"],
        textinfo="label+percent",
        textfont=dict(size=12),
    ))
    fig.update_layout(**PLOTLY_LAYOUT, height=280)
    return fig

def top_scorers_chart():
    names = [n for n, _ in TOP_SCORERS]
    runs  = [r for _, r in TOP_SCORERS]
    colors = [MI_BLUE,"#378ADD",MI_BLUE,"#378ADD",MI_BLUE,"#378ADD"]
    fig = go.Figure(go.Bar(
        y=names, x=runs,
        orientation="h",
        marker_color=colors,
        text=runs, textposition="outside",
        textfont=dict(size=11, color="#6b7280"),
    ))
    fig.update_layout(
        **PLOTLY_LAYOUT,
        xaxis=dict(gridcolor="rgba(0,0,0,0.05)"),
        yaxis=dict(gridcolor="rgba(0,0,0,0)"),
        height=280,
    )
    return fig

def wankhede_chart():
    fig = go.Figure(go.Scatter(
        x=WANKHEDE["labels"], y=WANKHEDE["data"],
        mode="lines+markers",
        line=dict(color=MI_BLUE, width=2.5),
        fill="tozeroy",
        fillcolor="rgba(0,75,160,0.07)",
        marker=dict(size=7, color=MI_GOLD, line=dict(width=1.5, color=MI_BLUE)),
    ))
    fig.update_layout(
        **PLOTLY_LAYOUT,
        yaxis=dict(range=[50,100], ticksuffix="%", gridcolor="rgba(0,0,0,0.05)"),
        xaxis=dict(gridcolor="rgba(0,0,0,0)"),
        height=240,
    )
    return fig

def rivals_bar_chart():
    shorts = [r["short"] for r in RIVALS]
    wins   = [r["wins"]   for r in RIVALS]
    losses = [r["losses"] for r in RIVALS]
    fig = go.Figure()
    fig.add_trace(go.Bar(name="Wins",   x=shorts, y=wins,   marker_color=MI_BLUE,  text=wins,   textposition="outside", textfont=dict(size=10)))
    fig.add_trace(go.Bar(name="Losses", x=shorts, y=losses, marker_color="#E0E0E0", text=losses, textposition="outside", textfont=dict(size=10, color="#6b7280")))
    fig.update_layout(
        **PLOTLY_LAYOUT,
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1, font=dict(size=11)),
        barmode="group", bargap=0.25,
        xaxis=dict(gridcolor="rgba(0,0,0,0)"),
        yaxis=dict(gridcolor="rgba(0,0,0,0.05)"),
        height=300,
    )
    return fig

def radar_chart():
    categories = RADAR["labels"] + [RADAR["labels"][0]]  # close the loop
    fig = go.Figure()
    for ds in RADAR["datasets"]:
        vals = ds["data"] + [ds["data"][0]]
        fig.add_trace(go.Scatterpolar(
            r=vals, theta=categories,
            fill="toself",
            name=ds["label"],
            line=dict(color=ds["color"], width=2),
            fillcolor=ds["color"] + "18",
            marker=dict(color=ds["color"], size=5),
        ))
    fig.update_layout(
        **PLOTLY_LAYOUT,
        showlegend=True,
        polar=dict(
            radialaxis=dict(visible=False, range=[0,100]),
            angularaxis=dict(tickfont=dict(size=11)),
            bgcolor="white",
        ),
        legend=dict(orientation="h", yanchor="bottom", y=-0.15, xanchor="center", x=0.5, font=dict(size=11)),
        height=320,
    )
    return fig

# ─────────────────────────────────────────────
# HTML COMPONENT BUILDERS
# ─────────────────────────────────────────────
def player_card_html(p: dict, mode: str = "bat") -> str:
    badge_cls = f"badge-{p['badge']}"
    if mode == "bat":
        stats = f"""
        <div class="stat-row">
          <div><div class="stat-val">{p['runs']}</div><div class="stat-key">Runs</div></div>
          <div><div class="stat-val">{p['avg']}</div><div class="stat-key">Avg</div></div>
          <div><div class="stat-val">{p['stat3']}</div><div class="stat-key">{p['s3l']}</div></div>
        </div>"""
    else:
        third = f'<div><div class="stat-val">{p.get("extra_val","")}</div><div class="stat-key">{p.get("extra_label","Avg")}</div></div>' if p.get("extra_label") else f'<div><div class="stat-val">{p["avg"]}</div><div class="stat-key">Avg</div></div>'
        stats = f"""
        <div class="stat-row">
          <div><div class="stat-val">{p['wkts']}</div><div class="stat-key">Wkts</div></div>
          <div><div class="stat-val">{p['eco']}</div><div class="stat-key">Eco</div></div>
          {third}
        </div>"""
    return f"""
    <div class="player-card">
      <div class="player-badge {badge_cls}">{p['initials']}</div>
      <div class="player-name">{p['name']}</div>
      <div class="player-role">{p['role']}</div>
      {stats}
    </div>"""

def venue_bars_html() -> str:
    rows = []
    for v in VENUES:
        pct = round(v["wins"] / v["total"] * 100)
        col = MI_BLUE if v["home"] else "#378ADD"
        badge = f' <span style="font-size:10px;color:{MI_GOLD};font-weight:600;">HOME</span>' if v["home"] else ""
        rows.append(f"""<div class="venue-row">
          <div class="venue-name">{v['name']}{badge}</div>
          <div class="venue-bar-wrap"><div class="venue-bar" style="width:{pct}%;background:{col};"><span>{pct}%</span></div></div>
          <div class="venue-stat">{v['wins']}/{v['total']}</div>
        </div>""")
    return "".join(rows)

def rival_cards_html() -> str:
    cards = []
    for r in RIVALS:
        total = r["wins"] + r["losses"]
        wpct  = round(r["wins"] / total * 100)
        cards.append(f"""<div class="rival-card">
          <div class="rival-name">{r['name']}</div>
          <div class="rival-bar-wrap">
            <div style="width:{wpct}%;background:{MI_BLUE};height:8px;"></div>
            <div style="width:{100-wpct}%;background:#E0E0E0;height:8px;"></div>
          </div>
          <div class="rival-labels">
            <span style="font-weight:600;color:{MI_BLUE};">{r['wins']}W / {r['losses']}L</span>
            <span>{wpct}%</span>
          </div>
        </div>""")
    return "".join(cards)

def kp_rows_html() -> str:
    tag_map = {"bat":("Batsman","kp-bat"),"bowl":("Bowler","kp-bowl"),"all":("All-rounder","kp-all")}
    rows = []
    for num, name, desc, kind in KEY_PLAYERS:
        label, cls = tag_map[kind]
        rows.append(f"""<div class="kp-row">
          <div class="kp-num">{num}</div>
          <div style="flex:1">
            <div class="kp-name">{name}</div>
            <div class="kp-desc">{desc}</div>
          </div>
          <div class="kp-tag {cls}">{label}</div>
        </div>""")
    return "".join(rows)

# ─────────────────────────────────────────────
# HEADER
# ─────────────────────────────────────────────
st.markdown(f"""
<div style="
  background:{MI_BLUE};
  border-radius:14px;
  padding:1.75rem 2rem;
  display:flex;
  align-items:center;
  gap:1.5rem;
  margin-bottom:1.5rem;
  position:relative;
  overflow:hidden;
">
  <div style="
    position:absolute;right:-40px;top:-40px;
    width:200px;height:200px;border-radius:50%;
    border:35px solid rgba(212,175,55,0.15);
  "></div>
  <div style="
    width:78px;height:78px;border-radius:50%;
    background:{MI_GOLD};
    display:flex;align-items:center;justify-content:center;
    font-family:'Bebas Neue',sans-serif;font-size:32px;
    color:{MI_DARK};flex-shrink:0;
  ">MI</div>
  <div>
    <div style="font-family:'Bebas Neue',sans-serif;font-size:36px;color:white;letter-spacing:1px;line-height:1;">
      Mumbai Indians
    </div>
    <div style="font-size:13px;color:rgba(255,255,255,0.65);margin-top:4px;">
      IPL Stats Dashboard &nbsp;·&nbsp; All-time record
    </div>
  </div>
  <div style="margin-left:auto;text-align:right;">
    <div style="font-family:'Bebas Neue',sans-serif;font-size:56px;color:{MI_GOLD};line-height:1;">5</div>
    <div style="font-size:11px;color:rgba(255,255,255,0.55);text-transform:uppercase;letter-spacing:1px;">IPL Titles</div>
  </div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# TABS
# ─────────────────────────────────────────────
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 Overview", "🏏 Player Stats", "🏟️ Venue Wins", "⚔️ H2H Records", "⭐ Key Players"
])

# ══════════════════════════════════════════════
# TAB 1 — OVERVIEW
# ══════════════════════════════════════════════
with tab1:
    c1, c2, c3, c4, c5, c6 = st.columns(6)
    c1.metric("Matches Played", "253")
    c2.metric("Wins", "145")
    c3.metric("Win Rate", "57%")
    c4.metric("Titles Won", "5")
    c5.metric("Finals Played", "8")
    c6.metric("First Title", "2013")

    st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)

    st.markdown(f"""
    <div class="chart-box">
      <div class="chart-box-title">Season-by-season win count</div>
      <div style="display:flex;gap:16px;margin-bottom:8px;font-size:12px;color:#6b7280;">
        <span style="display:flex;align-items:center;gap:5px;">
          <span style="width:10px;height:10px;border-radius:2px;background:{MI_GOLD};display:inline-block;"></span>
          Title-winning season
        </span>
        <span style="display:flex;align-items:center;gap:5px;">
          <span style="width:10px;height:10px;border-radius:2px;background:{MI_BLUE};display:inline-block;"></span>
          Regular season
        </span>
      </div>
    """, unsafe_allow_html=True)
    st.plotly_chart(season_bar_chart(), use_container_width=True, config={"displayModeBar": False})
    st.markdown("</div>", unsafe_allow_html=True)

    col_a, col_b = st.columns([1, 1])
    with col_a:
        st.markdown('<div class="chart-box"><div class="chart-box-title">Win % by match type</div>', unsafe_allow_html=True)
        st.plotly_chart(donut_chart(), use_container_width=True, config={"displayModeBar": False})
        st.markdown("</div>", unsafe_allow_html=True)
    with col_b:
        st.markdown(f"""
        <div class="chart-box" style="height:100%;">
          <div class="chart-box-title">Quick facts</div>
          <div style="display:flex;flex-direction:column;gap:12px;margin-top:1rem;">
            {"".join([f'''
            <div style="display:flex;justify-content:space-between;align-items:center;
                        border-bottom:0.5px solid rgba(0,0,0,0.06);padding-bottom:10px;">
              <span style="font-size:13px;color:#6b7280;">{label}</span>
              <span style="font-size:14px;font-weight:600;color:{MI_BLUE};">{val}</span>
            </div>''' for label, val in [
                ("Home win %","63%"), ("Away win %","52%"),
                ("Playoff win %","68%"), ("Highest season wins","12 (2013, 2015, 2021)"),
                ("Longest winning streak","9 matches"), ("Most titles","5 (joint record)"),
            ]])}
          </div>
        </div>
        """, unsafe_allow_html=True)

# ══════════════════════════════════════════════
# TAB 2 — PLAYER STATS
# ══════════════════════════════════════════════
with tab2:
    st.markdown('<div class="section-title">Batting Legends</div>', unsafe_allow_html=True)
    bcols = st.columns(4)
    for i, b in enumerate(BATTERS):
        with bcols[i]:
            st.markdown(player_card_html(b, "bat"), unsafe_allow_html=True)

    st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)
    st.markdown('<div class="section-title">Bowling Attack</div>', unsafe_allow_html=True)
    wcols = st.columns(4)
    for i, b in enumerate(BOWLERS):
        with wcols[i]:
            st.markdown(player_card_html(b, "bowl"), unsafe_allow_html=True)

    st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)
    st.markdown('<div class="chart-box"><div class="chart-box-title">Top run-scorers for MI (IPL career)</div>', unsafe_allow_html=True)
    st.plotly_chart(top_scorers_chart(), use_container_width=True, config={"displayModeBar": False})
    st.markdown("</div>", unsafe_allow_html=True)

# ══════════════════════════════════════════════
# TAB 3 — VENUE WINS
# ══════════════════════════════════════════════
with tab3:
    v1, v2, v3, v4 = st.columns(4)
    v1.metric("Home Win %", "74%")
    v2.metric("Away Win %", "58%")
    v3.metric("Best Away Venue", "DY Patil")
    v4.metric("Home Ground", "Wankhede")

    st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)
    st.markdown(f'<div class="chart-box"><div class="chart-box-title">Win record at each venue</div>{venue_bars_html()}</div>', unsafe_allow_html=True)

    st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)
    st.markdown('<div class="chart-box"><div class="chart-box-title">Win % trend — Wankhede Stadium (season-wise)</div>', unsafe_allow_html=True)
    st.plotly_chart(wankhede_chart(), use_container_width=True, config={"displayModeBar": False})
    st.markdown("</div>", unsafe_allow_html=True)

# ══════════════════════════════════════════════
# TAB 4 — H2H RECORDS
# ══════════════════════════════════════════════
with tab4:
    r1, r2, r3, r4 = st.columns(4)
    r1.metric("Biggest Rivalry", "CSK")
    r2.metric("vs CSK Matches", "33")
    r3.metric("vs CSK Wins", "18")
    r4.metric("vs CSK Win %", "55%")

    st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)

    rc1, rc2 = st.columns([1, 1])
    with rc1:
        st.markdown(f'<div class="chart-box"><div class="chart-box-title">Win ratio vs each team</div>{rival_cards_html()}</div>', unsafe_allow_html=True)
    with rc2:
        st.markdown('<div class="chart-box"><div class="chart-box-title">Wins vs losses by team</div>', unsafe_allow_html=True)
        st.plotly_chart(rivals_bar_chart(), use_container_width=True, config={"displayModeBar": False})
        st.markdown("</div>", unsafe_allow_html=True)

# ══════════════════════════════════════════════
# TAB 5 — KEY PLAYERS
# ══════════════════════════════════════════════
with tab5:
    kp_col, radar_col = st.columns([1, 1])

    with kp_col:
        st.markdown('<div class="section-title">All-time Impact XI</div>', unsafe_allow_html=True)
        st.markdown(kp_rows_html(), unsafe_allow_html=True)

    with radar_col:
        st.markdown('<div class="chart-box"><div class="chart-box-title">Impact score — key players (composite)</div>', unsafe_allow_html=True)
        st.plotly_chart(radar_chart(), use_container_width=True, config={"displayModeBar": False})
        st.markdown("</div>", unsafe_allow_html=True)