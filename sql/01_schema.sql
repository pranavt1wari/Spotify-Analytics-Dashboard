-- ============================================================
-- Spotify Analytics Dashboard -- Schema (PostgreSQL)
-- 8 Normalized Tables in 3NF/BCNF
-- ============================================================

-- Clean slate
DROP TABLE IF EXISTS blend        CASCADE;
DROP TABLE IF EXISTS user_stats   CASCADE;
DROP TABLE IF EXISTS play_history CASCADE;
DROP TABLE IF EXISTS app_user     CASCADE;
DROP TABLE IF EXISTS song         CASCADE;
DROP TABLE IF EXISTS album        CASCADE;
DROP TABLE IF EXISTS artist       CASCADE;
DROP TABLE IF EXISTS genre        CASCADE;

-- 1. GENRE
CREATE TABLE genre (
    genre_id   SERIAL        PRIMARY KEY,
    name       VARCHAR(100)  NOT NULL
);

-- 2. ARTIST
CREATE TABLE artist (
    artist_id   SERIAL        PRIMARY KEY,
    name        VARCHAR(200)  NOT NULL,
    spotify_uri VARCHAR(200)  NOT NULL,
    genre_id    INT           NOT NULL REFERENCES genre(genre_id)
);

-- 3. ALBUM
CREATE TABLE album (
    album_id     SERIAL        PRIMARY KEY,
    title        VARCHAR(300)  NOT NULL,
    release_date DATE          NOT NULL,
    total_tracks INT           NOT NULL,
    artist_id    INT           NOT NULL REFERENCES artist(artist_id)
);

-- 4. SONG
CREATE TABLE song (
    song_id      SERIAL        PRIMARY KEY,
    title        VARCHAR(300)  NOT NULL,
    duration_ms  INT           NOT NULL,
    spotify_uri  VARCHAR(200)  NOT NULL,
    track_number INT           NOT NULL,
    album_id     INT           NOT NULL REFERENCES album(album_id)
);

-- 5. APP_USER (named APP_USER to avoid conflict with reserved keyword USER)
CREATE TABLE app_user (
    user_id    SERIAL        PRIMARY KEY,
    username   VARCHAR(100)  NOT NULL,
    email      VARCHAR(200)  NOT NULL UNIQUE,
    spotify_id VARCHAR(200)  NOT NULL UNIQUE,
    created_at TIMESTAMP     DEFAULT CURRENT_TIMESTAMP
);

-- 6. PLAY_HISTORY
CREATE TABLE play_history (
    play_id            SERIAL     PRIMARY KEY,
    user_id            INT        NOT NULL REFERENCES app_user(user_id),
    song_id            INT        NOT NULL REFERENCES song(song_id),
    played_at          TIMESTAMP  NOT NULL,
    duration_played_ms INT        NOT NULL,
    CONSTRAINT chk_duration CHECK (duration_played_ms > 0 AND duration_played_ms <= 3600000)
);

-- 7. USER_STATS
CREATE TABLE user_stats (
    stat_id              SERIAL       PRIMARY KEY,
    user_id              INT          NOT NULL REFERENCES app_user(user_id),
    period_type          VARCHAR(10)  NOT NULL CHECK (period_type IN ('DAILY','WEEKLY','MONTHLY','YEARLY')),
    period_start         DATE         NOT NULL,
    period_end           DATE         NOT NULL,
    top_artist_id        INT          REFERENCES artist(artist_id),
    top_song_id          INT          REFERENCES song(song_id),
    top_genre_id         INT          REFERENCES genre(genre_id),
    total_minutes        NUMERIC      NOT NULL DEFAULT 0,
    total_songs_played   INT          NOT NULL DEFAULT 0,
    total_unique_songs   INT          NOT NULL DEFAULT 0,
    total_unique_artists INT          NOT NULL DEFAULT 0
);

-- 8. BLEND
CREATE TABLE blend (
    blend_id             SERIAL     PRIMARY KEY,
    user1_id             INT        NOT NULL REFERENCES app_user(user_id),
    user2_id             INT        NOT NULL REFERENCES app_user(user_id),
    compatibility_score  FLOAT      NOT NULL,
    common_artists_count INT        NOT NULL,
    common_songs_count   INT        NOT NULL,
    common_genres_count  INT        NOT NULL,
    created_at           TIMESTAMP  DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT chk_blend_users CHECK (user1_id <> user2_id)
);

-- Indexes on frequently queried columns
CREATE INDEX idx_ph_user_id   ON play_history(user_id);
CREATE INDEX idx_ph_song_id   ON play_history(song_id);
CREATE INDEX idx_ph_played_at ON play_history(played_at);
