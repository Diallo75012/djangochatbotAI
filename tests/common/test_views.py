import pytest
import os
from unittest.mock import patch, MagicMock
from django.contrib.auth.models import User
from django.urls import reverse
from django.test import Client
from django.utils.timezone import now
from common.models import LogAnalysisTask
from common.views import runLogAnalyzer

@pytest.mark.django_db
@patch("common.views.subprocess.run")  # Mock subprocess call
@patch("common.views.db_recorder")  # Mock database recorder function
def test_run_log_analyzer_success(mock_db_recorder, mock_subprocess, client):
    """
    Test runLogAnalyzer view when subprocess execution is successful.
    """
    # Setup user with admin permissions
    admin_user = User.objects.create_superuser(username="admin", password="adminpass")
    client.login(username="admin", password="adminpass")

    # Mock successful subprocess execution
    mock_subprocess.return_value = MagicMock(returncode=0, stdout="Success Output", stderr="")

    # Execute the view
    response = client.post(reverse("common:runloganalyzer"))

    # Assertions
    assert response.status_code == 200
    task = LogAnalysisTask.objects.latest("start_time")
    assert task.status == "Success"
    assert "Success Output" in task.output

    # Ensure db_recorder is called with expected values
    mock_db_recorder.assert_called_once()


@pytest.mark.django_db
@patch("common.views.subprocess.run")  # Mock subprocess call
@patch("common.views.db_recorder")  # Mock database recorder function
def test_run_log_analyzer_failure(mock_db_recorder, mock_subprocess, client):
    """
    Test runLogAnalyzer view when subprocess execution fails.
    """
    # Setup user with admin permissions
    admin_user = User.objects.create_superuser(username="admin", password="adminpass")
    client.login(username="admin", password="adminpass")

    # Mock failed subprocess execution
    mock_subprocess.return_value = MagicMock(returncode=1, stdout="", stderr="Error occurred")

    # Execute the view
    response = client.post(reverse("common:runloganalyzer"))

    # Assertions
    assert response.status_code == 200
    task = LogAnalysisTask.objects.latest("start_time")
    assert task.status == "Error"
    assert "Error occurred" in task.output

    # Ensure db_recorder is called
    mock_db_recorder.assert_called_once()


@pytest.mark.django_db
@patch("common.views.subprocess.run", side_effect=Exception("Unexpected failure"))  # Simulate unexpected error
@patch("common.views.db_recorder")  # Mock database recorder function
def test_run_log_analyzer_exception(mock_db_recorder, mock_subprocess, client):
    """
    Test runLogAnalyzer view when an unexpected exception occurs.
    """
    # Setup user with admin permissions
    admin_user = User.objects.create_superuser(username="admin", password="adminpass")
    client.login(username="admin", password="adminpass")

    # Execute the view
    response = client.post(reverse("common:runloganalyzer"))

    # Assertions
    assert response.status_code == 200
    task = LogAnalysisTask.objects.latest("start_time")
    assert task.status == "Error"
    assert "Unexpected failure" in task.output

    # Ensure db_recorder was not called due to failure
    mock_db_recorder.assert_not_called()
