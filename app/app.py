from flask import Flask, render_template, request
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import db

app = Flask(__name__)

def get_users():
    return db.query("SELECT user_id, username FROM app_user ORDER BY user_id")

def get_artists():
    return db.query("SELECT artist_id, name FROM artist ORDER BY name")


@app.route("/")
def index():
    return render_template("index.html", users=get_users(), artists=get_artists())


@app.route("/wrapped", methods=["GET", "POST"])
def wrapped():
    users  = get_users()
    result = None
    error  = None

    if request.method == "POST":
        user_id = int(request.form["user_id"])
        start   = request.form["start_date"]
        end     = request.form["end_date"]

        try:
            db.callproc("generate_wrapped", [user_id, db._parse_date(start), db._parse_date(end)])
        except Exception as e:
            error = f"Wrapped generation warning: {e}"

        p = (user_id, start, end)
        top_songs = db.query("""
            SELECT s.title AS song, ar.name AS artist, COUNT(*) AS plays,
                   ROUND(SUM(ph.duration_played_ms)/60000.0,1) AS total_mins
            FROM play_history ph
            JOIN song s ON s.song_id=ph.song_id
            JOIN album al ON al.album_id=s.album_id
            JOIN artist ar ON ar.artist_id=al.artist_id
            WHERE ph.user_id=%s AND ph.played_at::DATE BETWEEN %s AND %s
            GROUP BY s.title, ar.name ORDER BY plays DESC LIMIT 5
        """, p)

        top_artists = db.query("""
            SELECT ar.name AS artist, COUNT(*) AS plays
            FROM play_history ph
            JOIN song s ON s.song_id=ph.song_id
            JOIN album al ON al.album_id=s.album_id
            JOIN artist ar ON ar.artist_id=al.artist_id
            WHERE ph.user_id=%s AND ph.played_at::DATE BETWEEN %s AND %s
            GROUP BY ar.name ORDER BY plays DESC LIMIT 5
        """, p)

        top_genres = db.query("""
            SELECT g.name AS genre, ROUND(SUM(ph.duration_played_ms)/60000.0,1) AS total_mins
            FROM play_history ph
            JOIN song s ON s.song_id=ph.song_id
            JOIN album al ON al.album_id=s.album_id
            JOIN artist ar ON ar.artist_id=al.artist_id
            JOIN genre g ON g.genre_id=ar.genre_id
            WHERE ph.user_id=%s AND ph.played_at::DATE BETWEEN %s AND %s
            GROUP BY g.name ORDER BY total_mins DESC LIMIT 5
        """, p)

        summary = db.query("""
            SELECT ROUND(SUM(duration_played_ms)/60000.0,1) AS total_mins,
                   COUNT(*) AS total_plays, COUNT(DISTINCT song_id) AS unique_songs
            FROM play_history
            WHERE user_id=%s AND played_at::DATE BETWEEN %s AND %s
        """, p)

        hour_data = db.query("""
            SELECT EXTRACT(HOUR FROM played_at)::INT AS hour_of_day, COUNT(*) AS plays
            FROM play_history
            WHERE user_id=%s AND played_at::DATE BETWEEN %s AND %s
            GROUP BY hour_of_day ORDER BY hour_of_day
        """, p)

        username = next((u["username"] for u in users if u["user_id"] == user_id), "User")
        result = {
            "username": username, "start": start, "end": end,
            "top_songs": top_songs, "top_artists": top_artists,
            "top_genres": top_genres,
            "summary": summary[0] if summary else {},
            "hour_data": hour_data,
        }

    return render_template("wrapped.html", users=users, result=result, error=error)


