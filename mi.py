import base64
import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from pathlib import Path

#Page configuration
st.set_page_config(page_title="Mumbai Indians Dashboard", page_icon="🏏", layout="wide")

# Colours
BLUE  = "#004BA0"
GOLD  = "#D4AF37"
DARK  = "#002D6B"
LIGHT = "#E8F0FC"
TITLE_YEARS = {"2013", "2015", "2017", "2019", "2020"}

#LOGOs
TEAM_LOGOS = {
    "MI":   "assets/logos/mi.svg",
    "CSK":  "assets/logos/csk.svg",
    "KKR":  "assets/logos/kkr.svg",
    "RCB":  "assets/logos/rcb.svg",
    "DC":   "assets/logos/dc.svg",
    "RR":   "assets/logos/rr.svg",
    "SRH":  "assets/logos/srh.svg",
    "PBKS": "assets/logos/pbks.svg",
    "GT":   "assets/logos/gt.svg",
}

PLAYER_PHOTOS = {
    "Rohit Sharma":     "assets/players/rohit.png",
    "Sachin Tendulkar": "assets/players/tendulkar.png",
    "Suryakumar Yadav": "assets/players/surya.png",
    "Kieron Pollard":   "assets/players/pollard.png",
    "Lasith Malinga":   "assets/players/malinga.png",
    "Jasprit Bumrah":   "assets/players/bumrah.png",
    "Harbhajan Singh":  "assets/players/harbhajan.png",
    "Hardik Pandya":    "assets/players/hardik.png",
}

# img
def img_to_b64(path: str) -> str:
    p = Path(path)
    raw = p.read_bytes()
    b64 = base64.b64encode(raw).decode()
    mime = "image/svg+xml" if p.suffix == ".svg" else "image/png"
    return f"data:{mime};base64,{b64}"

def player_avatar(name: str, badge_color: str = BLUE) -> str:
    path = PLAYER_PHOTOS.get(name, "")
    if path and Path(path).exists():
        src = img_to_b64(path)
        return (
            f'<img src="{src}" style="width:48px;height:48px;border-radius:50%;'
            f'object-fit:cover;border:2px solid {GOLD};flex-shrink:0;">'
        )
    initials = "".join(w[0] for w in name.split()[:2]).upper()
    return (
        f'<div style="width:48px;height:48px;border-radius:50%;flex-shrink:0;'
        f'background:{LIGHT};display:flex;align-items:center;justify-content:center;'
        f'font-family:Bebas Neue,sans-serif;font-size:15px;color:{badge_color};">'
        f'{initials}</div>'
    )

def logo_tag(team: str, size: int = 32) -> str:
    path = TEAM_LOGOS.get(team, "")
    if path and Path(path).exists():
        src = img_to_b64(path)
        return f'<img src="{src}" style="width:{size}px;height:{size}px;object-fit:contain;vertical-align:middle;">'
    return f'<span style="font-size:11px;font-weight:600;color:{BLUE};">{team}</span>'

def mi_header_logo() -> str:
    path = TEAM_LOGOS.get("MI", "")
    if path and Path(path).exists():
        src = img_to_b64(path)
        return f'<img src="{src}" style="width:68px;height:68px;object-fit:contain;">'
    return f'<span style="font-family:Bebas Neue,sans-serif;font-size:30px;color:{DARK};">MI</span>'

# plotly
def hex_to_rgba(hex_color: str, alpha: float = 0.09) -> str:
    h = hex_color.lstrip("#")
    r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    return f"rgba({r},{g},{b},{alpha})"

BASE = dict(
    paper_bgcolor="white",
    plot_bgcolor="white",
    font=dict(family="DM Sans, sans-serif", color="rgb(26,26,46)"),
    margin=dict(l=10, r=10, t=30, b=10),
)

# input
SEASONS = [
    ("2008",7),("2009",6),("2010",8),("2011",6),("2012",10),
    ("2013",12),("2014",7),("2015",12),("2016",8),("2017",10),
    ("2018",6),("2019",9),("2020",9),("2021",12),("2022",5),
    ("2023",8),("2024",7),
]

