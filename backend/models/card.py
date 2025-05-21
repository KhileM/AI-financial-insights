from models.database import db

class Card(db.Model):
    __tablename__ = "cards"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)  # maps to client_id
    card_number = db.Column(db.String(25), unique=True, nullable=False)
    card_type = db.Column(db.String(20))
    card_brand = db.Column(db.String(20))
    expiry_date = db.Column(db.String(10))  # e.g., MM/YY or ISO
    cvv = db.Column(db.String(10))
    has_chip = db.Column(db.Boolean)
    num_cards_issued = db.Column(db.Integer)
    credit_limit = db.Column(db.Float)
    acct_open_date = db.Column(db.String(20))  # optional: could be converted to datetime
    year_pin_last_changed = db.Column(db.Integer)
    card_on_dark_web = db.Column(db.Boolean)