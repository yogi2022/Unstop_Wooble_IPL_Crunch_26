# 🏏 IPL CRUNCH '26 — Data Analytics Dashboard

> **Wooble Analytics Challenge · Ball-by-Ball Intelligence**  
> Every IPL opinion backed by data. Every chart earned by logic.

---

## 📸 Overview

IPL CRUNCH '26 is a fully interactive **Streamlit** analytics dashboard built for the [Wooble IPL Crunch '26 Challenge](https://wooble.org/hackathon/crunch-26). It ingests raw ball-by-ball IPL CSV data and delivers professional-grade answers to the three core challenge questions — plus a layer of surprise insights that go beyond the obvious.

---

## 🎯 What This Dashboard Solves

| Question | Answer Delivered |
|---|---|
| Do toss winners win more? | Win-rate bar chart + decision split + season trend line |
| Which phase wins matches? | Phase avg-run comparison + over-by-over run-rate chart |
| Top 5 batters & bowlers? | Ranked tables with avg, SR, economy + season-top-scorer bars |
| Surprising finding? | 5 data-backed insights incl. dot-ball supremacy, death-over dominance |

---

## 🗂️ Project Structure

```
ipl_crunch_26/
│
├── app.py                  ← Main Streamlit entry point
│
├── utils/
│   ├── __init__.py
│   ├── data_loader.py      ← CSV ingestion, cleaning, feature engineering
│   └── analysis.py         ← All analytical computations (pure functions)
│
├── .streamlit/
│   └── config.toml         ← Dark theme, brand colors
│
├── requirements.txt
└── README.md
```

---

## ⚙️ Setup & Run

### 1. Clone the repo

```bash
git clone https://github.com/YOUR_USERNAME/ipl-crunch-26.git
cd ipl-crunch-26
```

### 2. Create virtual environment (recommended)

```bash
python -m venv venv
source venv/bin/activate        # macOS / Linux
venv\Scripts\activate           # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Launch the dashboard

```bash
streamlit run app.py
```

The app opens at `http://localhost:8501`.

---

## 📂 Getting the Data

### Option A — Download from Wooble (easiest)
Download `ipl_matches.csv` directly from the [challenge resources page](https://wooble.org/hackathon/crunch-26).

### Option B — Cricsheet (learn from scratch)

```python
# download_cricsheet.py
import requests, zipfile, io, json, pandas as pd, os, glob

# 1. Download IPL JSON zip from cricsheet.org
url = "https://cricsheet.org/downloads/ipl_json.zip"
r   = requests.get(url)
z   = zipfile.ZipFile(io.BytesIO(r.content))
z.extractall("ipl_json/")

# 2. Parse every match JSON → ball-level rows
rows = []
for path in glob.glob("ipl_json/*.json"):
    with open(path) as f:
        data = json.load(f)
    info  = data["info"]
    match_id = os.path.basename(path).replace(".json","")
    for i, inning in enumerate(data.get("innings", []), 1):
        batting_team = inning.get("team","")
        for over_obj in inning.get("overs", []):
            ov = over_obj["over"]
            for del_obj in over_obj.get("deliveries", []):
                row = {
                    "match_id":      match_id,
                    "season":        info.get("season",""),
                    "date":          info.get("dates",[""])[0],
                    "venue":         info.get("venue",""),
                    "city":          info.get("city",""),
                    "team1":         info["teams"][0] if len(info["teams"])>0 else "",
                    "team2":         info["teams"][1] if len(info["teams"])>1 else "",
                    "toss_winner":   info.get("toss",{}).get("winner",""),
                    "toss_decision": info.get("toss",{}).get("decision",""),
                    "winner":        info.get("outcome",{}).get("winner",""),
                    "player_of_match": info.get("player_of_match",[""])[0],
                    "innings":       i,
                    "batting_team":  batting_team,
                    "over":          ov,
                    "ball":          del_obj.get("deliveries_in_over",0),
                    "batter":        del_obj["batter"],
                    "bowler":        del_obj["bowler"],
                    "non_striker":   del_obj.get("non_striker",""),
                    "runs_batter":   del_obj["runs"]["batter"],
                    "runs_extras":   del_obj["runs"]["extras"],
                    "runs_total":    del_obj["runs"]["total"],
                    "wicket_kind":   del_obj.get("wickets",[{}])[0].get("kind","") if del_obj.get("wickets") else "",
                    "wicket_player_out": del_obj.get("wickets",[{}])[0].get("player_out","") if del_obj.get("wickets") else "",
                }
                rows.append(row)

pd.DataFrame(rows).to_csv("ipl_matches.csv", index=False)
print("✅ ipl_matches.csv created")
```

---

## 📊 Dashboard Sections

### 🎲 Toss Impact
- Bar chart: win rate of toss winners vs toss losers
- Win rate by toss decision (bat / field)
- Season-wise toss advantage trend line
- Data verdict callout with business interpretation

### ⚡ Phase Analysis
- Grouped bar chart: avg runs per phase (Powerplay / Middle / Death) — winners vs losers
- Over-by-over run-rate area chart with phase zone overlays
- Largest run-gap phase highlighted as the "Key Phase"

### 🏆 Hall of Fame
- Top 5 batters: horizontal bar chart + table with Runs, Innings, Avg, SR
- Top 5 bowlers: horizontal bar chart + table with Wickets, Innings, Economy, Avg
- Season-wise top scorer bar chart (hover for player name)

### 📈 Season Trends
- Avg 1st innings score by season
- Avg wickets per innings by season
- Matches played per season
- Boundary % of total runs by season

### 💡 Surprise Insights
- 5 data-backed insights generated automatically from the uploaded dataset
- Box plot: dot-ball % comparison (winning bowlers vs losing bowlers)
- "The one sentence that surprised me most" highlight card

---

## 🔬 Key Technical Decisions

| Decision | Rationale |
|---|---|
| **Pure analysis functions** | `utils/analysis.py` contains no Streamlit calls — fully testable and reusable |
| **`@st.cache_data`** | Data loads once per file upload; filters re-compute instantly |
| **Plotly** over Matplotlib | Interactive hover, zoom, dark-theme native support |
| **CSS variables** | Single-source theming; override once, applies everywhere |
| **Phase bands via `pd.cut`** | Clean, vectorised; no per-row Python loops |
| **Graceful column fallback** | App never crashes on partial CSVs — missing columns default to NaN |


---

## 🏅 Evaluation Criteria Alignment

| Criteria | How This Submission Addresses It |
|---|---|
| **Answers correct & backed by data** (34%) | Every number computed directly from ball-by-ball records; methodology transparent in `analysis.py` |
| **Charts clear enough for anyone to read** (33%) | Labelled axes, colour legends, callout annotation on every chart; no chart without a plain-English verdict box |
| **Surprising finding is actually surprising** (33%) | 5 insights auto-generated from the data; the dot-ball insight is the headline finding |

---

## 🛠️ Tech Stack

| Layer | Tool |
|---|---|
| Language | Python 3.11+ |
| Web Framework | Streamlit 1.35+ |
| Data | Pandas 2.x, NumPy 1.26+ |
| Visualisation | Plotly 5.22+ |
| Styling | Custom CSS (Google Fonts: Bebas Neue, DM Sans, JetBrains Mono) |

---

## 📝 Skills Demonstrated

`Data Analysis` · `Data Preprocessing` · `Exploratory Data Analysis` · `Python` · `Streamlit` · `Plotly` · `Statistical Thinking` · `Data Storytelling`

---

## 👤 Author

Built for **Wooble IPL Crunch '26** analytics challenge.  
Portfolio: [wooble.org](https://wooble.org)

---

## 📄 License

MIT — free to use, modify, and build upon.

---

*"Everyone has IPL opinions. This dashboard backs them with numbers."*
