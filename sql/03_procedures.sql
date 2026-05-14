-- ============================================================
-- Spotify Analytics Dashboard -- Stored Procedures (PL/pgSQL)
-- ============================================================

CREATE OR REPLACE PROCEDURE generate_wrapped(
    p_user_id    INT,
    p_start_date DATE,
    p_end_date   DATE
)
LANGUAGE plpgsql
AS $$
DECLARE
    v_top_artist_id       INT;
    v_top_song_id         INT;
    v_top_genre_id        INT;
    v_total_minutes       NUMERIC;
    v_total_songs_played  INT;
    v_total_unique_songs  INT;
    v_total_unique_artists INT;
    v_period_type         VARCHAR(10) := 'YEARLY';
BEGIN
    -- Determine period label
    IF (p_end_date - p_start_date) <= 31 THEN
        v_period_type := 'MONTHLY';
    ELSIF (p_end_date - p_start_date) <= 90 THEN
        v_period_type := 'WEEKLY';
    END IF;

    -- Top artist by play count
    SELECT al.artist_id INTO v_top_artist_id
    FROM play_history ph
    JOIN song s   ON s.song_id   = ph.song_id
    JOIN album al ON al.album_id = s.album_id
    WHERE ph.user_id = p_user_id
      AND ph.played_at::DATE BETWEEN p_start_date AND p_end_date
    GROUP BY al.artist_id
    ORDER BY COUNT(*) DESC
    LIMIT 1;

    -- Top song by play count
    SELECT song_id INTO v_top_song_id
    FROM play_history
    WHERE user_id = p_user_id
      AND played_at::DATE BETWEEN p_start_date AND p_end_date
    GROUP BY song_id
    ORDER BY COUNT(*) DESC
    LIMIT 1;

    -- Top genre by listen time
    SELECT g.genre_id INTO v_top_genre_id
    FROM play_history ph
    JOIN song s   ON s.song_id   = ph.song_id
    JOIN album al ON al.album_id = s.album_id
    JOIN artist ar ON ar.artist_id = al.artist_id
    JOIN genre g   ON g.genre_id  = ar.genre_id
    WHERE ph.user_id = p_user_id
      AND ph.played_at::DATE BETWEEN p_start_date AND p_end_date
    GROUP BY g.genre_id
    ORDER BY SUM(ph.duration_played_ms) DESC
    LIMIT 1;

    -- Aggregate stats
    SELECT
        ROUND(SUM(ph.duration_played_ms) / 60000.0, 2),
        COUNT(*),
        COUNT(DISTINCT ph.song_id),
        COUNT(DISTINCT al.artist_id)
    INTO v_total_minutes, v_total_songs_played, v_total_unique_songs, v_total_unique_artists
    FROM play_history ph
    JOIN song s   ON s.song_id   = ph.song_id
    JOIN album al ON al.album_id = s.album_id
    WHERE ph.user_id = p_user_id
      AND ph.played_at::DATE BETWEEN p_start_date AND p_end_date;

    -- Upsert into USER_STATS (delete old row for same period, then insert)
    DELETE FROM user_stats
    WHERE user_id    = p_user_id
      AND period_type  = v_period_type
      AND period_start = p_start_date
      AND period_end   = p_end_date;

    INSERT INTO user_stats (
        user_id, period_type, period_start, period_end,
        top_artist_id, top_song_id, top_genre_id,
        total_minutes, total_songs_played,
        total_unique_songs, total_unique_artists
    ) VALUES (
        p_user_id, v_period_type, p_start_date, p_end_date,
        v_top_artist_id, v_top_song_id, v_top_genre_id,
        COALESCE(v_total_minutes, 0),
        COALESCE(v_total_songs_played, 0),
        COALESCE(v_total_unique_songs, 0),
        COALESCE(v_total_unique_artists, 0)
    );

    RAISE NOTICE 'Wrapped generated for user %', p_user_id;

EXCEPTION
    WHEN OTHERS THEN
        RAISE NOTICE 'ERROR in generate_wrapped: %', SQLERRM;
        RAISE;
END;
$$;
