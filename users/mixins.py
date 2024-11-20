import json
from django.core.exceptions import ValidationError


class JSONFieldValidationMixin:
  '''
    A mixin to validate that a field contains valid JSON.
  '''

  def clean_question_answer_data(self):
    '''
      validate that the 'question_answer_data' field is a proper JSON field
    '''
    data = self.cleaned_data.get('question_answer_data')

    if isinstance(data, dict):
      # If data is already a dictionary, no need to parse it as JSON.
      return data

    try:
      # check if it is valid JSON data by just loading it
      data = json.loads(data)
    except json.JSONDecodeError:
      raise ValidationError("Invalid JSON format. Please enter valid JSON data")
    # return cleaned data if it is valid
    return data
