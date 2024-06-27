import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense


def train_indexing_model(data, labels):
    """Train a neural network model for structural and behavioral indexing."""
    model = Sequential()
    model.add(Dense(128, activation='relu', input_shape=(data.shape[1],)))
    model.add(Dense(64, activation='relu'))
    model.add(Dense(32, activation='relu'))
    model.add(Dense(16, activation='sigmoid'))

    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
    model.fit(data, labels, epochs=10, batch_size=32)

    return model


def create_index(model, features):
    """Create an index using the trained neural network model."""
    features = np.array(features).reshape(1, -1)
    index = model.predict(features)[0]

    return index
