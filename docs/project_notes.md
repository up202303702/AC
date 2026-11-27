# Project notes

We predict three things about an NHL season, using only what is known the day before it starts:

- (a) where each team finishes in its conference
- (b) whether each team starts the season with a new coach
- (c) how many penalty minutes (PIM) each player gets

What is done is below, task by task, and what is left is at the end. The reasons behind every choice are in `decisions.md`, model settings in `model_settings.md`, every attempt in `experiment_log.md`, and the grading grid in `grading_checklist.md`.

## Where things are

| File | What it does |
|---|---|
| `notebooks/01_data_overview.ipynb` | Description of every table, plots, and multivariate plots for (a) and (b) |
| `notebooks/02_data_preparation.ipynb` | Team table, roster, coach table, quality checks, new teams |
| `notebooks/03_modeling.ipynb` | Models for (a) and (b) |
| `notebooks/04_penalty_minutes.ipynb` | Player table and models for (c) |
| `notebooks/05_model_behaviour.ipynb` | Learning curves and tree-depth curves for (a) and (c) |
| `notebooks/06_course_methods.ipynb` | Other approaches from the course methods for (a) and (c) |
| `notebooks/07_results_plots.ipynb` | Result plots for all three tasks |
| `src/evaluation.py` | Season-by-season test, practice test, conference ranking, scores |
| `sql/` | The coach-change table (b) and the player-season table (c) as SQL queries (SQLite), run and checked in notebook 02 |
| `R/player_types.R` | Player types and the position test in R (`Rscript R/player_types.R`) |
| `data/` | `team_table.csv`, `team_table_with_coaches.csv`, `player_table.csv` |

Run order: 02 (team tables) → 04 (player table) → 01 (uses both) → 03, 05, 06, 07.

## How we work

- Method: CRISP-DM. We went back several times: the conference clarification changed the target of (a); the first (b) model sent us back to build better inputs; the low first seasons of new teams changed how we fill them.
- Test: each season from 2000 to 2009 (no 2004) is predicted using only earlier seasons. 9 test seasons, score = average.
- Choosing settings: the last 3 training seasons act as a practice test. The test season is never used to choose anything.
- Is a difference real? Wilcoxon test on the 9 season scores. Below 0.05 = proven.
- Every model is compared with simple guesses, including hockey rules that learn nothing.

## Data

- NHL only, 1979–2009 (753 team-seasons, 24,712 player-seasons). From 1979 the NHL is the only league. The learning curves show this is enough data.
- Clubs are followed by `franchID`, because teams move cities and change code.
- Values are per game and compared with the season average (1.0 = average), because season length, scoring and the points system changed.
- 2005 follows 2003 (2004 was cancelled).
- New teams (13) have no last season. They get the average first season of earlier new clubs, because new teams finish low, so the league average would be wrong.
- Roster columns: last season's points of this season's players, and goals conceded by this season's goalies.
- Coaches: interim and co-coach rows (`notes`) are ignored for first/last coach, and split spells of the same coach are added up. `team_table_with_coaches.csv` is built at the end of notebook 02, on the finished team table.
- The coach and player tables are also built in SQL (`sql/`): 100% the same as pandas.
- Players (c): stints in one season are added up; players with no history get the median of first-season players of their position.

## Task (a): ranking in the conference

Ranked per conference with the NHL rules: points only until 1992, the 2 division winners first in 1993–97, the 3 division winners first from 1998. Ties by wins, then goal difference. This reproduces 99.5% of the real ranks (the rest were head-to-head tie-breaks). Models predict points, and the rules turn points into positions.

Measure: average positions off.

| Guess or model | Positions off | Proven better than "same as last season"? |
|---|---|---|
| Random order | 4.87 | |
| Same order as last season | 3.33 | |
| Pythagorean rule (GF² / (GF² + GA²)), no learning | 3.16 | No (p = 0.16) |
| Linear regression with goal difference | 3.16 | No (p = 0.27) |
| k-nearest neighbours, gradient boosting, voting, pairwise ranking | 3.13–3.20 | No |
| Decision tree | 3.37 | No |

Conclusion: no approach beats a simple hockey formula. Goal difference helps, because points include luck in close games that does not last (`luck_next_season.png`). Last season says most of what can be known before a season; what changes during it (trades, injuries) is not in the data.

An earlier version ranked per division (simple guess 1.07, best model 1.02 positions off). It is kept in notebook 03 for the record, but the conference version is the one to present.

## Task (b): coach change

Yes/no per team: does it start the season with a different coach than the one who finished last season? About 26% do.

