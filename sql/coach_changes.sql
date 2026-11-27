-- Task (b): one row per club per NHL season with the answer to predict, coach_change.
-- Same rules as the pandas version in notebooks/02_data_preparation.ipynb ("Coach information"):
--   * rows with notes (interim coaches, co-coaches) are left out;
--   * first coach = lowest stint, last coach = highest stint (ties: coachID order, as in pandas);
--   * clubs are followed with franchID (teams move city); "last season" = the club's previous NHL season.
--   * coach_change = 1 if this season's first coach is not last season's last coach; empty for new clubs.

WITH c AS (
    SELECT co.year, co.tmID, co.coachID, co.stint, t.franchID
    FROM Coaches co
    JOIN Teams t ON t.year = co.year AND t.tmID = co.tmID AND t.lgID = co.lgID
    WHERE co.lgID = 'NHL' AND co.notes IS NULL
),
ordered AS (
    SELECT *,
           ROW_NUMBER() OVER (PARTITION BY year, tmID ORDER BY stint, coachID) AS from_start,
           ROW_NUMBER() OVER (PARTITION BY year, tmID ORDER BY stint DESC, coachID DESC) AS from_end
    FROM c
),
season AS (
    SELECT franchID, year, tmID,
           MAX(CASE WHEN from_start = 1 THEN coachID END) AS first_coach,
           MAX(CASE WHEN from_end = 1 THEN coachID END) AS last_coach,
           COUNT(DISTINCT coachID) AS n_coaches
    FROM ordered
    GROUP BY franchID, year, tmID
),
with_last_season AS (
    SELECT *,
           LAG(last_coach) OVER w AS last_season_last_coach,
           LAG(n_coaches) OVER w AS last_season_coaches
    FROM season
    WINDOW w AS (PARTITION BY franchID ORDER BY year)
)
SELECT franchID, year, tmID, first_coach, last_season_last_coach, last_season_coaches,
       CASE WHEN last_season_last_coach IS NULL THEN NULL
            WHEN first_coach <> last_season_last_coach THEN 1 ELSE 0 END AS coach_change
FROM with_last_season
WHERE year >= 1979
ORDER BY year, franchID;
