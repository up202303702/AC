# Project Notes

Everything we know and decided. Source for the slides. Who does what: `docs/task_board.md`.

## Methodology

We follow CRISP-DM, the data mining method from class 1. Its six phases and where we are:

1. **Business understanding:** done (Task (a) and Task (b) below).
2. **Data understanding:** table descriptions done; plots and findings in progress.
3. **Data preparation:** team table, roster information, data quality checks and new teams done; coach table and the coach cases in progress.
4. **Modeling:** started. Test loop, simple guesses and first models for (a) done (see Modeling below); (b) waits for the coach table.
5. **Evaluation:** after the checkpoint.
6. **Deployment:** final predictions and presentation.

## Task (a): Final ranking

- **What we predict:** each team's position in its division, the `rank` column (1st to last; from 1979 divisions had 4 to 7 teams).
- **Season to predict:** any season requested, using only data from before it.
- **We can use:** anything known the day before the first game, including the new season's rosters.
- **Who wants it:** stakeholders (club management, sponsors, the league) and betting: know before the season how teams will finish.
- **How we measure it:** on average, how many positions off our prediction is.
- **Simple guess to beat:** inside each division, the same order as last season's points per game (new teams last). Tested season by season (`src/evaluation.py`, `notebooks/03_modeling.ipynb`): scores 1.07 positions off on average over 2000–2009; random order scores 1.55.

## Task (b): Coach change

- **What we predict:** for each team, yes or no: does it start the season with a different coach than the one who finished last season?
- **Season to predict:** any season requested, using only data from before it.
- **We can use:** anything known the day before the first game, except the new season's coach (that is the answer).
- **Who wants it:** stakeholders (club management, sponsors, the league) and betting: know before the season which teams will have a new coach.
- **Missing a real change is much worse than a false alarm.** So we measure how many real changes we catch ("recall"), and check how many false alarms we raise ("precision").
- **Simple guess to beat:** a team gets a new coach if it missed the playoffs last season.

## Data facts

- 1909–2009, leagues NHA, NHL, PCHA, WCHL, WHA. 2004 is missing (lockout).
- Teams move cities: follow a team with `franchID`, not `tmID`.
- About 1 in 4 NHL teams starts a season with a new coach.

## Data preparation

- **Data used:** NHL only, 1979–2009 (753 team-seasons). From 1979 the NHL is the only league in the data; earlier leagues are small and from a different era. Decided by the group; the professor agreed (less data, but more similar to today). Can be changed with `FIRST_YEAR` in notebook 02, and a different start year per task is worth testing later.
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
| 5 | Coaches: interim, co-coaches (DET 1998), empty games (OTT 2001) | 6 | Proposal: ignore interim and co-coaches for first/last coach; add up all spells of the same coach | Open (coach table) |
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

### Task (b)

Not started: needs the coach table (coach change yes/no and coach information). Simple guess planned: new coach if the team missed the playoffs last season.

### Next steps

- Task (b): coach table, simple guess, first model.
- More model types (a single decision tree to show on a slide, k-nearest neighbours, gradient boosting), chosen with the practice test.
- Feature selection (filter and wrapper), starting from the overlapping pairs.
- Task (c), once announced.

## Checkpoint (6 November)

- Business understanding, data understanding and data preparation done for task (a); the final team table has 753 rows and no empty values.
- First answer for (a): about 1 position off on average (best model 1.02, simple guess 1.07, random 1.55); no model proven better than the simple guess yet.
- Task (b) not started (coach table missing).

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
| [coach_changes.png](../figures/coach_changes.png) | |
| [coach_change_vs_results.png](../figures/coach_change_vs_results.png) | |
