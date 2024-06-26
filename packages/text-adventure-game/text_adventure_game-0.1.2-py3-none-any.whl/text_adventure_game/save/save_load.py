import pickle

def save_game(game, filename='savegame.pkl'):
    with open(filename, 'wb') as file:
        pickle.dump(game, file)
    print(f"Game saved to {filename}.")

def load_game(filename='savegame.pkl'):
    try:
        with open(filename, 'rb') as file:
            game = pickle.load(file)
        print(f"Game loaded from {filename}.")
        return game
    except FileNotFoundError:
        print("Save file not found.")
        return None
