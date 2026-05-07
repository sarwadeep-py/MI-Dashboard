import base64
import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from pathlib import Path

#Page configuration
st.set_page_config(page_title="Mumbai Indians Dashboard", page_icon="🏏", layout="wide")

# Colours
BLUE   = "#0052CC"
GOLD   = "#F0B429"
DARK   = "#001A4E"
LIGHT  = "#EEF4FF"
TEAL   = "#0B8ACB"
SILVER = "#F8FAFF"
TITLE_YEARS = {"2013", "2015", "2017", "2019", "2020"}

#LOGOs
TEAM_LOGOS = {
    "MI":   "images/mi.png",
    "CSK":  "images/csk.png",
    "KKR":  "images/kkr.png",
    "RCB":  "images/rcb.png",
    "DC":   "images/dc.png",
    "RR":   "images/rr.png",
    "SRH":  "images/srh.png",
    "PBKS": "images/pbks.png",
    "GT":   "images/gt.png",
}

PLAYER_PHOTOS = {
    "Rohit Sharma":     "images/rs.png",
    "Sachin Tendulkar": "images/st.png",
    "Suryakumar Yadav": "images/sky.png",
    "Kieron Pollard":   "images/kp.png",
    "Lasith Malinga":   "images/lm.png",
    "Jasprit Bumrah":   "images/jb.png",
    "Harbhajan Singh":  "images/hb.png",
    "Hardik Pandya":    "images/hp.png",
}

# img
def img_to_b64(path: str) -> str:
    # resolve relative to this script's directory, not CWD
    p = Path(__file__).parent / path
    raw = p.read_bytes()
    b64 = base64.b64encode(raw).decode()
    mime = "image/svg+xml" if p.suffix == ".svg" else "image/png"
    return f"data:{mime};base64,{b64}"

