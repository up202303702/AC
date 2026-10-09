# Ice Hockey Season Prediction: AC Data Mining Project

Predict, for a new season and the day before its first game: (a) the final regular-season ranking, (b) which teams change coach between seasons, (c) TBA.

## Setup

```bash
pip install -r requirements.txt
```

Open `notebooks/01_data_overview.ipynb`. Raw data lives in `hockey_development_data/`; never edit it.

## Rules

- Features for season *T* may only use what is known before *T*'s first game.
- Shared code goes in `src/`. Notes for the slides go in `docs/project_notes.md`.
