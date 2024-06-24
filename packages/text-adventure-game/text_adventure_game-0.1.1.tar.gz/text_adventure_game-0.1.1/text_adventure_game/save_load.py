import pickle
import os

SAVE_FILE = "savegame.pkl"

def save_game(game):
    with open(SAVE_FILE, "wb") as f:
        pickle.dump(game, f)

def load_game():
    if os.path.exists(SAVE_FILE):
        with open(SAVE_FILE, "rb") as f:
            game = pickle.load(f)
        return game
    return None
