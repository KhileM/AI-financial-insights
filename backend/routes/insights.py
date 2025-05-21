from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.transaction import Transaction
from sqlalchemy import func, desc
from models.database import db

insights_bp = Blueprint("insights", __name__)

@insights_bp.route("/get-insights", methods=["GET"])
def get_insights():
    user_id = request.args.get('user_id', type=int)
    if user_id is None:
        return jsonify({"error": "user_id is required"}), 400

    # Total spend
    total_spend = db.session.query(func.sum(Transaction.amount))\
        .filter_by(user_id=user_id).scalar() or 0

    # Average transaction
    avg_spend = db.session.query(func.avg(Transaction.amount))\
        .filter_by(user_id=user_id).scalar() or 0

    # Top 3 categories
    top_categories = db.session.query(
        Transaction.category,
        func.sum(Transaction.amount).label("total")
    ).filter_by(user_id=user_id)\
     .group_by(Transaction.category)\
     .order_by(desc("total"))\
     .limit(3)\
     .all()

    categories_list = [{"category": cat, "total": total} for cat, total in top_categories]

    # Simple insight
    insight = None
    if total_spend > 10000:
        insight = "You’ve spent more than $10,000 in total — consider reviewing your monthly budget."

    return jsonify({
        "total_spend": round(total_spend, 2),
        "average_transaction": round(avg_spend, 2),
        "top_categories": categories_list,
        "insight": insight
    })
