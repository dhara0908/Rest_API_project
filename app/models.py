"""
Data Model Layer
Simulates local database collections for integrated CRM and ERP environments.
"""

# Mock CRM Database Collection
CRM_ACCOUNTS = {
    "101": {"company_name": "Global Logistics Corp", "industry": "Transportation", "tier": "Enterprise", "manager": "Sarah Jenkins"},
    "102": {"company_name": "Apex Retail Solutions", "industry": "E-commerce", "tier": "Mid-Market", "manager": "Michael Chang"},
    "103": {"company_name": "BioHealth Systems", "industry": "Healthcare", "tier": "Enterprise", "manager": "Sarah Jenkins"}
}

# Mock ERP Database Collection
ERP_INVOICES = [
    {"invoice_id": "INV-2026-001", "account_id": "101", "amount": 12500.00, "status": "Paid", "issued_date": "2026-05-15"},
    {"invoice_id": "INV-2026-002", "account_id": "101", "amount": 8400.00, "status": "Overdue", "issued_date": "2026-05-20"},
    {"invoice_id": "INV-2026-003", "account_id": "102", "amount": 3100.00, "status": "Paid", "issued_date": "2026-05-22"},
    {"invoice_id": "INV-2026-004", "account_id": "103", "amount": 22000.00, "status": "Draft", "issued_date": "2026-06-01"}
]