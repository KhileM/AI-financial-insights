# Retrieves top-k chunks for a query
from chromadb import PersistentClient
from chromadb.config import Settings
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

# Initialize ChromaDB and OpenAI
client = PersistentClient(path="./chroma_storage")
openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Load collection
collection = client.get_collection("user_profile_chunks")

def get_relevant_chunks(query, k=3):
    query_embedding = openai_client.embeddings.create(
        input=[query],
        model="text-embedding-3-small"
    ).data[0].embedding

    results = collection.query(query_embeddings=[query_embedding], n_results=k)
    return results['documents'][0]
