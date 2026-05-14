# Spotify Analytics Dashboard

**DBMS Project** — Thapar Institute of Engineering & Technology  
Pranav Tiwari (1024160127) · Vrishank Nehru (1024160109)

---

## Quick Start

### 1. Start Oracle database
```bash
docker compose up -d
# Wait ~60s for Oracle to initialise (check: docker logs spotify_oracle)
```

### 2. Load schema + PL/SQL
```bash
# Connect as the app user
sqlplus spotify/spotify@//localhost:1521/FREEPDB1

SQL> @sql/01_schema.sql
SQL> @sql/02_views.sql
SQL> @sql/03_procedures.sql
SQL> @sql/04_functions.sql
SQL> @sql/05_triggers.sql
SQL> exit
```

### 3. Generate & load seed data
```bash
python3 seed/generate_seed.py         # regenerate (optional, already committed)
sqlplus spotify/spotify@//localhost:1521/FREEPDB1 @seed/seed_data.sql
```

### 4. Run the dashboard
```bash
pip install -r requirements.txt
cd app
python3 app.py
# Open http://localhost:5000
```

---

## Project Structure

```
dbms_proj/
├── sql/
│   ├── 01_schema.sql          DDL: 8 tables, sequences, indexes, constraints
│   ├── 02_views.sql           Views: v_play_full, v_user_top_songs/artists/genres
│   ├── 03_procedures.sql      GENERATE_WRAPPED(user_id, start_date, end_date)
│   ├── 04_functions.sql       GET_PERCENTILE · CALCULATE_BLEND_SCORE
│   ├── 05_triggers.sql        TRG_VALIDATE_PLAY_DURATION · TRG_UPDATE_STATS_ON_PLAY
│   ├── 06_cursor_demo.sql     CUR_USER_HISTORY explicit cursor demo
│   ├── 07_sample_queries.sql  JOINs, subqueries, window functions, INTERSECT, DELETE
│   └── 99_drop_all.sql        Teardown for re-runs
├── seed/
│   ├── generate_seed.py       Synthetic data generator (10 users, 200 songs, ~5k plays)
│   └── seed_data.sql          Pre-generated INSERT statements
├── app/
│   ├── app.py                 Flask web application
│   ├── db.py                  Oracle connection helper
│   └── templates/             Jinja2 HTML templates (dark Spotify theme)
├── docker-compose.yml         Oracle Free 23c container
└── requirements.txt
```

---

## Synopsis → Implementation Mapping

| Synopsis Requirement | File |
|---|---|
| 8 normalised tables (3NF) | `sql/01_schema.sql` |
| Views for analytics queries | `sql/02_views.sql` |
| `GENERATE_WRAPPED` procedure | `sql/03_procedures.sql` |
| `GET_PERCENTILE` function | `sql/04_functions.sql` |
| `CALCULATE_BLEND_SCORE` function | `sql/04_functions.sql` |
| `TRG_UPDATE_STATS_ON_PLAY` trigger | `sql/05_triggers.sql` |
| `TRG_VALIDATE_PLAY_DURATION` trigger | `sql/05_triggers.sql` |
| `CUR_USER_HISTORY` cursor | `sql/06_cursor_demo.sql` |
| JOINs, subqueries, GROUP BY/HAVING, window functions, INTERSECT | `sql/07_sample_queries.sql` |
| COMMIT / ROLLBACK / SAVEPOINT | `sql/03_procedures.sql`, `sql/04_functions.sql` |
| Python data ingestion | `seed/generate_seed.py` |
| Dashboard UI | `app/` |

---

## Running the cursor demo
```sql
SET SERVEROUTPUT ON;
@sql/06_cursor_demo.sql
```

## Running Wrapped from SQL*Plus
```sql
SET SERVEROUTPUT ON;
EXEC generate_wrapped(1, DATE '2025-01-01', DATE '2025-12-31');
SELECT * FROM user_stats WHERE user_id = 1;
```

## Running Blend / Percentile from SQL*Plus
```sql
SELECT calculate_blend_score(1, 2) AS score FROM dual;
SELECT get_percentile(1, 1) AS rank FROM dual;
```

## Environment variables
| Variable | Default | Description |
|---|---|---|
| `ORACLE_DSN` | `localhost:1521/FREEPDB1` | Oracle connect string |
| `ORACLE_USER` | `spotify` | DB username |
| `ORACLE_PASS` | `spotify` | DB password |
# dbms
