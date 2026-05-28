import unittest

from src.parser import parse_log_line


class TestParser(unittest.TestCase):

    def test_valid_log_line(self):

        line = (
            "2026-03-18 10:15:24 | "
            "ERROR | "
            "service_b | "
            "Timeout occurred"
        )

        parsed = parse_log_line(line)

        self.assertEqual(
            parsed["level"],
            "ERROR"
        )

        self.assertEqual(
            parsed["service"],
            "service_b"
        )

        self.assertEqual(
            parsed["message"],
            "Timeout occurred"
        )

    def test_malformed_log_line(self):

        line = "INVALID LOG"

        parsed = parse_log_line(line)

        self.assertIsNone(parsed)


if __name__ == "__main__":
    unittest.main()