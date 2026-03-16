# Mumbai Indians Dashboard
An IPL stats dashboard for MI fans — built with Streamlit and Plotly. Season wins, player cards, venue records, H2H results, and a key player radar chart, all in one place.
## Setup
You'll need Python 3.9+ and pip. Then just:
```bash
pip install -r requirements.txt
streamlit run mi_dashboard.py
```
Open `http://localhost:8501` in your browser. That's it.
## What's inside
- **Overview** — season-by-season wins (title years light up in gold), win % by match type
- **Player Stats** — batting and bowling cards with career numbers
- **Venue Wins** — win % at every stadium MI has played at
- **H2H Records** — head-to-head record against every IPL team
- **Key Players** — all-time Impact XI with a composite radar chart
## Want live scores?
The data is static right now. If you want live match updates during IPL, grab a free API key from [cricapi.com](https://cricapi.com) (100 calls/day free), store it in `.streamlit/secrets.toml`, and use `@st.cache_data(ttl=30)` to poll it every 30 seconds.
## Common issues
- `streamlit: command not found` → try `python -m streamlit run mi_dashboard.py`
- Blank page → make sure you're on `localhost:8501`, not the network IP
- Port busy → add `--server.port 8502` to the run command
**Stats cover IPL 2008–2024. Built for fun, not affiliated with Mumbai Indians.**
