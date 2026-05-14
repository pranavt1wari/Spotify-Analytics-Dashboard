-- ============================================================
-- Spotify Analytics Dashboard -- Functions (PL/pgSQL)
-- ============================================================

-- GET_PERCENTILE: returns "Top X%" for a user+artist pair
CREATE OR REPLACE FUNCTION get_percentile(p_user_id INT, p_artist_id INT)
RETURNS VARCHAR
LANGUAGE plpgsql
AS $$
DECLARE
    v_percentile NUMERIC;
BEGIN
    -- PERCENT_RANK must be computed over ALL users first, THEN filter
    SELECT ROUND((pr * 100)::NUMERIC, 2)
    INTO v_percentile
    FROM (
        SELECT ph.user_id,
               PERCENT_RANK() OVER (ORDER BY COUNT(*) DESC) AS pr
        FROM play_history ph
        JOIN song s   ON s.song_id   = ph.song_id
        JOIN album al ON al.album_id = s.album_id
        WHERE al.artist_id = p_artist_id
        GROUP BY ph.user_id
    ) ranked
    WHERE user_id = p_user_id;

    IF v_percentile IS NULL THEN RETURN 'Not ranked'; END IF;

    -- 0 = #1 listener (best), return exact value so it matches leaderboard
    IF v_percentile = 0 THEN
        RETURN 'Top 1%';
    ELSE
        RETURN 'Top ' || v_percentile || '%';
    END IF;

EXCEPTION
    WHEN NO_DATA_FOUND THEN RETURN 'Not ranked';
    WHEN OTHERS        THEN RETURN 'Error: ' || SQLERRM;
END;
$$;


-- CALCULATE_BLEND_SCORE: weighted Jaccard (artists 40%, songs 30%, genres 30%)
CREATE OR REPLACE FUNCTION calculate_blend_score(p_user1_id INT, p_user2_id INT)
RETURNS NUMERIC
LANGUAGE plpgsql
AS $$
DECLARE
    v_common_artists  INT := 0;
    v_common_songs    INT := 0;
    v_common_genres   INT := 0;
    v_u1_artists      INT := 0;  v_u2_artists INT := 0;
    v_u1_songs        INT := 0;  v_u2_songs   INT := 0;
    v_u1_genres       INT := 0;  v_u2_genres  INT := 0;
    v_score           NUMERIC;
BEGIN
    -- Common artists via INTERSECT
    SELECT COUNT(*) INTO v_common_artists FROM (
        SELECT al.artist_id FROM play_history ph
        JOIN song s ON s.song_id=ph.song_id JOIN album al ON al.album_id=s.album_id
        WHERE ph.user_id = p_user1_id
        INTERSECT
        SELECT al.artist_id FROM play_history ph
        JOIN song s ON s.song_id=ph.song_id JOIN album al ON al.album_id=s.album_id
        WHERE ph.user_id = p_user2_id
    ) t;

    -- Common songs
    SELECT COUNT(*) INTO v_common_songs FROM (
        SELECT song_id FROM play_history WHERE user_id = p_user1_id
        INTERSECT
        SELECT song_id FROM play_history WHERE user_id = p_user2_id
    ) t;

    -- Common genres
    SELECT COUNT(*) INTO v_common_genres FROM (
        SELECT ar.genre_id FROM play_history ph
        JOIN song s ON s.song_id=ph.song_id JOIN album al ON al.album_id=s.album_id
        JOIN artist ar ON ar.artist_id=al.artist_id WHERE ph.user_id = p_user1_id
        INTERSECT
        SELECT ar.genre_id FROM play_history ph
        JOIN song s ON s.song_id=ph.song_id JOIN album al ON al.album_id=s.album_id
        JOIN artist ar ON ar.artist_id=al.artist_id WHERE ph.user_id = p_user2_id
    ) t;

    -- Total unique counts per user
    SELECT COUNT(DISTINCT al.artist_id), COUNT(DISTINCT ph.song_id), COUNT(DISTINCT ar.genre_id)
    INTO v_u1_artists, v_u1_songs, v_u1_genres
    FROM play_history ph
    JOIN song s ON s.song_id=ph.song_id JOIN album al ON al.album_id=s.album_id
    JOIN artist ar ON ar.artist_id=al.artist_id WHERE ph.user_id = p_user1_id;

    SELECT COUNT(DISTINCT al.artist_id), COUNT(DISTINCT ph.song_id), COUNT(DISTINCT ar.genre_id)
    INTO v_u2_artists, v_u2_songs, v_u2_genres
    FROM play_history ph
    JOIN song s ON s.song_id=ph.song_id JOIN album al ON al.album_id=s.album_id
    JOIN artist ar ON ar.artist_id=al.artist_id WHERE ph.user_id = p_user2_id;

    -- Weighted Jaccard score (0-100)
    v_score := ROUND((
        0.4 * CASE WHEN (v_u1_artists+v_u2_artists-v_common_artists)=0 THEN 0
                   ELSE v_common_artists::NUMERIC/(v_u1_artists+v_u2_artists-v_common_artists) END +
        0.3 * CASE WHEN (v_u1_songs+v_u2_songs-v_common_songs)=0 THEN 0
                   ELSE v_common_songs::NUMERIC/(v_u1_songs+v_u2_songs-v_common_songs) END +
        0.3 * CASE WHEN (v_u1_genres+v_u2_genres-v_common_genres)=0 THEN 0
                   ELSE v_common_genres::NUMERIC/(v_u1_genres+v_u2_genres-v_common_genres) END
    ) * 100, 2);

    -- Persist to BLEND table
    INSERT INTO blend (user1_id, user2_id, compatibility_score,
                       common_artists_count, common_songs_count, common_genres_count)
    VALUES (p_user1_id, p_user2_id, v_score,
            v_common_artists, v_common_songs, v_common_genres);

    RETURN v_score;

EXCEPTION
    WHEN OTHERS THEN RAISE;
END;
$$;
