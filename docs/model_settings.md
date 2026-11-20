# Model settings: what went in, what we tried, what was chosen, why

For every model: the **inputs**, the **settings tried**, the setting the **practice test chose** (most often, over the 9 test seasons) and **why** those values. All values are copied from the notebooks. What the inputs mean: glossary at the end.

## Short version (what to say)

- **Linear regression:** we tried 2, 3 or 5 inputs; the practice test picked the set each season.
- **Decision tree:** kept shallow (2–4 questions in a row), because deeper trees memorised; the depth curve shows it.
- **k-nearest neighbours:** we tried small and large neighbourhoods; with our amount of data the larger one worked best.
- **Gradient boosting:** many small trees with a slow learning rate, the safe choice for small data; in (c) trained on absolute error, the same error we score with.
- **Logistic regression (b):** changes are rare (26%), so they were weighted more; the yes/no cut-off was set low, because missing a change is worse than a false alarm.
- **Clusters, recent-season weighting, ensembles:** the practice test chose the number of groups and how much recent seasons count.
- **The rule behind all of them:** from simple to complex, chosen fairly on practice seasons, never on the test.

The tables below are the detail, for the slides (one compact table per task) and for questions.

---

**How settings are chosen (all models):** before each test season, every setting is trained on the training seasons except the last 3, and scored on those 3 ("practice test", `pick_with_practice_test`). The best one is retrained on all training seasons and then scored on the test season. The test season is never used to choose.

**Why small grids (2–6 values per setting):** every value is retrained 4 times per test season × 9 test seasons. The grids cover "simple" to "complex" so the practice test can show where memorising starts, without testing hundreds of values on only 30 teams per season.

---

## Task (a): conference ranking (notebooks 03, 05, 06)

All models predict **points per game vs the season average** (`pts_vs_avg`); the NHL rules (`conference_rank`) turn the prediction into positions.

**Input sets**
- 3 inputs: `last_pts_vs_avg`, `avg3_pts_vs_avg`, `last_gd_per_game`
- 5 inputs: the 3 + `roster_pts_vs_avg`, `roster_goalie_ga_vs_avg`
- Style inputs (clusters only): `last_gf_vs_avg`, `last_ga_vs_avg`, `last_pim_vs_avg`, `last_pp_pct`, `last_pk_pct`

| Model | Inputs | Settings tried | Chosen | Why these values |
|---|---|---|---|---|
| Linear regression | 2, 3 or 5 inputs (practice test chooses the set) | input set only (no settings) | 2 inputs (2 seasons), 3 inputs (3), 5 inputs (4) | Tests whether goal difference and the roster add information |
| Decision tree | 5 | depth 2, 3, 4 × minimum teams per final box 10, 30 | depth 3, 10 teams | The tree learns from about 500–720 team-seasons. The depth curve (notebook 05) shows memorising from depth 4 on, so 2–4 covers "too simple" to "starts memorising"; at least 10–30 teams per box (⅓ to 1 season) stops a box from describing a handful of teams |
| k-nearest neighbours | 5, scaled (StandardScaler) | k = 10, 25, 50 neighbours | k = 50 | About 500–720 team-seasons to learn from: 10 is "very local", 50 is "smooth". Scaling so no input dominates the distance |
| Gradient boosting | 5 | 50 or 150 trees × depth 2 or 3; learning rate 0.05; each tree on 80% of the data | 50 trees, depth 2 | Small, shallow trees and a slow learning rate are the usual safe choice for small data; 150 trees and depth 3 test whether more complexity helps |
| Pairwise logistic | differences of the 3 or 5 inputs between two teams (scaled, no centring so A−B = −(B−A)) | none (default strength) | — | Each pair appears twice (A vs B, B vs A) so neither position is favoured |
| Voting | 5 | fixed: linear + kNN (k = 50) + boosting (50 trees, depth 2) | — | The settings the practice test chose most often for each member |
| K-means team styles + linear | 3 inputs + one 0/1 column per style group | k = 3, 4, 6 groups | k = 3 (5 seasons), 6 (4) | 3 = "strong / average / weak", 6 = finer styles; scaler and k-means fitted on training seasons only |
| Linear, recent seasons weighted | 3 | weight per season = decay^(years ago), decay 1, 0.95, 0.9, 0.8 | 1 (all equal) in 6 of 9 | 0.9 means a season 10 years ago counts 0.35; 0.8 means it counts 0.11 |
| Learning curve (notebook 05) | 3, linear | train on the last 1, 3, 5, 10, 20 or all seasons | — | From "very small" to "all data" |
| Depth curve (notebook 05) | 5, tree with no other limit | depth 1, 2, 3, 4, 6, 8, 12 | best 3 | Wide enough to show memorising clearly |