Measure: AUC (0.5 = coin flip, 1 = perfect), because with only 26% changes, "never changes" is already 74% accurate. Recall comes first: missing a change is worse than a false alarm.

| Guess or model | AUC | Proven better than "missed playoffs"? |
|---|---|---|
| Random | 0.557 | |
| Missed playoffs | 0.563 | |
| Rule "below usual level", no learning | 0.692 | Yes (p = 0.008) |
| Logistic regression, first 4 inputs | 0.616 | No (p = 0.20) |
| Logistic regression with "below usual level" and the coach's playoff win % | 0.683 | Yes (p = 0.012) |
| Naive Bayes / decision tree / random forest (same inputs) | 0.677 / 0.674 / 0.671 | Yes (p ≤ 0.016) |
| Gradient boosting / small neural network / k-nearest neighbours | 0.664 / 0.654 / 0.630 | Boosting and kNN: no; neural network: yes |
| Association rules as a classifier (learned on 1979–1999 only) | 0.678 | — |

- "Below usual level" = last season's points minus the 3-season average. Teams below it change coach 37% of the time, others 16%.
- The model is as good as the one-line rule, but not better: the gain comes from the idea, not from the learning.
- With a low cut-off the model catches 90% of real changes, but flags 75% of teams.
- No overfitting for logistic regression (training AUC 0.69, test 0.67). The tree, random forest and boosting do memorise (training 0.73–0.75); the practice test picked their simplest settings.
- Seven model types, none better than logistic regression or the "below usual" rule: as in (a), the limit is the information, not the algorithm. Every model relies first on "below usual level" (tree: `decision_tree_b.png`).
- Association rules: "below usual AND changed coach mid-season AND coach won < 45%" → 59% change (2× the normal rate, still 1.8× on 2000–09); "at or above usual AND coach won 50%+ of playoff games" → 85% kept (95% on 2000–09).
- Numbers after `team_table_with_coaches.csv` was rebuilt on the final team table (moved by ≤ 0.005 AUC).

## Task (c): penalty minutes

Measure: average minutes off per player (MAE), because a few enforcers with 200+ minutes would dominate a squared error.

What the data shows (notebook 01, "Players and penalty minutes"):
- PIM is skewed (skewness 2.1; median 28, mean 44, 12% zero), so medians, Spearman and rank tests.
- Per game it peaked in 1986–92 and fell by a third; the 2005 rules did not cut it (Mann-Whitney p = 0.93).
- Defencemen get the most, then wings, then centres; goalies almost none (Kruskal-Wallis p ≈ 0).
- A player's PIM rate is as stable as his scoring rate (Spearman 0.83 vs 0.86), his games played are not (0.57): the hard part of (c) is games.
- Four player types (k-means on PIM rate, points per game, games): enforcers ~12%, scorers ~23%, regulars ~41%, part-timers ~25%. Enforcers stayed 10–13% in every era; scorers fell from 33% to ~18%. Same result in R.

| Guess or model | Minutes off | Proven better than Marcel? |
|---|---|---|
| Median for everyone | 27.30 | |
| Same as last season | 18.37 | |
| Marcel (last 3 seasons, pulled toward average) | 17.17 | |
| Linear regression | 17.62 | No (worse) |
| Gradient boosting, trained on absolute error | 16.53 | Yes (9 of 9 seasons, p = 0.004) |

- Boosting wins because it is trained on the same error we measure.
- Last season's PIM matters most, then the career rate.
- The main unknown is how many games a player will play: knowing them would bring the error down to about 12–14 minutes.
- Other approaches tried (rate × games, two-step model, stacking, log of PIM) did not beat boosting. They are in notebooks 04 and 06, with the reasons.

## Still to do

Person 2
- Done (see the task board): data understanding for (c) with clustering, 3+D plots and R; SQL preparation; more models and association rules for (b); coach table rebuilt.

Person 3
- Name the 6 quality dimensions, with one check each (also for the player table).
- Systematic removal of overlapping inputs.
- Outliers: a detection method from the classes, plus a decision.
- SMOTE vs class weights for (b), on training seasons only.
- Feature selection (filter + wrapper).
- Regression-based guess for first-season players in (c), using age, height and weight from `Master.csv`.

Everyone
- Slides, built from `decisions.md`, this file and `figures/`.

## Data quality (notebook 02)

