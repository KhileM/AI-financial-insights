import csv
import json
from datetime import datetime
from app import create_app
from models.database import db
from models.user import User
from models.transaction import Transaction
from models.card import Card
from models.mcc_code import MCCCode
from models.user_profile import UserProfile

app = create_app()

def parse_currency(value):
    if not value:
        return 0.0
    return float(value.replace("$", "").replace(",", "").replace('"', "").strip())

def parse_int(value):
    try:
        # Remove anything that isn't a digit
        cleaned = ''.join(c for c in value if c.isdigit())
        return int(cleaned)
    except Exception as e:
        print(f"⚠️ parse_int error on value '{value}': {e}")
        return 0

def parse_bool(value):
    """Convert 'true'/'false' strings to boolean."""
    return str(value).strip().lower() in ("true", "1", "yes")

def load_user_profiles():
    with open("users_data.csv", newline='') as f:
        reader = csv.DictReader(f, quotechar='"')
        for row in reader:
            if UserProfile.query.filter_by(id=parse_int(row["id"])).first():
                continue  # Skip duplicates
            try:
                profile = UserProfile(
                    id=parse_int(row["id"]),
                    current_age=parse_int(row["current_age"]),
                    retirement_age=parse_int(row["retirement_age"]),
                    birth_year=parse_int(row["birth_year"]),
                    birth_month=parse_int(row["birth_month"]),
                    gender=row["gender"],
                    address=row["address"],
                    latitude=float(row["latitude"]),
                    longitude=float(row["longitude"]),
                    per_capita_income=parse_currency(row["per_capita_income"]),
                    yearly_income=parse_currency(row["yearly_income"]),
                    total_debt=parse_currency(row["total_debt"]),
                    credit_score=parse_int(row["credit_score"]),
                    num_credit_cards=parse_int(row["num_credit_cards"])
                )
                db.session.add(profile)
            except Exception as e:
                print(f"⚠️ Skipping user profile row due to error: {e}")
        db.session.commit()
    print("✅ User profiles loaded")


def load_transactions():
    with open("transactions_data.csv", newline='') as f:
        reader = csv.DictReader(f)
        print(f"CSV Headers: {reader.fieldnames}")
        
        for i, row in enumerate(reader, start=1):
            if i > 2000:
                break  # Stop after 2000 rows

            try:
                timestamp = datetime.strptime(row["date"], "%Y-%m-%d %H:%M:%S")

                tx = Transaction(
                    id=int(row["id"].replace(",", "")),
                    user_id=int(row["client_id"].replace(",", "")),
                    amount=float(row["amount"].replace("$", "").replace(",", "").strip()),
                    category="unknown",
                    description="",
                    timestamp=timestamp,
                    is_fraud=False
                )
                db.session.add(tx)
            except Exception as e:
                print(f"⚠️ Skipping transaction row #{i} due to error: {e}")
        
        db.session.commit()
    print("✅ First 2000 transactions loaded")

def load_cards():
    with open("cards_data.csv", newline='') as f:
        reader = csv.DictReader(f)
        print(f"CSV Headers: {reader.fieldnames}")
        
        for i, row in enumerate(reader, start=1):
            if i > 2000:
                break  # Only load first 2000 rows for the PoC

            if Card.query.filter_by(card_number=row["card_number"]).first():
                continue  # Skip duplicates by card number

            try:
                card = Card(
                    id=parse_int(row["id"]),
                    user_id=parse_int(row["client_id"]),
                    card_number=row["card_number"],
                    card_type=row.get("card_type", ""),
                    card_brand=row.get("card_brand", ""),
                    expiry_date=row.get("expires", ""),
                    has_chip=parse_bool(row.get("has_chip", False)),
                    num_cards_issued=parse_int(row.get("num_cards_issued", "0")),
                    credit_limit=parse_currency(row.get("credit_limit", "0")),
                    acct_open_date=row.get("acct_open_date", ""),
                    year_pin_last_changed=parse_int(row.get("year_pin_last_changed", "0")),
                    card_on_dark_web=parse_bool(row.get("card_on_dark_web", False))
                )
                db.session.add(card)
            except Exception as e:
                print(f"⚠️ Skipping card row #{i} due to error: {e}")
        
        db.session.commit()
    print("✅ First 2000 cards loaded")

def load_mcc_codes():
    with open("mcc_codes.json") as f:
        mcc_data = json.load(f)  # assumes a list of {"code": ..., "description": ...}
        for i, row in enumerate(mcc_data, start=1):
            try:
                if not MCCCode.query.filter_by(code=row["code"]).first():
                    mcc = MCCCode(
                        code=str(row["code"]),
                        description=row["description"]
                    ) 
                    db.session.add(mcc)
            except Exception as e:
                print(f"⚠️ Skipping MCC row #{i} due to error: {e}")
        db.session.commit()
    print("✅ MCC Codes loaded")

with app.app_context():
    # load_users()
    load_user_profiles()
    load_transactions()
    load_cards()
    load_mcc_codes()