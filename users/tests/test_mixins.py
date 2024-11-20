import pytest
import json
from django.core.exceptions import ValidationError
from users.mixins import JSONFieldValidationMixin


class MockForm(JSONFieldValidationMixin):
  # mock form class to test mixin
  def __init__(self, question_answer_data):
    self.cleaned_data = {
      "question_answer_data": question_answer_data
    }

@pytest.mark.parametrize("json_data",[
  # we need to have both valid inputs so we test both
  # json imput
  '{"question":"answer"}',
  '{"key1":"value1", "key2":"value2"}',
  # python dict imput
  {"question":"answer"},
  {"key1":"value1", "key2":"value2"},
])
def test_json_field_validation_valid(json_data):
  form = MockForm(question_answer_data=json_data)
  try:
    expected_data = json_data if isinstance(json_data, dict) else json.loads(json_data)
    # clean_question_answer_data() method comes from the mixin class `JSONFieldValidationMixin`
    # in Django the `clean_<fieldname>()` method is used to add custom validation logic to individual form field
    assert form.clean_question_answer_data() == expected_data
  except ValidationError:
    pytest.fail(
      "Valid JSON data raised ValidationError unexpectedly."
    )


@pytest.mark.parametrize("invalid_data",[
   # we are missing hte closing `}` on purpose
  '{"question":"answer"',
  '{key:value}', # invalid JSON
])
def test_json_field_validation_invalid(invalid_data):
  form = MockForm(
    question_answer_data=invalid_data
  )
  with pytest.raises(ValidationError):
    form.clean_question_answer_data()

