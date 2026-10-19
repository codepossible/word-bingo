
# Word Bingo

## Introduction

This is a web based game which allows game organizer to run a Word Bingo game.
The idea is simple. The words for the game are stored in the file `src/data/words.txt`. When the application launches it reads this file and make the words available as a list for players to see and then in the game mode, presents the same mode in random. The system allows multiple game sessions to run. The user - game master can join/leave session at will or end the session.

## Running the code locally

### Pre-requisites

- Git Client
- Python version 3.14 or higher
- uv (Rust based python toolchain)
- PyEnv (recommended, if you have multiple python versions)

### Running code locally

1. Ensure all pre-requisites tooling are met on your development machine.
2. On the terminal window of your development machine, download the code locally to to the folder of your choice with the command - `git clone <ssh|http URL from GitHub>`
3. Navigate to the root folder to the repository.
4. Run the command `uv sync` to download the dependencies.
5. The command above creates a python virtual environment under the folder - `.venv`. Activate the virtual environment with the command `source .venv/bin/activate`. (Deactivate the virtual environment with the command `deactivate`)
6. Launch the application using the command - `uv run word-bingo` and navigate to `http://127.0.0.1:5000` in the browser of your choice.

## How to play the game

Start the application with `word-bingo` as shown in the section above nd open `http://127.0.0.1:5000`.

The home page starts a new game or lists active games that can be resumed.
Game sessions are stored in memory and are cleared when the application
restarts.

Each game offers two modes: browse all words in a three-column grid, or play
bingo by drawing one unused random word at a time into the next open space on a
three-column board with one row per three words.
