# Grading checklist

Every row of the course grid, the top level it asks for, where we are, and what is missing. P1/P2/P3 = Person 1/2/3. Update the "Now" column when something is done. Tasks and dates: `docs/task_board.md`.

Status: ✅ at top level · 🟡 partly · ❌ missing

## Business understanding (BU)

| Row | Top level | Now | To do | Who |
|---|---|---|---|---|
| Requirements with the end user | Many business objectives + extra relevant business info | 🟡 Goals, stakeholders, "day before the season" rule, professor's answers | Add (c), the conference rule, and a short list of every question we asked the professor and the answer | P1 |
| Business goals | Clearly and quickly identified | 🟡 (a) and (b) | Add (c): who wants PIM predictions (clubs: discipline and line-up planning; betting; fantasy hockey) | P1 |
| Business → data mining goals | DM goals clearly aligned | 🟡 | One table: business goal → DM task type → target column → measure → baseline. (a) regression of points + NHL rules → conference rank; (b) classification, recall first; (c) regression of PIM | P1 |

## Data understanding (DU)

| Row | Top level | Now | To do | Who |
|---|---|---|---|---|
| Diversity of statistical methods | Rich and justified set | 🟡 Descriptive stats, correlations, Wilcoxon, test on coach change vs playoffs | Add for (c): skewness, Spearman (not Pearson, because PIM is skewed), Mann-Whitney or Kruskal-Wallis for PIM by position; one line on why each method | P2 |
| Complexity of statistical methods | Integrated 3+D methods with clear results | ❌ Mostly 1D/2D | One multivariate method per task: e.g. PCA of team stats, or clustering of players into types (enforcers, scorers, defenders) using PIM, points, games | P2 |
| Interpretation of statistical results | Generally correct | 🟡 | One finding sentence under every result | All |
| Knowledge extraction (statistics) | Interesting, novel and non-trivial | 🟡 "Below its usual level" predicts a coach change; playoff wins protect the coach | Same for (c): e.g. the 2005 rule change cut penalties per game; how stable PIM is from season to season | P2 |
| Diversity of plots | Rich and justified set | 🟡 | List each plot with why it was chosen | All |
| Complexity of plots | Integrated 3+D plots with clear results | 🟡 Goals scored vs conceded vs points | Add 3+D plots: PIM vs games vs points coloured by position; coach change vs last season vs 3-season average coloured by outcome | P2 |
| Presentation (DU) | Well structured | 🟡 | Notebook 01 in sections: teams, coaches, players; same structure in the slides | P2 |
| Interpretation of plots | Generally correct | 🟡 | One finding sentence under every plot | All |
| Visual knowledge extraction | Interesting, novel and non-trivial | 🟡 | See "knowledge extraction" above | P2 |

## Data preparation (DP)

| Row | Top level | Now | To do | Who |
|---|---|---|---|---|
| Data integration | Format conversion AND matching entities | ✅ tmID → franchID, players across teams and stints, coaches to teams; per game, vs season average | Write it down in one place | P3 |
| Data quality dimensions | 6 dimensions | 🟡 6 checks, but not named as dimensions | Name them: accuracy, completeness, consistency, uniqueness, timeliness, validity, with one check each (also for the player table) | P3 |
| Redundancy | Systematic removal of redundant attributes | 🟡 | Correlation matrix, drop one of every pair above a fixed limit (e.g. 0.9), done the same way for all three tasks, inside the training seasons | P3 |
| Missing data | Complex method (regression/classification) with correct setup | 🟡 Simple fill (average of earlier new teams) | For (c), players with no earlier season (18%): predict their PIM rate with a regression on position and other known values, learned on training seasons only | P3 |
| Outliers | Identify, discuss, address with complex or domain approach | 🟡 Identified | Domain approaches: per-game values (short 1994 season); Marcel pulls players with few games toward the league average; enforcers kept but measured with MAE | P3 |
| Transformation for algorithms | Adequate complex discretization or rescaling | 🟡 StandardScaler, vs season average | Add log transform of PIM and explain why (skewed); scaling only inside the pipeline | P1 |
| Feature engineering | Complex methods AND business knowledge | ✅ Roster aggregation, 3-season averages, "below usual level", coach playoff win% | Add for (c): Marcel weighted average, PIM per game, career rate | P1 |
| Sampling, domain-specific | Adequate subset of the population | ✅ NHL 1979–2009, justified | (c): decide and justify goalies (separate rule or left out) | P1 |
| Sampling for development | Start very small, grow to significant | ❌ | Learning curve: train on the last 3, 5, 10, 20 seasons and show the error; this also justifies starting in 1979 | P1 |
| Imbalanced data | SMOTE used correctly | ❌ class_weight only | SMOTE inside the training seasons only (imblearn pipeline), compared with class weights | P3 |
| Feature selection | Filter AND wrapper, used correctly | ❌ | Filter (correlation) + wrapper (add one input at a time, practice test), inside training seasons, for all three tasks | P3 |

