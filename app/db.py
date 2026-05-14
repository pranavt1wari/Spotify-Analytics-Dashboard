import psycopg2
import psycopg2.extras
import os
from datetime import datetime

DB_CONFIG = {
    "host":     os.getenv("PG_HOST",   "localhost"),
    "port":     int(os.getenv("PG_PORT", "5432")),
    "dbname":   os.getenv("PG_DB",     "spotify_analytics"),
    "user":     os.getenv("PG_USER",   "spotify"),
    "password": os.getenv("PG_PASS",   "spotify"),
}

def get_conn():
    return psycopg2.connect(**DB_CONFIG)

def _parse_date(s):
    return datetime.strptime(s, "%Y-%m-%d").date()

def query(sql, params=None):
    with get_conn() as conn:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute(sql, params or ())
            return [dict(r) for r in cur.fetchall()]

def callproc(name, params):
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(f"CALL {name}({','.join(['%s']*len(params))})", params)
        conn.commit()

def callfunc(name, params):
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(f"SELECT {name}({','.join(['%s']*len(params))})", params)
            result = cur.fetchone()[0]
        conn.commit()
        return result
