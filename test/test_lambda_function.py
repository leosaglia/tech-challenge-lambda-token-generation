import json
import pytest
from unittest.mock import patch, MagicMock

import src.lambda_function as lambda_function

@patch("src.lambda_function.requests.get")
def test_generate_token_for_customer_not_found(mock_get):
    mock_resp = MagicMock(status_code=404)
    mock_get.return_value = mock_resp
    response = lambda_function.generate_token_for_customer("999999")
    assert response["statusCode"] == 404

def test_lambda_handler_customer():
    event = {
        "body": json.dumps({"user_type": "customer", "document_id": "123456"})
    }
    with patch("src.lambda_function.generate_token_for_customer") as mock_func:
        mock_func.return_value = {"statusCode": 200, "body": json.dumps({"token": "fake"})}
        resp = lambda_function.lambda_handler(event, None)
        assert resp["statusCode"] == 200
