import pytest
from unittest.mock import MagicMock
from django.http import HttpRequest, HttpResponse
from common.middleware_logs_custom import CurrentUserMiddleware, get_current_user


@pytest.fixture
def mock_request():
    """Fixture to create a mock Django request object."""
    request = MagicMock(spec=HttpRequest)
    request.user = MagicMock(username="testuser", id="123")
    return request


@pytest.fixture
def mock_response():
    """Fixture to create a mock Django response object."""
    response = MagicMock(spec=HttpResponse)
    return response


def test_current_user_middleware(mock_request, mock_response):
    """
    Test that `CurrentUserMiddleware` correctly sets and clears the current user.
    """

    def mock_get_response(request):
        """Mock get_response function that returns a response."""
        assert get_current_user() == request.user  # Ensure the user is set inside middleware
        return mock_response

    # Initialize middleware
    middleware = CurrentUserMiddleware(mock_get_response)

    # Process request
    response = middleware(mock_request)

    # Assert that middleware correctly sets the user
    assert get_current_user() is None  # Should be cleared after request handling
    assert response == mock_response  # Ensure response is returned correctly


def test_get_current_user_without_middleware():
    """
    Test `get_current_user` without middleware execution (should return None).
    """
    assert get_current_user() is None

