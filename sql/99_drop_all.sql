-- Drop all objects in reverse dependency order (for clean re-runs)
BEGIN
    FOR t IN (SELECT table_name FROM user_tables
              WHERE table_name IN ('BLEND','USER_STATS','PLAY_HISTORY',
                                   'APP_USER','SONG','ALBUM','ARTIST','GENRE'))
    LOOP
        EXECUTE IMMEDIATE 'DROP TABLE ' || t.table_name || ' CASCADE CONSTRAINTS';
    END LOOP;
    FOR s IN (SELECT sequence_name FROM user_sequences
              WHERE sequence_name LIKE 'SEQ_%')
    LOOP
        EXECUTE IMMEDIATE 'DROP SEQUENCE ' || s.sequence_name;
    END LOOP;
END;
/
