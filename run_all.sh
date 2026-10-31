#!/bin/bash
gnome-terminal -- python3 backend_ml.py &
gnome-terminal -- python3 facial_tracking_ml.py &
gnome-terminal -- python3 game_ml.py




project_directory/
├── main.py               # Main application script
├── facial_tracking.py    # Handles facial tracking and landmark detection
├── game_logic.py         # Contains the logic for the therapeutic games
├── ml_model.py           # ML model creation and training
├── utils.py              # Utility functions
├── config.json           # Configuration file
├── ml_model.h5           # Pretrained machine learning model
├── requirements.txt      # Required Python packages
└── assets/               # Assets for the game (images, sounds, etc.)
    ├── background.png
    ├── button.png
    ├── ...





project_directory/
├── app/
│   ├── __init__.py             # Marks the app directory as a package
│   ├── main.py                 # Main application script
│   ├── facial_tracking.py      # Facial tracking and recognition logic
│   ├── game_logic.py           # Game-based exercises logic
│   ├── ml_model.py             # Machine learning model creation and evaluation
│   └── feedback_system.py      # System to provide user feedback
├── models/
│   └── swallowing_model.h5     # Pre-trained machine learning model
├── assets/
│   ├── images/                 # Game visuals
│   ├── sounds/                 # Game sounds
│   └── videos/                 # Tutorial or instruction videos
├── docs/
│   ├── README.md               # Project documentation
│   └── How_To_Run.md           # Instructions for running the project
├── config.json                 # Configuration file for parameters
├── requirements.txt            # Python dependencies
└── LICENSE                     # License for the project





SwallowTrainingSystem/
├── src/
│   ├── exercises/
│   │   ├── lip_exercise.py
│   │   ├── tongue_exercise.py
│   │   ├── jaw_exercise.py
│   ├── utils/
│   │   ├── mediapipe_tracker.py
│   │   ├── feedback.py
│   └── main.py
├── assets/
│   ├── images/
│   ├── sounds/
├── requirements.txt
└── README.md




# Catch The Egg Game - Main Script -- waiting 


only run 

python3 game.py 

in terminal 