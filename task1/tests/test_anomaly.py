import unittest
from datetime import datetime
from src.anomaly import AnomalyDetector


class TestAnomalyDetector(unittest.TestCase):
    def test_anomaly_detected(self):
        detector = AnomalyDetector(threshold=2)

        logs = [
            {
                "timestamp": datetime(
                    2026, 3, 18, 10, 1, 0
                ),
                "level": "ERROR",
                "service": "service_a",
                "message": "Timeout occurred"
            },
            {
                "timestamp": datetime(
                    2026, 3, 18, 10, 2, 0
                ),
                "level": "ERROR",
                "service": "service_a",
                "message": "Timeout occurred"
            },
            {
                "timestamp": datetime(
                    2026, 3, 18, 10, 3, 0
                ),
                "level": "ERROR",
                "service": "service_a",
                "message": "Timeout occurred"
            }
        ]

        for log in logs:
            detector.process_log(log)

        anomalies = detector.get_anomalies()

        self.assertEqual(
            len(anomalies),
            1
        )

        self.assertEqual(
            anomalies[0]["error_count"],
            3
        )

    def test_no_anomaly_detected(self):

        detector = AnomalyDetector(
            threshold=5
        )

        logs = [
            {
                "timestamp": datetime(
                    2026, 3, 18, 10, 1, 0
                ),
                "level": "ERROR",
                "service": "service_a",
                "message": "Timeout occurred"
            },
            {
                "timestamp": datetime(
                    2026, 3, 18, 10, 2, 0
                ),
                "level": "ERROR",
                "service": "service_a",
                "message": "Timeout occurred"
            }
        ]

        for log in logs:
            detector.process_log(log)

        anomalies = detector.get_anomalies()

        self.assertEqual(
            len(anomalies),
            0
        )

    def test_non_error_logs_ignored(self):

        detector = AnomalyDetector(
            threshold=1
        )

        log = {
            "timestamp": datetime(
                2026, 3, 18, 10, 1, 0
            ),
            "level": "INFO",
            "service": "service_a",
            "message": "Request completed"
        }

        detector.process_log(log)

        anomalies = detector.get_anomalies()

        self.assertEqual(
            len(anomalies),
            0
        )


if __name__ == "__main__":
    unittest.main()