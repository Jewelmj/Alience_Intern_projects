from collections import Counter

class MetricsAnalyzer:
    def __init__(self):
        self.total_logs = 0

        self.level_counts = Counter()

        self.service_counts = Counter()

        self.error_counts = Counter()

        self.service_errors = Counter()

    def process_log(self, log):
        self.total_logs += 1

        level = log["level"]

        service = log["service"]

        message = log["message"]

        self.level_counts[level] += 1

        self.service_counts[service] += 1

        if level == "ERROR":

            self.error_counts[message] += 1

            self.service_errors[service] += 1

    def get_error_rates(self):
        error_rates = {}

        for service in self.service_counts:

            total = self.service_counts[service]

            errors = self.service_errors[service]

            error_rate = errors / total

            error_rates[service] = round(
                error_rate,
                4
            )

        return error_rates
    
    def get_top_errors(self, k=5):
        return [
            {
                "message": message,
                "count": count
            }
            for message, count
            in self.error_counts.most_common(k)
        ]
    
    def get_summary(self):
        return {
            "total_logs": self.total_logs,

            "levels": dict(
                self.level_counts
            ),

            "services": dict(
                self.service_counts
            ),

            "error_rates": self.get_error_rates()
        }
    
    def merge(self, other):
        self.total_logs += other.total_logs

        self.level_counts.update(
            other.level_counts
        )

        self.service_counts.update(
            other.service_counts
        )

        self.error_counts.update(
            other.error_counts
        )

        self.service_errors.update(
            other.service_errors
        )