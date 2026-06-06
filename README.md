# Confidence-Aware RAG API v2

## Overview

Confidence-Aware RAG API v2 is a Retrieval-Augmented Generation (RAG) system designed with a strong focus on reliability, observability, maintainability, and engineering discipline.

Unlike traditional AI systems that only return answers, this project provides:

* Confidence Scoring
* Confidence Reasoning
* Source Attribution
* Request Tracing
* Latency Monitoring
* Metrics Collection
* Structured Logging

The goal is to make AI outputs more transparent, measurable, and easier to maintain.

---

# Problem Statement

Most AI systems return answers without indicating:

* Why the answer was generated
* How reliable the answer is
* What sources were used
* Whether the system is performing correctly

This project addresses those challenges by combining Retrieval-Augmented Generation (RAG) with Confidence Engine V2 and Observability Hardening.

---

# Key Features

## PDF Question Answering

Users can upload PDF documents and ask questions about the content.

The system:

1. Extracts PDF text
2. Splits content into chunks
3. Creates vector embeddings
4. Retrieves relevant chunks
5. Generates answers using OpenRouter

---

## Confidence Engine V2

Confidence is no longer a simple score.

The system evaluates:

* Retrieval similarity
* Source coverage
* Answer completeness
* Supporting evidence count

Example:

```json
{
  "score": 0.89,
  "level": "High",
  "reasons": [
    "High retrieval similarity",
    "Multiple supporting sources",
    "Complete answer generated"
  ]
}
```

This improves transparency and helps users understand answer reliability.

---

## Observability Hardening

Every request generates:

* Trace ID
* Latency metrics
* Structured logs

Example:

```json
{
  "trace_id": "f82a7d7f",
  "latency_ms": 412
}
```

Logs are stored in:

```text
logs/app.log
```

This makes troubleshooting and monitoring easier.

---

## Metrics Endpoint

The system continuously tracks:

* Total requests
* Error count
* Average latency
* Average confidence

Available at:

```text
GET /metrics
```

---

## Health Monitoring

Health endpoint:

```text
GET /health
```

Response:

```json
{
  "status": "healthy"
}
```

---

## Version Tracking

Version endpoint:

```text
GET /version
```

Response:

```json
{
  "version": "2.0.0"
}
```

---

# Architecture

PDF Upload
↓
Document Processing
↓
Chunking
↓
Embeddings
↓
FAISS Vector Store
↓
Retriever
↓
OpenRouter LLM
↓
Confidence Engine V2
↓
Observability Layer
↓
API Response

---

# Project Structure

```text
confidence-rag-api/
│
├── app.py
├── rag.py
├── confidence.py
├── observability.py
│
├── tests/
│   ├── test_confidence.py
│   └── test_observability.py
│
├── uploads/
├── vectorstore/
├── logs/
│
├── requirements.txt
├── README.md
├── .env.example
└── .gitignore
```

---

# V1 vs V2 Improvements

| Feature                | V1     | V2       |
| ---------------------- | ------ | -------- |
| RAG Question Answering | ✓      | ✓        |
| Confidence Score       | ✓      | ✓        |
| Confidence Reasons     | ✗      | ✓        |
| Structured Logging     | ✗      | ✓        |
| Health Endpoint        | ✗      | ✓        |
| Version Endpoint       | ✗      | ✓        |
| Observability Layer    | Basic  | Hardened |
| Modular Architecture   | ✗      | ✓        |
| Test Coverage          | ✗      | ✓        |
| Continuation Quality   | Medium | High     |

---

# Running the Project

Install dependencies:

```bash
pip install -r requirements.txt
```

Create:

```text
.env
```

Add:

```env
OPENROUTER_API_KEY=your_key_here
```

Run:

```bash
uvicorn app:app --reload
```

Swagger UI:

```text
http://127.0.0.1:8000/docs
```

---

# Testing

Run:

```bash
pytest
```

The test suite validates:

* Confidence Engine V2
* Confidence Levels
* Trace Generation
* Latency Tracking
* Metrics Collection

---

# Engineering Goals

This project prioritizes:

* Correctness
* Observability
* Maintainability
* Continuation Quality
* Testing Discipline

The repository is structured so that a new developer can understand, run, test, and extend the system with minimal onboarding effort.