**First round, per division (kept for the record, notebook 03):** target `rank / div_size`; linear on 3 inputs (`last_pts_vs_avg`, `roster_pts_vs_avg`, `roster_goalie_ga_vs_avg`) or all 9; random forest 200 trees × leaf 5, 20, 40 × depth 3, 6, unlimited (chosen most: leaf 20, depth 3); then on 5 inputs (3 + `avg3_pts_vs_avg`, `new_coach`): tree depth 2–4 × leaf 10, 30 (chosen: depth 4, leaf 30), kNN k = 10, 25, 50, 100 (chosen: 25), boosting 50/150 trees × depth 2/3 (chosen: 50, depth 3).

## Task (b): coach change (notebook 03)

**Model:** logistic regression with `class_weight="balanced"` (changes, only 26%, count as much as non-changes), missing values filled with the median plus a "was missing" column (`SimpleImputer`), inputs scaled (StandardScaler).

| Input set | Inputs |
|---|---|
| Person 2's 4 | `coach_seasons`, `last_coach_win_pct`, `last_pts_vs_avg`, `last_season_coaches` |
| + made playoffs | the 4 + `last_made_playoffs` |
| + playoff win% | the 4 + `last_made_playoffs`, `last_coach_po_win_pct` |
| + below usual | the 4 + `last_made_playoffs`, `last_coach_po_win_pct`, `pts_vs_usual` |
| split win% | `coach_seasons`, `last_coach_reg_win_pct`, `last_coach_po_win_pct`, `last_made_playoffs`, `last_pts_vs_avg`, `last_season_coaches`, `pts_vs_usual` |

- **Chosen by the practice test:** "+ below usual" in 6 seasons, "split win%" in 3.
- **Cut-off for "yes, new coach":** tried 0.3, 0.4, 0.5, 0.6; chosen with a score that counts recall twice as much as precision (F2), because missing a change is worse than a false alarm. Chosen: 0.3 (4 seasons), 0.4 (3), 0.5 (2).

## Task (c): penalty minutes (notebooks 04, 05, 06)

**Inputs (20, all from earlier seasons or the starting roster):** `PIM_1`, `PIM_2`, `PIM_3`, `GP_1`, `GP_2`, `GP_3`, `rate_1`, `career_rate`, `marcel_rate_vs_league`, `games_guess`, `pts_rate_1`, `seasons_before`, `first_season`, `pos_C`, `pos_D`, `pos_L`, `pos_R`, `pos_G`, `team_style_last`, `league_rate_last`. Missing history is −1 for linear, tree and kNN; gradient boosting handles missing values itself.

