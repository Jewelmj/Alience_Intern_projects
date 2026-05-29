import json
import os
import argparse

from config.settings import (
    LOG_DIR,
    OUTPUT_DIR,
    OUTPUT_FILE,
    ANOMALY_THRESHOLD,
)

from src.concurrent_processor import (process_logs_concurrently)

def parse_arguments():

    parser = argparse.ArgumentParser(
        description="Log Processing and Anomaly Detection"
    )

    parser.add_argument(
        "--log-dir",
        default=LOG_DIR,
        help="Directory containing log files"
    )

    parser.add_argument(
        "--threshold",
        type=int,
        default=ANOMALY_THRESHOLD,
        help="Error threshold for anomaly detection"
    )

    return parser.parse_args()

def main():
    args = parse_arguments()

    metrics, anomaly_detector = (
        process_logs_concurrently(
            args.log_dir,
            args.threshold
        )
    )

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