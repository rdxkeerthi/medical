import tensorflow as tf
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import Dense
import numpy as np

class SwallowingModel:
    def __init__(self):
        self.model = Sequential([
            Dense(128, activation="relu", input_shape=(204,)),
            Dense(64, activation="relu"),
            Dense(1, activation="sigmoid")
        ])
        self.model.compile(optimizer="adam", loss="binary_crossentropy", metrics=["accuracy"])

    def train(self, x_train, y_train, epochs=10, batch_size=32):
        self.model.fit(x_train, y_train, epochs=epochs, batch_size=batch_size)

    def save_model(self, filepath="models/ml_model.h5"):
        self.model.save(filepath)
        print(f"Model saved to {filepath}")

    def load_model(self, filepath="models/ml_model.h5"):
        try:
            self.model = load_model(filepath)
            print(f"Model loaded from {filepath}")
        except Exception as e:
            print(f"Failed to load model: {e}")

    def predict(self, landmarks):
        data = np.array(landmarks).flatten()
        if data.shape[0] < 204:
            data = np.pad(data, (0, 204 - data.shape[0]), 'constant')
        elif data.shape[0] > 204:
            data = data[:204]
        return self.model.predict(data.reshape(1, -1))