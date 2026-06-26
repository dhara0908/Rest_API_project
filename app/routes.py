from flask import Blueprint, jsonify, request
# Import the data structures from our model layer
from app.models import CRM_ACCOUNTS, ERP_INVOICES

bp = Blueprint('api', __name__)

@bp.route('/', methods=['GET'])
def health_check():
    """
    Root endpoint serving as an API status check for connected business tools.
    """
    return jsonify({
        "status": "healthy",
        "service": "Business Application Integration Gateway",
        "version": "1.0.0"
    }), 200

@bp.route('/api/v1/integration/summary', methods=['GET'])
def get_integrated_summary():
    """
    Integration Endpoint: Joins CRM Account profiles with ERP Invoice history
    based on a provided account_id query parameter.
    """
    # Extract the 'account_id' argument from the URL query string
    account_id = request.args.get('account_id')
    
    if not account_id:
        return jsonify({
            "success": False,
            "error": "Bad Request",
            "message": "Missing required query parameter: 'account_id'"
        }), 400
        
    # Lookup the account details within the CRM dataset
    crm_data = CRM_ACCOUNTS.get(str(account_id))
    
    if not crm_data:
        return jsonify({
            "success": False,
            "error": "Not Found",
            "message": f"Account with ID '{account_id}' does not exist in the CRM system."
        }), 404

    # Filter and extract related billing records out of the ERP dataset
    matching_invoices = [inv for inv in ERP_INVOICES if inv["account_id"] == str(account_id)]
    
    # Compute aggregate KPIs dynamically for stakeholder visibility
    total_billing = sum(inv["amount"] for inv in matching_invoices)
    overdue_invoices = any(inv["status"] == "Overdue" for inv in matching_invoices)

    # Build the unified enterprise data payload
    integrated_payload = {
        "account_id": account_id,
        "crm_profile": crm_data,
        "erp_financials": {
            "total_invoiced_amount": total_billing,
            "has_overdue_balances": overdue_invoices,
            "invoice_records": matching_invoices
        }
    }

    # CRITICAL RETURN: Ensures Flask always receives a valid response payload
    return jsonify({
        "success": True,
        "integrated_data": integrated_payload
    }), 200

@bp.route('/api/v1/erp/invoices', methods=['POST'])
def create_erp_invoice():
    """
    ERP Integration Endpoint: Validates and writes a new invoice record
    into the ERP system, ensuring relational integrity with the CRM.
    """
    data = request.get_json()
    
    if not data:
        return jsonify({
            "success": False,
            "error": "Bad Request",
            "message": "Missing request body or content-type is not application/json"
        }), 400

    invoice_id = data.get('invoice_id')
    account_id = data.get('account_id')
    amount = data.get('amount')
    status = data.get('status', 'Draft') 
    issued_date = data.get('issued_date')

    # 1. Validation Check: Verify all mandatory parameters are present
    if not all([invoice_id, account_id, amount, issued_date]):
        return jsonify({
            "success": False,
            "error": "Unprocessable Entity",
            "message": "Missing required fields. Required: invoice_id, account_id, amount, issued_date"
        }), 422

    # 2. Security/Data Integrity Check: Ensure account_id exists in CRM database
    if str(account_id) not in CRM_ACCOUNTS:
        return jsonify({
            "success": False,
            "error": "Conflict",
            "message": f"Foreign Key Violation: Account ID '{account_id}' does not exist in CRM system."
        }), 409

    # 3. Validation Check: Ensure amount is a valid positive number
    try:
        amount = float(amount)
        if amount <= 0:
            raise ValueError
    except (ValueError, TypeError):
        return jsonify({
            "success": False,
            "error": "Validation Error",
            "message": "Field 'amount' must be a positive numerical value greater than 0."
        }), 400

    # Construct the clean record object
    new_invoice = {
        "invoice_id": str(invoice_id),
        "account_id": str(account_id),
        "amount": amount,
        "status": str(status),
        "issued_date": str(issued_date)
    }

    # Append the clean record directly into our in-memory ERP database
    ERP_INVOICES.append(new_invoice)

    return jsonify({
        "success": True,
        "message": "Invoice successfully synchronized and recorded in ERP system.",
        "created_record": new_invoice
    }), 201