def player_avatar(name: str, badge_color: str = BLUE, size: int = 56) -> str:
    path = PLAYER_PHOTOS.get(name, "")
    resolved = Path(__file__).parent / path if path else None
    font_size = max(12, size // 3)
    border_px = max(2, size // 22)
    if resolved and resolved.exists():
        src = img_to_b64(path)
        return (
            f'<div style="width:{size}px;height:{size}px;border-radius:50%;flex-shrink:0;'
            f'overflow:hidden;border:{border_px+0.5}px solid {GOLD};'
            f'box-shadow:0 3px 10px rgba(0,0,0,0.18);">'
            f'<img src="{src}" style="width:100%;height:100%;object-fit:cover;display:block;">'
            f'</div>'
        )
    initials = "".join(w[0] for w in name.split()[:2]).upper()
    return (
        f'<div style="width:{size}px;height:{size}px;border-radius:50%;flex-shrink:0;'
        f'background:linear-gradient(135deg,{badge_color},{TEAL});'
        f'display:flex;align-items:center;justify-content:center;'
        f'font-family:\'Bebas Neue\',sans-serif;font-size:{font_size}px;color:white;'
        f'border:{border_px+0.5}px solid {GOLD};box-shadow:0 3px 10px rgba(0,0,0,0.18);">'
        f'{initials}</div>'
    )

def logo_tag(team: str, size: int = 32) -> str:
    path = TEAM_LOGOS.get(team, "")
    resolved = Path(__file__).parent / path if path else None
    if resolved and resolved.exists():
        src = img_to_b64(path)
        pad = max(2, size // 10)
        return (
            f'<div style="width:{size+pad*2}px;height:{size+pad*2}px;border-radius:50%;'
            f'background:rgba(255,255,255,0.95);display:inline-flex;align-items:center;'
            f'justify-content:center;vertical-align:middle;flex-shrink:0;'
            f'box-shadow:0 2px 6px rgba(0,0,0,0.12);border:1px solid rgba(0,0,0,0.06);">'
            f'<img src="{src}" style="width:{size}px;height:{size}px;object-fit:contain;">'
            f'</div>'
        )
    return f'<span style="font-size:11px;font-weight:700;color:{BLUE};padding:2px 6px;background:{LIGHT};border-radius:4px;">{team}</span>'

def mi_header_logo() -> str:
    path = TEAM_LOGOS.get("MI", "")
    resolved = Path(__file__).parent / path if path else None
    if resolved and resolved.exists():
        src = img_to_b64(path)
        return f'<img src="{src}" style="width:72px;height:72px;object-fit:contain;">'
    return f'<span style="font-family:\'Bebas Neue\',sans-serif;font-size:30px;color:{DARK};">MI</span>'

# plotly
def hex_to_rgba(hex_color: str, alpha: float = 0.09) -> str:
    h = hex_color.lstrip("#")
    r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    return f"rgba({r},{g},{b},{alpha})"

BASE = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Inter, DM Sans, sans-serif", color="rgb(30,41,59)"),
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

# Player profile data — used by the individual player pages
PLAYER_PROFILES = {
    "rohit-sharma": {
        "name": "Rohit Sharma",
        "nickname": "Hitman / Shana",
        "kind": "bat",
        "emoji": "🏏",
        "tagline": "All-title winning captain · Record breaker · MI's heart",
        "tags": ["Hitman", "Shana", "5× Title Captain", "Record Breaker"],
        "highlights": [
            ("🏆", "All 5 Title Wins", "The only captain to lead MI to all five IPL titles — 2013, 2015, 2017, 2019, 2020"),
            ("📊", "IPL Records", "Holds multiple IPL batting records including most runs for MI with 5611 runs at an average of 45+"),
            ("🎯", "Hitman", "Famous for his effortless stroke play and ability to dismantle any bowling attack with elegance"),
            ("🌟", "Shana", "Affectionately called 'Shana' — the Mumbai lad who rose to become one of cricket's greatest captains"),
        ],
        "stats": [("Runs", "5611"), ("Avg", "45.3"), ("100s", "4"), ("Titles", "5")],
    },
    "lasith-malinga": {
        "name": "Lasith Malinga",
        "nickname": "Slinga Malinga",
        "kind": "bowl",
        "emoji": "🎳",
        "tagline": "Right-arm Slinger · 2019 Final Hero · Sri Lankan Legend",
        "tags": ["Right-arm Slinger", "Yorker King", "2019 Final Hero", "Sri Lankan Legend"],
        "highlights": [
            ("🏏", "2019 Final Hero", "Bowled the last-ball yorker to defend 1 run off the final ball vs CSK — one of the greatest moments in IPL history"),
            ("🌀", "Right-arm Slinger", "His unorthodox slingy round-arm action made him virtually unplayable at the death"),
            ("🇱🇰", "Sri Lankan Legend", "The greatest Sri Lankan fast bowler ever, who chose MI as his IPL home for 11 seasons"),
            ("🎯", "Yorker Specialist", "170 wickets for MI — the highest by any bowler in IPL history at the time of his retirement"),
        ],
        "stats": [("Wickets", "170"), ("Eco", "7.14"), ("Avg", "17.0"), ("Seasons", "11")],
    },
    "kieron-pollard": {
        "name": "Kieron Pollard",
        "nickname": "Polly",
        "kind": "all",
        "emoji": "💪",
        "tagline": "West Indian Legend · Best Finisher · CSK's Nightmare",
        "tags": ["West Indian Legend", "Best Finisher", "CSK's Nightmare", "Saviour", "Gun Fielder"],
        "highlights": [
            ("🌴", "West Indian Legend", "The greatest West Indian cricketer in IPL history — 13 seasons of heart, muscle, and magic for MI"),
            ("🏏", "Best Finisher", "Consistently one of the best finishers in T20 cricket — capable of winning matches from any situation"),
            ("😤", "CSK's Nightmare", "Holds an exceptional record against CSK with match-winning performances at crucial moments"),
            ("🤲", "Saviour & Gun Fielder", "3412 runs + crucial wickets, plus one of the best outfielders in IPL history"),
        ],
        "stats": [("Runs", "3412"), ("Avg", "27.5"), ("SR", "191"), ("Seasons", "13")],
    },
    "jasprit-bumrah": {
        "name": "Jasprit Bumrah",
        "nickname": "Jassi / The GOAT",
        "kind": "bowl",
        "emoji": "🔥",
        "tagline": "GOAT · Diamond of MI · Death Bowling Maestro",
        "tags": ["GOAT", "Yorker Machine", "Diamond of MI", "Death Bowling", "Economical"],
        "highlights": [
            ("💎", "Diamond of the Team", "Bumrah is the crown jewel of MI's bowling — irreplaceable, priceless, and match-defining"),
            ("🎯", "Yorker Machine", "His yorkers at the death are legendary — pin-point accuracy at 140+ kmph with a near-unplayable action"),
            ("💰", "Economical", "Economy of 7.39 in T20 cricket — remarkable for a pace bowler who bowls the toughest overs"),
            ("🐐", "The GOAT", "145 wickets for MI and widely regarded as the greatest fast bowler in T20 cricket history"),
        ],
        "stats": [("Wickets", "145"), ("Eco", "7.39"), ("Avg", "21.7"), ("Best", "5/10")],
    },
    "suryakumar-yadav": {
        "name": "Suryakumar Yadav",
        "nickname": "SKY / Mr. 360",
        "kind": "bat",
        "emoji": "🌟",
        "tagline": "Mr. 360 · Scoop Shot King · T20 World Cup Winning Captain",
        "tags": ["Mr. 360", "Supadupla Shot", "T20 WC Winning Captain", "Long Off Conqueror"],
        "highlights": [
            ("🌀", "Mr. 360", "Named for his ability to hit the ball to every part of the ground — no fielder placement is safe from SKY"),
            ("🥄", "The Supadupla Shot", "His iconic ramp/scoop shot over fine leg or third man is almost impossible to bowl against"),
            ("🏆", "T20 World Cup Captain", "Led India to the T20 World Cup title — the pinnacle of his remarkable T20 career"),
            ("📐", "Long Off, Long Off, Long Off", "Ensured India's trophy after a decade with a stunning catch at long off in the 2024 T20 World Cup final — a moment that defined a generation"),
        ],
        "stats": [("Runs", "2644"), ("Avg", "31.9"), ("SR", "148"), ("World No.", "1")],
    },
    "sachin-tendulkar": {
        "name": "Sachin Tendulkar",
        "nickname": "God of Cricket / Master Blaster",
        "kind": "bat",
        "emoji": "🙏",
        "tagline": "God of Cricket · MI Icon · Mentor · 100 International Hundreds",
        "tags": ["God of Cricket", "MI Legend", "Indian Legend", "Mentor", "1st Orange Cap", "100 Hundreds"],
        "highlights": [
            ("🙏", "God of Cricket", "The greatest batsman to ever play the game — Sachin Tendulkar is cricket's deity"),
            ("🍊", "First Orange Cap", "Won the very first IPL Orange Cap in 2010, proving his genius translated seamlessly to T20"),
            ("💯", "100 International Hundreds", "The only cricketer in history to score 100 international centuries — a record that may never be broken"),
            ("🧠", "Mentor", "Served as MI's mentor, shaping the culture and values of the most successful IPL franchise"),
        ],
        "stats": [("MI Runs", "2334"), ("Avg", "34.8"), ("100s", "100"), ("IPL 100s", "1")],
    },
    "hardik-pandya": {
        "name": "Hardik Pandya",
        "nickname": "Kung-fu Pandya",
        "kind": "all",
        "emoji": "⚡",
        "tagline": "All-rounder · Gun Fielder · Kung-fu Pandya · Finisher",
        "tags": ["All-rounder", "Gun Fielder", "Kung-fu Pandya", "Finisher"],
        "highlights": [
            ("🥋", "Kung-fu Pandya", "Nicknamed for his lightning-quick reflexes in the field and his explosive, martial-arts-like energy"),
            ("🏏", "All-rounder", "1476 runs + 42 wickets for MI — a genuine match-winner with both bat and ball"),
            ("🤸", "Gun Fielder", "One of the most athletic and dynamic fielders in IPL history — multiple stunning catches and run-outs"),
            ("💥", "Finisher", "Capable of hitting sixes at will in the death overs and defending small totals with his pace"),
        ],
        "stats": [("Runs", "1476"), ("Wickets", "42"), ("SR", "145"), ("Eco", "8.89")],
    },
}

PLAYER_SLUG = {
    "Rohit Sharma":     "rohit-sharma",
    "Lasith Malinga":   "lasith-malinga",
    "Kieron Pollard":   "kieron-pollard",
    "Jasprit Bumrah":   "jasprit-bumrah",
    "Suryakumar Yadav": "suryakumar-yadav",
    "Sachin Tendulkar": "sachin-tendulkar",
    "Hardik Pandya":    "hardik-pandya",
}

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
        **BASE, bargap=0.35, height=320, showlegend=False,
        xaxis=dict(tickmode="array", tickvals=years, ticktext=ticks,
                   tickfont=dict(size=11), showgrid=False),
        yaxis=dict(
            gridcolor="rgba(0,0,0,0.05)", zeroline=False,
            range=[0, max(wins) * 1.25],   # headroom so "outside" labels never clip
        ),
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

def finals_chart():
    """Annotated bar chart showing how MI won each of the 5 IPL finals."""
    finals = [
        {"year": "2013", "opponent": "CSK",  "venue": "Eden Gardens, Kolkata","margin": 23,  "type": "runs",    "color": BLUE},
        {"year": "2015", "opponent": "CSK",  "venue": "Eden Gardens, Kolkata","margin": 41,  "type": "runs",    "color": BLUE},
        {"year": "2017", "opponent": "RPS",  "venue": "Hyderabad",            "margin": 1,   "type": "run",     "color": TEAL},
        {"year": "2019", "opponent": "CSK",  "venue": "Hyderabad",            "margin": 1,   "type": "run",     "color": TEAL},
        {"year": "2020", "opponent": "DC",   "venue": "Dubai",                "margin": 5,   "type": "wickets", "color": GOLD},
    ]

    years    = [f["year"] for f in finals]
    margins  = [f["margin"] for f in finals]
    colors   = [f["color"] for f in finals]
    labels   = [
        f"{f['margin']} {f['type']}" for f in finals
    ]
    hover   = [
        f"<b>{f['year']} Final</b><br>vs {f['opponent']}<br>{f['venue']}<br>Won by {f['margin']} {f['type']}"
        for f in finals
    ]

    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=years,
        y=margins,
        marker_color=colors,
        marker_line_width=0,
        marker_line_color="rgba(0,0,0,0)",
        text=labels,
        textposition="outside",
        textfont=dict(size=13, color="#0f172a", family="Inter, sans-serif"),
        hovertext=hover,
        hoverinfo="text",
        cliponaxis=False,
    ))

    # Opponent + venue annotations inside/below each bar
    for i, f in enumerate(finals):
        fig.add_annotation(
            x=f["year"],
            y=max(0.5, f["margin"] / 2),
            text=f"vs {f['opponent']}",
            showarrow=False,
            font=dict(size=11, color="white", family="Inter, sans-serif"),
            bgcolor="rgba(0,0,0,0)",
        )
        fig.add_annotation(
            x=f["year"],
            y=-4.5,
            text=f['venue'],
            showarrow=False,
            font=dict(size=10, color="#1e293b", family="Inter, sans-serif"),
            yref="y",
        )

    # Legend annotations (top right)
    for label, color, ypos in [("Run wins", BLUE, 44), ("1-run thriller", TEAL, 41), ("Wicket win", GOLD, 38)]:
        fig.add_annotation(
            x=1.01, y=ypos, xref="paper", yref="y",
            text=f'<span style="color:{color};">●</span> {label}',
            showarrow=False,
            font=dict(size=10, color="#1e293b", family="Inter, sans-serif"),
            xanchor="left",
        )

    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=340,
        showlegend=False,
        margin=dict(l=10, r=110, t=20, b=50),
        bargap=0.4,
        xaxis=dict(
            showgrid=False,
            tickfont=dict(size=13, color="#0f172a", family="Inter, sans-serif"),
            tickmode="array",
            tickvals=years,
            ticktext=[f"🏆 {y}" for y in years],
        ),
        yaxis=dict(
            showgrid=False,
            showticklabels=False,
            range=[-6, 52],
        ),
    )
    return fig

