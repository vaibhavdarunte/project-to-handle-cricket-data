WITH BatsmanStats AS (
    SELECT
        p.player_id,
        p.player_name,
        COUNT(DISTINCT b.match_id) AS MatchesPlayed,
        SUM(b.runs_by_onstrike_player) AS TotalRuns,
        SUM(CASE WHEN b.runs_by_onstrike_player > 0 THEN 1 ELSE 0 END) AS BallsFaced,
        COUNT(DISTINCT CASE WHEN b.wicket = 0 THEN b.match_id END) AS InningsPlayed
    FROM
        Players p
    JOIN
        ball_by_ball b ON p.player_id = b.onstrike_player_id
    JOIN
        match_results m ON b.match_id = m.match_id
    WHERE
        EXTRACT(YEAR FROM m.date_of_match) = 2019
    GROUP BY
        p.player_id
)
SELECT
    player_name,
    player_id,
    AVG(TotalRuns / NULLIF(BallsFaced, 0)) * 100 AS StrikeRate,
    TotalRuns,
    BallsFaced
FROM
    BatsmanStats
WHERE
    BallsFaced > 0
GROUP BY
    player_name, player_id, TotalRuns, BallsFaced
ORDER BY
    StrikeRate DESC
LIMIT 100; -- Adjust the limit based on your requirements
