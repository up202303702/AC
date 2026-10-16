# Project Notes

Everything we know and decided. Source for the slides.

## Task (a): Final ranking

- **What we predict:** each team's position (1–5) in its division, the `rank` column.
- **Season to predict:** any season requested, using only data from before it.
- **We can use:** anything known the day before the first game, including the new season's rosters.
- **Who wants it:** stakeholders (club management, sponsors, the league) and betting: know before the season how teams will finish.
- **How we measure it:** on average, how many positions off our prediction is.
- **Simple guess to beat:** every team finishes in the same position as last season.

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
| teams_per_season.png | |
| missing_teams.png | |
| points_last_vs_this.png | |
| goals_per_game.png | |
| gf_ga_points.png | |
| correlations.png | |
| coach_changes.png | |
| coach_change_vs_results.png | |
