import os

from src.parser import parse_log_file
from src.metrics import MetricsAnalyzer
from src.anomaly import AnomalyDetector

from concurrent.futures import (
    ThreadPoolExecutor
)

def process_single_file(file_path,threshold):
    metrics = MetricsAnalyzer()

    anomaly_detector = AnomalyDetector(
        threshold=threshold
    )

    for log in parse_log_file(file_path):
        metrics.process_log(log)

        anomaly_detector.process_log(log)

    return (metrics,anomaly_detector)

def get_log_files(log_dir):

    return [
        os.path.join(log_dir,file_name)
        for file_name in os.listdir(log_dir)
        if file_name.endswith(".log")
    ]

def process_logs_concurrently(log_dir,threshold):
    log_files = get_log_files(log_dir)

    with ThreadPoolExecutor() as executor:
        results = list(
            executor.map(
                lambda file_path:
                process_single_file(
                    file_path,
                    threshold
                ),
                log_files
            )
        )

    final_metrics = MetricsAnalyzer()

    final_anomaly = AnomalyDetector(
        threshold=threshold
    )

    for metrics, anomaly in results:
        final_metrics.merge(
            metrics
        )

        final_anomaly.merge(
            anomaly
        )
    
    return (
        final_metrics,
        final_anomaly
    )