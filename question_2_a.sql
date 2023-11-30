SELECT
    EXTRACT(YEAR FROM date_of_match) AS Year,
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
        result NOT IN ('Tie', 'No Result') 
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
        result NOT IN ('Tie', 'No Result') 
) AS Matches
GROUP BY
    Year,
    gender,
    Team
order by Year, WinPercentage desc;