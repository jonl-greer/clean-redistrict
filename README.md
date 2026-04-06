# Redistricting Precinct Data: Coverage Map & Cleaning Interface
**DATA 31500 — University of Chicago - Spring 2026**
1. **Coverage Map** — an interactive national map showing precinct data availability 
and quality across all 50 states
2. **Cleaning Interface** — a web app that takes raw precinct shapefiles and election 
returns, automatically resolves common data quality issues, and exports a cleaned 
dataset

## Project Structure

    redistrict/
    ├── backend/                   # Python FastAPI server
    │   └── app/
    │       ├── main.py            # Entry point — starts the server
    │       ├── routes.py          # API endpoints
    │       ├── validation.py      # Fuzzy matching and quality checklist
    │       ├── topology.py        # Geometry repair using maup
    │       └── utils.py           # Shared helpers
    ├── frontend/                  # Svelte app — everything the user sees
    │   └── src/
    │       ├── App.svelte         # Root component
    │       └── lib/
    │           ├── CoverageMap.svelte         # National choropleth map
    │           ├── FileUploader.svelte        # Upload boundary + election files
    │           ├── TopologyPanel.svelte       # View and repair geometry errors
    │           ├── MatchingTable.svelte       # Review and confirm precinct matches
    │           ├── ValidationChecklist.svelte # Data quality checks
    │           ├── BeforeAfterChart.svelte    # Visualize impact of cleaning
    │           └── ExportPanel.svelte         # Download cleaned GeoJSON
    ├── data/                      # Data files — most gitignored, see data/README.md
    │   ├── coverage.json          # Coverage scores for all 50 states
    │   └── README.md              # Download instructions for raw shapefiles
    └── validation/
        └── compare.py             # Compares tool output to MGGG ground truth


### Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```
Server runs at `http://localhost:8000`

### Frontend
```bash
cd frontend
npm install
npm run dev
```
App runs at `http://localhost:5173`

---

## Data

Raw shapefiles are not committed to this repo — see `data/README.md` for 
instructions. The only committed data file is `data/coverage.json`.

---
