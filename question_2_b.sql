WITH TeamStats AS (
    SELECT
        gender,
        team AS Team,
        COUNT(*) AS TotalMatches,
        SUM(CASE WHEN winner = team THEN 1 ELSE 0 END) AS TotalWins,
        (SUM(CASE WHEN winner = team THEN 1 ELSE 0 END) / COUNT(*)) * 100 AS WinPercentage
    FROM (
        SELECT
            Match_id,
            team1 AS team,
            winner,
            result,
            gender,
            date_of_match
        FROM
            match_results
        WHERE
            EXTRACT(YEAR FROM date_of_match) = 2019 
        UNION
        SELECT
            Match_id,
            team2 AS team,
            winner,
            result,
            gender,
            date_of_match
        FROM
            match_results
        WHERE
            EXTRACT(YEAR FROM date_of_match) = 2019 
    ) AS Matches
    GROUP BY
        gender,
        Team
)
SELECT
    gender,
    Team,
    TotalMatches,
    TotalWins,
    WinPercentage
FROM (
    SELECT
        gender,
        Team,
        TotalMatches,
        TotalWins,
        WinPercentage,
        ROW_NUMBER() OVER (PARTITION BY gender ORDER BY WinPercentage DESC) AS RowNum
    FROM
        TeamStats
) AS RankedTeams
WHERE
    RowNum = 1;