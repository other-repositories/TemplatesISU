import pytest
from  src.settings_manager import settings_manager
from unittest.mock import patch, mock_open
import json

@pytest.fixture
def test_manager():
    return settings_manager()

def test_convert(test_manager):
    test_data = {
        "inn": "123456789012",
        "organization_name": "Test Organization"
    }

    result = test_manager.convert(test_data)

    assert result.inn == "123456789012"
    assert result.organization_name == "Test Organization"

def test_open(test_manager):
    mock_data = {
        "inn": "123456789012",
        "organization_name": "Mock Organization"
    }
    
    with patch("builtins.open", mock_open(read_data=json.dumps(mock_data))):
        result = test_manager.open("settings.json")

    assert result == True
    assert test_manager.current_settings.inn == "123456789012"
    assert test_manager.current_settings.organization_name == "Mock Organization"

def test_open_invalid_file(test_manager):
    with patch("builtins.open", side_effect=FileNotFoundError):
        result = test_manager.open("invalid_file.json")

    assert result == False
    assert test_manager.current_settings.inn == "380080920202"  
    assert test_manager.current_settings.organization_name == "Рога и копыта (default)"

def test_open_file_relative(test_manager):
    absolute_file_path = "../tests_data/task_1.json"

    result = test_manager.open(absolute_file_path)

    assert result == True
    assert test_manager.current_settings.inn == "123456789012"
    assert test_manager.current_settings.organization_name == "test1"