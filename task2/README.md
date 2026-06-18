# Chat Engine Assignment

Step 1 of the final project "Chat Engine Assignment", where multiple agents work together to perform RAG operations.

## Tech Stack

- Python 3.12
- Conda
- FastAPI

## Current Features

### File Upload API

The upload endpoint supports:

- Uploading up to the configured maximum number of files.
- File type validation using environment configuration.
- Persistent storage of uploaded files.
- Automatic duplicate filename handling.
- Upload status responses.

### Supported File Types

- PDF
- PNG
- JPG
- JPEG

## Setup

```bash
conda create -n final_project_alience_intern python=3.12
conda activate final_project_alience_intern

pip install -r requirements.txt
```

## Example API Test

```bash
curl.exe -X POST `
  -F "files=@storage/uploads/test_file-sample_150kB.pdf" `
  -F "files=@storage/uploads/test_sample.pdf" `
  http://127.0.0.1:8000/upload
```
```bash
curl.exe -X POST http://127.0.0.1:8000/chat ^
  -H "Content-Type: application/json" ^
  -d "{\"query\": \"What is covered in the document?\"}"
```

## Example Response

```json
{
  "status": "success",
  "files": [
    "test_file-sample_150kB_1.pdf",
    "test_sample_1.pdf"
  ]
}
```

## Project Structure

```text
chat_engine/

├── api/
├── agents/
│   ├── conversation/
│   ├── embedding/
│   ├── extraction/ 
│   ├── ingestion/
├── config/
├── logs/
├── models/
├── schema/
│   ├── prompts/
│   ├── tests/
│   └── utils/
├── documentation/
├── storage/
│   ├── uploads/
│   ├── vectordb/
│   └── extracted_txt/
├── ui/
└── .env
└── main.py
└── README.md
└── requirements.txt
```

## Current Progress

- [x] File Upload API
- [ ] Text Extraction
- [ ] Embedding Generation
- [ ] Vector Database Integration
- [ ] Retrieval Pipeline
- [ ] Chat Interface