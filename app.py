from flask import Flask, jsonify, request
import sqlite3

app = Flask(__name__)

DATABASE = "games.db"

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS games (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            genre TEXT NOT NULL,
            platform TEXT NOT NULL,
            release_year INTEGER NOT NULL,
            developer TEXT NOT NULL,
            rating REAL NOT NULL
            )
    """)

    count = conn.execute("SELECT COUNT(*) FROM games").fetchone()[0]

    if count == 0:
        games = [
            ("Hollow Knight", "Metroidvania", "PC", 2017, "Team Cherry", 9.0),
            ("Stardew Valley", "Farming RPG", "PC", 2016, "ConcernedApe", 9.1),
            ("Hades", "Roguelike", "PC", 2020, "Supergiant Games", 9.2),
            ("Celeste", "Platformer", "PC", 2018, "Maddy Makes Games", 9.0),
            ("Terraria", "Sandbox", "PC", 2011, "Re-Logic", 8.9),
            ("Minecraft", "Sandbox", "PC", 2011, "Mojang Studios", 9.3),
            ("Undertale", "RPG", "PC", 2015, "Toby Fox", 9.2),
            ("Portal 2", "Puzzle", "PC", 2011, "Valve", 9.5),
            ("Elden Ring", "Action RPG", "PC", 2022, "FromSoftware", 9.4),
            ("Baldur's Gate 3", "RPG", "PC", 2023, "Larian Studios", 9.6),
            ("Dead Cells", "Roguelike", "PC", 2018, "Motion Twin", 8.8),
            ("Cuphead", "Run and Gun", "PC", 2017, "Studio MDHR", 8.7),
            ("Slay the Spire", "Deckbuilding", "PC", 2019, "Mega Crit", 8.9),
            ("Ori and the Blind Forest", "Platformer", "PC", 2015, "Moon Studios", 8.8),
            ("Risk of Rain 2", "Roguelike", "PC", 2020, "Hopoo Games", 8.7)
        ]

        conn.executemany("""
            INSERT INTO games
            (title, genre, platform, release_year, developer, rating)
            VALUES (?,?,?,?,?,?)
        """, games)

    conn.commit()
    conn.close()

@app.route("/")
def home():
    return{"message": "Video Game API running"}

@app.route("/games", methods=["GET"])
def get_games():
    conn = get_db()
    games = conn.execute("SELECT * FROM games").fetchall()
    conn.close()
    return jsonify([dict(game) for game in games]), 200

@app.route("/games/<int:game_id>", methods=["GET"])
def get_game(game_id):
     conn = get_db()
     game = conn.execute(
        "SELECT * FROM games WHERE id = ?",
        (game_id,)
     ).fetchone()
     conn.close()

     if game is None:
        return jsonify({"Error": "Game Not Found"}), 404

     return jsonify(dict(game)), 200

@app.route("/games", methods=["POST"])
def create_game():
    data = request.get_json(silent=True)
    print("POST DATA:", data)
    if not data:
        return jsonify({"Error": "Bad Request, Missing Field"}), 400

    required_fields = [
        "title",
        "genre",
        "platform",
        "release_year",
        "developer",
        "rating"
    ]

    for field in required_fields:
        if field not in data or data[field] in ("", None):
            return jsonify({"Error": f"Missing required field: {field}"}), 400

    conn = get_db()
    cursor = conn.execute("""
        INSERT INTO games
        (title, genre, platform, release_year, developer, rating)
        VALUES (?,?,?,?,?,?)
    """,(
        data["title"],
        data["genre"],
        data["platform"],
        data["release_year"],
        data["developer"],
        data["rating"]
    ))

    conn.commit()

    game = conn.execute(
        "SELECT * FROM games WHERE ID = ?",
        (cursor.lastrowid,)
    ).fetchone()

    conn.close()

    return jsonify(dict(game)), 201

@app.route("/games/<int:game_id>", methods=["PUT"])
def update_game(game_id):
    data = request.get_json(silent=True)

    if not data:
        return jsonify({"error": "Request body is required"}), 400

    required_fields = [
        "title",
        "genre",
        "platform",
        "release_year",
        "developer",
        "rating"
    ]

    for field in required_fields:
        if field not in data or data[field] in ("", None):
            return jsonify({"error": f"Missing required field: {field}"}), 400

    conn = get_db()

    game = conn.execute(
        "SELECT * FROM games WHERE id = ?",
        (game_id,)
    ).fetchone()

    if game is None:
        conn.close()
        return jsonify({"error": "Game not found"}), 404

    conn.execute("""
        UPDATE games
        SET title = ?,
            genre = ?,
            platform = ?,
            release_year = ?,
            developer = ?,
            rating = ?
        WHERE id = ?
    """, (
        data["title"],
        data["genre"],
        data["platform"],
        data["release_year"],
        data["developer"],
        data["rating"],
        game_id
    ))

    conn.commit()

    updated_game = conn.execute(
        "SELECT * FROM games WHERE id = ?",
        (game_id,)
    ).fetchone()

    conn.close()

    return jsonify(dict(updated_game)), 200

@app.route("/games/<int:game_id>", methods=["DELETE"])
def delete_game(game_id):
    conn = get_db()

    game = conn.execute(
        "SELECT * FROM games WHERE id = ?",
        (game_id,)
    ).fetchone()

    if game is None:
        conn.close()
        return jsonify({"error": "Game not found"}), 404

    conn.execute(
        "DELETE FROM games WHERE id = ?",
        (game_id,)
    )

    conn.commit()
    conn.close()

    return jsonify({"message": "Game deleted successfully", "id": game_id}), 200
        
init_db()

if __name__ == "__main__":
        app.run(debug=True)
