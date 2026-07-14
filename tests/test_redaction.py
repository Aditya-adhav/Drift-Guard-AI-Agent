import sys
import os

# Add src to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from detector import DriftDetector

def test_redaction():
    detector = DriftDetector(tf_dir=".")
    
    mock_data = {
        "db_name": "production_db",
        "db_password": "super_secret_password",
        "aws_access_key_id": "AKIA1234567890",
        "aws_secret_access_key": "secret_key_123",
        "api_token": "token_abc",
        "tags": {
            "Environment": "Production",
            "SecretValue": "nested_secret",
            "Owner": "DevOps"
        },
        "list_of_configs": [
            {"name": "config1", "auth_token": "xyz"},
            {"name": "config2", "public_value": "hello"}
        ],
        "empty_secret": "",
        "none_secret": None
    }
    
    redacted = detector._redact_sensitive_data(mock_data)
    
    print("Original Data:")
    import json
    print(json.dumps(mock_data, indent=2))
    
    print("\nRedacted Data:")
    print(json.dumps(redacted, indent=2))
    
    assert redacted["db_password"] == "***REDACTED***"
    assert redacted["aws_access_key_id"] == "***REDACTED***"
    assert redacted["aws_secret_access_key"] == "***REDACTED***"
    assert redacted["api_token"] == "***REDACTED***"
    assert redacted["tags"]["SecretValue"] == "***REDACTED***"
    assert redacted["list_of_configs"][0]["auth_token"] == "***REDACTED***"
    
    assert redacted["db_name"] == "production_db"
    assert redacted["tags"]["Environment"] == "Production"
    assert redacted["list_of_configs"][1]["public_value"] == "hello"
    
    # Should not redact empty strings or Nones
    assert redacted["empty_secret"] == ""
    assert redacted["none_secret"] == None
    
    print("\nAll tests passed successfully!")

if __name__ == "__main__":
    test_redaction()
