# NEW: Handles intent parsing and routes to DB or LLM

from services.db_queries import get_avg_income_by_gender, get_gender_summary, get_income_by_location, get_high_net_worth, get_young_high_earners
from services.llm_service import query_llm
from services.response_formatter import format_report_summary

def handle_prompt(prompt: str):
    prompt = prompt.lower()

    if "gender summary" in prompt or "gender breakdown" in prompt:
        # Reuse your existing function
        results = get_gender_summary()  # or get_avg_income_by_gender() if that's what you want
        return format_report_summary(results, "Gender Summary")
    
    elif "average income by gender" in prompt:
        results = get_avg_income_by_gender()
        return format_report_summary(results, "Average Income by Gender")
    
    elif "income by location" in prompt or "income by area" in prompt:
        results = get_income_by_location()
        return format_report_summary(results, "Income by Location")
    
    elif "high net worth" in prompt or "wealthy users" in prompt:
        results = get_high_net_worth()
        return format_report_summary(results, "High Net Worth Users")
    
    elif "young high earners" in prompt or "young rich" in prompt:
        results = get_young_high_earners()
        return format_report_summary(results, "Young High Earners")

    else:
        
        # Default fallback to raw LLM query
        return query_llm(prompt)

