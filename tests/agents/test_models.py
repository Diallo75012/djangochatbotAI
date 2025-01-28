import pytest
from agents.models import LogAnalyzer
from django.db import models

def test_log_analyzer_model_fields():
    """
    Test that the LogAnalyzer model has the correct fields and field types.
    """
    log_analyzer = LogAnalyzer()
    assert hasattr(log_analyzer, 'chunk')
    assert isinstance(log_analyzer._meta.get_field('chunk'), models.CharField)
    assert hasattr(log_analyzer, 'log_level')
    assert isinstance(log_analyzer._meta.get_field('log_level'), models.CharField)
    # assert hasattr(log_analyzer, 'advice') # removed advice field
    # assert isinstance(log_analyzer._meta.get_field('advice'), models.CharField)

def test_log_analyzer_model_create():
    """
    Test that a LogAnalyzer object can be created and its fields can be set.
    """
    log_analyzer = LogAnalyzer.objects.create(
        chunk="test chunk",
        log_level="ERROR",
        # advice="test advice" # removed advice field
    )
    assert log_analyzer.chunk == "test chunk"
    assert log_analyzer.log_level == "ERROR"
    # assert log_analyzer.advice == "test advice" # removed advice field
