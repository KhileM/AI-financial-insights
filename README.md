# AI-financial-insights

Here’s a **README.md** summarizing everything you've implemented so far in your **Mini GenAI App** using Flask and OpenAI, including AI-powered insights, database querying, and dynamic prompt handling.

---

```markdown
# Mini GenAI App – AI-Powered Insights with Flask & OpenAI

## Overview

This project is a Proof of Concept (PoC) Flask application that integrates OpenAI's Large Language Models (LLMs) to generate insights and summaries based on user prompts. It connects to a PostgreSQL database and supports both static and dynamic reports, served via traditional endpoints and AI-driven queries.

---

## 🚀 Features

### ✅ Core Functionality

- **Prompt-based AI querying** (`/llm/ask`)
  - Accepts natural language prompts
  - Routes to appropriate SQL queries based on intent
  - Returns structured results or summaries

- **Predefined Report Endpoints**
  - `/reports/gender-summary`: Users by gender
  - `/reports/income-by-location`: Income stats by lat/lon
  - `/reports/high-net-worth`: High-income, low-debt users
  - `/reports/young-high-earners`: Young users with high income
  - `/reports/avg-income-by-gender`: Avg income broken down by gender

- **Excel Export Support**
  - Automatically exports report results to Excel format

- **Modular Structure**
  - Organized routes, services, and utilities for scalability

---

## 🗂️ Project Structure

```

├── app.py                      # App factory and initialization
├── routes/
│   ├── insights.py            # AI-driven insight routes
│   ├── reports.py             # Traditional report routes
│   └── llm\_routes.py          # LLM prompt handling route
├── services/
│   ├── llm\_service.py         # OpenAI API integration
│   ├── query\_router.py        # Prompt intent routing logic
│   └── db\_utils.py            # DB connection and fetch logic
├── utils/
│   └── formatters.py          # Result formatting helper
├── models/
│   └── user\_profile.py        # SQLAlchemy models
├── config.py                  # App configuration
└── requirements.txt

````

---

## 🧪 Sample Prompts for Testing

Here are some test queries you can use via Postman or UI:

| Prompt | Functionality Triggered |
|--------|--------------------------|
| What is the average income for each gender? | `avg_income_by_gender` |
| How many male and female users do we have? | `gender_summary` |
| Where are the users with the highest income located? | `income_by_location` |
| Show me high net worth individuals. | `high_net_worth` |
| Who are the top young earners in our system? | `young_high_earners` |

---

## 🛠️ Setup & Run

### 1. Clone the Repo

```bash
git clone <repo-url>
cd mini-genai-app
````

### 2. Install Requirements

```bash
pip install -r requirements.txt
```

### 3. Environment Setup

Create a `.env` file and add your OpenAI API key:

```
OPENAI_API_KEY=your_openai_key_here
DATABASE_URL=your_postgres_connection_string
```

### 4. Run the Flask App

```bash
python app.py
```

---

## 🧠 Tech Stack

* **Flask** – Web framework
* **PostgreSQL** – Database
* **OpenAI API** – Language model for insights
* **psycopg2** – PostgreSQL connector
* **pandas + openpyxl** – Excel report export
* **SQLAlchemy** – ORM (optional, models imported)

---

## 📈 In Progress / Next Steps

* [ ] Add UI (streamlit or frontend form for prompts)
* [ ] Implement Mini-RAG PoC with vector DB
* [ ] Add hybrid search (BM25 + embeddings)
* [ ] Complete Prompt Lab & Hello LLM Tool (notebooks)
* [ ] Create architecture diagram and comparative report

---