-- Task (c): one row per player per NHL season, with his last 3 NHL seasons.
-- Same result as the player table built with pandas in notebooks/04_penalty_minutes.ipynb (section 1-2).
--   * A player traded during the season has one row per team (stint): games, PIM and points are summed.
--   * Position and team = those of his first stint (the roster he starts the season with).
--   * "Last season" = his previous NHL season in the data (2005 follows 2003: there is no 2004).

WITH nhl AS (
    SELECT * FROM Scoring WHERE lgID = 'NHL'
),
totals AS (                                   -- stints summed
    SELECT playerID, year,                    -- COALESCE: a season with no numbers counts as 0 (as in pandas)
           COALESCE(SUM(GP), 0) AS GP, COALESCE(SUM(PIM), 0) AS PIM, COALESCE(SUM(Pts), 0) AS Pts
    FROM nhl
    GROUP BY playerID, year
),
first_stint AS (                              -- team and position of the first stint
    SELECT playerID, year, SUBSTR(pos, 1, 1) AS pos, tmID
    FROM (SELECT playerID, year, pos, tmID,
                 ROW_NUMBER() OVER (PARTITION BY playerID, year ORDER BY stint) AS nr
          FROM nhl)
    WHERE nr = 1
),
league AS (                                   -- league penalty minutes per game played, per season
    SELECT year, 1.0 * SUM(PIM) / SUM(GP) AS league_rate
    FROM totals
    GROUP BY year
),
history AS (                                  -- previous seasons of the same player
    SELECT t.playerID, t.year, t.GP, t.PIM, t.Pts, f.pos, f.tmID, l.league_rate,
           LAG(t.PIM, 1) OVER w AS PIM_1, LAG(t.GP, 1) OVER w AS GP_1, LAG(t.Pts, 1) OVER w AS Pts_1,
           LAG(t.PIM, 2) OVER w AS PIM_2, LAG(t.GP, 2) OVER w AS GP_2,
           LAG(t.PIM, 3) OVER w AS PIM_3, LAG(t.GP, 3) OVER w AS GP_3,
           ROW_NUMBER() OVER w - 1 AS seasons_before
    FROM totals t
    JOIN first_stint f ON f.playerID = t.playerID AND f.year = t.year
    JOIN league l ON l.year = t.year
    WINDOW w AS (PARTITION BY t.playerID ORDER BY t.year)
)
SELECT *,
       1.0 * PIM_1 / NULLIF(GP_1, 0) AS rate_1,          -- PIM per game last season
       CASE WHEN PIM_1 IS NULL THEN 1 ELSE 0 END AS first_season
FROM history
WHERE year >= 1979
ORDER BY playerID, year;
