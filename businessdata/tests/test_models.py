import pytest
from django.contrib.auth.models import User
from users.models import BusinessUserData


@pytest.mark.django_db
def test_create_business_user_data():
  # create user
  user = User.objects.create_user(
    username="testuser",
    password="testpassword"
  )

  # create business instance
  business_data = BusinessUserData.objects.create(
    user=user,
    document_title="Test Document",
    question_answer_data='{"question": "answer"}'
  )

  # check taht instance is created succcessfully
  assert BusinessUserData.objects.count() == 1
  assert business_data.document_title == "Test Document"
  assert business_data.question_answer_data == '{"question": "answer"}'


@pytest.mark.django_db
def test_business_user_data_str():
  # create user
  user = User.objects.create_user(
    username="testuser",
    password="testpassword"
  )
  # create BusinessUserData instance
  business_data = BusinessUserData.objects.create(
    user=user,
    document_title="Test Document",
    question_answer_data='{"question": "answer"}'
  )

  # check the  __str__ method works fine
  assert str(business_data) == 'Test Document: {"question": "answer"}'


@pytest.mark.django_db
def test_business_user_data_unique_document_title():
  # create user
  user = User.objects.create_user(
    username="testuser",
    password="testpassword"
  )
  # create BusinessUserData instance
  business_data = BusinessUserData.objects.create(
    user=user,
    document_title="Unique Title",
    question_answer_data='{"question": "answer"}'
  )

  # attempt to create another business data instance with the same document title
  with pytest.raises(Exception):
    business_data = BusinessUserData.objects.create(
      user=user,
      document_title="Unique Title",
      question_answer_data='{"question": "answer"}'
    )