| Check | Result |
|---|---|
| `(franchID, year)` is unique, no duplicates | OK |
| Joins with Coaches, Scoring and Goalies have no orphans | OK |
| Missing values | Only the last-season columns of the 13 new teams (the season before does not exist) |
| Columns determined by others or strongly correlated | `tmID`, `name`, `div_size` are helpers. Overlapping pairs: last points / last rank (−0.84), goals conceded / goalies (0.85) |
| Rules: W+L+T+OTL = games, points = 2W+T+OTL, valid ranks | OK |
| Outliers (z-score, IQR, robust z-score) | 23 flagged, all real extremes, kept. Only doubtful: Quebec 1979 roster (WHA stats) |

Known limits, kept as they are: goalies with no earlier NHL season are left out of the goalie value; the 4 ex-WHA teams of 1979 use WHA stats; the roster includes players called up during the season.

## The data tables

Used: Teams (a, and penalties for c), Coaches (b), Scoring (roster, and c), Goalies (roster). Not used yet, but useful: Master (age, height, weight), TeamVsTeam (head-to-head tie-breaks). The other tables are too old, too short or not relevant (descriptions in notebook 01).

## What each plot shows

Data understanding (notebooks 01, 02)

| Plot | Finding |
|---|---|
| `teams_per_season.png` | From 1979 the NHL is the only league, growing from 21 to 30 teams |
| `goals_per_game.png` | Scoring changes a lot over time (peak in the 1980s), so stats are compared with their season's average |
| `points_last_vs_this.png` | Last season's points predict this season's fairly well (correlation 0.64), but far from perfectly |
| `missing_teams.png` | The only missing values are the 13 new teams' last-season columns |
| `gf_ga_points.png` | Goal difference explains almost all of a team's points (r = 0.96) |
| `correlations.png` | Last season's points relate most to the position; two pairs of inputs overlap |
| `coach_changes.png` | About 1 in 4 teams changes coach each season; the rate depends on the era |
| `points_by_coach_change.png` | Changing coach does not guarantee better results |
| `below_usual_coach_change.png` | Teams below their usual level change coach 37% of the time, others 16% |
| `coach_change_heatmap.png` | How far below usual matters much more than missing the playoffs |
| `luck_next_season.png` | Teams with more points than their goals deserved drop the next season |
| `pca_teams.png` | Teams differ mainly in strength; playing style is a separate dimension that does not decide the ranking |
| `scatter_matrix_a.png` | Several (a) inputs overlap, e.g. last points vs 3-season average (0.83) |
| `division_rule_effect.png` | The division rule changes the conference order for 16% of teams from 1998 |
| `pim_overview.png` | PIM is very skewed (median 28, maximum 409) and fairly stable from season to season (0.71) |
| `pim_distribution.png` | PIM is strongly right-skewed (skewness 2.1); much less on the log scale |
| `pim_by_season.png` | Penalties per game peaked in the late 1980s and fell by a third; 2005 had more, then back to the 2000–03 level |
| `pim_by_position.png` | Defencemen get the most penalties per game, then wings, then centres; goalies almost none |
| `player_types.png` | Four player types in 3 variables: enforcers, scorers, regulars, part-timers |
| `player_types_R.png` | The same four types found in R, with 4 variables (points, PIM, games as size, type as colour) |

Models (notebooks 03–07)

| Plot | Finding |
|---|---|
| `decision_tree_a.png` | The tree first asks about last season's points, then the 3-season average and the goalies |
| `feature_importance_a.png` | Last season's points matter most for (a), then the 3-season average |
| `feature_importance_b.png` | "Below usual level" matters most for (b) |
| `decision_tree_b.png` | The coach-change tree asks first "below its usual level?", then "did the coach win few games?", then "did the club change coach mid-season?" |
| `feature_importance_c.png` | Last season's PIM matters most for (c), then the career rate |
| `learning_curves.png` | (a) needs very little data; (c) improves up to about 10 seasons |
| `tree_depth_curves.png` | Deeper trees memorise: best depth 3 for (a), 6 for (c) |
| `team_styles.png` | Team-style groups mostly re-describe strength |
| `results_a_all.png`, `results_a_seasons.png` | All (a) approaches are close; the differences between seasons are bigger than between approaches |
| `results_a_2009.png` | A real season: right at the top, wrong on teams that changed a lot over the summer |
| `results_b_all.png`, `results_b_seasons.png` | The "below usual" rule and the model are tied, both above "missed playoffs" |
| `results_b_roc_cutoff.png` | Catching more coach changes always means more false alarms |
| `results_c_all.png`, `results_c_seasons.png` | Gradient boosting is best in every season |
| `results_c_errors.png` | Most of the error comes from the few players with 100+ minutes |
