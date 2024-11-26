import pytest
from django.contrib.auth.models import User
from users.forms import (
  CreateUserForm,
  BusinessUserDataForm,
  UpdateUserForm
)

@pytest.mark.django_db
def test_create_user_form_valid():
  form_data = {
    "username": "testuser",
    "email": "testuser@example.com",
    "password1": "Password123!",
    "password2": "Password123!"
  }
  form = CreateUserForm(data=form_data)
  assert form.is_valid()


@pytest.mark.django_db
def test_create_user_form_invalid():
  form_data = {
    "username": "testuser",
    "email": "testuser@example.com",
    "password1": "Password123!",
    "password2": "wrongdoublepassword"
  }
  form = CreateUserForm(data=form_data)
  assert not form.is_valid()

@pytest.mark.django_db
def test_business_user_data_form():
  user = User.objects.create_user(
    username="testuser",
    password="Testpassword123!"
  )
  form_data = {
    "user": user.id,
    "document_title": "Test Title",
    "question_answer_data": '{"question": "answer"}'
  }
  form  = BusinessUserDataForm(data=form_data)
  assert form.is_valid()

@pytest.mark.django_db
def test_update_user_form():
  user = User.objects.create_user(
    username="testuser",
    password="Testpassword123!",
    email="testuser@eample.com"
  )
  form_data = {
    "username": "testuser",
    "email": "testuser@example.com",
    "password1": "Password123!",
    "password2": "wrongdoublepassword"
  }
  form = UpdateUserForm(data=form_data, instance=user)
  assert form.is_valid()