#  UI 
def chart_card(title: str, fig, key: str):
    st.markdown(
        f'<div style="background:rgba(255,255,255,0.85);backdrop-filter:blur(12px);'
        f'-webkit-backdrop-filter:blur(12px);border-radius:16px;'
        f'padding:1.4rem 1.4rem 0.6rem;'
        f'border:1px solid rgba(255,255,255,0.9);'
        f'box-shadow:0 4px 24px rgba(0,82,204,0.08),0 1px 3px rgba(0,0,0,0.06);'
        f'margin-bottom:1.2rem;">'
        f'<div style="font-size:11px;font-weight:700;color:#1e293b;'
        f'text-transform:uppercase;letter-spacing:0.8px;margin-bottom:.6rem;'
        f'display:flex;align-items:center;gap:6px;">'
        f'<span style="width:3px;height:12px;background:linear-gradient(180deg,{BLUE},{GOLD});'
        f'border-radius:2px;display:inline-block;"></span>{title}</div>',
        unsafe_allow_html=True,
    )
    st.plotly_chart(fig, width="stretch", config={"displayModeBar": False}, key=key)
    st.markdown("</div>", unsafe_allow_html=True)

def player_row_html(name: str, role: str, stats: list, badge_color: str = BLUE) -> str:
    avatar     = player_avatar(name, badge_color)
    stats_html = "".join(
        f'<div style="text-align:center;min-width:58px;padding:0 4px;">'
        f'<div style="font-size:17px;font-weight:700;color:{BLUE};letter-spacing:-0.3px;">{v}</div>'
        f'<div style="font-size:9px;color:#374151;font-weight:700;text-transform:uppercase;letter-spacing:0.8px;margin-top:1px;">{k}</div>'
        f'</div>'
        for k, v in stats
    )
    return (
        f'<div style="display:flex;align-items:center;gap:14px;'
        f'background:rgba(255,255,255,0.9);backdrop-filter:blur(8px);'
        f'-webkit-backdrop-filter:blur(8px);'
        f'border:1px solid rgba(255,255,255,0.95);border-radius:14px;'
        f'padding:.9rem 1.1rem;border-left:4px solid {GOLD};margin-bottom:10px;'
        f'box-shadow:0 2px 12px rgba(0,82,204,0.07),0 1px 2px rgba(0,0,0,0.04);'
        f'transition:transform 0.15s;">'
        f'{avatar}'
        f'<div style="flex:1;min-width:0;">'
        f'<div style="font-size:14px;font-weight:700;color:#0f172a;letter-spacing:-0.1px;">{name}</div>'
        f'<div style="font-size:11px;color:#374151;font-weight:600;margin-top:1px;">{role}</div>'
        f'</div>'
        f'<div style="display:flex;gap:4px;flex-shrink:0;flex-wrap:wrap;'
        f'background:{LIGHT};border-radius:10px;padding:6px 8px;">{stats_html}</div>'
        f'</div>'
    )

