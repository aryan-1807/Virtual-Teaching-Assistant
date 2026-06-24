from langchain_text_splitters import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

# Load local light-weight embedding transformer
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

def create_chunks(text):
    """
    Splits input text strings into targeted semantic data blocks.
    Optimized for short assignment list structures.
    """
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=400,  # Smaller blocks stop question blending noise
        chunk_overlap=50
    )
    return splitter.split_text(text)

def create_vector_store(text):
    chunks = create_chunks(text)
    embeddings = embedding_model.encode(chunks)
    dimension = embeddings.shape[1]

    index = faiss.IndexFlatL2(dimension)
    index.add(np.array(embeddings).astype("float32"))

    return index, chunks

def search_document(query, index, chunks, k=4):  # Increased retrieval context pull
    query_embedding = embedding_model.encode([query])
    distances, indices = index.search(np.array(query_embedding).astype("float32"), k)

    retrieved_chunks = []
    for idx in indices[0]:
        if idx < len(chunks):
            retrieved_chunks.append(chunks[idx])

    return "\n\n".join(retrieved_chunks)