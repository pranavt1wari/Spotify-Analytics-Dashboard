-- ============================================================
-- Spotify Analytics Dashboard -- Triggers (PL/pgSQL)
-- ============================================================

-- Trigger function: validate play duration (BEFORE INSERT)
CREATE OR REPLACE FUNCTION fn_validate_play_duration()
RETURNS TRIGGER LANGUAGE plpgsql AS $$
BEGIN
    IF NEW.duration_played_ms <= 0 THEN
        RAISE EXCEPTION 'Invalid play duration: must be > 0. Got: %', NEW.duration_played_ms
            USING ERRCODE = 'P0001';
    END IF;
    IF NEW.duration_played_ms > 3600000 THEN
        RAISE EXCEPTION 'Suspicious duration: % ms exceeds 1 hour', NEW.duration_played_ms
            USING ERRCODE = 'P0002';
    END IF;
    RETURN NEW;
END;
$$;

DROP TRIGGER IF EXISTS trg_validate_play_duration ON play_history;
CREATE TRIGGER trg_validate_play_duration
BEFORE INSERT ON play_history
FOR EACH ROW EXECUTE FUNCTION fn_validate_play_duration();


-- Trigger function: update daily USER_STATS on every new play (AFTER INSERT)
CREATE OR REPLACE FUNCTION fn_update_stats_on_play()
RETURNS TRIGGER LANGUAGE plpgsql AS $$
DECLARE
    v_play_date       DATE := NEW.played_at::DATE;
    v_top_song_id     INT;
    v_top_artist_id   INT;
    v_top_genre_id    INT;
    v_stat_id         INT;
BEGIN
    -- Find top song today for this user
    SELECT song_id INTO v_top_song_id
    FROM play_history
    WHERE user_id = NEW.user_id AND played_at::DATE = v_play_date
    GROUP BY song_id ORDER BY COUNT(*) DESC LIMIT 1;

    SELECT al.artist_id INTO v_top_artist_id
    FROM play_history ph
    JOIN song s ON s.song_id=ph.song_id JOIN album al ON al.album_id=s.album_id
    WHERE ph.user_id = NEW.user_id AND ph.played_at::DATE = v_play_date
    GROUP BY al.artist_id ORDER BY COUNT(*) DESC LIMIT 1;

    SELECT ar.genre_id INTO v_top_genre_id
    FROM play_history ph
    JOIN song s ON s.song_id=ph.song_id JOIN album al ON al.album_id=s.album_id
    JOIN artist ar ON ar.artist_id=al.artist_id
    WHERE ph.user_id = NEW.user_id AND ph.played_at::DATE = v_play_date
    GROUP BY ar.genre_id ORDER BY SUM(ph.duration_played_ms) DESC LIMIT 1;

    -- Upsert daily stat
    SELECT stat_id INTO v_stat_id FROM user_stats
    WHERE user_id=NEW.user_id AND period_type='DAILY'
      AND period_start=v_play_date AND period_end=v_play_date;

    IF FOUND THEN
        UPDATE user_stats SET
            top_song_id          = v_top_song_id,
            top_artist_id        = v_top_artist_id,
            top_genre_id         = v_top_genre_id,
            total_minutes        = total_minutes + (NEW.duration_played_ms / 60000.0),
            total_songs_played   = total_songs_played + 1,
            total_unique_songs   = (SELECT COUNT(DISTINCT song_id) FROM play_history
                                    WHERE user_id=NEW.user_id AND played_at::DATE=v_play_date),
            total_unique_artists = (SELECT COUNT(DISTINCT al2.artist_id) FROM play_history ph2
                                    JOIN song s2 ON s2.song_id=ph2.song_id
                                    JOIN album al2 ON al2.album_id=s2.album_id
                                    WHERE ph2.user_id=NEW.user_id AND ph2.played_at::DATE=v_play_date)
        WHERE stat_id = v_stat_id;
    ELSE
        INSERT INTO user_stats (user_id, period_type, period_start, period_end,
            top_artist_id, top_song_id, top_genre_id,
            total_minutes, total_songs_played, total_unique_songs, total_unique_artists)
        VALUES (NEW.user_id, 'DAILY', v_play_date, v_play_date,
            v_top_artist_id, v_top_song_id, v_top_genre_id,
            NEW.duration_played_ms/60000.0, 1, 1, 1);
    END IF;

    RETURN NEW;
EXCEPTION WHEN OTHERS THEN
    RAISE WARNING 'trg_update_stats_on_play: %', SQLERRM;
    RETURN NEW;
END;
$$;

DROP TRIGGER IF EXISTS trg_update_stats_on_play ON play_history;
CREATE TRIGGER trg_update_stats_on_play
AFTER INSERT ON play_history
FOR EACH ROW EXECUTE FUNCTION fn_update_stats_on_play();
