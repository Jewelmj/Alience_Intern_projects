import os
import tempfile
import unittest

from src.metrics import MetricsAnalyzer
from src.anomaly import AnomalyDetector
from src.concurrent_processor import (
    process_logs_concurrently
)


class TestConcurrentProcessor(unittest.TestCase):

    def test_metrics_merge(self):

        metrics_1 = MetricsAnalyzer()

        metrics_2 = MetricsAnalyzer()

        log_1 = {
            "level": "INFO",
            "service": "service_a",
            "message": "Request completed"
        }

        log_2 = {
            "level": "ERROR",
            "service": "service_b",
            "message": "Timeout occurred"
        }

        metrics_1.process_log(log_1)

        metrics_2.process_log(log_2)

        metrics_1.merge(metrics_2)

        self.assertEqual(
            metrics_1.total_logs,
            2
        )

        self.assertEqual(
            metrics_1.level_counts["INFO"],
            1
        )

        self.assertEqual(
            metrics_1.level_counts["ERROR"],
            1
        )

        self.assertEqual(
            metrics_1.service_counts["service_a"],
            1
        )

        self.assertEqual(
            metrics_1.service_counts["service_b"],
            1
        )

    def test_anomaly_merge(self):

        detector_1 = AnomalyDetector(
            threshold=10
        )

        detector_2 = AnomalyDetector(
            threshold=10
        )

        from datetime import datetime

        log_1 = {
            "timestamp": datetime(
                2026, 3, 18, 10, 1, 0
            ),
            "level": "ERROR",
            "service": "service_a",
            "message": "Timeout occurred"
        }

        log_2 = {
            "timestamp": datetime(
                2026, 3, 18, 10, 2, 0
            ),
            "level": "ERROR",
            "service": "service_a",
            "message": "Timeout occurred"
        }

        detector_1.process_log(log_1)

        detector_2.process_log(log_2)

        detector_1.merge(detector_2)

        self.assertEqual(
            sum(
                detector_1.error_windows.values()
            ),
            2
        )

    def test_concurrent_processing(self):

        with tempfile.TemporaryDirectory() as temp_dir:

            file_1 = os.path.join(
                temp_dir,
                "log_1.log"
            )

            file_2 = os.path.join(
                temp_dir,
                "log_2.log"
            )

            with open(
                file_1,
                "w"
            ) as f:

                f.write(
                    "2026-03-18 10:00:00 | INFO | service_a | Request completed\n"
                )

                f.write(
                    "2026-03-18 10:01:00 | ERROR | service_a | Timeout occurred\n"
                )

            with open(
                file_2,
                "w"
            ) as f:

                f.write(
                    "2026-03-18 10:02:00 | ERROR | service_b | Timeout occurred\n"
                )

                f.write(
                    "2026-03-18 10:03:00 | WARN | service_b | Retry attempt\n"
                )

            metrics, anomaly_detector = (
                process_logs_concurrently(
                    temp_dir,
                    threshold=10
                )
            )

            self.assertEqual(
                metrics.total_logs,
                4
            )

            self.assertEqual(
                metrics.level_counts["INFO"],
                1
            )

            self.assertEqual(
                metrics.level_counts["ERROR"],
                2
            )

            self.assertEqual(
                metrics.level_counts["WARN"],
                1
            )

            self.assertEqual(
                metrics.service_counts["service_a"],
                2
            )

            self.assertEqual(
                metrics.service_counts["service_b"],
                2
            )

            self.assertEqual(
                metrics.error_counts[
                    "Timeout occurred"
                ],
                2
            )

            self.assertEqual(
                len(
                    anomaly_detector.get_anomalies()
                ),
                0
            )


if __name__ == "__main__":
    unittest.main()