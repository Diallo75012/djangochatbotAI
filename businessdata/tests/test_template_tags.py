import pytest
from django import forms
from django.template import Context, Template
from users.templatetags.form_tags import add_class


@pytest.mark.django_db
def test_add_class_filter():
  #create a simple form field
  class SampleForm(forms.Form):
    name = forms.CharField()

  form = SampleForm()
  field = form["name"]
  # apply the add class filter
  rendered_field = add_class(field, "test-class")
  assert 'class="test-class"' in rendered_field


@pytest.mark.django_db
def test_add_class_filter_invalid_field():
  # passing None as field to check how the function handles it
  with pytest.raises(AttributeError):
    add_class(None, "test-class")

