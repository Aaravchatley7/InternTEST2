import os
import requests

from dotenv import load_dotenv

from langchain_community.document_loaders import (
    PyPDFLoader
)

from langchain.text_splitter import (
    RecursiveCharacterTextSplitter
)

from langchain_huggingface import (
    HuggingFaceEmbeddings
)

from langchain_community.vectorstores import (
    FAISS
)

load_dotenv()

OPENROUTER_API_KEY = os.getenv(
    "OPENROUTER_API_KEY"
)

VECTOR_FOLDER = "vectorstore"

embedding_model = HuggingFaceEmbeddings(
    model_name=
    "sentence-transformers/all-MiniLM-L6-v2"
)


def process_pdf(file_path):

    loader = PyPDFLoader(file_path)

    docs = loader.load()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )

    chunks = splitter.split_documents(
        docs
    )

    vectorstore = FAISS.from_documents(
        chunks,
        embedding_model
    )

    vectorstore.save_local(
        VECTOR_FOLDER
    )

    return len(chunks)


def retrieve(question):

    db = FAISS.load_local(
        VECTOR_FOLDER,
        embedding_model,
        allow_dangerous_deserialization=True
    )

    return db.similarity_search_with_score(
        question,
        k=4
    )


def generate_answer(
    question,
    context
):

    headers = {
        "Authorization":
            f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type":
            "application/json"
    }

    payload = {
        "model":
            "openai/gpt-3.5-turbo",

        "messages": [
            {
                "role":
                    "system",

                "content":
                    "Answer only using provided context."
            },
            {
                "role":
                    "user",

                "content":
                    f"Context:\n{context}\n\nQuestion:{question}"
            }
        ]
    }

    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers=headers,
        json=payload
    )

    data = response.json()

    if "choices" not in data:
        raise Exception(
            f"OpenRouter Error: {data}"
        )

    return data["choices"][0]["message"]["content"]