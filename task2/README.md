## Overview

Chat Engine is a Retrieval-Augmented Generation (RAG) system that allows users to upload documents and ask questions about their contents through a Streamlit interface powered by FastAPI, ChromaDB, SentenceTransformers, and Ollama.

## Tech Stack

- Python 3.12
- Conda
- FastAPI
- Streamlit
- ChromaDB
- Ollama
- SentenceTransformers

## Setup

```bash
conda create -n final_project_alience_intern python=3.12

conda activate final_project_alience_intern

pip install -r requirements.txt
```

## Ollama Setup

Pull the required model:

```bash
ollama pull llama3.2
```

Start the Ollama server:

```bash
ollama serve
```

## Environment Configuration

Copy the example environment file:

```bash
cp .env.example .env
```

Update values as needed before starting the application.

## Optional GPU Acceleration

Install a CUDA-enabled PyTorch build:

```bash
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu132
```

## Project Architecture

### Upload Flow

```text
Streamlit UI
    ↓
POST /upload
    ↓
IngestionAgent
    ↓
ExtractionAgent
    ↓
Chunking
    ↓
EmbeddingAgent
    ↓
ChromaDB
```

### Chat Flow

```text
Streamlit UI
    ↓
POST /chat
    ↓
RetrievalAgent
    ↓
ChromaDB Similarity Search
    ↓
RAG Prompt Builder
    ↓
Ollama (llama3.2)
    ↓
Response
```

## Run FastAPI

```bash
uvicorn main:app --reload
```

## Run Streamlit

```bash
streamlit run ui/app.py
```

## Example Workflow

1. Start Ollama

```bash
ollama serve
```

2. Start FastAPI

```bash
uvicorn main:app --reload
```

3. Start Streamlit

```bash
streamlit run ui/app.py
```

4. Upload documents through the UI

5. Ask questions about the uploaded documents

## Example API Test

Upload documents:

```bash
curl.exe -X POST ^
  -F "files=@document.pdf" ^
  http://127.0.0.1:8000/upload
```

Chat with uploaded documents:

```bash
curl.exe -X POST http://127.0.0.1:8000/chat ^
  -H "Content-Type: application/json" ^
  -d "{\"query\":\"What is covered in the document?\",\"session_id\":\"<session_id>\"}"
```

## Example Response

```json
{
  "status": "success",
  "session_id": "12345678-abcd-1234-abcd-1234567890ab",
  "files": [
    {
      "document_id": "abc123",
      "filename": "document.pdf",
      "page_count": 5,
      "characters": 1200
    }
  ]
}
```

## Project Status

- [x] Agent 1 - Ingestion Agent
- [x] Agent 2 - Embedding Agent
- [x] Agent 3 - Retrieval Agent
- [x] FastAPI Backend
- [x] ChromaDB Integration
- [x] Session-Aware Retrieval
- [x] Streamlit UI