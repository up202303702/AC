# Task Board

Owner in brackets. Move a task to "Done" when finished. Why each task exists: `docs/grading_checklist.md`.
Deliver slides: **Thursday 4 December**. All analysis finished: **Thursday 27 November**. Before working: `git pull`. After: commit and push.
Results do not count, only the grid (`docs/grading_checklist.md`): no more tuning for better numbers.

## Part 1 · 20–24 November: the missing grid rows (❌ first)

Check-in **Monday 24 November**: everyone says what is done and what is stuck.

- [Person 1] Learning curve (train on 3, 5, 10, 20 seasons), for (a) and (c): "sampling for development"
- [Person 1] Tree-depth plot (training vs test error): overfitting and effect of parameters
- [Person 1] Experiment log (`docs/experiment_log.md`): every attempt so far, why, result, kept or not
- [Person 1] Board in GitHub Projects: "PM tools"
- [Person 2] Data understanding for (c) in notebook 01: PIM distribution, by era and position, season-to-season stability; Spearman, Kruskal-Wallis; one finding per result
- [Person 2] Clustering of player types + one 3+D plot (part in R)
- [Person 2] Player and coach tables as SQL queries in SQLite: "database"
- [Person 3] 6 quality dimensions named, one check each, also for the player table
- [Person 3] SMOTE vs class weights for (b), training seasons only
- [Person 3] Feature selection, filter + wrapper, for all three tasks, training seasons only

## Part 2 · 25–27 November: the partly done rows (🟡)

- [Person 1] Business understanding for (c) and the goal → DM goal → measure → baseline table for all 3 tasks (`docs/project_notes.md`)
- [Person 1] Feature importance and overfitting for (b) and (c) where missing; log transform of PIM with the reason
- [Person 1] Other (a) models with the conference ranking (tree, kNN, boosting)
- [Person 2] More models for (b): tree (drawn), kNN, forest/boosting, naive Bayes; overfitting; importance
- [Person 2] Small neural network on one task
- [Person 2] Rebuild `data/team_table_with_coaches.csv` on the current team table
- [Person 3] Systematic redundancy removal (correlation limit)
- [Person 3] Outliers: detection method from T06 (IQR or isolation forest) + hockey-based decision
- [Person 3] First-season players in (c): regression fill (age, height, weight from `Master.csv`, position), training seasons only
- [Group] One finding sentence under every plot and result

**Friday 27 November: analysis frozen.** After this, nothing new, only fixes.

## Part 3 · 28 November–4 December: slides

- [Group] Slide plan: each slide's message, plot or table, and the grid rows it covers
- [Group] Final results table per task: baselines, best model, significance
- [Group] Slides: one section per task, each person presents their part
- [Group] Run-through with a timer, before 4 December

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
