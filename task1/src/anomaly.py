from collections import Counter
from datetime import timedelta

class AnomalyDetector:
    def __init__(self, threshold):
        self.threshold = threshold
        self.error_windows = Counter()
    
    def get_window_start(self, timestamp):
        window_minute = (timestamp.minute // 5) * 5

        return timestamp.replace(
            minute=window_minute,
            second=0,
            microsecond=0
        )
    
    def process_log(self, log):
        if log["level"] != "ERROR":
            return

        window_start = self.get_window_start(
            log["timestamp"]
        )

        self.error_windows[window_start] += 1

    def get_anomalies(self):
        anomalies = []

        for window_start, count in (
            self.error_windows.items()
        ):

            if count > self.threshold:

                anomalies.append(
                    {
                        "window_start":
                            window_start.strftime(
                                "%Y-%m-%d %H:%M:%S"
                            ),

                        "window_end":
                            (
                                window_start +
                                timedelta(minutes=5)
                            ).strftime(
                                "%Y-%m-%d %H:%M:%S"
                            ),

                        "error_count": count
                    }
                )

        return anomalies
    
    def merge(self, other):
        self.error_windows.update(
            other.error_windows
        )