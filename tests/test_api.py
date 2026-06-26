import pytest
from app import create_app

@pytest.fixture
def client():
    """
    Test fixture: Configures the Flask app instance for testing mode.
    """
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_health_check_endpoint(client):
    """
    GIVEN a running Flask application factory
    WHEN the root health check endpoint '/' is requested (GET)
    THEN verify the status code is 200 and returns correct health metadata.
    """
    response = client.get('/')
    assert response.status_code == 200
    json_data = response.get_json()
    assert json_data['status'] == 'healthy'
    assert 'version' in json_data

def test_integration_summary_valid_account(client):
    """
    GIVEN a valid account_id existing in the mock CRM data
    WHEN requested via the integration endpoint (GET)
    THEN verify a 200 response with accurately linked CRM and ERP properties.
    """
    response = client.get('/api/v1/integration/summary?account_id=101')
    assert response.status_code == 200
    json_data = response.get_json()
    assert json_data['success'] is True
    assert json_data['integrated_data']['account_id'] == '101'
    assert 'crm_profile' in json_data['integrated_data']
    assert 'erp_financials' in json_data['integrated_data']

def test_integration_summary_missing_parameter(client):
    """
    GIVEN an integration summary request missing an account_id
    WHEN processed by the API gateway
    THEN verify a 400 Bad Request client error is securely raised.
    """
    response = client.get('/api/v1/integration/summary')
    assert response.status_code == 400
    json_data = response.get_json()
    assert json_data['success'] is False
    assert "Missing required query parameter" in json_data['message']

def test_create_invoice_validation_error(client):
    """
    GIVEN a POST request with an invalid negative amount parameter
    WHEN pushing the record to the ERP invoice sync gateway
    THEN verify a 400 Validation Error is thrown to intercept malformed data.
    """
    malformed_invoice = {
        "invoice_id": "INV-TEST-ERR",
        "account_id": "101",
        "amount": -500.00, # Invalid negative numerical value
        "issued_date": "2026-06-02"
    }
    response = client.post('/api/v1/erp/invoices', json=malformed_invoice)
    assert response.status_code == 400
    json_data = response.get_json()
    assert json_data['success'] is False
    assert "must be a positive numerical value" in json_data['message']