def kp_row_html(num: int, name: str, desc: str, kind: str) -> str:
    colors = {"bat":(LIGHT,BLUE), "bowl":("#FFF4ED","#C2410C"), "all":("#F0FDF4","#15803D")}
    tags   = {"bat":"Batsman", "bowl":"Bowler", "all":"All-rounder"}
    bg, fg = colors[kind]
    avatar = player_avatar(name, fg)
    slug   = PLAYER_SLUG.get(name, "")
    link_html = (
        f'<a href="?player={slug}" target="_self" style="font-size:10px;color:{fg};'
        f'font-weight:600;text-decoration:none;padding:4px 10px;border-radius:20px;'
        f'background:{bg};border:1px solid {fg}44;white-space:nowrap;'
        f'transition:opacity 0.15s;" '
        f'onmouseover="this.style.opacity=\'0.75\'" '
        f'onmouseout="this.style.opacity=\'1\'">View Profile →</a>'
    ) if slug else ""
    return (
        f'<div style="display:flex;align-items:center;gap:12px;'
        f'background:rgba(255,255,255,0.9);backdrop-filter:blur(8px);'
        f'-webkit-backdrop-filter:blur(8px);'
        f'border:1px solid rgba(255,255,255,0.95);border-radius:14px;'
        f'padding:.8rem 1.1rem;margin-bottom:10px;'
        f'box-shadow:0 2px 12px rgba(0,82,204,0.07),0 1px 2px rgba(0,0,0,0.04);">'
        f'<div style="font-family:\'Bebas Neue\',sans-serif;font-size:24px;'
        f'background:linear-gradient(135deg,{GOLD},{BLUE});-webkit-background-clip:text;'
        f'-webkit-text-fill-color:transparent;background-clip:text;'
        f'width:26px;text-align:center;flex-shrink:0;line-height:1;">{num}</div>'
        f'{avatar}'
        f'<div style="flex:1;min-width:0;">'
        f'<div style="font-size:14px;font-weight:700;color:#0f172a;letter-spacing:-0.1px;">{name}</div>'
        f'<div style="font-size:11px;color:#374151;font-weight:600;margin-top:2px;">{desc}</div>'
        f'</div>'
        f'<div style="display:flex;align-items:center;gap:8px;flex-shrink:0;">'
        f'<div style="font-size:10px;padding:4px 12px;border-radius:20px;'
        f'background:{bg};color:{fg};font-weight:600;white-space:nowrap;'
        f'letter-spacing:0.3px;border:1px solid {fg}22;">{tags[kind]}</div>'
        f'{link_html}'
        f'</div>'
        f'</div>'
    )

