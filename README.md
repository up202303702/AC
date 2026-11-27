# Ice Hockey Season Prediction: AC Data Mining Project

Predict, for a new season and the day before its first game: (a) the final regular-season ranking, (b) which teams change coach between seasons, (c) how many penalty minutes each player gets.

## Setup

```bash
pip install -r requirements.txt
```

Open `notebooks/01_data_overview.ipynb`. Raw data lives in `hockey_development_data/`; never edit it.

Run order: `02_data_preparation` (team tables, SQL checks) → `04_penalty_minutes` (player table) → `01_data_overview` (uses both) → `03`, `05`, `06`.

Other tools:
- **SQL:** `sql/coach_changes.sql` and `sql/player_seasons.sql` build the tables for tasks (b) and (c) in SQLite (run and checked in notebook 02).
- **R:** `Rscript R/player_types.R` (from the project folder; base R only) repeats the player-type clustering and the position test of notebook 01.

## Rules

- Features for season *T* may only use what is known before *T*'s first game.
- Shared code goes in `src/`. Notes for the slides go in `docs/project_notes.md`.
