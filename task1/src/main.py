import json
import os

from config.settings import (
    LOG_DIR,
    OUTPUT_DIR,
    OUTPUT_FILE,
    ANOMALY_THRESHOLD,
)

from src.parser import parse_log_directory
from src.metrics import MetricsAnalyzer
from src.anomaly import AnomalyDetector

def main():
    metrics = MetricsAnalyzer()

    anomaly_detector = AnomalyDetector(
        threshold=ANOMALY_THRESHOLD
    )

    for log in parse_log_directory(LOG_DIR):

        metrics.process_log(log)

        anomaly_detector.process_log(log)

    result = {
        "summary": metrics.get_summary(),
        "top_errors": metrics.get_top_errors(),
        "anomalies": anomaly_detector.get_anomalies()
    }

    os.makedirs(
        OUTPUT_DIR,
        exist_ok=True
    )

    output_path = os.path.join(
        OUTPUT_DIR,
        OUTPUT_FILE
    )

    with open(output_path,"w") as file:
        json.dump(
            result,
            file,
            indent=4
        )

    print(f"Results written to {output_path}")

if __name__ == "__main__":
    main()