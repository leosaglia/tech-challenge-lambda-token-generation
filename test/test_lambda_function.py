import json
import pytest
from unittest.mock import patch, MagicMock

import src.lambda_function as lambda_function

def test_validate_event_body_valid_customer():
    event_body = {"user_type": "customer"}
    assert lambda_function.validate_event_body(event_body) is True

def test_validate_event_body_valid_employee():
    event_body = {"user_type": "employee"}
    assert lambda_function.validate_event_body(event_body) is True

def test_validate_event_body_no_user_type():
    event_body = {}
    assert lambda_function.validate_event_body(event_body) is False

def test_validate_event_body_invalid_user_type():
    event_body = {"user_type": "invalid"}
    assert lambda_function.validate_event_body(event_body) is False

@patch("src.lambda_function.requests.get")
def test_generate_token_for_customer_not_found(mock_get):
    mock_resp = MagicMock(status_code=404)
    mock_get.return_value = mock_resp
    response = lambda_function.generate_token_for_customer("999999")
    assert response["statusCode"] == 404

def test_generate_token_for_employee_no_id():
    response = lambda_function.generate_token_for_employee(None)
    assert response["statusCode"] == 400

def test_generate_token_for_employee_invalid_id():
    response = lambda_function.generate_token_for_employee("999")
    assert response["statusCode"] == 404

def test_lambda_handler_customer():
    event = {
        "body": json.dumps({"user_type": "customer", "document_id": "123456"})
    }
    with patch("src.lambda_function.generate_token_for_customer") as mock_func:
        mock_func.return_value = {"statusCode": 200, "body": json.dumps({"token": "fake"})}
        resp = lambda_function.lambda_handler(event, None)
        assert resp["statusCode"] == 200

def test_lambda_handler_employee():
    event = {
        "body": json.dumps({"user_type": "employee", "employee_id": "123"})
    }
    with patch("src.lambda_function.generate_token_for_employee") as mock_func:
        mock_func.return_value = {"statusCode": 200, "body": json.dumps({"token": "fake"})}
        resp = lambda_function.lambda_handler(event, None)
        assert resp["statusCode"] == 200

def test_lambda_handler_invalid_user_type():
    event = {
        "body": json.dumps({"user_type": "invalid"})
    }
    resp = lambda_function.lambda_handler(event, None)
    assert resp["statusCode"] == 400