import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense


def train_anomaly_detection_model(data, labels):
    """Train a deep learning model for anomaly detection."""
    model = Sequential()
    model.add(Dense(128, activation='relu', input_shape=(data.shape[1],)))
    model.add(Dense(64, activation='relu'))
    model.add(Dense(32, activation='relu'))
    model.add(Dense(1, activation='sigmoid'))

    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
    model.fit(data, labels, epochs=10, batch_size=32)

    return model


def detect_anomalies(model, file_metadata):
    """Detect anomalies using the trained deep learning model."""
    file_metadata = np.array(file_metadata).reshape(1, -1)
    anomaly_score = model.predict(file_metadata)[0][0]

    return anomaly_score