## Predictive modeling

| Row | Top level | Now | To do | Who |
|---|---|---|---|---|
| Diversity of tasks | Classification AND regression | ✅ (b) classification; (a), (c) regression | — | — |
| Diversity of algorithms | 4+ with very different biases | 🟡 (a) has 5; (b) only logistic | (b): decision tree, k-nearest neighbours, random forest or boosting, naive Bayes. (c): linear, tree, kNN, boosting | P2 (b), P1 (c) |
| Parameter tuning | Systematic | ✅ Practice test over a grid | Same for (b) and (c); list the grids | All |
| Understanding algorithm behaviour | Majority of algorithms, including the effect of parameters | 🟡 | One plot: training vs test error as tree depth grows (shows overfitting); one line per algorithm on how it learns | P1 |
| Training vs test | Correct split, multiple splits | ✅ 9 test seasons, train only on earlier ones | — | — |
| Other factors (time) | Correctly taken into account | ✅ Only data known before the season; 2005 follows 2003 | Check every new input of (b) and (c) for leaks | All |
| Performance measure | Aligned with DM goals AND data characteristics | 🟡 | Write why: (a) positions off + Spearman (order matters); (b) AUC + recall (imbalanced, missing a change is worse); (c) MAE (skewed, in minutes) + RMSE + Spearman | P1 |
| Interpretation of measures | Advanced (e.g. AUC) | ✅ AUC in (b) | — | — |
| Baseline | Suitable | 🟡 | 4 levels per task: no information, same as last season, hockey knowledge, ceiling (not allowed) | All |
| Analysis of results | Tests for statistical significance | ✅ (a), (b) Wilcoxon | Same for (c) | P1 |
| Overfitting | Correctly estimated and analysed | ✅ (a) | Same for (b) and (c) | P2, P1 |
| Model improvement | Guided by performance goals | 🟡 | Experiment log: each attempt, why, result, kept or not (`docs/experiment_log.md`) | All |
| Feature importance | Correct, related to hockey | ✅ (a) | Same for (b) and (c) | P2, P1 |
| White-box models | Correct, related to hockey | ✅ (a) tree, (b) logistic weights | Tree for (b) and (c) | P2, P1 |

## Project management and tools

| Row | Top level | Now | To do | Who |
|---|---|---|---|---|
| Methodology | Followed carefully, reflecting on the documentation | 🟡 CRISP-DM in the notes | Notes ordered by CRISP-DM phase; one line per phase on what we went back and changed | P1 |
| Plan | Detailed plan that guided the work | 🟡 | Dated plan in `docs/task_board.md` (done below), kept up to date | All |
| PM tools | Detailed task sharing with an appropriate tool | 🟡 Markdown board | Move the board to GitHub Projects (issues with owner and date) | P1 |
| Collaboration tools | Easy communication, data, workflows, documentation | 🟡 GitHub + WhatsApp | Keep data, notebooks and docs in GitHub; everyone pulls before working | All |
| Analytics tools | Multiple tools from the course | ❌ Python only | Run at least one part in a second tool shown in class (check which ones the labs used) | P2 |
| Database | Extensive use for exploration and preparation | ❌ SQLite built, hardly used | Do real preparation steps in SQL: e.g. the player-season table and the coach table as SQL queries | P2 |
| Other tools | Extensive and correct | 🟡 matplotlib, scikit-learn, scipy | Add imbalanced-learn (SMOTE); list all tools with their use | P3 |

## Presentation (last week)

| Row | Top level | To do |
|---|---|---|
| Layout | Simple AND clear | One message per slide, one plot or table |
| Content | To the point | Per task: goal → data → baseline → best model → is it significant → what we learned |
| Delivery | Clear AND confident | Each person presents their part; one run-through before |
| Time | To the point | Time the run-through |
