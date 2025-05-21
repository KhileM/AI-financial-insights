from models.user_profile import UserProfile
from models.database import db
from sqlalchemy import func, text

def get_avg_income_by_gender():
    result = (
        db.session.query(
            UserProfile.gender,
            func.avg(UserProfile.yearly_income).label("avg_income")
        )
        .group_by(UserProfile.gender)
        .all()
    )
    return {gender: float(avg_income) for gender, avg_income in result}

def get_gender_summary():
    query = """
        SELECT gender, COUNT(*) AS user_count
        FROM user_profiles
        GROUP BY gender;
    """
    return db.session.execute(text(query)).fetchall()

def get_income_by_location():
    query = """
        SELECT latitude, longitude,
               ROUND(AVG(per_capita_income)::numeric, 2) AS avg_per_capita_income,
               ROUND(AVG(yearly_income)::numeric, 2) AS avg_yearly_income,
               COUNT(*) AS users_in_location
        FROM user_profiles
        GROUP BY latitude, longitude
        ORDER BY users_in_location DESC;
    """
    return db.session.execute(text(query)).fetchall()

def get_high_net_worth():
    query = """
        SELECT id, current_age, yearly_income, total_debt, credit_score
        FROM user_profiles
        WHERE yearly_income > 100000
          AND total_debt < 20000
        ORDER BY yearly_income DESC;
    """
    return db.session.execute(text(query)).fetchall()

def get_young_high_earners():
    query = """
        SELECT id, current_age, yearly_income, total_debt, credit_score
        FROM user_profiles
        WHERE current_age < 30
          AND yearly_income > 75000
        ORDER BY yearly_income DESC;
    """
    return db.session.execute(text(query)).fetchall()
