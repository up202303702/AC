# Grading checklist

Every row of the course grid, the top level it asks for, where we are, and what is missing. The reason behind each decision, row by row: `docs/decisions.md`. P1/P2/P3 = Person 1/2/3. Update the "Now" column when something is done. Tasks and dates: `docs/task_board.md`.

Status: ✅ at top level · 🟡 partly · ❌ missing

## Business understanding (BU)

| Row | Top level | Now | To do | Who |
|---|---|---|---|---|
| Requirements with the end user | Many business objectives + extra relevant business info | ✅ Goals, stakeholders, constraints (day before the season; no games played for (c)), conference clarification, for all 3 tasks (`docs/project_notes.md`) | Slide: list of questions asked to the professor and the answers | P1 |
| Business goals | Clearly and quickly identified | ✅ (a), (b), (c) | — | — |
| Business → data mining goals | DM goals clearly aligned | ✅ Goals table in `docs/project_notes.md` | — | — |

## Data understanding (DU)

| Row | Top level | Now | To do | Who |
|---|---|---|---|---|
| Diversity of statistical methods | Rich and justified set | ✅ Descriptive stats, skewness, Spearman, Wilcoxon, Mann-Whitney, Kruskal-Wallis, chi-square, k-means with silhouette; one line on why each (notebook 01, "Players and penalty minutes") | — | — |
| Complexity of statistical methods | Integrated 3+D methods with clear results | ✅ k-means player types on 3 variables (PIM rate vs league, points per game, games), k by silhouette, repeated in R; team-style clusters (notebook 06); association rules on 11 items (b) | — | — |
| Interpretation of statistical results | Generally correct | 🟡 | One finding sentence under every result | All |
| Knowledge extraction (statistics) | Interesting, novel and non-trivial | ✅ (b) "below its usual level" doubles coach changes (37% vs 16%, chi-square p ≈ 4e-10, holds with or without playoffs); playoff wins protect the coach (rules: 95% kept). (c) PIM rate is as stable as scoring (Spearman 0.83) but games are not (0.57); the 2005 rules did not cut penalties (p = 0.93); enforcers stayed 10–13% of players while scorers fell from 33% to ~18% | — | — |
| Diversity of plots | Rich and justified set | 🟡 | List each plot with why it was chosen | All |
| Complexity of plots | Integrated 3+D plots with clear results | ✅ `player_types.png` (3D + colour), `player_types_R.png` (x, y, size, colour), `coach_change_usual_level.png` (x, y, colour, size), `team_styles.png`, goals scored vs conceded vs points | — | — |
| Presentation (DU) | Well structured | 🟡 Notebook 01: tables, team plots, coach plots, multivariate views of teams and coaches, players (c) | Same structure in the slides: teams → coaches → players | All |
| Interpretation of plots | Generally correct | 🟡 | One finding sentence under every plot | All |
| Visual knowledge extraction | Interesting, novel and non-trivial | ✅ Coach changes gather below the "usual level" diagonal; player types; penalties by era and position | — | — |

## Data preparation (DP)

| Row | Top level | Now | To do | Who |
|---|---|---|---|---|
| Data integration | Format conversion AND matching entities | ✅ tmID → franchID, players across teams and stints, coaches to teams; per game, vs season average | Write it down in one place | P3 |
| Data quality dimensions | 6 dimensions | 🟡 6 checks, but not named as dimensions | Name them: accuracy, completeness, consistency, uniqueness, timeliness, validity, with one check each (also for the player table) | P3 |
| Redundancy | Systematic removal of redundant attributes | 🟡 | Correlation matrix, drop one of every pair above a fixed limit (e.g. 0.9), done the same way for all three tasks, inside the training seasons | P3 |
| Missing data | Complex method (regression/classification) with correct setup | 🟡 Simple fill (average of earlier new teams) | For (c), players with no earlier season (18%): predict their PIM rate with a regression on position and other known values, learned on training seasons only | P3 |
| Outliers | Identify, discuss, address with complex or domain approach | 🟡 Identified | Domain approaches: per-game values (short 1994 season); Marcel pulls players with few games toward the league average; enforcers kept but measured with MAE | P3 |
| Transformation for algorithms | Adequate complex discretization or rescaling | ✅ Values vs season average and vs league rate; StandardScaler inside pipelines; log(1 + PIM) tested with reasons (notebook 04, section 8) | — | — |
| Feature engineering | Complex methods AND business knowledge | ✅ Roster aggregation, 3-season averages, "below usual level", coach playoff win%, goal difference, Marcel, career rate, team style | — | — |
| Sampling, domain-specific | Adequate subset of the population | ✅ NHL 1979–2009, justified; learning curves confirm 1979 is enough | (c): goalies kept, with position as input (they get almost 0) | — |
| Sampling for development | Start very small, grow to significant | ✅ Learning curves 1 → 20 → all seasons for (a) and (c) (notebook 05) | — | — |
| Imbalanced data | SMOTE used correctly | ❌ class_weight only | SMOTE inside the training seasons only (imblearn pipeline), compared with class weights | P3 |
| Feature selection | Filter AND wrapper, used correctly | ❌ | Filter (correlation) + wrapper (add one input at a time, practice test), inside training seasons, for all three tasks | P3 |

