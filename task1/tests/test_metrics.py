import unittest

from src.metrics import MetricsAnalyzer


class TestMetrics(unittest.TestCase):

    def test_metrics_processing(self):

        analyzer = MetricsAnalyzer()

        sample_log = {
            "timestamp": "dummy",
            "level": "ERROR",
            "service": "auth_service",
            "message": "Timeout occurred"
        }

        analyzer.process_log(sample_log)

        self.assertEqual(
            analyzer.total_logs,
            1
        )

        self.assertEqual(
            analyzer.level_counts["ERROR"],
            1
        )

        self.assertEqual(
            analyzer.service_counts["auth_service"],
            1
        )

        self.assertEqual(
            analyzer.error_counts["Timeout occurred"],
            1
        )


if __name__ == "__main__":
    unittest.main()