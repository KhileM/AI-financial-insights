from models.database import db

class UserProfile(db.Model):
    __tablename__ = "user_profiles"

    id = db.Column(db.Integer, primary_key=True)
    current_age = db.Column(db.Integer)
    retirement_age = db.Column(db.Integer)
    birth_year = db.Column(db.Integer)
    birth_month = db.Column(db.Integer)
    gender = db.Column(db.String(10))
    address = db.Column(db.String(255))
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    per_capita_income = db.Column(db.Float)
    yearly_income = db.Column(db.Float)
    total_debt = db.Column(db.Float)
    credit_score = db.Column(db.Integer)
    num_credit_cards = db.Column(db.Integer)