# Log Processing and Anomaly Detection

This project is based on a problem statement given during an internship task at Allianz.  
The objective is to build a Python-based log processing system capable of handling large log files efficiently while extracting structured insights and detecting anomalies.

---

# Tech Stack

- Python 3.12
- Conda Environment
- Standard Python Libraries
- `python-dotenv` for environment configuration

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

The project focuses on:

- Efficient log parsing
- Memory-efficient processing
- Summary metric generation
- Sliding window anomaly detection
- Top-K error analysis

---

# Environment Setup

## Create Conda Environment

```bash
conda create -n log_processor python=3.12
```

## Activate Environment

```bash
conda activate log_processor
```

## Install Requirements

```bash
pip install -r requirements.txt
```

---

# Running the Log Generator

Generate sample log files using:

```bash
python -m scripts.generate_logs
```

This creates large log datasets for testing and analysis.

---

# Running Tests

Run unit tests using:

```bash
python -m unittest tests.test_generator
```
