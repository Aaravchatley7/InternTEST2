import os
import uuid
import time
import requests

from dotenv import load_dotenv

from fastapi import FastAPI, UploadFile, File
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

app = FastAPI(
    title="Confidence Scoring + Observability RAG API"
)

UPLOAD_FOLDER = "uploads"
VECTOR_FOLDER = "vectorstore"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(VECTOR_FOLDER, exist_ok=True)



metrics_data = {
    "total_requests": 0,
    "total_errors": 0,
    "latencies": [],
    "confidences": []
}


embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

@app.get("/")
def home():
    return {
        "message": "Confidence Scoring + Observability API Running",
        "docs": "/docs"
    }



@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):

    file_path = os.path.join(
        UPLOAD_FOLDER,
        file.filename
    )

    with open(file_path, "wb") as f:
        f.write(await file.read())

    loader = PyPDFLoader(file_path)
    documents = loader.load()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )

    chunks = splitter.split_documents(documents)

    vectorstore = FAISS.from_documents(
        chunks,
        embedding_model
    )

    vectorstore.save_local(VECTOR_FOLDER)

    return {
        "status": "success",
        "file": file.filename,
        "chunks_created": len(chunks)
    }

def generate_answer(question, context):

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "openai/gpt-3.5-turbo",
        "messages": [
            {
                "role": "system",
                "content": "Answer only using the provided context."
            },
            {
                "role": "user",
                "content": f"Context:\n{context}\n\nQuestion:\n{question}"
            }
        ]
    }

    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers=headers,
        json=payload
    )

    print("STATUS:", response.status_code)
    print("RESPONSE:", response.text)

    data = response.json()

    if "choices" not in data:
        raise Exception(f"OpenRouter Error: {data}")

    return data["choices"][0]["message"]["content"]



def calculate_confidence(scores, answer):

    similarities = [
        1 / (1 + score)
        for score in scores
    ]

    avg_similarity = (
        sum(similarities)
        / len(similarities)
    )

    answer_quality = 1.0

    if len(answer) < 50:
        answer_quality = 0.6

    source_coverage = min(
        len(scores) / 4,
        1
    )

    confidence = (
        avg_similarity * 0.5
        + answer_quality * 0.2
        + source_coverage * 0.3
    )

    return float(round(confidence, 2))


def confidence_level(score):

    if score >= 0.85:
        return "High"

    if score >= 0.65:
        return "Medium"

    return "Low"


@app.post("/ask")
def ask_question(question: str):

    trace_id = str(uuid.uuid4())

    start_time = time.time()

    try:

        db = FAISS.load_local(
            VECTOR_FOLDER,
            embedding_model,
            allow_dangerous_deserialization=True
        )

        docs_with_scores = db.similarity_search_with_score(
            question,
            k=4
        )

        context = "\n\n".join(
            doc.page_content
            for doc, score in docs_with_scores
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

        confidence = calculate_confidence(
            scores,
            answer
        )

        latency = round(
            (time.time() - start_time) * 1000,
            2
        )

        metrics_data["total_requests"] += 1
        metrics_data["latencies"].append(latency)
        metrics_data["confidences"].append(confidence)
        avg_similarity = float(
                    round(
                        sum(
                            float(1/(1+float(s)))
                            for s in scores
                        ) / len(scores),
                        2
                    )
                )

        return {

            "answer": answer,

            "confidence_score": confidence,

            "confidence_level":
                confidence_level(confidence),

            "explanation": {
                "retrieved_chunks":len(docs_with_scores),
                "average_similarity": avg_similarity

                
            },

            "sources": [
                {
                    "page":
                        doc.metadata.get(
                            "page",
                            "unknown"
                        )
                }
                for doc, score
                in docs_with_scores
            ],

            "observability": {
                "trace_id": trace_id,
                "latency_ms": latency
            }
        }

    except Exception as e:

        metrics_data["total_errors"] += 1

        return {
            "error": str(e),
            "trace_id": trace_id
        }



@app.get("/metrics")
def get_metrics():

    avg_latency = 0

    if metrics_data["latencies"]:
        avg_latency = round(
            sum(metrics_data["latencies"])
            / len(metrics_data["latencies"]),
            2
        )

    avg_confidence = 0

    if metrics_data["confidences"]:
        avg_confidence = round(
            sum(metrics_data["confidences"])
            / len(metrics_data["confidences"]),
            2
        )

    return {

        "total_requests":
            metrics_data["total_requests"],

        "total_errors":
            metrics_data["total_errors"],

        "average_latency_ms":
            avg_latency,

        "average_confidence":
            avg_confidence
    }