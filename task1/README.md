# Log Processing and Anomaly Detection

This project is based on a problem statement provided during an internship task at Allianz.

The objective is to build a Python-based log processing system capable of efficiently processing large log files, extracting structured insights, and detecting anomalies while maintaining low memory usage.

---

# Features

## Implemented Requirements

- Parse log files from a directory
- Convert log entries into structured Python dictionaries
- Compute summary metrics
- Detect anomalies using 5-minute windows
- Identify Top-K most frequent error messages
- Generate structured JSON output
- Process large files using generators for memory efficiency
- Handle malformed log entries gracefully
- Unit tests for all major components

---

# Project Objective

The system processes multiple log files containing application logs in the following format:

```text
YYYY-MM-DD HH:MM:SS | LEVEL | SERVICE_NAME | MESSAGE
```

Example:

```text
2026-03-18 10:15:23 | INFO | service_a | Request completed in 120ms
2026-03-18 10:15:24 | ERROR | service_b | Timeout occurred
```

---

# Tech Stack

- Python 3.12
- Conda Environment
- python-dotenv
- unittest

---

# Project Structure

project_root/
├── config/
├── logs/
├── output/
├── scripts/
├── src/
├── tests/
├── .env
├── requirements.txt
└── README.md

---

# Environment Setup

conda create -n log_processor python=3.12
conda activate log_processor
pip install -r requirements.txt

---

# Generate Sample Logs

python -m scripts.generate_logs

---

# Run Log Analysis

python -m src.main

---

# Testing

python -m unittest discover tests

---

# Architecture

Log Files
 -> Parser
 -> Metrics Analyzer
 -> Anomaly Detector
 -> JSON Output

---

# Completed Optional Enhancements

- Generators for memory-efficient processing
- Unit tests
- Malformed log handling

# Planned Enhancements

- Command Line Interface (CLI)
- Concurrent log processing