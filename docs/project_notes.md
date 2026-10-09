# Project Notes

The source for the BU, EDA and plan slides. Methodology: **CRISP-DM**.

## Lecturer's answers

| # | Question | Answer |
|---|---|---|
| 1 | Ranking: division, conference or league? | TODO |
| 2 | What counts as "changing coaches"? | **Between seasons:** the team starts the new season with a different coach from the previous season. |
| 3 | Can we use new-season info known before the first game? | **Yes, and we should** (e.g. rosters). |
| 4 | Test season, files we'll get, prediction format? | TODO |

## Business goals → DM goals

| | (a) Ranking | (b) Coach change |
|---|---|---|
| Business goal | TODO | TODO |
| DM goal | TODO | Per team: does the season's **first coach** differ from the **last coach of the previous season**? (yes/no) |
| Task type | TODO (justify) | Binary classification, ~26% "yes" (NHL 1967–2009) |
| Metric | TODO (justify) | TODO: why not accuracy? |
| Baseline | TODO | TODO |

## Data facts

- 1909–2009, leagues NHA, NHL, PCHA, WCHL, WHA. Season 2004 missing (lockout).
- `Teams.rank` = position within the division (2009: 6 divisions × 5 teams).
- Use `franchID`, not `tmID`, to follow a team across seasons (teams relocate).

## EDA findings

| Plot | Finding |
|---|---|
| | |

## Plan

| Class | Lab checkpoint | Done when |
|---|---|---|
| 3 | BU & DU | Questions answered, goals written, first findings |
| 4 | Data prep | Population chosen, missing values and outliers handled |
| 5 | First model | Team-season table, time-based split, baseline + model for (a) |
| 7 | Evaluation check-up | (a) and (b): baseline + several models + metrics |
| 8–10 | Development | (c), tuning, feature selection, final predictions, slides |
| 11 | Presentations | Submit by Dec 3 |
