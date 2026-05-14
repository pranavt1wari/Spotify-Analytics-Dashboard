-- ============================================================
-- Spotify Analytics Dashboard -- Sample Analytics Queries
-- JOINs, subqueries, GROUP BY/HAVING, window functions, INTERSECT
-- ============================================================

-- Q1: Full listening history (4-table JOIN)
SELECT ph.play_id, u.username, s.title AS song, ar.name AS artist,
       al.title AS album, g.name AS genre,
       TO_CHAR(ph.played_at, 'YYYY-MM-DD HH24:MI') AS played_at,
       ROUND(ph.duration_played_ms / 60000.0, 2) AS mins
FROM play_history ph
JOIN app_user u  ON u.user_id   = ph.user_id
JOIN song     s  ON s.song_id   = ph.song_id
JOIN album    al ON al.album_id = s.album_id
JOIN artist   ar ON ar.artist_id = al.artist_id
JOIN genre    g  ON g.genre_id  = ar.genre_id
WHERE ph.user_id = 1
ORDER BY ph.played_at DESC
LIMIT 20;

-- Q2: Top 5 songs for user 1 in 2025
SELECT s.title, ar.name AS artist, COUNT(*) AS plays,
       ROUND(SUM(ph.duration_played_ms)/60000.0, 1) AS total_mins
FROM play_history ph
JOIN song s ON s.song_id=ph.song_id
JOIN album al ON al.album_id=s.album_id
JOIN artist ar ON ar.artist_id=al.artist_id
WHERE ph.user_id=1 AND EXTRACT(YEAR FROM ph.played_at)=2025
GROUP BY s.song_id, s.title, ar.name
ORDER BY plays DESC LIMIT 5;

-- Q3: Peak listening hour (GROUP BY + HAVING)
SELECT EXTRACT(HOUR FROM played_at)::INT AS hour_of_day, COUNT(*) AS play_count
FROM play_history WHERE user_id=1
GROUP BY hour_of_day HAVING COUNT(*) > 5
ORDER BY play_count DESC;

-- Q4: Correlated subquery -- users above avg for artist 1
SELECT u.username, counts.play_count
FROM app_user u
JOIN (
    SELECT ph.user_id, COUNT(*) AS play_count
    FROM play_history ph
    JOIN song s ON s.song_id=ph.song_id
    JOIN album al ON al.album_id=s.album_id
    WHERE al.artist_id=1
    GROUP BY ph.user_id
) counts ON counts.user_id=u.user_id
WHERE counts.play_count > (
    SELECT AVG(cnt) FROM (
        SELECT COUNT(*) AS cnt
        FROM play_history ph
        JOIN song s ON s.song_id=ph.song_id
        JOIN album al ON al.album_id=s.album_id
        WHERE al.artist_id=1
        GROUP BY ph.user_id
    ) sub
)
ORDER BY counts.play_count DESC;

-- Q5: ROW_NUMBER -- top 3 songs per user
SELECT username, song_title, artist_name, play_count FROM (
    SELECT u.username, s.title AS song_title, ar.name AS artist_name,
           COUNT(*) AS play_count,
           ROW_NUMBER() OVER (PARTITION BY ph.user_id ORDER BY COUNT(*) DESC) AS rn
    FROM play_history ph
    JOIN app_user u  ON u.user_id   = ph.user_id
    JOIN song     s  ON s.song_id   = ph.song_id
    JOIN album    al ON al.album_id = s.album_id
    JOIN artist   ar ON ar.artist_id = al.artist_id
    GROUP BY ph.user_id, u.username, s.song_id, s.title, ar.name
) t WHERE rn <= 3
ORDER BY username, rn;

-- Q6: PERCENT_RANK -- listener rank for artist 1
SELECT u.username, up.play_count,
       ROUND(PERCENT_RANK() OVER (ORDER BY up.play_count DESC)::NUMERIC * 100, 2) AS top_pct
FROM (
    SELECT ph.user_id, COUNT(*) AS play_count
    FROM play_history ph
    JOIN song s ON s.song_id=ph.song_id
    JOIN album al ON al.album_id=s.album_id
    WHERE al.artist_id=1
    GROUP BY ph.user_id
) up JOIN app_user u ON u.user_id=up.user_id
ORDER BY top_pct;

-- Q7: INTERSECT -- common artists between users 1 and 2
SELECT ar.name AS common_artist FROM artist ar
WHERE ar.artist_id IN (
    SELECT al.artist_id FROM play_history ph
    JOIN song s ON s.song_id=ph.song_id JOIN album al ON al.album_id=s.album_id
    WHERE ph.user_id=1
    INTERSECT
    SELECT al.artist_id FROM play_history ph
    JOIN song s ON s.song_id=ph.song_id JOIN album al ON al.album_id=s.album_id
    WHERE ph.user_id=2
);

-- Q8: Monthly summary
SELECT TO_CHAR(played_at,'YYYY-MM') AS month,
       COUNT(*) AS total_plays, COUNT(DISTINCT song_id) AS unique_songs,
       ROUND(SUM(duration_played_ms)/3600000.0, 1) AS hours
FROM play_history WHERE user_id=1
GROUP BY TO_CHAR(played_at,'YYYY-MM') ORDER BY month;

-- Q9: Artists with >50 plays in any month (GROUP BY + HAVING)
SELECT ar.name, TO_CHAR(ph.played_at,'YYYY-MM') AS month, COUNT(*) AS plays
FROM play_history ph
JOIN song s ON s.song_id=ph.song_id
JOIN album al ON al.album_id=s.album_id
JOIN artist ar ON ar.artist_id=al.artist_id
GROUP BY ar.name, TO_CHAR(ph.played_at,'YYYY-MM')
HAVING COUNT(*) > 50
ORDER BY plays DESC;