BATTERS = pd.DataFrame([
    {"Name":"Rohit Sharma",    "Role":"Batsman · Captain", "Runs":5611,"Avg":45.3,"Stat3":4,   "S3L":"100s"},
    {"Name":"Sachin Tendulkar","Role":"Batsman",            "Runs":2334,"Avg":34.8,"Stat3":1,   "S3L":"100s"},
    {"Name":"Suryakumar Yadav","Role":"Batsman",            "Runs":2644,"Avg":31.9,"Stat3":148, "S3L":"SR"},
    {"Name":"Kieron Pollard",  "Role":"All-rounder",        "Runs":3412,"Avg":27.5,"Stat3":191, "S3L":"SR"},
])

BOWLERS = pd.DataFrame([
    {"Name":"Lasith Malinga", "Role":"Right-arm Fast","Wkts":170,"Eco":7.14,"Avg":"17.0"},
    {"Name":"Jasprit Bumrah", "Role":"Right-arm Fast","Wkts":145,"Eco":7.39,"Avg":"21.7"},
    {"Name":"Harbhajan Singh","Role":"Off-spin",      "Wkts":127,"Eco":6.97,"Avg":"24.6"},
    {"Name":"Hardik Pandya",  "Role":"All-rounder",   "Wkts":42, "Eco":8.89,"Avg":"—"},
])

TOP_SCORERS = pd.DataFrame({
    "Player":["Rohit Sharma","K Pollard","SKY","R Agarwal","Tendulkar","JP Duminy"],
    "Runs":  [5611, 3412, 2644, 2400, 2334, 2000],
})

VENUES = pd.DataFrame([
    {"Venue":"Wankhede Stadium",    "Wins":52,"Total":70,"Home":True},
    {"Venue":"DY Patil Stadium",    "Wins":14,"Total":18,"Home":True},
    {"Venue":"Eden Gardens",        "Wins":12,"Total":19,"Home":False},
    {"Venue":"Chinnaswamy Stadium", "Wins":11,"Total":17,"Home":False},
    {"Venue":"Chepauk Stadium",     "Wins":9, "Total":17,"Home":False},
    {"Venue":"Arun Jaitley Stadium","Wins":10,"Total":16,"Home":False},
    {"Venue":"Sawai Mansingh",      "Wins":8, "Total":14,"Home":False},
])
VENUES["WinPct"] = (VENUES["Wins"] / VENUES["Total"] * 100).round(0).astype(int)
VENUES["Label"]  = VENUES.apply(lambda r: f"{r['Venue']} (H)" if r["Home"] else r["Venue"], axis=1)

RIVALS = pd.DataFrame([
    {"Team":"CSK", "Wins":18,"Losses":15},
    {"Team":"KKR", "Wins":20,"Losses":12},
    {"Team":"RCB", "Wins":19,"Losses":11},
    {"Team":"DC",  "Wins":18,"Losses":13},
    {"Team":"RR",  "Wins":17,"Losses":11},
    {"Team":"SRH", "Wins":16,"Losses":10},
    {"Team":"PBKS","Wins":18,"Losses":10},
    {"Team":"GT",  "Wins":5, "Losses":6},
])
RIVALS["WinPct"] = (RIVALS["Wins"] / (RIVALS["Wins"] + RIVALS["Losses"]) * 100).round(0).astype(int)

KEY_PLAYERS = [
    (1,"Rohit Sharma",    "5611 runs · 4 centuries · Captain for all 5 titles","bat"),
    (2,"Lasith Malinga",  "170 wickets · All-time IPL leading wicket-taker",   "bowl"),
    (3,"Kieron Pollard",  "3412 runs + wickets · 13 seasons at MI",            "all"),
    (4,"Jasprit Bumrah",  "145 wickets · Best death bowler in IPL history",    "bowl"),
    (5,"Suryakumar Yadav","2644 runs · SR 148 · T20 World No.1 batsman",      "bat"),
    (6,"Sachin Tendulkar","2334 runs · MI's iconic figure",                    "bat"),
    (7,"Hardik Pandya",   "1476 runs + 42 wickets · Title-winning allrounder", "all"),
]

# bar
def season_chart():
    years  = [y for y, _ in SEASONS]
    wins   = [w for _, w in SEASONS]
    colors = [GOLD if y in TITLE_YEARS else BLUE for y in years]
    ticks  = [f"{y} 🏆" if y in TITLE_YEARS else y for y in years]
    fig = go.Figure(go.Bar(
        x=years, y=wins,
        marker_color=colors,
        marker_line_color=["#B8960C" if y in TITLE_YEARS else "#003580" for y in years],
        marker_line_width=1,
        text=wins, textposition="outside",
        textfont=dict(size=11, color="#6b7280"),
    ))
    fig.update_layout(
        **BASE, bargap=0.35, height=300, showlegend=False,
        xaxis=dict(tickmode="array", tickvals=years, ticktext=ticks,
                   tickfont=dict(size=11), showgrid=False),
        yaxis=dict(gridcolor="rgba(0,0,0,0.05)", zeroline=False),
    )
    return fig

