-- ============================================================
-- Spotify Analytics Dashboard -- Cursor Demo (PL/pgSQL)
-- CUR_USER_HISTORY: explicit cursor iterating a user's history
-- ============================================================

DO $$
DECLARE
    v_user_id   INT := 1;
    v_count     INT := 0;
    v_rec       RECORD;

    -- Explicit named cursor
    cur_user_history CURSOR FOR
        SELECT ph.play_id,
               s.title       AS song_title,
               ar.name       AS artist_name,
               ph.played_at,
               ROUND(ph.duration_played_ms / 60000.0, 2) AS minutes_played
        FROM play_history ph
        JOIN song   s  ON s.song_id   = ph.song_id
        JOIN album  al ON al.album_id = s.album_id
        JOIN artist ar ON ar.artist_id = al.artist_id
        WHERE ph.user_id = v_user_id
        ORDER BY ph.played_at DESC
        LIMIT 20;
BEGIN
    RAISE NOTICE '=== Recent Listening History for User % ===', v_user_id;
    RAISE NOTICE '%-40s %-25s %-22s %s', 'Song', 'Artist', 'Played At', 'Mins';
    RAISE NOTICE '%', REPEAT('-', 95);

    OPEN cur_user_history;
    LOOP
        FETCH cur_user_history INTO v_rec;
        EXIT WHEN NOT FOUND;

        v_count := v_count + 1;
        RAISE NOTICE '%-40s %-25s %-22s %s',
            SUBSTR(v_rec.song_title,   1, 38),
            SUBSTR(v_rec.artist_name,  1, 23),
            TO_CHAR(v_rec.played_at, 'YYYY-MM-DD HH24:MI'),
            v_rec.minutes_played;
    END LOOP;
    CLOSE cur_user_history;

    RAISE NOTICE '%', REPEAT('-', 95);
    RAISE NOTICE 'Total records: %', v_count;
END;
$$;
