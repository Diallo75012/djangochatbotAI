import pytest
from agents.app_utils.formatters import string_to_dict, collection_normalize_name

def test_string_to_dict_valid():
    test_string = '{"key1": "value1", "key2": 123}'
    result = string_to_dict(test_string)
    assert result == {"key1": "value1", "key2": 123}

def test_string_to_dict_invalid():
    test_string = 'invalid json'
    with pytest.raises(ValueError, match="Error converting string to dictionary"):
        string_to_dict(test_string)

def test_string_to_dict_empty():
    test_string = '{}'
    result = string_to_dict(test_string)
    assert result == {}

def test_string_to_dict_with_upper_case_keys():
    test_string = '{"Key1": "value1", "Key2": 123}'
    result = string_to_dict(test_string)
    assert result == {"key1": "value1", "key2": 123}

def test_collection_normalize_name():
    test_name = "  Test Collection Name  "
    result = collection_normalize_name(test_name)
    assert result == "test-collection-name"

def test_collection_normalize_name_already_normalized():
    test_name = "test-collection-name"
    result = collection_normalize_name(test_name)
    assert result == "test-collection-name"

def test_collection_normalize_name_with_uppercase():
    test_name = "Test Collection Name"
    result = collection_normalize_name(test_name)
    assert result == "test-collection-name"