@app.route("/blend", methods=["GET", "POST"])
def blend():
    users  = get_users()
    result = None
    error  = None

    if request.method == "POST":
        u1 = int(request.form["user1_id"])
        u2 = int(request.form["user2_id"])
        if u1 == u2:
            error = "Please select two different users."
        else:
            try:
                score = db.callfunc("calculate_blend_score", [u1, u2])
                p = (u1, u2)

                common_artists = db.query("""
                    SELECT ar.name FROM artist ar WHERE ar.artist_id IN (
                        SELECT al.artist_id FROM play_history ph
                        JOIN song s ON s.song_id=ph.song_id JOIN album al ON al.album_id=s.album_id
                        WHERE ph.user_id=%s
                        INTERSECT
                        SELECT al.artist_id FROM play_history ph
                        JOIN song s ON s.song_id=ph.song_id JOIN album al ON al.album_id=s.album_id
                        WHERE ph.user_id=%s
                    ) ORDER BY ar.name
                """, p)

                common_songs = db.query("""
                    SELECT s.title, ar.name AS artist FROM song s
                    JOIN album al ON al.album_id=s.album_id
                    JOIN artist ar ON ar.artist_id=al.artist_id
                    WHERE s.song_id IN (
                        SELECT song_id FROM play_history WHERE user_id=%s
                        INTERSECT
                        SELECT song_id FROM play_history WHERE user_id=%s
                    ) ORDER BY s.title LIMIT 20
                """, p)

                common_genres = db.query("""
                    SELECT g.name FROM genre g WHERE g.genre_id IN (
                        SELECT ar.genre_id FROM play_history ph
                        JOIN song s ON s.song_id=ph.song_id JOIN album al ON al.album_id=s.album_id
                        JOIN artist ar ON ar.artist_id=al.artist_id WHERE ph.user_id=%s
                        INTERSECT
                        SELECT ar.genre_id FROM play_history ph
                        JOIN song s ON s.song_id=ph.song_id JOIN album al ON al.album_id=s.album_id
                        JOIN artist ar ON ar.artist_id=al.artist_id WHERE ph.user_id=%s
                    ) ORDER BY g.name
                """, p)

                u1_name = next(u["username"] for u in users if u["user_id"] == u1)
                u2_name = next(u["username"] for u in users if u["user_id"] == u2)
                result = {
                    "score": round(float(score), 1),
                    "u1_name": u1_name, "u2_name": u2_name,
                    "common_artists": common_artists,
                    "common_songs": common_songs,
                    "common_genres": common_genres,
                }
            except Exception as e:
                error = str(e)

    return render_template("blend.html", users=users, result=result, error=error)


@app.route("/percentile", methods=["GET", "POST"])
def percentile():
    users   = get_users()
    artists = get_artists()
    result  = None
    error   = None

    if request.method == "POST":
        user_id   = int(request.form["user_id"])
        artist_id = int(request.form["artist_id"])
        try:
            rank_str = db.callfunc("get_percentile", [user_id, artist_id])

            leaderboard = db.query("""
                SELECT u.username, up.play_count,
                       ROUND((PERCENT_RANK() OVER (ORDER BY up.play_count DESC) * 100)::NUMERIC,1) AS top_pct
                FROM (
                    SELECT ph.user_id, COUNT(*) AS play_count
                    FROM play_history ph
                    JOIN song s ON s.song_id=ph.song_id
                    JOIN album al ON al.album_id=s.album_id
                    WHERE al.artist_id=%s
                    GROUP BY ph.user_id
                ) up JOIN app_user u ON u.user_id=up.user_id
                ORDER BY up.play_count DESC LIMIT 10
            """, (artist_id,))

            user_plays = db.query("""
                SELECT COUNT(*) AS plays FROM play_history ph
                JOIN song s ON s.song_id=ph.song_id
                JOIN album al ON al.album_id=s.album_id
                WHERE al.artist_id=%s AND ph.user_id=%s
            """, (artist_id, user_id))

            username    = next(u["username"] for u in users if u["user_id"] == user_id)
            artist_name = next(a["name"] for a in artists if a["artist_id"] == artist_id)
            result = {
                "rank_str":    rank_str,
                "username":    username,
                "artist_name": artist_name,
                "plays":       user_plays[0]["plays"] if user_plays else 0,
                "leaderboard": leaderboard,
            }
        except Exception as e:
            error = str(e)

    return render_template("percentile.html",
                           users=users, artists=artists, result=result, error=error)


if __name__ == "__main__":
    app.run(debug=True, port=5000)
