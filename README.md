# Corporate ERP & CRM Application Integration REST API Gateway

An enterprise-grade RESTful API Microservice built using **Python and Flask** utilizing the **Application Factory and Blueprint structural patterns**. This gateway serves as an agile integration layer that safely bridges isolated corporate operational ecosystems, unifying data streams between a **Customer Relationship Management (CRM)** platform and an **Enterprise Resource Planning (ERP)** financial system.

---

## Architectural Overview & Design Patterns
- **Application Factory Pattern:** Encapsulates initialization logic within `app/__init__.py` to allow clean app state isolation, scalability, and simplified test client integration.
- **Flask Blueprints:** Deployed to modularize and decouple routes, keeping functional code maintainable.
- **Relational Integrity Assurance:** Implements manual data constraints across separate mock datasets, enforcing relationship parameters based on a shared tracking ID (`account_id`).

---

##  Repository Directory Structure

```text
M608-Business-REST-API/
│
├── app/
│   ├── __init__.py        # Application Factory and Blueprint 
│   ├── routes.py          # GET Summary & POST Validation 
│   └── models.py          # Mock CRM & ERP relational database 
│
├── tests/                 # Automated Unit Testing Engine
│   └── test_api.py        # Pytest assertion suites
│
├── run.py                 # Core Microservice entry execution 
├── README.md              # Project documentation 
├── requirements.txt       # Project package dependencies
└── .gitignore             # Git system tracking exclusions
```
## Local Installation & Deployment Guide

```text
1. Clone the Repository & Enter Folder
Bash
git clone <YOUR-GITHUB-REPOSITORY-URL>
cd M608-Business-REST-API
2. Configure Virtual Environment (Isolate Dependencies)
Bash
# Create Environment
python3 -m venv venv

# Activate Environment (Linux/WSL)
source venv/bin/activate

# Activate Environment (Windows Command Prompt)
venv\Scripts\activate
3. Install Required Dependencies
Bash
pip install -r requirements.txt
4. Boot Up the REST API Gateway
Bash
python run.py
The server will initialize locally on development environment port 5000: http://127.0.0.1:5000/
```

## Automated Testing
```text
Run the comprehensive test suite to confirm endpoint validity, input constraints, and routing status codes:

Bash
python -m pytest tests/test_api.py
```