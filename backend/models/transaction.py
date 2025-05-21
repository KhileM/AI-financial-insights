from datetime import datetime
from models.database import db

class Transaction(db.Model):
    __tablename__ = "transactions"

    id = db.Column(db.Integer, primary_key=True)  # CSV: id
    date = db.Column(db.DateTime, nullable=False)  # CSV: date
    client_id = db.Column(db.Integer, nullable=False)  # CSV: client_id
    card_id = db.Column(db.String(50), nullable=False)  # CSV: card_id
    amount = db.Column(db.Float, nullable=False)  # CSV: amount
    use_chip = db.Column(db.Boolean, nullable=False)  # CSV: use_chip
    merchant_id = db.Column(db.String(100), nullable=False)  # CSV: merchant_id
    merchant_city = db.Column(db.String(100))  # CSV: merchant_city
    merchant_state = db.Column(db.String(50))  # CSV: merchant_state
    zip = db.Column(db.String(20))  # CSV: zip
    mcc = db.Column(db.String(10))  # CSV: mcc
    errors = db.Column(db.String(255))  # CSV: errors


    # Optional additional fields for enrichment
    is_fraud = db.Column(db.Boolean, default=False)
    category = db.Column(db.String(120))  # You may derive this from MCC
    description = db.Column(db.String(255))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

