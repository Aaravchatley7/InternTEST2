# Confidence-Aware RAG API with Observability

A Retrieval-Augmented Generation (RAG) API built with FastAPI that not only answers questions from uploaded PDF documents but also provides confidence scoring, explainability, and observability metrics.

## Overview

Traditional AI systems often return answers without indicating how reliable they are. This project enhances a standard RAG pipeline by introducing:

* Confidence Scoring
* Explainability
* Source Attribution
* Request Tracing
* Latency Monitoring
* API Observability

The system allows users to upload PDF documents, ask questions, and receive answers along with metadata that explains how the answer was generated and how trustworthy it is.

---

## Features

### PDF Document Upload

* Upload PDF documents through an API endpoint.
* Documents are automatically parsed and chunked.
* Chunks are indexed into a FAISS vector database.

### Retrieval-Augmented Generation (RAG)

* Retrieves the most relevant chunks for a user query.
* Uses semantic search with sentence embeddings.
* Generates answers using OpenRouter LLMs.

### Confidence Scoring

Each response includes:

* Confidence Score (0–1)
* Confidence Level (High / Medium / Low)

Confidence is calculated using:

* Retrieval similarity
* Source coverage
* Answer quality heuristics

### Explainability

Every response includes:

* Number of retrieved chunks
* Average similarity score
* Source pages used

### Observability

Every request generates:

* Trace ID
* Latency measurement
* Request statistics

### Metrics Endpoint

Track:

* Total requests
* Average confidence
* Average latency
* Error count

---

## Architecture

PDF Upload
↓
Document Parsing
↓
Chunking
↓
Embeddings (all-MiniLM-L6-v2)
↓
FAISS Vector Store
↓
Retriever
↓
OpenRouter LLM
↓
Confidence Scoring
↓
Observability Layer
↓
API Response

---

## Tech Stack

### Backend

* FastAPI
* Uvicorn

### Retrieval Layer

* LangChain
* FAISS
* HuggingFace Embeddings

### LLM

* OpenRouter API (Key from OpenRouter website)
* Mistral / GPT Models

### Document Processing

* PyPDF

### Utilities

* Python Dotenv
* Requests

---

## Project Structure

```text
confidence_rag_api/
│
├── app.py
├── requirements.txt
├── .env
├── uploads/
└── vectorstore/
```

---

## Installation

### Clone Repository

```bash
git clone <your-repository-url>
cd confidence_rag_api
```

### Create Virtual Environment

```bash
python -m venv venv
```

Activate:

Windows

```bash
venv\Scripts\activate
```

Linux / Mac

```bash
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Environment Variables

Create a `.env` file:

```env
OPENROUTER_API_KEY=your_openrouter_api_key
```

---

## Run Application

```bash
uvicorn app:app --reload
```

Application:

```text
http://127.0.0.1:8000
```

Swagger Documentation:

```text
http://127.0.0.1:8000/docs
```

---

## API Endpoints

### Upload PDF

**POST** `/upload`

Upload a PDF document and create vector embeddings.

Response:

```json
{
  "status": "success",
  "file": "sample.pdf",
  "chunks_created": 42
}
```

---

### Ask Question

**POST** `/ask`

Parameters:

```text
question=What is conditional probability?
```

Response:

```json
{
  "answer": "Conditional probability is the probability of an event occurring given that another event has already occurred.",
  "confidence_score": 0.89,
  "confidence_level": "High",
  "explanation": {
    "retrieved_chunks": 4,
    "average_similarity": 0.83
  },
  "sources": [
    {
      "page": 12
    }
  ],
  "observability": {
    "trace_id": "f82a7d7f-5e2d-4d95-b03c-123456789abc",
    "latency_ms": 532
  }
}
```

---

### Metrics

**GET** `/metrics`

Response:

```json
{
  "total_requests": 15,
  "total_errors": 0,
  "average_latency_ms": 420,
  "average_confidence": 0.86
}
```

---

## Confidence Scoring

The confidence score is calculated using:

```text
Confidence =
(Avg Similarity × 0.5)
+
(Answer Quality × 0.2)
+
(Source Coverage × 0.3)
```

Where:

* Avg Similarity = Average retrieval similarity score
* Answer Quality = Heuristic based on answer completeness
* Source Coverage = Number of supporting chunks retrieved

Confidence Levels:

| Score Range | Level  |
| ----------- | ------ |
| ≥ 0.85      | High   |
| 0.65 – 0.84 | Medium |
| < 0.65      | Low    |

---

## Observability Metrics

The system tracks:

* Request Count
* Error Count
* Average Latency
* Average Confidence
* Trace IDs

These metrics help monitor system performance and answer reliability.

---

## Example Workflow

1. Upload a PDF document.
2. Ask a question related to the document.
3. View:

   * Generated answer
   * Confidence score
   * Confidence level
   * Source pages
   * Latency
   * Trace ID
4. Monitor usage through `/metrics`.

---

## Future Improvements

* Prometheus Integration
* Grafana Dashboard
* Multi-document Support
* Persistent Vector Storage
* Advanced Confidence Models
* User Authentication
* Streaming Responses

---

## Author

**Aarav Chatley**

Applied AI Engineering Project – Confidence Scoring & Observability API Layer
