from flask import Blueprint, request, jsonify
from services.llm_service import query_llm, answer_with_rag
from services.query_router import handle_prompt


llm_bp = Blueprint("llm", __name__, url_prefix="/llm")

@llm_bp.route("/ask", methods=["POST"])
def ask_llm():
    data = request.get_json()
    prompt = data.get("prompt")

    if not prompt:
        return jsonify({"error": "Prompt is required."}), 400

    try:
        response = handle_prompt(prompt)
        return jsonify({"response": response})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
rag_bp = Blueprint("rag", __name__, url_prefix="/rag")

@rag_bp.route("/query", methods=["POST"])
def rag_ask():
    data = request.get_json()
    query = data.get("query")

    if not query:
        return jsonify({"error": "Query is required"}), 400

    try:
        answer = answer_with_rag(query)
        return jsonify({"answer": answer})
    except Exception as e:
        return jsonify({"error": str(e)}), 500