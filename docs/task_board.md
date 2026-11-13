# Task Board

Owner in brackets. Move a task to "Done" when finished. Why each task exists: `docs/grading_checklist.md`.
Deadline: **4 December**. Before working: `git pull`. After: commit and push.

## Week 1 · 16–22 November: data for (c), conference ranking, preparation

- [Person 1] Redo the other (a) models (tree, kNN, boosting, importance, tree figure) with the conference ranking (notebook 03, section "ranking per conference")
- [Person 1] Learning curve (train on 3, 5, 10, 20 seasons) and tree-depth plot (training vs test error), for (a) and (c)
- [Person 1] Business understanding for (c) and the goal → DM goal table (`docs/project_notes.md`)
- [Person 1] Experiment log (`docs/experiment_log.md`): every attempt so far, why, result, kept or not
- [Person 2] Data understanding for (c): PIM distribution, PIM by era and position, season-to-season stability, with tests and findings (notebook 01)
- [Person 2] One 3+D method and one 3+D plot (e.g. clustering players into types; PIM vs games vs points by position)
- [Person 2] Player and coach tables as SQL queries in SQLite (`src/data_loading.py` already builds the database)
- [Person 3] Name the 6 quality dimensions, one check each, also for the player table
- [Person 3] Systematic redundancy removal (correlation limit, inside the training seasons)
- [Person 3] Outliers: discuss enforcers, short seasons, players with few games
- [Person 3] For (c): better guess for players in their first NHL season (16%): a regression on what is known (position, team), training seasons only (notebook 04)

## Week 2 · 23–29 November: models for all three tasks

- [Person 1] Improve (c): fewer, non-overlapping inputs; try a two-step model (PIM per game × expected games)
- [Person 1] Final (a) model per conference, with significance test
- [Person 2] More models for (b): tree, kNN, forest/boosting, naive Bayes; overfitting; importance; tree drawn
- [Person 2] Rebuild `data/team_table_with_coaches.csv` on the current team table
- [Person 2] One part of the work in a second analytics tool from the course
- [Person 3] SMOTE vs class weights for (b), training seasons only
- [Person 3] Feature selection, filter + wrapper, for all three tasks
- [Person 3] Missing values for (c): regression fill for players with no earlier season, training seasons only

## Week 3 · 30 November–4 December: evaluation and presentation

- [Group] Final results table per task: baselines, best model, significance
- [Group] Experiment log complete (`docs/experiment_log.md`)
- [Group] Slides: one section per task, each person presents their part
- [Group] Run-through with a timer

## Done

- [Person 1] (c) player table, baselines (median, position, same as last season, Marcel) and 4 models (`notebooks/04_penalty_minutes.ipynb`): gradient boosting 16.5 minutes off vs Marcel 17.2, better in 9/9 seasons (p = 0.004)
- [Person 1] (a) per conference: real conference rank, baselines, points models with goal difference: 3.16 vs 3.33 positions off, not proven (p = 0.27) (notebook 03)
- [Person 1] Improved (b): "below usual level" and coach playoff win%, AUC 0.68, beats the simple guess (Wilcoxon p ≈ 0.01)
- [Person 1] `conference_rank` and `pim_mae` in `src/evaluation.py`
- [Person 2] First model for (b): logistic regression, AUC 0.62
- [Person 2] Plots: coach changes per season; last season's results, kept vs changed coach (with test)
- [Person 2] Coach table (new coach yes/no + coach info), joined to `data/team_table.csv`
- [Person 1] New inputs for (a): 3-season average, roster change, new coach
- [Person 1] More model types for (a): decision tree, k-nearest neighbours, gradient boosting (practice test)
- [Person 1] Feature importance and decision tree figure for (a)
- [Person 1] First model for (a)
- [Person 3] Plots: missing values map, goals scored vs conceded, correlations, with findings
- [Person 3] 6 data quality checks (keys, joins, missing, redundant, inconsistent, outliers)
- [Person 3] List of missing and odd values, with a proposed decision for each
- [Group] How to fill the 13 new teams
- [Group] Goalies with no earlier season and ex-WHA rosters: kept as they are, noted as limits
- [Group] Data used: NHL only, 1979–2009
- [Group] Business understanding for (a) and (b)
- [Group] Description of every table (`notebooks/01_data_overview.ipynb`, `docs/project_notes.md`)
- [Person 1] Plots: teams per season, points last vs this season, goals per game, with findings
- [Person 1] Team table, one row per team per season (`data/team_table.csv`)
- [Person 1] Roster information for (a)
- [Person 1] Season-by-season test loop
- [Person 1] Simple guess for (a)