# ── Player Profile Page ──────────────────────────────────────────────────────
def show_player_page(slug: str):
    """Render a standalone player profile page."""
    profile = PLAYER_PROFILES.get(slug)
    if not profile:
        st.error("Player not found.")
        if st.button("← Back to Dashboard", key="back_err"):
            st.query_params.clear()
            st.rerun()
        return

    name    = profile["name"]
    kind    = profile["kind"]
    colors  = {"bat": (LIGHT, BLUE), "bowl": ("#FFF4ED","#C2410C"), "all": ("#F0FDF4","#15803D")}
    bg, fg  = colors[kind]
    # Large avatar (90px) for the hero banner — no extra wrapper div needed
    avatar  = player_avatar(name, fg, size=90)

    # ── Hero card ──
    tags_html = "".join(
        f'<span style="font-size:11px;padding:4px 12px;border-radius:20px;'
        f'background:{bg};color:{fg};font-weight:600;border:1px solid {fg}33;'
        f'white-space:nowrap;">{t}</span>'
        for t in profile["tags"]
    )
    st.markdown(
        f'<div style="background:linear-gradient(135deg,{DARK} 0%,{BLUE} 60%,{TEAL} 100%);'
        f'border-radius:20px;padding:1.8rem 2rem;display:flex;align-items:center;'
        f'gap:1.5rem;margin-bottom:1.4rem;flex-wrap:wrap;'
        f'box-shadow:0 8px 32px rgba(0,82,204,0.25);">'
        f'{avatar}'
        f'<div style="flex:1;min-width:200px;">'
        f'<div style="font-size:11px;color:rgba(255,255,255,0.5);text-transform:uppercase;'
        f'letter-spacing:1.5px;font-weight:600;margin-bottom:4px;">{profile["emoji"]} Player Profile</div>'
        f'<div style="font-family:\'Bebas Neue\',sans-serif;font-size:clamp(28px,7vw,44px);'
        f'color:white;line-height:1;letter-spacing:1.5px;">{name}</div>'
        f'<div style="font-size:12px;color:rgba(255,255,255,0.55);margin-top:6px;font-style:italic;">'
        f'"{profile["nickname"]}"</div>'
        f'<div style="font-size:13px;color:rgba(255,255,255,0.75);margin-top:8px;">'
        f'{profile["tagline"]}</div>'
        f'</div>'
        f'</div>',
        unsafe_allow_html=True,
    )

    # ── Tags row ──
    st.markdown(
        f'<div style="display:flex;flex-wrap:wrap;gap:8px;margin-bottom:1.4rem;">{tags_html}</div>',
        unsafe_allow_html=True,
    )

    # ── Stats strip ──
    stats_html = "".join(
        f'<div style="flex:1;min-width:90px;text-align:center;padding:1rem;'
        f'background:rgba(255,255,255,0.9);border-radius:14px;'
        f'border:1px solid rgba(255,255,255,0.95);'
        f'box-shadow:0 2px 12px rgba(0,82,204,0.07);">'
        f'<div style="font-family:\'Bebas Neue\',sans-serif;font-size:26px;'
        f'background:linear-gradient(135deg,{BLUE},{TEAL});'
        f'-webkit-background-clip:text;-webkit-text-fill-color:transparent;'
        f'background-clip:text;line-height:1;">{v}</div>'
        f'<div style="font-size:9px;color:#374151;text-transform:uppercase;'
        f'letter-spacing:0.8px;font-weight:600;margin-top:3px;">{k}</div>'
        f'</div>'
        for k, v in profile["stats"]
    )
    st.markdown(
        f'<div style="display:flex;gap:10px;flex-wrap:wrap;margin-bottom:1.4rem;">'
        f'{stats_html}</div>',
        unsafe_allow_html=True,
    )

    # ── Highlights ──
    st.markdown(
        f'<div style="font-family:\'Bebas Neue\',sans-serif;font-size:22px;'
        f'background:linear-gradient(135deg,{DARK},{BLUE});'
        f'-webkit-background-clip:text;-webkit-text-fill-color:transparent;'
        f'background-clip:text;margin-bottom:.8rem;letter-spacing:1px;">Highlights</div>',
        unsafe_allow_html=True,
    )
    for icon, title, body in profile["highlights"]:
        st.markdown(
            f'<div style="background:rgba(255,255,255,0.9);border-radius:14px;'
            f'padding:1rem 1.2rem;margin-bottom:10px;'
            f'border:1px solid rgba(255,255,255,0.95);border-left:4px solid {GOLD};'
            f'box-shadow:0 2px 12px rgba(0,82,204,0.07);">'
            f'<div style="font-size:14px;font-weight:700;color:#0f172a;margin-bottom:4px;">'
            f'{icon} {title}</div>'
            f'<div style="font-size:13px;color:#475569;line-height:1.55;">{body}</div>'
            f'</div>',
            unsafe_allow_html=True,
        )

    # ── Back button at bottom ──
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("← Back to Dashboard", key="back_bottom"):
        st.query_params.clear()
        st.rerun()