## Predictive modeling

| Row | Top level | Now | To do | Who |
|---|---|---|---|---|
| Diversity of tasks | Classification AND regression | ✅ (b) classification; (a), (c) regression | — | — |
| Diversity of algorithms | 4+ with very different biases | ✅ (a) linear, tree, kNN, boosting, forest, pairwise logistic, voting; (b) logistic, tree, kNN, random forest, gradient boosting, naive Bayes, neural network, association rules; (c) linear, tree, kNN, boosting, two-step, stacking | — | — |
| Parameter tuning | Systematic | ✅ Practice test over a grid for (a), (b) input sets and cut-off, (c) | List the grids on a slide | — |
| Understanding algorithm behaviour | Majority of algorithms, including the effect of parameters | ✅ Tree-depth curves (notebook 05); explanations of why boosting with absolute error wins (c), why trees fail with ~30 teams (a), why log helps boosting but hurts linear | One line per algorithm on a slide | P1 |
| Training vs test | Correct split, multiple splits | ✅ 9 test seasons, train only on earlier ones | — | — |
| Other factors (time) | Correctly taken into account | ✅ Only data known before the season; 2005 follows 2003 | Checked: all inputs of (b) and (c) come from earlier seasons or the starting roster | — |
| Performance measure | Aligned with DM goals AND data characteristics | ✅ Reasons in the goals table (`docs/project_notes.md`) | — | — |
| Interpretation of measures | Advanced (e.g. AUC) | ✅ AUC in (b) | — | — |
| Baseline | Suitable | ✅ Several levels per task, including hockey rules with no learning: (a) random, last season, 3 seasons, goal difference, Pythagorean, roster; (b) never changes, random, missed playoffs, below usual level, coach playoff win %, mid-season change; (c) median, position, last season, Marcel, ceiling | — | — |
| Analysis of results | Tests for statistical significance | ✅ Wilcoxon for (a), (b), (c) | — | — |
| Overfitting | Correctly estimated and analysed | ✅ (a), (b), (c), plus depth curves; (b) new models: tree 0.73 / forest 0.74 / boosting 0.75 training AUC vs 0.66–0.67 test, logistic and naive Bayes do not memorise | — | — |
| Model improvement | Guided by performance goals | ✅ `docs/experiment_log.md`: goal, attempt, result, decision | Keep adding new attempts | All |
| Feature importance | Correct, related to hockey | ✅ (a), (b), (c) (`figures/feature_importance_*.png`) | — | — |
| White-box models | Correct, related to hockey | ✅ (a) tree, (b) logistic weights, tree drawn (`decision_tree_b.png`) and association rules (AUC 0.678 as a classifier) | — | — |

## Project management and tools

| Row | Top level | Now | To do | Who |
|---|---|---|---|---|
| Methodology | Followed carefully, reflecting on the documentation | ✅ CRISP-DM phases with status and where we went back (`docs/project_notes.md`) | — | — |
| Plan | Detailed plan that guided the work | 🟡 | Dated plan in `docs/task_board.md` (done below), kept up to date | All |
| PM tools | Detailed task sharing with an appropriate tool | 🟡 Markdown board | Move the board to GitHub Projects (issues with owner and date) | P1 |
| Collaboration tools | Easy communication, data, workflows, documentation | 🟡 GitHub + WhatsApp | Keep data, notebooks and docs in GitHub; everyone pulls before working | All |
| Analytics tools | Multiple tools from the course | ✅ Python + R (`R/player_types.R`: Kruskal-Wallis, k-means, plot) + SQL (SQLite) | — | — |
| Database | Extensive use for exploration and preparation | ✅ Preparation: player-season and coach-change tables as SQL queries (`sql/`, window functions), 100% equal to pandas (notebook 02); exploration: penalties per game by season in SQL (notebook 01) | — | — |
| Other tools | Extensive and correct | 🟡 matplotlib, scikit-learn, scipy | Add imbalanced-learn (SMOTE); list all tools with their use | P3 |

## Presentation (last week)

| Row | Top level | To do |
|---|---|---|
| Layout | Simple AND clear | One message per slide, one plot or table |
| Content | To the point | Per task: goal → data → baseline → best model → is it significant → what we learned |
| Delivery | Clear AND confident | Each person presents their part; one run-through before |
| Time | To the point | Time the run-through |
