# Task Board

Move a task to the right section when its status changes. Owner in brackets.

## To do

- [Person 2] First models for (b): logistic regression and decision tree, with class weights; recall, precision, AUC
- [Person 3] Feature selection for (a): filter (correlation, drop overlapping) and wrapper (add/remove one at a time, practice test)
- [Person 3] Quality checks on the coach columns
- [Person 3] For (b): compare SMOTE vs class weights, applied to training seasons only
- [Group] Agree on the coach cases with Person 2: interim coaches, co-coaches (DET 1998), empty games (OTT 2001) (`docs/project_notes.md`, "Missing and odd values", case 5)
- [Group] Task (c), once announced

## In progress

- [Person 3] Apply the agreed decisions and save the final table (new teams and division size done; coach columns and coach cases still to apply)
- 
- [Person 2] Plot: last season's results, kept vs changed coach (with test), with finding
- [Person 2] Plot: coach changes per season, with finding

TODO: plot conclusions

- [Person 2] Simple guess for (b): new coach if the team missed the playoffs, scored with the test loop

## Done

- [Person 1] New inputs for (a): 3-season average, roster change, new coach
- [Person 1] More model types for (a): decision tree, k-nearest neighbours, gradient boosting (practice test)
- [Person 1] Feature importance and decision tree figure for (a)
- [Person 1] First model for (a)
- [Person 3] Plots: missing values map, goals scored vs conceded, correlations, with findings
- [Person 3] 6 data quality checks (chapter 4 / Lab 2: keys, joins, missing, redundant, inconsistent, outliers)
- [Person 3] List of missing and odd values, with a proposed decision for each
- [Group] How to fill the 13 new teams
- [Group] Goalies with no earlier season and ex-WHA rosters: kept as they are, noted as limits
- [Group] Confirm the data used: NHL only, 1979–2009
- [Group] Business understanding: goals, who wants it, how we measure it, simple guesses to beat
- [Group] Description of every table (`notebooks/01_data_overview.ipynb`, `docs/project_notes.md`)
- [Person 1] Plots: teams per season, points last vs this season, goals per game, with findings
- [Person 1] Team table, one row per team per season (`data/team_table.csv`)
- [Person 1] Roster information for (a): how good each team's players were last season
- [Person 1] Season-by-season test loop (train on earlier seasons, predict the next)
- [Person 1] Simple guess for (a): same position as last season, scored with the test loop
- [Person 2] Coach table (new coach yes/no + coach info), joined to `data/team_table.csv`
