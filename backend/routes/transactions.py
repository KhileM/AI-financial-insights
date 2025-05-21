from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.transaction import Transaction
from models.database import db
from services.fraud_detector import is_fraudulent

tx_bp = Blueprint('transactions', __name__)

@tx_bp.route("/submit-transaction", methods=["POST"])
def submit_transaction():
    data = request.get_json()
    user_id = data.get('user_id')  # <-- ensure this is included
    if user_id is None:
        return jsonify({"error": "user_id is required"}), 400


    try:
        amount = float(data["amount"])
        category = data.get("category", "uncategorized")
        description = data.get("description", "")
    except (KeyError, ValueError):
        return jsonify({"error": "Invalid input"}), 400

    flagged = is_fraudulent(data)

    tx = Transaction(
        user_id=user_id,
        amount=amount,
        category=category,
        description=description,
        is_fraud=flagged
    )

    db.session.add(tx)
    db.session.commit()

    return jsonify({
        "message": "Transaction submitted",
        "is_fraud": flagged
    }), 201
