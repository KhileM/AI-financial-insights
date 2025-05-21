import json
import os

def format_report_summary(results, report_name):
    summary = f"Report: {report_name}\n\n"
    if not results:
        return summary + "No data found."

    # Example: show top 3 rows as text
    for row in results[:3]:
        summary += str(row) + "\n"

    summary += f"\nShowing top {min(3, len(results))} results out of {len(results)} total."

    return summary
