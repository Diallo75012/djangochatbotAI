import pytest
from django.contrib.auth.models import User
from common.models import LogAnalysisTask
from django.core.exceptions import ValidationError


@pytest.mark.django_db
def test_log_analysis_task_creation():
    """Test creating a LogAnalysisTask instance with valid data."""
    user = User.objects.create_user(username="testuser", password="securepassword")

    task = LogAnalysisTask.objects.create(
        user=user,
        output="Log analysis completed.",
        status="Success",
    )

    # Assertions
    assert task.user == user
    assert task.output == "Log analysis completed."
    assert task.status == "Success"
    assert task.start_time is not None  # Should be auto-set
    assert task.end_time is not None  # Should update on save


@pytest.mark.django_db
def test_log_analysis_task_status_choices():
    """Test that only valid status choices are allowed."""
    user = User.objects.create_user(username="testuser", password="securepassword")

    valid_statuses = ["Running", "Success", "Error"]
    for status in valid_statuses:
        task = LogAnalysisTask.objects.create(user=user, status=status)
        assert task.status == status

    # Try invalid status (should raise a ValidationError)
    task_invalid = LogAnalysisTask(user=user, status="InvalidStatus")
    with pytest.raises(ValidationError):
        task_invalid.full_clean()  # Ensures Django validates before saving
