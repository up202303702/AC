# Project Notes

Everything we know and decided. Source for the slides. Who does what: `docs/task_board.md`.

## Methodology

We follow CRISP-DM (the CRISP-DM 1.0 step-by-step guide in the course resources). Its six phases and where we are:

1. **Business understanding:** done for (a), (b) and (c) (below, and the goals table).
2. **Data understanding:** table descriptions and plots for teams and coaches done; players for (c) in progress (Person 2).
3. **Data preparation:** team table, roster, coach table, player table, quality checks, new teams done; feature selection, SMOTE, outliers and the first-season fill in progress (Person 3).
4. **Modeling:** all three tasks have baselines and several model types (below).
5. **Evaluation:** significance tests, overfitting, importance and learning curves done for the main models (below, notebook 05).
6. **Deployment:** the presentation (slides due 4 December).

**Where we went back (CRISP-DM is a loop, not a line):**
- Modeling (a) → business understanding: the professor clarified the ranking is per conference, so the target and the ranking function changed (division → conference).
- Modeling (b) → data preparation: the first model (AUC 0.62) led us back to build new inputs ("below usual level", coach playoff win %).
- Data understanding → data preparation: new teams finished low, so filling them with the league average would be wrong; filled with earlier new clubs instead.

## Goals: business → data mining

| | Business goal | Data mining task | Target | Measure (why) | Baselines |
|---|---|---|---|---|---|
| (a) | Know before the season where each team will finish | Regression of points, then the NHL rules turn points into a ranking | Position in the conference (`conf_rank`) | Average positions off (easy to read) + Wilcoxon vs the simple guess | Random order; same order as last season |
| (b) | Know before the season which teams will start with a new coach | Binary classification | `coach_change` (1 = new coach) | AUC (only 26% are changes, so accuracy is misleading: "never changes" already gets 74%); recall first, because missing a change is worse than a false alarm | "Never changes"; new coach if the team missed the playoffs |
| (c) | Know before the season how many penalty minutes each player will get | Regression | `PIM` in the regular season | MAE in minutes (PIM is very skewed: a few enforcers would dominate a squared error) + Spearman (order of players) | Median; position average; same as last season; Marcel |

## Task (a): Final ranking

- **What we predict:** each team's position in its **conference** (`conf_rank`). Professor's clarification (13 November): if the data has conferences, rank per conference, and divisions can change the points order. Our data has conferences in every season from 1979.
- **NHL rules used** (`conference_rank` in `src/evaluation.py`): 1979–1992 by points; 1993–1997 the 2 division winners are 1st–2nd; 1998–2009 the 3 division winners are 1st–3rd; ties by wins, then goal difference. Reproduces 99.5% of the real division ranks (the rest were head-to-head tie-breaks). Checked against the real 2009–10 playoff seeds: identical.
- **Design decision:** models predict points per game vs the season average, then the rules give the position. The rules are fixed facts, so the model should not have to learn them.
- **Season to predict:** any season requested, using only data from before it.
- **We can use:** anything known the day before the first game, including the new season's rosters, conference and division.
- **Who wants it:** stakeholders (club management, sponsors, the league) and betting: know before the season how teams will finish.
- **How we measure it:** on average, how many positions off our prediction is.
- **Simple guess to beat:** same order as last season's points, with the conference rules: 3.33 positions off (random order: 4.87). The older division results (1.07 simple guess) are kept below for the record; they cannot be compared with conference results, because conferences have 10–15 teams.

## Task (b): Coach change

- **What we predict:** for each team, yes or no: does it start the season with a different coach than the one who finished last season?
- **Season to predict:** any season requested, using only data from before it.
- **We can use:** anything known the day before the first game, except the new season's coach (that is the answer).
- **Who wants it:** stakeholders (club management, sponsors, the league) and betting: know before the season which teams will have a new coach.
- **Missing a real change is much worse than a false alarm.** So we measure how many real changes we catch ("recall"), and check how many false alarms we raise ("precision").
- **Simple guess to beat:** a team gets a new coach if it missed the playoffs last season.