def donut_chart():
    fig = go.Figure(go.Pie(
        labels=["Home","Away","Neutral","Playoffs"],
        values=[63, 52, 55, 68], hole=0.65,
        marker_colors=[BLUE, "#378ADD", GOLD, "#BA7517"],
        textinfo="label+percent", textfont=dict(size=12),
    ))
    fig.update_layout(**BASE, height=280, showlegend=False)
    return fig

def scorers_chart():
    fig = go.Figure(go.Bar(
        y=TOP_SCORERS["Player"], x=TOP_SCORERS["Runs"], orientation="h",
        marker_color=[BLUE,"#378ADD",BLUE,"#378ADD",BLUE,"#378ADD"],
        text=TOP_SCORERS["Runs"], textposition="outside",
        textfont=dict(size=11, color="#6b7280"),
    ))
    fig.update_layout(
        **BASE, height=280, showlegend=False,
        xaxis=dict(gridcolor="rgba(0,0,0,0.05)"),
        yaxis=dict(showgrid=False),
    )
    return fig

def venue_chart():
    fig = go.Figure(go.Bar(
        y=VENUES["Label"], x=VENUES["WinPct"], orientation="h",
        marker_color=[GOLD if h else BLUE for h in VENUES["Home"]],
        text=[f"{w}%" for w in VENUES["WinPct"]], textposition="outside",
        textfont=dict(size=11, color="#6b7280"),
    ))
    fig.update_layout(
        **BASE, height=300, showlegend=False,
        xaxis=dict(range=[0, 105], ticksuffix="%", gridcolor="rgba(0,0,0,0.05)"),
        yaxis=dict(showgrid=False),
    )
    return fig

def wankhede_chart():
    xl = ["2010","2012","2013","2015","2017","2019","2020","2021","2022","2023"]
    yd = [60, 67, 80, 78, 72, 75, 71, 82, 60, 74]
    fig = go.Figure(go.Scatter(
        x=xl, y=yd, mode="lines+markers",
        line=dict(color=BLUE, width=2.5),
        fill="tozeroy", fillcolor="rgba(0,75,160,0.07)",
        marker=dict(size=7, color=GOLD, line=dict(width=1.5, color=BLUE)),
    ))
    fig.update_layout(
        **BASE, height=260,
        yaxis=dict(range=[50, 100], ticksuffix="%", gridcolor="rgba(0,0,0,0.05)"),
        xaxis=dict(showgrid=False),
    )
    return fig

def rivals_chart():
    fig = go.Figure()
    fig.add_trace(go.Bar(
        name="Wins", x=RIVALS["Team"], y=RIVALS["Wins"],
        marker_color=BLUE,
        text=RIVALS["Wins"], textposition="outside", textfont=dict(size=11),
    ))
    fig.add_trace(go.Bar(
        name="Losses", x=RIVALS["Team"], y=RIVALS["Losses"],
        marker_color="#E0E0E0",
        text=RIVALS["Losses"], textposition="outside", textfont=dict(size=11, color="#6b7280"),
    ))
    fig.update_layout(
        **BASE, barmode="group", bargap=0.25, height=300,
        xaxis=dict(showgrid=False),
        yaxis=dict(gridcolor="rgba(0,0,0,0.05)"),
        legend=dict(orientation="h", yanchor="bottom", y=1.02,
                    xanchor="right", x=1, font=dict(size=11)),
    )
    return fig

def radar_chart():
    cats = ["Runs","Wickets","Strike Rate","Economy","Consistency","Match Wins"]
    cc   = cats + [cats[0]]
    datasets = [
        ("Rohit Sharma", [95,40,72,50,90,98], BLUE),
        ("Malinga",      [20,98,30,85,88,95], GOLD),
        ("Bumrah",       [15,90,25,92,85,90], "#E65100"),
    ]
    fig = go.Figure()
    for lbl, vals, col in datasets:
        fig.add_trace(go.Scatterpolar(
            r=vals + [vals[0]], theta=cc,
            fill="toself", name=lbl,
            line=dict(color=col, width=2),
            fillcolor=hex_to_rgba(col, 0.09),
            marker=dict(color=col, size=5),
        ))
    fig.update_layout(
        **BASE, height=320,
        polar=dict(
            radialaxis=dict(visible=False, range=[0,100]),
            angularaxis=dict(tickfont=dict(size=11)),
            bgcolor="white",
        ),
        legend=dict(orientation="h", yanchor="bottom", y=-0.2,
                    xanchor="center", x=0.5, font=dict(size=11)),
    )
    return fig

