from facial_tracking_ml import FacialTracker
from game_logic import SwallowingGame
from ml_model import SwallowingModel


def main():
    print("Initializing Swallowing Function Training System...")

    # Initialize the ML model
    model = SwallowingModel()
    model.load_model()

    # Initialize facial tracking
    tracker = FacialTracker()
    tracker.start_camera()

    # Initialize the game
    game = SwallowingGame(model=model, tracker=tracker)
    game.start()

if __name__ == "__main__":
    main()