# ── Route: player profile OR main dashboard ───────────────────────────────────
_params      = st.query_params
_player_slug = _params.get("player", "")

#  CSS 
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Inter:wght@400;500;600;700&family=DM+Sans:wght@400;500;600&display=swap');
html, body, [class*="css"] {{ font-family: 'Inter', 'DM Sans', sans-serif; }}

/* Mesh gradient background */
.stApp {{
    background: linear-gradient(135deg, #EEF4FF 0%, #F0F7FF 35%, #EFF6FF 60%, #F5F0FF 100%) !important;
    background-attachment: fixed !important;
}}

#MainMenu, footer, header {{ visibility: hidden; }}

/* Metric cards — glass */
[data-testid="metric-container"] {{
    background: rgba(255,255,255,0.85) !important;
    backdrop-filter: blur(12px) !important;
    -webkit-backdrop-filter: blur(12px) !important;
    border-radius: 16px !important;
    padding: 1.1rem 1.2rem !important;
    border: 1px solid rgba(255,255,255,0.95) !important;
    box-shadow: 0 4px 20px rgba(0,82,204,0.09), 0 1px 3px rgba(0,0,0,0.05) !important;
    transition: transform 0.15s, box-shadow 0.15s !important;
}}
[data-testid="metric-container"]:hover {{
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 28px rgba(0,82,204,0.14), 0 2px 4px rgba(0,0,0,0.06) !important;
}}
[data-testid="stMetricValue"] {{
    font-family: 'Bebas Neue', sans-serif !important;
    font-size: 2.2rem !important;
    background: linear-gradient(135deg, {BLUE}, {TEAL}) !important;
    -webkit-background-clip: text !important;
    -webkit-text-fill-color: transparent !important;
    background-clip: text !important;
    line-height: 1.1 !important;
}}
[data-testid="stMetricLabel"] {{
    font-size: 10px !important;
    text-transform: uppercase !important;
    letter-spacing: 0.8px !important;
    color: #94a3b8 !important;
    font-weight: 600 !important;
}}
[data-testid="stMetricDelta"] {{ display:none !important; }}

/* Tabs */
[data-baseweb="tab-list"] {{
    background: rgba(255,255,255,0.7) !important;
    backdrop-filter: blur(10px) !important;
    border-radius: 24px !important;
    padding: 4px !important;
    gap: 2px !important;
    border: 1px solid rgba(255,255,255,0.9) !important;
    box-shadow: 0 2px 10px rgba(0,82,204,0.07) !important;
    margin-bottom: 1.2rem !important;
}}
[data-baseweb="tab"] {{
    border-radius: 20px !important;
    border: none !important;
    background: transparent !important;
    color: #64748b !important;
    font-weight: 500 !important;
    font-size: 13px !important;
    padding: 8px 16px !important;
    transition: all 0.2s !important;
}}
[aria-selected="true"][data-baseweb="tab"] {{
    background: linear-gradient(135deg, {BLUE}, {TEAL}) !important;
    color: white !important;
    box-shadow: 0 4px 12px rgba(0,82,204,0.3) !important;
}}
[data-baseweb="tab-highlight"], [data-baseweb="tab-border"] {{ display: none !important; }}
.block-container {{ padding-top: 1rem !important; }}

/* ── Mobile overrides ── */
@media (max-width: 640px) {{
    .block-container {{
        padding-left: 0.75rem !important;
        padding-right: 0.75rem !important;
    }}
    /* Tab list: allow wrapping on small screens */
    [data-baseweb="tab-list"] {{
        flex-wrap: wrap !important;
        border-radius: 16px !important;
        justify-content: center !important;
    }}
    [data-baseweb="tab"] {{
        font-size: 11px !important;
        padding: 6px 10px !important;
    }}
    /* Metric cards: stack 2-per-row */
    [data-testid="metric-container"] {{
        padding: 0.75rem 0.9rem !important;
    }}
    [data-testid="stMetricValue"] {{
        font-size: 1.6rem !important;
    }}
}}
</style>
""", unsafe_allow_html=True)

if _player_slug:
    show_player_page(_player_slug)
    st.stop()

#  Header 
st.markdown(f"""
<div style="background:linear-gradient(135deg, {DARK} 0%, {BLUE} 55%, {TEAL} 100%);
            border-radius:20px;padding:1.4rem 1.5rem;
            display:flex;align-items:center;gap:1.2rem;margin-bottom:1.5rem;
            flex-wrap:wrap;
            position:relative;overflow:hidden;
            box-shadow:0 8px 32px rgba(0,82,204,0.25),0 2px 8px rgba(0,0,0,0.15);">
  <!-- Decorative circles -->
  <div style="position:absolute;right:-60px;top:-60px;width:240px;height:240px;
              border-radius:50%;border:40px solid rgba(240,180,41,0.12);pointer-events:none;"></div>
  <div style="position:absolute;right:80px;bottom:-80px;width:180px;height:180px;
              border-radius:50%;border:30px solid rgba(255,255,255,0.06);pointer-events:none;"></div>
  <!-- Logo -->
  <div style="width:82px;height:82px;border-radius:50%;
              background:rgba(255,255,255,0.12);backdrop-filter:blur(8px);
              flex-shrink:0;display:flex;align-items:center;justify-content:center;
              border:2px solid rgba(240,180,41,0.6);overflow:hidden;padding:6px;
              box-shadow:0 4px 16px rgba(0,0,0,0.2);">
    {mi_header_logo()}
  </div>
  <!-- Title -->
  <div>
    <div style="font-family:'Bebas Neue',sans-serif;font-size:clamp(24px,6vw,38px);color:white;
                letter-spacing:2px;line-height:1;text-shadow:0 2px 8px rgba(0,0,0,0.2);">Mumbai Indians</div>
    <div style="font-size:12px;color:rgba(255,255,255,0.6);margin-top:5px;
                letter-spacing:0.5px;font-weight:500;">
      IPL Stats Dashboard &nbsp;·&nbsp; All-time record
    </div>
  </div>
  <!-- Trophy count -->
  <div style="margin-left:auto;text-align:right;flex-shrink:0;">
    <div style="font-family:'Bebas Neue',sans-serif;font-size:clamp(40px,10vw,62px);
                color:{GOLD};line-height:1;
                text-shadow:0 0 30px rgba(240,180,41,0.4);">5</div>
    <div style="font-size:10px;color:rgba(255,255,255,0.5);
                text-transform:uppercase;letter-spacing:1.5px;font-weight:600;">IPL Titles</div>
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
            f'<div style="display:flex;justify-content:space-between;align-items:center;'
            f'padding:10px 0;border-bottom:1px solid rgba(0,82,204,0.06);">'
            f'<span style="font-size:12px;color:#1e293b;font-weight:600;">{lbl}</span>'
            f'<span style="font-size:13px;font-weight:700;color:{BLUE};">{val}</span>'
            f'</div>'
            for lbl, val in facts
        )
        st.markdown(
            f'<div style="background:rgba(255,255,255,0.85);backdrop-filter:blur(12px);'
            f'-webkit-backdrop-filter:blur(12px);border-radius:16px;padding:1.4rem;'
            f'border:1px solid rgba(255,255,255,0.95);height:100%;'
            f'box-shadow:0 4px 24px rgba(0,82,204,0.08),0 1px 3px rgba(0,0,0,0.05);">'
            f'<div style="font-size:10px;font-weight:700;color:#374151;'
            f'text-transform:uppercase;letter-spacing:0.8px;margin-bottom:1rem;'
            f'display:flex;align-items:center;gap:6px;">'
            f'<span style="width:3px;height:12px;background:linear-gradient(180deg,{BLUE},{GOLD});'
            f'border-radius:2px;display:inline-block;"></span>Quick facts</div>'
            f'{rows}</div>',
            unsafe_allow_html=True,
        )

