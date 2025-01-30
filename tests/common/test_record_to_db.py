import pytest
from unittest.mock import patch, MagicMock
from common.record_to_db import db_recorder

@pytest.mark.parametrize("mock_execute_success, mock_connect_success, expected", [
    (True, True, {"success": "data recorded"}),  # Successful DB insert
    (False, True, {"error": "An exception occured when recorded data to database: cannot access local variable 'e' where it is not associated with a value"}),  # Query execution failure
    (True, False, {"error": "An exception occured when recorded data to database: Mock Connection Error"}),  # Connection failure
])
@patch("psycopg.connect")  # Mock PostgreSQL connection
def test_db_recorder(mock_connect, mock_execute_success, mock_connect_success, expected):
    """
    Unit test for db_recorder function.

    - Tests both successful and failed database inserts.
    - Mocks PostgreSQL connection and cursor to prevent actual DB writes.
    """

    # Mock connection
    mock_conn = MagicMock()
    mock_cursor = MagicMock()

    if mock_connect_success:
        # Simulate connection success
        mock_connect.return_value.__enter__.return_value = mock_conn
    else:
        # Simulate connection failure
        mock_connect.side_effect = Exception("Mock Connection Error")

    if mock_execute_success:
        mock_cursor.execute.return_value = None  # Success case
    else:
        mock_cursor.execute.side_effect = Exception("Mock Query Execution Error")  # Simulated DB failure

    # Set cursor behavior
    mock_conn.cursor.return_value.__enter__.return_value = mock_cursor

    # Run function
    query = "INSERT INTO test_table (col1, col2) VALUES (%s, %s)"
    result = db_recorder(query, "val1", "val2")

    # Assertions: Ensure output matches the expected dictionary
    assert result == expected
