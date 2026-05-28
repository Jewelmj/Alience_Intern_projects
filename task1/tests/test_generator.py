import unittest

from scripts.generate_logs import (
    choose_level,
    generate_log_line
)

from datetime import datetime


class TestLogGenerator(unittest.TestCase):

    def test_choose_level(self):

        level = choose_level()

        self.assertIn(
            level,
            ["INFO", "WARN", "ERROR"]
        )

    def test_generate_log_line(self):

        timestamp = datetime.now()

        log_line = generate_log_line(
            timestamp
        )

        self.assertIsInstance(
            log_line,
            str
        )

        self.assertIn("|", log_line)


if __name__ == "__main__":
    unittest.main()