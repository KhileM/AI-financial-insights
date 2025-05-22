# Constructs prompt, calls OpenAI
from flask import Flask, request, jsonify
from retriever import get_relevant_chunks
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
app = Flask(__name__)
openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def construct_prompt(context_chunks: list, user_query: str) -> str:
    context = "\n\n".join(context_chunks)
    system_instructions = (
        "You are a financial assistant. Use the following user profile data "
        "to answer questions accurately. Be concise and only refer to the data provided.\n\n"
    )
    return system_instructions + f"Context:\n{context}\n\nQuestion: {user_query}"

def ask_llm(prompt: str):
    response = openai_client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a financial assistant."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3
    )
    return response.choices[0].message.content

@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json()
    user_query = data.get("query")

    if not user_query:
        return jsonify({"error": "Missing 'query' in request body"}), 400

    try:
        relevant_chunks = get_relevant_chunks(user_query, k=5)
        full_prompt = construct_prompt(relevant_chunks, user_query)
        answer = ask_llm(full_prompt)
        return jsonify({"answer": answer})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
    # user_query = input("Ask a question about the user data: ")
    # relevant_chunks = get_relevant_chunks(user_query, k=5)
    # full_prompt = construct_prompt(relevant_chunks, user_query)
    # answer = ask_llm(full_prompt)
    # print("\n LLM Response:\n", answer)
