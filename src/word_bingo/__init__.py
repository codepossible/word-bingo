from datetime import datetime, timezone
from pathlib import Path
from random import choice
from typing import TypedDict
from uuid import uuid4

from flask import Flask, abort, redirect, render_template, url_for


class GameSession(TypedDict):
    id: str
    status: str
    created_at: str
    board: list[str | None]


app = Flask(__name__)
print(f"Loading words from {Path('./src/data/words.txt')}")
app.config["WORDS"] = (
    Path("./src/data/words.txt").read_text(encoding="utf-8").splitlines()
)
game_sessions: dict[str, GameSession] = {}


@app.get("/")
def home():
    active_sessions = sorted(
        (game for game in game_sessions.values() if game["status"] == "active"),
        key=lambda game: game["created_at"],
        reverse=True,
    )
    return render_template("home.html", active_sessions=active_sessions)


@app.post("/games")
def new_game():
    game_id = str(uuid4())
    game_sessions[game_id] = {
        "id": game_id,
        "status": "active",
        "created_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "board": [None] * len([word for word in app.config["WORDS"] if word.strip()]),
    }
    return redirect(url_for("show_game", game_id=game_id))


@app.get("/games/<game_id>")
def show_game(game_id: str):
    game = game_sessions.get(game_id)
    if game is None or game["status"] != "active":
        abort(404)
    return render_template("game.html", game=game)


@app.get("/games/<game_id>/words")
def show_words(game_id: str):
    game = game_sessions.get(game_id)
    if game is None or game["status"] != "active":
        abort(404)

    words = [word for word in app.config["WORDS"] if word.strip()]
    return render_template("words.html", game=game, words=words)


@app.get("/games/<game_id>/play")
def play_bingo(game_id: str):
    game = game_sessions.get(game_id)
    if game is None or game["status"] != "active":
        abort(404)

    words = [word for word in app.config["WORDS"] if word.strip()]
    called_words = {word for word in game["board"] if word is not None}
    available_words = [word for word in words if word not in called_words]
    next_cell = next(
        (index for index, word in enumerate(game["board"]) if word is None),
        None,
    )
    return render_template(
        "play.html",
        game=game,
        total_words=len(game["board"]),
        can_draw=bool(available_words) and None in game["board"],
        filled_count=sum(word is not None for word in game["board"]),
        rows=[
            (index // 3, game["board"][index : index + 3])
            for index in range(0, len(game["board"]), 3)
        ],
        next_cell=next_cell,
        next_row=next_cell // 3 if next_cell is not None else None,
    )


@app.post("/games/<game_id>/next")
def next_word(game_id: str):
    game = game_sessions.get(game_id)
    if game is None or game["status"] != "active":
        abort(404)

    empty_cell = next(
        (index for index, word in enumerate(game["board"]) if word is None), None
    )
    called_words = {word for word in game["board"] if word is not None}
    available_words = [
        word
        for word in app.config["WORDS"]
        if word.strip() and word not in called_words
    ]
    if empty_cell is not None and available_words:
        game["board"][empty_cell] = choice(available_words)

    next_cell = next(
        (index for index, word in enumerate(game["board"]) if word is None),
        None,
    )
    target_row = (
        next_cell // 3
        if next_cell is not None
        else max(0, (len(game["board"]) - 1) // 3)
    )
    return redirect(url_for("play_bingo", game_id=game_id, _anchor=f"row-{target_row}"))


@app.post("/games/<game_id>/clear")
def clear_board(game_id: str):
    game = game_sessions.get(game_id)
    if game is None or game["status"] != "active":
        abort(404)

    game["board"] = [None] * len(game["board"])
    return redirect(url_for("play_bingo", game_id=game_id, _anchor="row-0"))


@app.post("/games/<game_id>/end")
def end_game(game_id: str):
    game = game_sessions.get(game_id)
    if game is None or game["status"] != "active":
        abort(404)
    game["status"] = "ended"
    game["ended_at"] = datetime.now(timezone.utc).isoformat(timespec="seconds")
    return redirect(url_for("home"))


def main() -> None:
    app.run()