#TAB2—PLAYER STATS 
with tab2:
    st.markdown(
        f'<div style="font-family:\'Bebas Neue\',sans-serif;font-size:24px;'
        f'background:linear-gradient(135deg,{DARK},{BLUE});'
        f'-webkit-background-clip:text;-webkit-text-fill-color:transparent;'
        f'background-clip:text;margin-bottom:.9rem;letter-spacing:1px;">Batting Legends</div>',
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
        f'<div style="font-family:\'Bebas Neue\',sans-serif;font-size:24px;'
        f'background:linear-gradient(135deg,{DARK},{BLUE});'
        f'-webkit-background-clip:text;-webkit-text-fill-color:transparent;'
        f'background-clip:text;margin-bottom:.9rem;letter-spacing:1px;">Bowling Attack</div>',
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
            f'<div style="margin-bottom:12px;">'
            f'<div style="display:flex;align-items:center;justify-content:space-between;'
            f'font-size:12px;margin-bottom:5px;">'
            f'<span style="display:flex;align-items:center;gap:7px;">'
            f'{logo_tag(r["Team"], 22)}'
            f'<span style="color:#0f172a;font-weight:600;">{r["Team"]}</span></span>'
            f'<span style="color:#374151;font-size:11px;">{r["Wins"]}W &nbsp;{r["Losses"]}L'
            f'&nbsp;<b style="color:{BLUE};font-size:12px;">{r["WinPct"]}%</b></span>'
            f'</div>'
            f'<div style="display:flex;height:7px;border-radius:6px;overflow:hidden;'
            f'background:#e2e8f0;">'
            f'<div style="width:{r["WinPct"]}%;background:linear-gradient(90deg,{BLUE},{TEAL});'
            f'border-radius:6px;transition:width 0.3s;"></div>'
            f'</div></div>'
            for _, r in RIVALS.iterrows()
        )
        st.markdown(
            f'<div style="background:rgba(255,255,255,0.85);backdrop-filter:blur(12px);'
            f'-webkit-backdrop-filter:blur(12px);border-radius:16px;padding:1.4rem;'
            f'border:1px solid rgba(255,255,255,0.95);'
            f'box-shadow:0 4px 24px rgba(0,82,204,0.08),0 1px 3px rgba(0,0,0,0.05);">'
            f'<div style="font-size:10px;font-weight:700;color:#374151;'
            f'text-transform:uppercase;letter-spacing:0.8px;margin-bottom:1.1rem;'
            f'display:flex;align-items:center;gap:6px;">'
            f'<span style="width:3px;height:12px;background:linear-gradient(180deg,{BLUE},{GOLD});'
            f'border-radius:2px;display:inline-block;"></span>'
            f'Win ratio vs each team</div>{bars}</div>',
            unsafe_allow_html=True,
        )
    with col_r:
        chart_card("Wins vs losses by opponent", rivals_chart(), "rivals")

#TAB5—KEY PLAYERS
with tab5:
    st.markdown(
        f'<div style="font-family:\'Bebas Neue\',sans-serif;font-size:24px;'
        f'background:linear-gradient(135deg,{DARK},{BLUE});'
        f'-webkit-background-clip:text;-webkit-text-fill-color:transparent;'
        f'background-clip:text;margin-bottom:.9rem;letter-spacing:1px;">All-time Impact XI</div>',
        unsafe_allow_html=True,
    )

    # 2-column grid for player cards
    left_col, right_col = st.columns(2)
    for i, (num, name, desc, kind) in enumerate(KEY_PLAYERS):
        col = left_col if i % 2 == 0 else right_col
        with col:
            st.markdown(kp_row_html(num, name, desc, kind), unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    chart_card("How MI won each IPL Final 🏆", finals_chart(), "finals")