## Task (c): Penalty minutes

- **What we predict:** for every player on a roster, his penalty minutes (`PIM`) in the regular season.
- **Season to predict:** any season requested, using only data from before it. The player's team at the start of the season is known (the roster is known the day before); **his games played this season are not** (injuries, being sent down).
- **Who wants it:** clubs (discipline, planning the line-up: a player in the penalty box cannot help the team), fantasy hockey and betting (PIM is a common category).
- **Data:** `Scoring.csv` (one row per player, season and team: `PIM`, `GP`, `Pts`, `pos`), stints summed per season; `Teams.csv` for each team's penalty style last season. Player table: `data/player_table.csv`, built in `notebooks/04_penalty_minutes.ipynb` (24,712 player-seasons, 1979–2009).
- **What the data looks like:** very skewed (mean 44, median 28, maximum 409, 12% have 0; the top 10% of players take a third of all minutes). Penalties per game changed by era (about 1.26 in 1986–92, 0.73 in 2004–09), so a player's history is compared to the league rate. 16% of player-seasons are a first NHL season (no history).
- **How we measure it:** MAE (average minutes off), plus Spearman (are players in the right order?).
- **Simple guesses to beat:** median for everyone; position average; same as last season; **Marcel** (last 3 seasons weighted 5/4/3, pulled toward the league average with 100 games, times an expected number of games; a classic sports forecast, simple and hard to beat).

## Data facts

- 1909–2009, leagues NHA, NHL, PCHA, WCHL, WHA. 2004 is missing (lockout).
- Teams move cities: follow a team with `franchID`, not `tmID`.
- About 1 in 4 NHL teams starts a season with a new coach.

## Data preparation

