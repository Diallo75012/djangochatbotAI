import pytest
import json
from django import forms
from django.core.exceptions import ValidationError
from users.mixins import JSONFieldValidationMixin

class MockForm(forms.Form, JSONFieldValidationMixin):
  question_answer_data = forms.CharField()

  def __init__(self, *args, **kwargs):
    # Properly initialize the form by passing args and kwargs to the base class
    super().__init__(*args, **kwargs)

@pytest.mark.parametrize("json_data", [
  '{"question":"answer"}',
  '{"key1":"value1", "key2":"value2"}',
  {"question": "answer"},
  {"key1": "value1", "key2": "value2"},
])
def test_json_field_validation_valid(json_data):
  # Properly initialize MockForm using the data keyword argument
  form_data = {'question_answer_data': json_data if isinstance(json_data, str) else json.dumps(json_data)}
  form = MockForm(data=form_data)
  try:
    expected_data = json_data if isinstance(json_data, dict) else json.loads(json_data)
    assert form.is_valid(), f"Form errors: {form.errors}"
    # clean_question_answer_data() method comes from the mixin class `JSONFieldValidationMixin`
    # in Django the `clean_<fieldname>()` method is used to add custom validation logic to individual form field
    assert form.clean_question_answer_data() == expected_data
  except ValidationError:
    pytest.fail("Valid JSON data raised ValidationError unexpectedly.")

@pytest.mark.parametrize("invalid_data", [
  '{"question":"answer"',  # Missing closing `}`
  '{key:value}',           # Invalid JSON format
])
def test_json_field_validation_invalid(invalid_data):
  form_data = {'question_answer_data': invalid_data}
  form = MockForm(data=form_data)
  # Ensure form is not valid and raises validation error on calling clean_question_answer_data
  assert not form.is_valid(), "Invalid form data passed validation unexpectedly"
  with pytest.raises(ValidationError):
    form.clean_question_answer_data()

@pytest.mark.parametrize("json_data", [
  {},  # Python dict input with empty data
])
@pytest.mark.django_db
def test_json_field_validation_empty_dict(json_data):
  """
  Ensure the JSON validation mixin works correctly with an empty dictionary.
  """
  form_data = {'question_answer_data': json.dumps(json_data)}
  form = MockForm(data=form_data)
  assert form.is_valid(), f"Form errors: {form.errors}"
  assert form.clean_question_answer_data() == json_data
