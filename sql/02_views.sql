-- ============================================================
-- Spotify Analytics Dashboard -- Views (PostgreSQL)
-- ============================================================

CREATE OR REPLACE VIEW v_play_full AS
    SELECT
        ph.play_id,
        ph.user_id,
        u.username,
        ph.song_id,
        s.title            AS song_title,
        s.duration_ms,
        ph.duration_played_ms,
        ph.played_at,
        al.album_id,
        al.title           AS album_title,
        ar.artist_id,
        ar.name            AS artist_name,
        g.genre_id,
        g.name             AS genre_name
    FROM play_history ph
    JOIN app_user u  ON u.user_id    = ph.user_id
    JOIN song     s  ON s.song_id    = ph.song_id
    JOIN album    al ON al.album_id  = s.album_id
    JOIN artist   ar ON ar.artist_id = al.artist_id
    JOIN genre    g  ON g.genre_id   = ar.genre_id;

CREATE OR REPLACE VIEW v_user_top_songs AS
    SELECT
        user_id,
        song_id,
        song_title,
        artist_name,
        COUNT(*)                                         AS play_count,
        ROUND(SUM(duration_played_ms) / 60000.0, 2)     AS total_minutes,
        RANK() OVER (PARTITION BY user_id ORDER BY COUNT(*) DESC) AS rnk
    FROM v_play_full
    GROUP BY user_id, song_id, song_title, artist_name;

CREATE OR REPLACE VIEW v_user_top_artists AS
    SELECT
        user_id,
        artist_id,
        artist_name,
        COUNT(*)                                        AS play_count,
        ROUND(SUM(duration_played_ms) / 60000.0, 2)    AS total_minutes,
        RANK() OVER (PARTITION BY user_id ORDER BY COUNT(*) DESC) AS rnk
    FROM v_play_full
    GROUP BY user_id, artist_id, artist_name;

CREATE OR REPLACE VIEW v_user_top_genres AS
    SELECT
        user_id,
        genre_id,
        genre_name,
        ROUND(SUM(duration_played_ms) / 60000.0, 2)    AS total_minutes,
        RANK() OVER (PARTITION BY user_id ORDER BY SUM(duration_played_ms) DESC) AS rnk
    FROM v_play_full
    GROUP BY user_id, genre_id, genre_name;
