import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from users.models import BusinessUserData

@pytest.mark.django_db
def test_regiester_user(client):
  # test user registration
  response = client.post(reverse("users:registeruser"),{
    "username": "newuser",
    "email": "newuser@example.com",
    "password1": "Newpassword123!",
    "password2": "Newpassword123!",
  })
  # redirect to login page after registration
  assert response.status_code == 302
  assert User.objects.filter(username="newuser").exists()


@pytest.mark.django_db
def test_login_user(client, django_user_model):
  # create test user
  user =  django_user_model.objects.create_user(
    username="testuser",
    password="Testpassword123!",
  )
  response = client.post(reverse(
    "users:loginuser"
  ),{
    "username": "testuser",
    "password": "Testpassword123!",
  })
  # redirect after successful login
  assert response.status_code == 302
  assert response.url == reverse("users:index")


@pytest.mark.django_db
def test_logout(client, django_user_model):
  # create test user
  user =  django_user_model.objects.create_user(
    username="testuser",
    password="Testpassword123!",
  )
  client.login(
    username="testuser",
    password="Testpassword123!",
  )
  response = client.get(reverse(
    "users:logoutuser"
  ))
  assert response.status_code == 302


@pytest.mark.django_db
def test_add_business_data(client, django_user_model):
  # create test user
  user =  django_user_model.objects.create_user(
    username="testuser",
    password="Testpassword123!",
  )
  client.login(
    username="testuser",
    password="Testpassword123!",
  )
  response = client.post(reverse(
    "users:addbusinessdata"
  ), {
    "document_title": "Test Title",
    "question_answer_data": '{"question":"answer"}',
  })
  # redirect successful after submission
  assert response.status_code == 302
  assert BusinessUserData.objects.filter(
    document_title="Test Title",
    user=user
  ).exists()


@pytest.mark.django_db
def test_update_business_data(client, django_user_model):
  # create test user
  user =  django_user_model.objects.create_user(
    username="testuser",
    password="Testpassword123!",
  )
  client.login(
    username="testuser",
    password="Testpassword123!",
  )
  # create initial business data
  business_data = BusinessUserData.objects.create(
    user=user,
    document_title="Intitial Title",
    question_answer_data='{"question":"initial_answer"}'
  )
  # update business data (pk present)
  response = client.post(reverse(
    "users:updatebusinessdata",
    kwargs={
      "pk": business_data.pk
    }
  ), {
    "document_title": "Updated Title",
    "question_answer_data": '{"question":"updated_answer"}',
  })
  # redirect successful after update
  assert response.status_code == 302
  business_data.refresh_from_db()
  assert business_data.document_title == "Updated Title"
  assert business_data.question_answer_data == {"question":"updated_answer"}



@pytest.mark.django_db
def test_update_user_profile(client, django_user_model):
  # create test user
  user =  django_user_model.objects.create_user(
    username="testuser",
    password="Testpassword123",
  )
  client.login(
    username="testuser",
    password="Testpassword123",
  )
  response = client.post(reverse(
    "users:updateuser"
  ), {
    "username": "updateduser",
    "email": "updateduser@example.com",
    "first_name": "UpdatedFirst",
    "last_name": "UpdatedLast",
  })
  # redirect successful after update
  # refresh user instance to get updated data retrieved after making request
  user.refresh_from_db()
  assert user.username == "updateduser"
  assert user.email == "updateduser@example.com"
  assert user.first_name == "UpdatedFirst"
  assert user.last_name == "UpdatedLast"

