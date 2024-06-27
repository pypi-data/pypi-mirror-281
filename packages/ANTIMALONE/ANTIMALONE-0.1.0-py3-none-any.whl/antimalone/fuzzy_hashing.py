import numpy as np
import hashlib
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Flatten, Conv1D


def train_fuzzy_hash_model(data, labels):
    """Train a neural network model to generate fuzzy hashes."""
    model = Sequential()
    model.add(Conv1D(64, 3, activation='relu', input_shape=(4096, 1)))
    model.add(Flatten())
    model.add(Dense(256, activation='relu'))
    model.add(Dense(64, activation='sigmoid'))

    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
    model.fit(data, labels, epochs=10, batch_size=32)

    return model


def generate_fuzzy_hash(model, byte_array):
    """Generate a fuzzy hash using the trained neural network model."""
    byte_array = np.array(byte_array[:4096]).reshape(1, 4096, 1)
    hash_vector = model.predict(byte_array)[0]
    fuzzy_hash = hashlib.sha256(hash_vector.tobytes()).hexdigest()

    return fuzzy_hash
