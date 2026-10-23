# Project Notes

Everything we know and decided. Source for the slides. Who does what: `docs/task_board.md`.

## Methodology

We follow CRISP-DM, the data mining method from class 1. Its six phases and where we are:

1. **Business understanding:** done (Task (a) and Task (b) below).
2. **Data understanding:** table descriptions done; plots and findings in progress.
3. **Data preparation:** team table and roster information done; coach table, missing values and outliers in progress.
4. **Modeling:** started. Season-by-season test loop and the simple guess for (a) done; first models before the checkpoint.
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
- **Compared to the season average:** goals scored and conceded are divided by that season's league average (1.0 = average), because scoring levels changed over time.
- **Last season:** taken from the same club (`franchID`), so teams that moved city keep their history. For 2005, last season is 2003 (2004 lockout).
- **Division size:** kept as a column (4 to 7 teams), because 5th of 5 is last but 5th of 7 is not.
- **New teams:** 13 team-seasons have no previous NHL season (the 4 ex-WHA teams in 1979 and 9 expansion teams). Their last-season columns are empty. In their first season all 13 finished in the bottom half of their division and 8 finished last (0.72 points per game vs 1.03 league average), so filling with the league average would be wrong. How to fill them is a group decision.
- **Roster:** for each team-season, last season's points of its players (`roster_pts_vs_avg`) and goals conceded per 60 minutes by its goalies (`roster_goalie_ga_vs_avg`), both compared to the season average. Roster = players whose first spell of the season was with that team.
- **Roster finding:** it adds little beyond last season's team points (a simple model explains 38.2% without it, 38.7% with it), because most players stay with the same team. It does give values for the 13 new teams.
- **Roster limits:** includes players called up during the season; the 4 ex-WHA teams in 1979 use WHA stats, which are inflated (Quebec 1.56).

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
| [missing_teams.png](../figures/missing_teams.png) | |
| [points_last_vs_this.png](../figures/points_last_vs_this.png) | Points per game last season and this season have a correlation of 0.64 (0.62 for 1979–2009 only): a team's previous season is a good guide to the next, but far from perfect, so other information (like roster changes) is needed. |
| [goals_per_game.png](../figures/goals_per_game.png) | Goals per game change a lot over time: lowest in 1928 (1.5), a jump during World War II, a peak in the 1980s (about 4.0), then down to about 2.6 by the early 2000s. Even within 1979–2009 scoring levels differ, so team stats are compared to their season's average. |
| [gf_ga_points.png](../figures/gf_ga_points.png) | |
| [correlations.png](../figures/correlations.png) | |
| [coach_changes.png](../figures/coach_changes.png) | |
| [coach_change_vs_results.png](../figures/coach_change_vs_results.png) | |
