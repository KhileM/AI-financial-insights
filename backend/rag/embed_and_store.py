# Prepares and stores data chunks
import os
import pandas as pd
import chromadb
import uuid
from openai import OpenAI
from dotenv import load_dotenv

# Load .env variables
load_dotenv()

# Initialize OpenAI client
openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))  # ✅ Fixed this line

# Initialize ChromaDB persistent client
chroma_client = chromadb.PersistentClient(path="./chroma_storage")

COLLECTION_NAME = "user_profile_chunks"

def chunk_csv_rows(filepath, chunk_size=10):
    df = pd.read_csv(filepath)
    chunks = []

    for i in range(0, len(df), chunk_size):
        chunk = df.iloc[i:i + chunk_size]
        text_chunk = chunk.to_string(index=False)
        chunks.append(text_chunk)

    return chunks

def embed_text(text):
    response = openai_client.embeddings.create(
        input=[text],
        model="text-embedding-3-small"
    )
    return response.data[0].embedding

def store_embeddings(chunks):
    # Create or get collection
    try:
        chroma_client.delete_collection(name=COLLECTION_NAME)
    except Exception:
        pass  # Ignore if collection doesn't exist

    collection = chroma_client.create_collection(name=COLLECTION_NAME)

    for i, chunk in enumerate(chunks):
        embedding = embed_text(chunk)
        collection.add(
            ids=[str(uuid.uuid4())],
            documents=[chunk],
            embeddings=[embedding],
            metadatas=[{"source": "users_data.csv"}]
        )

    print(f"✅ Stored {len(chunks)} chunks in ChromaDB.")

if __name__ == "__main__":
    chunks = chunk_csv_rows("data/users_data.csv", chunk_size=10)
    store_embeddings(chunks)
