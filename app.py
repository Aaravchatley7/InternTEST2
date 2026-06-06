import os

from fastapi import (
    FastAPI,
    UploadFile,
    File
)

from rag import (
    process_pdf,
    retrieve,
    generate_answer
)

from confidence import (
    calculate_confidence_v2
)

from observability import (
    start_trace,
    end_trace,
    log_event,
    update_metrics,
    record_error,
    get_metrics
)

app = FastAPI(
    title="Confidence Aware RAG API v2"
)

UPLOAD_FOLDER = "uploads"

os.makedirs(
    UPLOAD_FOLDER,
    exist_ok=True
)


@app.get("/")
def home():

    return {
        "message":
            "Confidence Aware RAG API v2",
        "docs":
            "/docs"
    }


@app.get("/health")
def health():

    return {
        "status":
            "healthy"
    }


@app.get("/version")
def version():

    return {
        "version":
            "2.0.0"
    }


@app.post("/upload")
async def upload_pdf(
    file: UploadFile = File(...)
):

    file_path = os.path.join(
        UPLOAD_FOLDER,
        file.filename
    )

    with open(
        file_path,
        "wb"
    ) as f:

        f.write(
            await file.read()
        )

    chunks = process_pdf(
        file_path
    )

    return {
        "status":
            "success",

        "file":
            file.filename,

        "chunks_created":
            chunks
    }


@app.post("/ask")
def ask_question(
    question: str
):

    trace = start_trace()

    trace_id = trace["trace_id"]

    try:

        log_event(
            "request_started",
            trace_id
        )

        docs_with_scores = retrieve(
            question
        )

        log_event(
            "retrieval_complete",
            trace_id,
            {
                "chunks":
                    len(docs_with_scores)
            }
        )

        context = "\n\n".join(
            doc.page_content
            for doc, score
            in docs_with_scores
        )

        answer = generate_answer(
            question,
            context
        )

        scores = [
            score
            for doc, score
            in docs_with_scores
        ]

        confidence_data = (
            calculate_confidence_v2(
                scores,
                answer
            )
        )

        latency = end_trace(
            trace
        )

        update_metrics(
            latency,
            confidence_data["score"]
        )

        log_event(
            "request_completed",
            trace_id,
            {
                "latency_ms":
                    latency
            }
        )

        return {

            "answer":
                answer,

            "confidence":
                {
                    "score":
                        confidence_data["score"],

                    "level":
                        confidence_data["level"],

                    "reasons":
                        confidence_data["reasons"]
                },

            "explanation":
                {
                    "retrieved_chunks":
                        len(docs_with_scores),

                    "average_similarity":
                        confidence_data[
                            "avg_similarity"
                        ]
                },

            "sources": [
                {
                    "page":
                        int(
                            doc.metadata.get(
                                "page",
                                -1
                            )
                        )
                }
                for doc, score
                in docs_with_scores
            ],

            "observability":
                {
                    "trace_id":
                        trace_id,

                    "latency_ms":
                        latency
                }
        }

    except Exception as e:

        record_error()

        return {
            "error":
                str(e),

            "trace_id":
                trace_id
        }


@app.get("/metrics")
def metrics():

    return get_metrics()