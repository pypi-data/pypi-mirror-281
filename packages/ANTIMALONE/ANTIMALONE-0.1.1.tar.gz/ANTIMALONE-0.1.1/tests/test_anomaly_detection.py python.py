import unittest
import numpy as np
from antimalone.anomaly_detection import train_anomaly_detection_model, detect_anomalies

class TestAnomalyDetection(unittest.TestCase):

    def test_anomaly_detection(self):
        data = np.random.rand(100, 10)
        labels = np.random.randint(0, 2, 100)
        model = train_anomaly_detection_model(data, labels)
        file_metadata = np.random.rand(10)
        anomaly_score = detect_anomalies(model, file_metadata)
        self.assertIsInstance(anomaly_score, float)

if __name__ == '__main__':
    unittest.main()