| Model | Settings tried | Chosen | Why these values |
|---|---|---|---|
| Marcel (rule, no learning) | weights 5, 4, 3 for the last 3 seasons; 100 games of league average added; games guess = 0.5 × last season's games + 0.1 × the season before + 20 | — | The standard Marcel recipe (Tom Tango); compared with the league rate of each season because penalties per game changed by era |
| Linear regression | none | — | Scaled inputs |
| Decision tree | depth 4, 6, 8; at least 50 players per box; splits chosen by absolute error | depth 4 | ~900 players per season allows deeper trees than (a); absolute error to match MAE |
| k-nearest neighbours | k = 25, 100 | k = 100 | Many more rows than (a), so larger neighbourhoods are possible |
| **Gradient boosting (final model)** | learning rate 0.05 or 0.1 × 7 or 15 leaves per tree; 300 trees; at least 40 players per leaf; **loss = absolute error** | 0.05, 7 leaves | Absolute error = what MAE measures (not pulled by enforcers); small trees + slow learning = less memorising |
| Log transform test | linear and boosting (squared error), learning log(1 + PIM) | — | Tests the usual fix for a skewed target |
| Rate × games | rate: boosting (squared error) on PIM per game, each player weighted by his games; games: boosting (absolute error) on games played, capped at 82 | — | A rate from 80 games is more reliable than one from 2 |
| Two-step | classifier (boosting): any PIM?; regressor (boosting, absolute error) on players with PIM > 0; cut-off 0.5 | — | 12% of player-seasons have 0 |
| Stacking | members: linear, tree (depth 6, 50 per box), kNN (k = 100), boosting; weights ≥ 0 learned on the 3 practice seasons | weights change by season (e.g. linear 0.03–0.57) | Weights learned without seeing the test season |
| Boosting, recent seasons weighted | decay 1, 0.95, 0.9 | 1 (all equal) in 6 of 9 | Same idea as (a) |
| Learning curve (notebook 05) | train on the last 1, 3, 5, 10, 20 or all seasons | — | From "very small" to "all data" |
| Depth curve (notebook 05) | tree depth 1, 2, 4, 6, 8, 12, 16 | best 6 | Wider than (a) because there is more data |

---

## Glossary: what each input means

| Input | Meaning |
|---|---|
| `last_pts_vs_avg` | Team's points per game last season ÷ league average (1.0 = average) |
| `avg3_pts_vs_avg` | Same, averaged over the last 3 seasons |
| `last_gd_per_game` | Goals scored minus conceded per game, last season |
| `last_pyth` | Pythagorean expectation last season: GF² ÷ (GF² + GA²) |
| `roster_pts_vs_avg` | Points last season of the players on this season's roster, vs average |
| `roster_goalie_ga_vs_avg` | Goals conceded per 60 minutes last season by this season's goalies, vs average (higher = worse) |
| `last_gf_vs_avg`, `last_ga_vs_avg` | Goals scored / conceded per game last season, vs average |
| `last_pim_vs_avg` | Team penalty minutes per game last season, vs average |
| `last_pp_pct`, `last_pk_pct` | Power-play % (goals with an extra player) and penalty-kill % (goals prevented with one less), last season |
| `pts_vs_usual` | Last season's points minus the 3-season average (negative = worse than usual) |
| `coach_seasons` | Seasons the current coach has been with the club |
| `last_coach_win_pct` | Win % of last season's last coach (Person 2's version, includes playoffs) |
| `last_coach_reg_win_pct`, `last_coach_po_win_pct` | The same coach's win % in the regular season / in the playoffs (0 if no playoffs) |
| `last_season_coaches` | Number of coaches the club used last season (2+ = changed during the season) |
| `last_made_playoffs` | 1 if the team made the playoffs last season |
| `PIM_1`, `PIM_2`, `PIM_3` | Player's penalty minutes 1, 2, 3 seasons ago |
| `GP_1`, `GP_2`, `GP_3` | Player's games 1, 2, 3 seasons ago |
| `rate_1` | Penalty minutes per game last season |
| `career_rate` | All earlier penalty minutes ÷ all earlier games |
| `marcel_rate_vs_league` | Marcel's rate (see above), compared with the league rate (1.0 = league average) |
| `games_guess` | Marcel's guess of games: 0.5 × last season + 0.1 × the season before + 20 |
| `pts_rate_1` | Player's points per game last season |
| `seasons_before` | Number of earlier NHL seasons |
| `first_season` | 1 if he has no earlier NHL season |
| `pos_C`, `pos_D`, `pos_L`, `pos_R`, `pos_G` | Position: centre, defence, left wing, right wing, goalie |
| `team_style_last` | His team's penalty minutes per game last season |
| `league_rate_last` | League penalty minutes per game last season |
