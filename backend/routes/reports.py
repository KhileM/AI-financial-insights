from flask import Blueprint, send_file
from db import fetch_all
import pandas as pd
from io import BytesIO
from datetime import datetime

reports_bp = Blueprint('reports', __name__)

def export_to_excel(data, sheet_name: str, filename_prefix: str):
    df = pd.DataFrame(data)
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name=sheet_name, index=False)
    output.seek(0)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{filename_prefix}_{timestamp}.xlsx"
    return send_file(
        output,
        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        as_attachment=True,
        download_name=filename
    )


@reports_bp.route('/reports/gender-summary', methods=['GET'])
def gender_summary():
    query = """
        SELECT gender, COUNT(*) AS user_count
        FROM user_profiles
        GROUP BY gender;
    """
    results = fetch_all(query)
    return export_to_excel(results, sheet_name="Gender Summary", filename_prefix="gender_summary")


@reports_bp.route('/reports/income-by-location', methods=['GET'])
def income_by_location():
    query = """
        SELECT
            latitude,
            longitude,
            ROUND(AVG(per_capita_income)::numeric, 2) AS avg_per_capita_income,
            ROUND(AVG(yearly_income)::numeric, 2) AS avg_yearly_income,
            COUNT(*) AS users_in_location
        FROM user_profiles
        GROUP BY latitude, longitude
        ORDER BY users_in_location DESC;
    """
    results = fetch_all(query)
    return export_to_excel(results, sheet_name="Income by Location", filename_prefix="income_by_location")


@reports_bp.route('/reports/high-net-worth', methods=['GET'])
def high_net_worth():
    query = """
        SELECT id, current_age, yearly_income, total_debt, credit_score
        FROM user_profiles
        WHERE yearly_income > 100000
        AND total_debt < 20000
        ORDER BY yearly_income DESC;
    """
    results = fetch_all(query)
    return export_to_excel(results, sheet_name="High Net Worth", filename_prefix="high_net_worth")


@reports_bp.route('/reports/young-high-earners', methods=['GET'])
def young_high_earners():
    query = """
        SELECT id, current_age, yearly_income, total_debt, credit_score
        FROM user_profiles
        WHERE current_age < 30
        AND yearly_income > 75000
        ORDER BY yearly_income DESC;
    """
    results = fetch_all(query)
    return export_to_excel(results, sheet_name="Young High Earners", filename_prefix="young_high_earners")