#  UI 
def chart_card(title: str, fig, key: str):
    st.markdown(
        f'<div style="background:white;border-radius:12px;padding:1.25rem 1.25rem 0.5rem;'
        f'border:1px solid rgba(0,0,0,0.07);margin-bottom:1rem;">'
        f'<div style="font-size:11px;font-weight:500;color:#6b7280;'
        f'text-transform:uppercase;letter-spacing:0.5px;margin-bottom:.5rem;">{title}</div>',
        unsafe_allow_html=True,
    )
    st.plotly_chart(fig, width="stretch", config={"displayModeBar": False}, key=key)
    st.markdown("</div>", unsafe_allow_html=True)

def player_row_html(name: str, role: str, stats: list, badge_color: str = BLUE) -> str:
    avatar     = player_avatar(name, badge_color)
    stats_html = "".join(
        f'<div style="text-align:center;min-width:55px;">'
        f'<div style="font-size:16px;font-weight:600;color:{BLUE};">{v}</div>'
        f'<div style="font-size:10px;color:#6b7280;text-transform:uppercase;">{k}</div>'
        f'</div>'
        for k, v in stats
    )
    return (
        f'<div style="display:flex;align-items:center;gap:14px;background:white;'
        f'border:1px solid rgba(0,0,0,0.07);border-radius:12px;'
        f'padding:.85rem 1rem;border-left:4px solid {GOLD};margin-bottom:8px;">'
        f'{avatar}'
        f'<div style="flex:1;min-width:0;">'
        f'<div style="font-size:14px;font-weight:600;color:#1a1a2e;">{name}</div>'
        f'<div style="font-size:11px;color:#6b7280;">{role}</div>'
        f'</div>'
        f'<div style="display:flex;gap:16px;flex-shrink:0;">{stats_html}</div>'
        f'</div>'
    )

def kp_row_html(num: int, name: str, desc: str, kind: str) -> str:
    colors = {"bat":(LIGHT,BLUE), "bowl":("#FFF3E0","#E65100"), "all":("#E8F5E9","#2E7D32")}
    tags   = {"bat":"Batsman", "bowl":"Bowler", "all":"All-rounder"}
    bg, fg = colors[kind]
    avatar = player_avatar(name, fg)
    return (
        f'<div style="display:flex;align-items:center;gap:12px;background:white;'
        f'border:1px solid rgba(0,0,0,0.07);border-radius:12px;'
        f'padding:.75rem 1rem;margin-bottom:8px;">'
        f'<div style="font-family:Bebas Neue,sans-serif;font-size:22px;'
        f'color:{GOLD};width:24px;text-align:center;flex-shrink:0;">{num}</div>'
        f'{avatar}'
        f'<div style="flex:1;">'
        f'<div style="font-size:14px;font-weight:600;color:#1a1a2e;">{name}</div>'
        f'<div style="font-size:12px;color:#6b7280;">{desc}</div>'
        f'</div>'
        f'<div style="font-size:11px;padding:3px 11px;border-radius:12px;'
        f'background:{bg};color:{fg};font-weight:500;white-space:nowrap;">{tags[kind]}</div>'
        f'</div>'
    )

