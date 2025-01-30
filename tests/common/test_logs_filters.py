import pytest
import logging
from unittest.mock import patch, MagicMock
from common.logs_filters import UserIDFilter


@pytest.fixture
def log_record():
    """Fixture to create a dummy log record."""
    return logging.LogRecord(name="test", level=logging.INFO, pathname="", lineno=0, msg="Test log", args=(), exc_info=None)


@pytest.mark.parametrize("user_authenticated, user_id, expected_user_id", [
    (True, "42", "42"),  # Authenticated user with string ID
    (False, None, "anonymous"),  # Unauthenticated user → always "anonymous"
])
@patch("common.logs_filters.get_current_user")
def test_user_id_filter(mock_get_current_user, log_record, user_authenticated, user_id, expected_user_id):
    """
    Test UserIDFilter to ensure correct user ID assignment in logs.
    """
    # Mock user behavior
    mock_user = MagicMock()
    mock_user.is_authenticated = user_authenticated
    mock_user.id = user_id  # Mock the ID as a string to match expected behavior

    # Apply mock to simulate current user retrieval
    mock_get_current_user.return_value = mock_user if user_authenticated else None

    # Apply filter
    user_filter = UserIDFilter()
    user_filter.filter(log_record)

    # Assertions
    assert log_record.user_id == expected_user_id  # Ensures expected user ID format