- **Data used:** NHL only, 1979–2009 (753 team-seasons). From 1979 the NHL is the only league in the data; earlier leagues are small and from a different era. Decided by the group; the professor agreed (less data, but more similar to today). Can be changed with `FIRST_YEAR` in notebook 02. The learning curves (notebook 05) confirm 1979 gives enough training seasons.
- **Team table:** one row per team per season, saved in `data/team_table.csv`. Built in `notebooks/02_data_preparation.ipynb`.
- **Per game:** points and goals are divided by games played, because season lengths changed.
- **Compared to the season average:** points, goals scored and goals conceded are divided by that season's league average (1.0 = average), because scoring levels and the points system changed (league average points per game: 1.00 in 1979–1998, 1.05 in 1999–2003, 1.12 in 2005–2009). The 2005 season scored 1.13 positions off with the simple guess, close to the 1.07 average, so the lockout did not break predictions.
- **Last season:** taken from the same club (`franchID`), so teams that moved city keep their history. For 2005, last season is 2003 (2004 lockout). Column `last_pts_vs_avg` (last season's points per game compared to the season average).
- **Division size:** kept as a column (4 to 7 teams), because 5th of 5 is last but 5th of 7 is not.
- **New teams:** 13 team-seasons have no previous NHL season (the 4 ex-WHA teams in 1979 and 9 expansion teams). Their last-season columns are empty. In their first season all 13 finished in the bottom half of their division and 8 finished last (0.72 points per game vs 1.03 league average), so filling with the league average would be wrong. Decided: they get the average first NHL season of the clubs that joined before them (only earlier seasons, so no future data), using the 12 expansion clubs of 1967–1974 for the 4 ex-WHA clubs (0.74 points per game, close to the 0.72 of the new teams since 1979). `last_rank` = last place, `last_made_playoffs` = 0, and `new_team` stays as the missing indicator.
- **Roster:** for each team-season, the points of its players (`roster_pts_vs_avg`) and goals conceded per 60 minutes by its goalies (`roster_goalie_ga_vs_avg`) in each player's most recent season before this one, both compared to the season average. Roster = players whose first spell of the season was with that team. Players returning after missed seasons use their last season played; rookies count as 0 (their median first season is 1 point; 67% score under 5).
- **Roster finding:** it adds little beyond last season's team points (a simple model explains 36.8% without it, 37.8% with it), because most players stay with the same team. It does give values for the 13 new teams.
- **Roster limits:** includes players called up during the season; the 4 ex-WHA teams in 1979 use WHA stats, which are inflated (Quebec 1.53); goalies with no earlier NHL season are left out of the goalie value (16 teams where they played over half the minutes). The last two were kept as they are by group decision.
- **Division size:** saved as a whole number.
- **More inputs for (a)** (end of notebook 02): `avg3_pts_vs_avg` (average of the last 3 seasons; one good season can be luck), `roster_change_vs_avg` (last-season points of players who arrived minus those who left, vs an average team) and `new_coach` (1 if the season's first coach is not last season's last coach; allowed for (a) because it is known before the season, never an input for (b) because it is the answer).

### Data quality

Checked in `notebooks/02_data_preparation.ipynb` with the problems from chapter 4 and Lab 2. Noisy data is not checked: the values are counts recorded exactly.

| # | Check | Problem (chapter 4) | Result |
|---|---|---|---|
| 1 | `(franchID, year)` is a key, no duplicated rows | redundant | OK |
| 2 | Joins with Coaches, Scoring and Goalies: no orphans in either direction | missing | OK |
| 3 | Missing values: where, why, missing rows | missing | Only the 5 last-season columns of the 13 new teams, always together (structural: the season before does not exist). No club-season missing; 2004 is the lockout |
| 4 | Constant, determined and strongly correlated columns | redundant | `tmID`, `name`, `div_size` are determined by other columns (helpers, not features). Two almost redundant pairs: `last_pts_vs_avg`/`last_rank` (−0.84) and `last_ga_vs_avg`/`roster_goalie_ga_vs_avg` (0.85) |
| 5 | Rules: W+L+T+OTL = games, points = 2W+T+OTL, ranks 1 to division size, no negatives | inconsistent | OK, 0 rows break a rule |
| 6 | Outliers with z-score, IQR and robust z-score | outliers | 23 values flagged by z-score, all genuine extremes (Edmonton 1980s, first-season expansion teams, Pittsburgh 2005 goalies). Kept. Only doubtful: Quebec 1979 roster (1.53, WHA stats) |

### Missing and odd values

| # | Case | Rows | Decision | Status |
|---|---|---|---|---|
| 1 | New teams have no last season | 13 | Average first NHL season of the clubs that joined before them (expansion clubs since 1967, ex-WHA clubs); `last_rank` = last place; `last_made_playoffs` = 0; `new_team` kept as missing indicator | Decided, applied |
| 2 | Points system changed (1999, 2005); 2005 follows 2003 | all | `last_pts_vs_avg`; 2005 kept | Decided, applied |
| 3 | Players with no last season | 1036 returning, 3910 rookies | Returning: last season played; rookies: 0 | Decided, applied |
| 4 | Goalies with no earlier NHL season left out of the goalie average | 16 teams where they played over half the minutes | Keep as it is: the value comes from the goalies with a record | Decided: limit for the slides |
| 5 | Coaches: interim, co-coaches (DET 1998), empty games (OTT 2001) | 6 | Rows with `notes` (interim and co-coaches) dropped for first/last coach; all spells of the same coach in a season added up | Decided, applied |
| 6 | Ex-WHA clubs in 1979: roster from WHA stats | 4 | Keep as it is (outside the test seasons) | Decided: limit for the slides |
| 7 | `div_size` as a decimal number | all | Whole number | Applied |
| 8 | Roster = players who played during the season | all | Keep; do not use roster size or number of rookies (they depend on how the season goes) | Limit for the slides |

## Modeling

All results use the season-by-season test loop (`src/evaluation.py`): each season from 2000 to 2009 (no 2004) is predicted using only the seasons before it, and the score is the average over the 9 seasons. Code in `notebooks/03_modeling.ipynb`.

### Task (a): first models

Each model learns a team's relative position in its division (`rank / div_size`, so 1st of 5 and 1st of 7 are comparable) and its prediction is turned back into positions inside each division. Plain-language explanation: `docs/modeling_explained.md`.

Versions are chosen fairly with a **practice test** (`pick_with_practice_test` in `src/evaluation.py`): inside the training seasons only, the last 3 are used to choose between versions; the real test season is never looked at.

| Guess or model | Positions off (test) | Training error | Better / equal / worse than simple guess | Wilcoxon p |
|---|---|---|---|---|
| Random order | 1.55 | | | |
| Simple guess: same order as last season | 1.07 | | | |
| **Linear regression, chosen fairly** (chose 3 features in all 9 seasons: last points, roster players, roster goalies) | **1.02** | 1.08 | 5 / 3 / 1 | 0.16 |
| Random forest, chosen fairly (tree detail chosen per season; most often at least 20 teams per leaf, depth 3) | 1.07 | 1.02 | 5 / 1 / 3 | 0.98 |
| First try: random forest, 5 teams per leaf, unlimited depth | 1.07 | **0.57** | | |

- All models beat random order clearly, but none is proven better than the simple guess (all p-values above 0.05): last season's results already carry most of what can be known before the season, and 9 test seasons are too few to prove a gap of about 0.05 positions.
- The linear model with 3 features is the best and the fair choice picks it every season, so 1.02 is not an optimistic number.
- The first-try forest overfitted (0.57 on the seasons it learned from vs 1.07 on new ones). Less detailed trees close that gap (1.02 vs 1.07) but still do not beat the simple guess, and the chosen setting changes from season to season: no forest setting is clearly better.
- Fewer features did better: several features overlap (last points vs last rank −0.84, last goals conceded vs roster goalies 0.85).

### Task (a): new inputs

The practice test chose, before each test season, between the 3-feature linear model alone, plus one new input, or plus all three.

- Result: **0.985 positions off**, the first result below 1. Better than the simple guess in 6 seasons, equal in 2, worse in 1. Wilcoxon p = 0.08: closer, but still not proven.
- Chosen: + new coach (5 seasons), + 3-season average (3), nothing added (1). Roster change was never chosen (Spearman with the position: −0.04).
- This 0.985 is fragile: with a fixed set of 5 inputs (3 features + 3-season average + new coach) the linear model scores 1.04, so the gain came from switching inputs between seasons.

### Task (a): more model types

All with the 5 inputs above and settings chosen by the practice test (`notebooks/03_modeling.ipynb`, "More model types").

| Model | Test error | Better / equal / worse than simple guess | Wilcoxon p | Training error | Setting chosen most |
|---|---|---|---|---|---|
| Linear, 5 inputs | 1.04 | 5 / 1 / 3 | 0.60 | 1.05 | — |
| Simple guess | 1.07 | | | | |
| k-nearest neighbours (inputs rescaled) | 1.07 | 5 / 2 / 2 | 0.47 | 1.05 | k = 25 |
| Gradient boosting | 1.07 | 4 / 2 / 3 | 0.83 | 0.84 | 50 trees, depth 3 |
| Decision tree | 1.14 | 3 / 0 / 6 | 0.32 | 1.01 | depth 4, 30 teams per leaf |

- No model type beats the linear one, and none is proven better than the simple guess.
- Gradient boosting still memorises part of the training seasons (0.84 vs 1.07).
- **Decision tree** (`figures/decision_tree_a.png`, white-box): first split on last season's points (1.09 of the average), then the 3-season average and the goalies. Strong last season and over 3 seasons → highest (0.27–0.39); weak with leaky goalies → lowest (0.91).
- **Feature importance** (`figures/feature_importance_a.png`, scrambling each input in the test seasons): last season's points +0.22 positions off, 3-season average +0.09, roster goalies +0.03, roster players +0.02, new coach −0.02 (no help).
- Overall finding for (a): last season's points first, the 3-season average second, everything else close to nothing; the limit is the information available before the season.

### Task (a): per conference (current target)

`notebooks/03_modeling.ipynb`, section "ranking per conference". Models predict points, the NHL rules give the position.

| Guess or model | Positions off | Better / equal / worse than simple guess | Wilcoxon p | Training error |
|---|---|---|---|---|
| Random order | 4.87 | | | |
| Simple guess: same order as last season | 3.33 | | | |
| Linear: last season + 3-season average | 3.31 | 5 / 0 / 4 | 0.91 | |
| **Linear: + last season's goal difference** | **3.16** | 6 / 2 / 1 | 0.27 | |
| Linear: practice test chooses the input set | 3.18 | 6 / 1 / 2 | 0.23 | |
| k-nearest neighbours (k = 50 most chosen) | 3.18 | 6 / 1 / 2 | 0.25 | 3.51 |
| Gradient boosting (50 trees, depth 2) | 3.20 | 5 / 1 / 3 | 0.27 | 3.40 |
| Decision tree (depth 3) | 3.37 | 4 / 1 / 4 | 0.77 | 3.73 |

- Goal difference helps: it shows a team's real strength better than points, which include luck in close games. Not proven (p above 0.05).
- No model type is proven better than the simple guess; same conclusion as for divisions: the limit is what is known before the season.

### Task (b): coach change

`notebooks/03_modeling.ipynb`, Task (b). AUC over the 9 test seasons (0.5 = coin flip).

| Guess or model | AUC | Better than simple guess | Wilcoxon p |
|---|---|---|---|
| Simple guess: new coach if missed playoffs | 0.56 | | |
| Logistic regression, first 4 inputs (Person 2) | 0.62 | 6 / 9 | 0.20 |
| **Logistic + "below usual level" + coach playoff win %, chosen fairly** | **0.68** | 8 / 9 | 0.012 |
| Logistic, "split win%" set fixed | 0.67 | 9 / 9 | 0.004 |

- New inputs: `pts_vs_usual` (last season's points minus the 3-season average) and `last_coach_po_win_pct` / `last_coach_reg_win_pct` (the coach's playoff and regular-season win %). Coaches with `notes` dropped and split spells summed, as in notebook 02.
- Statistically proven better than the simple guess.
- Weights and importance: below usual level matters most (scrambling it costs 0.12 AUC), then the number of coaches last season and the coach's playoff win %. Clubs replace the coach when the team falls below what it usually achieves; playoff wins protect him.
- No overfitting: training AUC 0.69, test 0.67.
- Cut-off chosen by the practice test with recall counted double: catches 90% of real changes (simple guess 56%), but says "yes" for 75% of teams (precision 26%).

### Task (c): penalty minutes

`notebooks/04_penalty_minutes.ipynb`. MAE in minutes over the 9 test seasons.

| Guess or model | MAE | Better than Marcel | Wilcoxon p vs Marcel | Training MAE (2006–08) |
|---|---|---|---|---|
| Position average | 28.98 | | | |
| Median | 27.30 | | | |
| Same as last season | 18.37 | | | |
| **Marcel** | 17.17 | | | |
| k-nearest neighbours (k = 100) | 17.93 | 1 / 9 | 0.012 | 16.80 |
| Linear | 17.62 | 0 / 9 | 0.004 | 16.65 |
| Decision tree (depth 4) | 17.29 | 4 / 9 | 0.36 | 16.19 |
| **Gradient boosting, absolute error** | **16.54** | 9 / 9 | 0.004 | 15.44 |
| (not allowed) last rate × real games this season | 13.97 | | | |

- Gradient boosting wins because it is trained on absolute error, the same thing MAE measures: it is not pulled up by the few enforcers. Proven better than Marcel. Linear and kNN are significantly *worse* than Marcel.
- Most used inputs: last season's PIM, then the career rate; points per game a little. Position and team style add almost nothing once a player's history is known.
- Log transform of PIM: helps gradient boosting with squared error (17.8 → 17.1), hurts linear regression (17.6 → 18.7). Kept absolute error instead.
- The limit is games played this season (14.0 if they were known).

### Model behaviour (`notebooks/05_model_behaviour.ipynb`)

- **Learning curves** (train on the last 1, 3, 5, 10, 20 or all seasons; `figures/learning_curves.png`): (a) is flat (a 3-input linear model needs only 1 season); (c) improves until about 10 seasons, then flat. Every test season has at least 21 training seasons, so starting in 1979 is enough.
- **Tree depth** (`figures/tree_depth_curves.png`): training error keeps falling with depth while test error falls then rises: best depth 3 for (a), about 6 for (c); deep trees memorise (c at depth 16: 8.9 training vs 23.9 test).

Experiment by experiment, with the reason for each: `docs/experiment_log.md`.

## Checkpoint (6 November)

1. **Goal:** predict, before the season, the division position (a) and coach change (b).
2. **Data:** NHL 1979–2009 (753 team-seasons), stats compared to the season average.
3. **Quality:** keys, joins, missing values, rules and outliers checked; only the 13 new teams had missing values, filled from earlier new clubs.
4. **Testing:** season by season (2000–2009), each season predicted only from earlier ones.
5. **Result (a):** random 1.55, simple guess 1.07, linear model 1.02 (0.985 when the inputs are chosen per season, 1.04 with them fixed). 4 model types tried (linear, tree, k-nearest neighbours, gradient boosting, plus random forest): none proven better than the simple guess. Last season's points matter most, then the 3-season average: last season already says most of what is known before the season.
6. **Missing:** task (b) not started (coach table); feature selection for (a) (Person 3).

## Tables

| Table | One row = | Years | Linked by | Use | Watch out |
|---|---|---|---|---|---|
| Teams | a team in a season | 1909–2009 | tmID + year | **(a) core**: rank, points, goals | Empty `playoff` = missed playoffs. OTL from 1999, shootouts from 2005, power play from 1963. Odd rows: WHA national teams 1977–78, Montreal Wanderers 1917 |
| Coaches | a coach's spell with a team in a season | 1909–2009 | coachID, tmID + year | **(b) core**: coach change comes from here | `stint` = order of coaches that season. 9 interim coaches, 1 co-coach case (DET 1998) |
| Scoring | a player's spell with a team in a season | 1909–2009 | playerID, tmID + year | (a) roster quality | ~35 players per team. Advanced stats (power play, +/-) missing in old years |
| Goalies | a goalie's spell with a team in a season | 1909–2009 | playerID, tmID + year | (a) goalie quality | Shots against (`SA`) missing in 39% |
| Master | one person (player and/or coach) | — | playerID, coachID | Age, experience, height/weight | 268 people were both player and coach |
| TeamsPost | a team's playoff totals in a season | 1913–2009 | tmID + year | Last season's playoff run | Only playoff teams |
| SeriesPost | one playoff series | 1912–2009 | tmIDWinner / tmIDLoser + year | Same, per round | |
| TeamSplits | a team's home/road and monthly record | 1909–2009 | tmID + year | Late-season collapse, home/road form | September always empty |
| TeamVsTeam | a team's record vs one opponent | 1909–2009 | tmID, oppID + year | Probably low | |
| AwardsCoaches | an award won by a coach | 1930–2009 | coachID + year | (b): award winners keep jobs? | 75 rows |
| AwardsPlayers | an award won by a player | 1917–2009 | playerID + year | (a): star players on roster | |
| AwardsMisc, HOF | other awards, Hall of Fame | — | name / hofID | Probably low | |
| abbrev | a code and its meaning | — | Code | Lookup (e.g. playoff codes) | |
| TeamsHalf | half-season standings | 1916–1920 | — | Too old | |
| TeamsSC, ScoringSC, GoaliesSC | Stanley Cup final stats | 1912–1925 | — | Too old | |
| ScoringShootout, GoaliesShootout | shootout stats | 2005–2009 | — | Too short | |
| ScoringSup | extra scoring stats | 1987–1990 | — | Too short | |
| CombinedShutouts | a shared shutout | 1929–2009 | — | Useless | 50 rows |

## Findings (one sentence per plot)

| Plot | Finding |
|---|---|
| [teams_per_season.png](../figures/teams_per_season.png) | The NHA, PCHA and WCHL overlapped with the early NHL until 1925, and the WHA ran alongside it from 1972 to 1978. From 1979 the NHL is the only league, growing from 21 to 30 teams by 2000. |
| [missing_teams.png](../figures/missing_teams.png) | The only empty values are the 5 last-season columns of the 13 new teams (4 in 1979, 9 between 1991 and 2000), always together: the season before does not exist (structural missingness), so they are filled with the first season of earlier new clubs and flagged with `new_team`. |
| [points_last_vs_this.png](../figures/points_last_vs_this.png) | Points per game last season and this season have a correlation of 0.64 (0.62 for 1979–2009 only): a team's previous season is a good guide to the next, but far from perfect, so other information (like roster changes) is needed. |
| [goals_per_game.png](../figures/goals_per_game.png) | Goals per game change a lot over time: lowest in 1928 (1.5), a jump during World War II, a peak in the 1980s (about 4.0), then down to about 2.6 by the early 2000s. Even within 1979–2009 scoring levels differ, so team stats are compared to their season's average. |
| [gf_ga_points.png](../figures/gf_ga_points.png) | Goal difference explains almost all of a team's points (r = 0.96 with points per game) and most of its position in the division (Spearman −0.82): teams that score more than they concede finish high. |
| [correlations.png](../figures/correlations.png) | Last season's points are the feature most related to the position (Spearman −0.50), then last rank (0.49), goals scored and conceded (±0.40) and the roster (−0.34 players, 0.31 goalies). Two pairs are almost redundant: last points vs last rank (−0.84) and last goals conceded vs roster goalies (0.85). |
| [coach_changes.png](../figures/coach_changes.png) | About 27% of NHL teams start a season with a new coach, and teams that missed the playoffs change more often than average. The rate depends on the era (about 15% in 1943–67, 30% in 1968–92, 23% in 1993–2009). |
| [points_by_coach_change.png](../figures/points_by_coach_change.png) | Teams that kept their coach had more consistent results, but changing coach did not guarantee improvement: neither group consistently outperformed the other. |
| [pim_overview.png](../figures/pim_overview.png) | PIM is very skewed (median 28, maximum 409, 12% of players have 0) and fairly stable from one season to the next (Spearman 0.71), so a player's own history is the main input for (c). |
| [learning_curves.png](../figures/learning_curves.png) | (a) is flat: a 3-input linear model learns as well from 1 season as from all. (c) improves until about 10 seasons, then flat. Starting in 1979 gives every test season at least 21 training seasons: enough. |
| [tree_depth_curves.png](../figures/tree_depth_curves.png) | Deeper trees keep lowering the training error while the test error rises again (best depth 3 for (a), 6 for (c)): the clearest picture of overfitting in the project. |
| [feature_importance_b.png](../figures/feature_importance_b.png) | "Below its usual level" is by far the most used input for coach changes (0.12 AUC lost when scrambled), then the number of coaches last season and the coach's playoff win %. |
| [feature_importance_c.png](../figures/feature_importance_c.png) | Last season's PIM is by far the most used input for penalty minutes, then the career rate; position and team style add almost nothing once a player's history is known. |
