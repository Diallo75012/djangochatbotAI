import re
import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.messages import get_messages
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
    password="Testpassword123!",
  )
  client.login(
    username="testuser",
    password="Testpassword123!",
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


@pytest.mark.django_db
def test_index_view_access_logged_in(
  client, django_user_model
):
  # create test user
  user =  django_user_model.objects.create_user(
    username="testuser",
    password="Testpassword123!",
  )
  client.login(
    username="testuser",
    password="Testpassword123!",
  )
  response = client.get(reverse("users:index"))
  # ensure logged-in user can access index page
  assert response.status_code == 200

@pytest.mark.django_db
def test_index_view_access_not_logged_in(client):
  response = client.get(reverse("users:index"))
  # ensure not logged-in user is redirected to login
  assert response.status_code == 302
  assert response.url.startswith(reverse(
    "users:loginuser"
  ))


@pytest.mark.django_db
def test_delete_business_data(
  client, django_user_model
):
  # create test user
  user =  django_user_model.objects.create_user(
    username="testuser",
    password="Testpassword123!",
  )
  client.login(
    username="testuser",
    password="Testpassword123!",
  )
  # create business data
  business_data = BusinessUserData.objects.create(
    user=user,
    document_title="Title to Delete",
    question_answer_data='{"question": "answer"}'
  )
  response = client.post(reverse(
    "users:deletebusinessdata",
    kwargs={
      "pk": business_data.pk
    }
  ))
  # ensure data is deleted successfully
  assert response.status_code == 302
  assert not BusinessUserData.objects.filter(
    pk=business_data.pk
  ).exists()


@pytest.mark.django_db
def test_delete_business_data_not_owned(
  client, django_user_model
):
  # create two users
  user1 =  django_user_model.objects.create_user(
    username="user1",
    password="Password123!",
  )
  user2 =  django_user_model.objects.create_user(
    username="user2",
    password="Password123!",
  )
  # login one of those two users
  client.login(
    username="user1",
    password="Password123!",
  )
  # create business data for user2
  business_data = BusinessUserData.objects.create(
    user=user2,
    document_title="Title to Delete",
    question_answer_data='{"question": "answer"}'
  )
  response = client.post(reverse(
    "users:deletebusinessdata",
    kwargs={
      "pk": business_data.pk
    }
  ))
  # ensure user1 cannot delete user2's data
  assert response.status_code == 404
  assert BusinessUserData.objects.filter(
    pk=business_data.pk
  ).exists()


@pytest.mark.django_db
def test_login_already_authenticated_user(
  client, django_user_model
):
  # create test user
  user =  django_user_model.objects.create_user(
    username="testuser",
    password="Testpassword123!",
  )
  client.login(
    username="testuser",
    password="Testpassword123!",
  )
  response = client.get(reverse("users:loginuser"))
  # ensure authenticated user is redirected
  assert response.status_code == 302
  assert response.url == reverse("users:index")


@pytest.mark.django_db
def test_register_existing_user(
  client, django_user_model
):
  # create test user
  user =  django_user_model.objects.create_user(
    username="existinguser",
    password="Existingpassword123!",
    email="existinguser@example.com",
  )
  # attempt to register with same username
  response = client.post(reverse(
    "users:registeruser"
  ), {
    "username": "existinguser",
    "email": "existinguser@example.com",
    "password1": "ExistingPassword123!",
    "password2": "ExistingPassword123!",
  })
  # ensure an error message is returned
  # and no user is created
  assert response.status_code == 200
  # Use get_messages to retrieve all messages
  messages = list(get_messages(response.wsgi_request))
  print("MESSAGES: ", messages)
  assert any(
    "A user with the username 'existinguser' already exists." in message.message for message in messages
  ), "Expected error message not found in response messages"
  assert User.objects.filter(
    username="existinguser"
  ).count() == 1


@pytest.mark.django_db
def test_add_business_data_invalid_json(
  client, django_user_model
):
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
    "question_answer_data": "Invalid JSON Format",
  })
  # ensure form error is displayed for invalid JSON format
  assert response.status_code == 200
  print("RESPONSE FORM ERRORS: ", response.context["form"].errors["question_answer_data"])
  assert "question_answer_data" in response.context["form"].errors
  # this message comes from the override of django-built-in JSON error message "Enter a valid JSON." and is used in the models JSONField
  # you can get rid of this override in the models.py JSONField and here just put "Enter a valid JSON" instead of "Invalid JSON format. Please enter valid JSON data"
  # i choose to use just nor mal built-ion django error message for invalid JSON and leave model.py alone 
  assert "Enter a valid JSON." in response.context["form"].errors["question_answer_data"]

def test_update_business_data_not_owned(
  client, django_user_model
):
  # create two test users
  user1 = django_user_model.objects.create_user(
    username="user1",
    password="Password123!",
  )
  user2 = django_user_model.objects.create_user(
    username="user2",
    password="Password123!",
  )
  client.login(
    username="user1",
    password="Password123!"
  )
  # create business data owned by user2
  business_data = BusinessUserData.objects.create(
    user=user2,
    document_title="Title Not Owned",
    question_answer_data='{"question":"answer"}'
  )
  response = client.post(reverse(
    "users:updatebusinessdata",
    kwargs={
      "pk": business_data.pk
  }), {
    "document_title": "Updated Title",
    "question_answer_data": '{"question":"updated_answer"}',
  })
  # ensure user1 cannot update user2's data
  assert response.status_code == 404
  assert BusinessUserData.objects.filter(
    pk=business_data.pk
  ).exists()
  business_data.refresh_from_db()
  assert business_data.document_title == "Title Not Owned"


@pytest.mark.django_db
def test_update_user_unauthenticated(client):
  """
  Ensure an unauthenticated user trying to access updateUser is redirected to the login page.
  """
  response = client.get(reverse('users:updateuser'))
  assert response.status_code == 302
  assert response.url.startswith(reverse('users:loginuser'))


@pytest.mark.django_db
def test_delete_business_data_unauthorized_user(client, django_user_model):
  """
  Ensure unauthorized users cannot delete business data.
  """
  # Create an owner user and a non-owner user
  owner_user = django_user_model.objects.create_user(
    username="owneruser",
    password="Ownerpassword123!",
  )
  non_owner_user = django_user_model.objects.create_user(
    username="nonowneruser",
    password="NonOwnerpassword123!",
  )
  # Log in as the owner and create business data
  client.login(username="owneruser", password="Ownerpassword123!")
  business_data = BusinessUserData.objects.create(
    user=owner_user,
    document_title="Owned Business Data",
    question_answer_data='{"question": "answer"}',
  )
  # Log out the owner user and log in as the non-owner
  client.logout()
  client.login(username="nonowneruser", password="NonOwnerpassword123!")
    
  # Attempt to delete business data created by another user
  response = client.post(reverse("users:deletebusinessdata", kwargs={"pk": business_data.pk}))
    
  # Ensure the user receives a forbidden (403) or is redirected appropriately
  assert response.status_code in [404, 403]
    
  # Ensure the business data still exists
  assert BusinessUserData.objects.filter(pk=business_data.pk).exists()
  


