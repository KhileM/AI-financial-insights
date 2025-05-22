# llm_service.py
import os
from openai import OpenAI
from rag.retriever import get_relevant_chunks
from rag.prompt_builder import build_prompt
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def query_llm(prompt: str) -> str:
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",  # or "gpt-4" if you have access
        messages=[
            {"role": "system", "content": "You are a helpful assistant that analyzes user financial data."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.2,
        max_tokens=300
    )
    return response.choices[0].message.content.strip()

# openai_client = OpenAI()

def answer_with_rag(user_query):
    context = get_relevant_chunks(user_query)
    prompt = build_prompt(user_query, context)

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )

    return response.choices[0].message.content.strip()
