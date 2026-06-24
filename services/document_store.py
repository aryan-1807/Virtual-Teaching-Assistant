import os
import pickle

DOCUMENT_PATH = "data/processed/document.txt"
VECTOR_PATH = "data/processed/vector_store.pkl"


def save_document(text):
    os.makedirs("data/processed", exist_ok=True)

    with open(DOCUMENT_PATH, "w", encoding="utf-8") as f:
        f.write(text)


def load_document():
    if not os.path.exists(DOCUMENT_PATH):
        return ""

    with open(DOCUMENT_PATH, "r", encoding="utf-8") as f:
        return f.read()


def save_vector_store(index, chunks):
    with open(VECTOR_PATH, "wb") as f:
        pickle.dump(
            {
                "index": index,
                "chunks": chunks
            },
            f
        )


def load_vector_store():
    if not os.path.exists(VECTOR_PATH):
        return None, None

    with open(VECTOR_PATH, "rb") as f:
        data = pickle.load(f)

    return data["index"], data["chunks"]