#  CSS 
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=DM+Sans:wght@400;500;600&display=swap');
html, body, [class*="css"] {{ font-family: 'DM Sans', sans-serif; }}
.stApp {{ background-color: #f0f3fa; }}
#MainMenu, footer, header {{ visibility: hidden; }}
[data-testid="metric-container"] {{
    background: white; border-radius: 12px;
    padding: 1rem; border: 1px solid rgba(0,0,0,0.07);
}}
[data-testid="stMetricValue"] {{
    font-family: 'Bebas Neue', sans-serif !important;
    font-size: 2rem !important; color: {BLUE} !important;
}}
[data-testid="stMetricLabel"] {{
    font-size: 11px !important; text-transform: uppercase;
    letter-spacing: 0.5px; color: #6b7280 !important;
}}
[data-baseweb="tab-list"] {{ background: transparent !important; gap: 6px; }}
[data-baseweb="tab"] {{
    border-radius: 20px !important; border: 1.5px solid #d1d5db !important;
    background: white !important; color: #6b7280 !important; font-weight: 500 !important;
}}
[aria-selected="true"][data-baseweb="tab"] {{
    background: {BLUE} !important; color: white !important; border-color: {BLUE} !important;
}}
[data-baseweb="tab-highlight"], [data-baseweb="tab-border"] {{ display: none !important; }}
.block-container {{ padding-top: 1rem !important; }}
</style>
""", unsafe_allow_html=True)

#  Header 
st.markdown(f"""
<div style="background:{BLUE};border-radius:14px;padding:1.5rem 2rem;
            display:flex;align-items:center;gap:1.5rem;margin-bottom:1.5rem;
            position:relative;overflow:hidden;">
  <div style="position:absolute;right:-40px;top:-40px;width:200px;height:200px;
              border-radius:50%;border:35px solid rgba(212,175,55,0.15);"></div>
  <div style="width:80px;height:80px;border-radius:50%;background:white;flex-shrink:0;
              display:flex;align-items:center;justify-content:center;
              border:3px solid {GOLD};overflow:hidden;padding:4px;">
    {mi_header_logo()}
  </div>
  <div>
    <div style="font-family:'Bebas Neue',sans-serif;font-size:34px;color:white;
                letter-spacing:1px;line-height:1;">Mumbai Indians</div>
    <div style="font-size:13px;color:rgba(255,255,255,0.65);margin-top:4px;">
      IPL Stats Dashboard &nbsp;&middot;&nbsp; All-time record
    </div>
  </div>
  <div style="margin-left:auto;text-align:right;">
    <div style="font-family:'Bebas Neue',sans-serif;font-size:54px;
                color:{GOLD};line-height:1;">5</div>
    <div style="font-size:11px;color:rgba(255,255,255,0.55);
                text-transform:uppercase;letter-spacing:1px;">IPL Titles</div>
  </div>
</div>
""", unsafe_allow_html=True)

#Tabs 
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊  Overview", "🏏  Player Stats", "🏟️  Venue Wins",
    "⚔️  H2H Records", "⭐  Key Players",
])

# TAB1 
with tab1:
    c1, c2, c3, c4, c5, c6 = st.columns(6)
    c1.metric("Matches",      "253")
    c2.metric("Wins",         "145")
    c3.metric("Win Rate",     "57%")
    c4.metric("Titles",       "5")
    c5.metric("Finals",       "8")
    c6.metric("First Title",  "2013")

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(
        f'<div style="display:flex;gap:16px;margin-bottom:6px;font-size:12px;color:#6b7280;">'
        f'<span style="display:flex;align-items:center;gap:5px;">'
        f'<span style="width:10px;height:10px;border-radius:2px;background:{GOLD};display:inline-block;"></span>'
        f'Title-winning season</span>'
        f'<span style="display:flex;align-items:center;gap:5px;">'
        f'<span style="width:10px;height:10px;border-radius:2px;background:{BLUE};display:inline-block;"></span>'
        f'Regular season</span></div>',
        unsafe_allow_html=True,
    )
    chart_card("Season-by-season win count", season_chart(), "season")

    col_a, col_b = st.columns(2)
    with col_a:
        chart_card("Win % by match type", donut_chart(), "donut")
    with col_b:
        facts = [
            ("Home win %","63%"), ("Away win %","52%"),
            ("Playoff win %","68%"), ("Best season","12W (2013,2015,2021)"),
            ("Longest win streak","9 matches"), ("Titles (joint record)","5"),
        ]
        rows = "".join(
            f'<div style="display:flex;justify-content:space-between;padding:9px 0;'
            f'border-bottom:0.5px solid rgba(0,0,0,0.06);">'
            f'<span style="font-size:13px;color:#6b7280;">{lbl}</span>'
            f'<span style="font-size:13px;font-weight:600;color:{BLUE};">{val}</span>'
            f'</div>'
            for lbl, val in facts
        )
        st.markdown(
            f'<div style="background:white;border-radius:12px;padding:1.25rem;'
            f'border:1px solid rgba(0,0,0,0.07);">'
            f'<div style="font-size:11px;font-weight:500;color:#6b7280;'
            f'text-transform:uppercase;letter-spacing:0.5px;margin-bottom:1rem;">Quick facts</div>'
            f'{rows}</div>',
            unsafe_allow_html=True,
        )

#TAB2—PLAYER STATS 
with tab2:
    st.markdown(
        f'<div style="font-family:Bebas Neue,sans-serif;font-size:22px;'
        f'color:#1a1a2e;margin-bottom:.75rem;">Batting Legends</div>',
        unsafe_allow_html=True,
    )
    for _, r in BATTERS.iterrows():
        st.markdown(
            player_row_html(r["Name"], r["Role"],
                            [("Runs", r["Runs"]), ("Avg", r["Avg"]), (r["S3L"], r["Stat3"])]),
            unsafe_allow_html=True,
        )

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(
        f'<div style="font-family:Bebas Neue,sans-serif;font-size:22px;'
        f'color:#1a1a2e;margin-bottom:.75rem;">Bowling Attack</div>',
        unsafe_allow_html=True,
    )
    for _, r in BOWLERS.iterrows():
        st.markdown(
            player_row_html(r["Name"], r["Role"],
                            [("Wkts", r["Wkts"]), ("Eco", r["Eco"]), ("Avg", r["Avg"])],
                            badge_color="#E65100"),
            unsafe_allow_html=True,
        )

    st.markdown("<br>", unsafe_allow_html=True)
    chart_card("Top run-scorers for MI (IPL career)", scorers_chart(), "scorers")

#TAB3—VENUE WINS
with tab3:
    v1, v2, v3, v4 = st.columns(4)
    v1.metric("Home Win %",      "74%")
    v2.metric("Away Win %",      "58%")
    v3.metric("Best Away Venue", "DY Patil")
    v4.metric("Home Ground",     "Wankhede")

    st.markdown("<br>", unsafe_allow_html=True)
    chart_card("Win % at each venue  —  (H) = home ground", venue_chart(), "venues")
    chart_card("Win % trend — Wankhede Stadium", wankhede_chart(), "wankhede")

#TAB4—H2H RECORDS
with tab4:
    r1, r2, r3, r4 = st.columns(4)
    r1.metric("Biggest Rivalry", "CSK")
    r2.metric("vs CSK Played",   "33")
    r3.metric("vs CSK Wins",     "18")
    r4.metric("vs CSK Win %",    "55%")

    st.markdown("<br>", unsafe_allow_html=True)
    col_l, col_r = st.columns(2)

    with col_l:
        bars = "".join(
            f'<div style="margin-bottom:10px;">'
            f'<div style="display:flex;align-items:center;justify-content:space-between;'
            f'font-size:12px;margin-bottom:4px;">'
            f'<span style="display:flex;align-items:center;gap:6px;">'
            f'{logo_tag(r["Team"], 22)}'
            f'<span style="color:#1a1a2e;font-weight:500;">{r["Team"]}</span></span>'
            f'<span style="color:#6b7280;">{r["Wins"]}W &nbsp;{r["Losses"]}L'
            f'&nbsp;<b style="color:{BLUE};">{r["WinPct"]}%</b></span>'
            f'</div>'
            f'<div style="display:flex;height:6px;border-radius:4px;overflow:hidden;">'
            f'<div style="width:{r["WinPct"]}%;background:{BLUE};"></div>'
            f'<div style="width:{100 - r["WinPct"]}%;background:#e0e0e0;"></div>'
            f'</div></div>'
            for _, r in RIVALS.iterrows()
        )
        st.markdown(
            f'<div style="background:white;border-radius:12px;padding:1.25rem;'
            f'border:1px solid rgba(0,0,0,0.07);">'
            f'<div style="font-size:11px;font-weight:500;color:#6b7280;'
            f'text-transform:uppercase;letter-spacing:0.5px;margin-bottom:1rem;">'
            f'Win ratio vs each team</div>{bars}</div>',
            unsafe_allow_html=True,
        )
    with col_r:
        chart_card("Wins vs losses by opponent", rivals_chart(), "rivals")

#TAB5—KEY PLAYERS
with tab5:
    kp_col, radar_col = st.columns(2)
    with kp_col:
        st.markdown(
            f'<div style="font-family:Bebas Neue,sans-serif;font-size:22px;'
            f'color:#1a1a2e;margin-bottom:.75rem;">All-time Impact XI</div>',
            unsafe_allow_html=True,
        )
        for num, name, desc, kind in KEY_PLAYERS:
            st.markdown(kp_row_html(num, name, desc, kind), unsafe_allow_html=True)
    with radar_col:
        chart_card("Impact score — key players (composite)", radar_chart(), "radar")
