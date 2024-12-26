import os
import json
import requests
import logging
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.urls import reverse
from .models import BusinessUserData
from .forms import (
  BusinessUserDataForm,
  BusinessUserDataUpdateForm
)

# setup logger
businessdata_app_logger = logging.getLogger('businessdata')

# setup function that checks if user is business
# and use in decorator for group filtering views
def is_business_user(user):
  return user.groups.filter(name='business').exists()

# business user management page (like index page)
@login_required(login_url='users:loginbusinessuser')
@user_passes_test(is_business_user, login_url='users:loginbusinessuser')
def businessDataManagement(request):
  data = BusinessUserData.objects.filter(user=request.user).values("id", "document_title", "chat_bot__name")
  context = {"data": data}
  return render(request, 'business/businessdatamanagement.html', context)

# add business data
@login_required(login_url='users:loginbusinessuser')
@user_passes_test(is_business_user, login_url='users:loginbusinessuser')
def addBusinessData(request):
  '''
    Handle adding business daa with JSONField validation.
  '''

  form = BusinessUserDataForm()

  if request.method == 'POST':
    form = BusinessUserDataForm(request.POST)
    if form.is_valid():
      # here we save to database
      business_data = form.save(commit=False)
      business_data.user = request.user
      
      businessdata_app_logger.info(f"Business user: {request.user}")
      print("Business user: ", request.user)
      
      business_data.save()
      messages.success(
        request,
        "Business data added successfully! Wait a for embedding validation."
      )
      ##### API CALL TO EMBED DOCUMENTS #####
      """
        ##### CAN BE DECOUPLED IN THE FUTURE FOR CRON JOBS AND NOTIFICATION TO BUSINESS USER WHEN READY TO BE USED BY CLIENT USER #####
        ##### WILL NEED TO CREATE ADDITION ROW IN BUSSINESSDATA MODEL BOOLEAN FOR EMBEDDED COMPLETE OR NOT AND HAVE DATA AVAILABLE #####
        ##### SO WILL NEED TO HAVE THE DOCUMENT PRESENT IN THE DROPDOWN ONLY IF DATA IS FLAGGED `TRUE` FOR THE NEW EMBEDDED CHECK COLUMN IN DB #####
      """
      # get the id of the document_title saved to make a call to the embedding route which will use that id to start working
      business_document = get_object_or_404(BusinessUserData, document_title=business_data.document_title, user=request.user)
      document_title_id = business_document.id
      # Reverse the URL for the 'embed-data' route with the given document_title_id (pk)
      embed_data_url = reverse("agents:embed-data", kwargs={"pk": document_title_id})
      # Construct the full URL using the request's base URI
      full_url = request.build_absolute_uri(embed_data_url)
      session = requests.Session()
      # no payload send as we don't want to have a size limit
      # but will fetch data fom database to create embeddings on the fly using document id
      # document title will be the collection name there, and question/answers will be looped through to create doc to embed
      # with document title as metadata
      try:
        # call the route using post request for the moment if we need to add data to payload (which is empty in this code version)
        response = session.post(full_url, headers={"Content-Type": "application/json"}, cookies=request.COOKIES)
        # Check the response status
        if response.status_code == 200:
          response_success = response.json()["success"]

          businessdata_app_logger.info(f"Embedding created successfully: {response_success}")
          print("Embedding created successfully:", response_success)

          messages.success(
            request,
            "Business data added successfully! Embeddings Done! Data ready for client user questions."
          )
          return redirect("businessdata:addbusinessdata")

        # if error we delete data from database as if not embedded no need it, the whole purpose is to embed it
        elif response.status_code == 302:
          # Handle unexpected redirects
          error_message = f"Error embedding route, Redirect detected to: {response.headers.get('Location')}"

          businessdata_app_logger.info(error_message)
          print(error_message)

          messages.error(
            request,
            f"We experience some issue with the embedding route, the whole team is working it and we apologize. Please try to save your data later."
          )
          business_data_to_update = get_object_or_404(BusinessUserData, pk=document_title_id, user=request.user)
          business_data_to_delete.delete()
          return HttpResponse(json.dumps({"error": error_message}), content_type="application/json", status=302)

        # if error we delete data from database as if not embedded no need it, the whole purpose is to embed it   
        else:
          '''
           Log error to Devops/Security team
          '''
          response_error = json.loads(response)["error"]
          messages.error(
            request,
            f"Failed to create embedding. Status code: {response.status_code}, Response: {response_error}"
          )
          businessdata_app_logger.info(f"Failed to create embedding. Status code: {response.status_code}, Response: {response_error}")
          business_data_to_update = get_object_or_404(BusinessUserData, pk=document_title_id, user=request.user)
          business_data_to_delete.delete()
          return redirect("businessdata:addbusinessdata")

      # if error we delete data from database as if not embedded no need it, the whole purpose is to embed it
      except requests.exceptions.RequestException as e:
        '''
         Log erro to Devops/Security team
        '''
        message_error = f"Error making the request: {e}"
        businessdata_app_logger.info(message_error)
        messages.error(
          request,
          message_error
        )
        business_data_to_update = get_object_or_404(BusinessUserData, pk=document_title_id, user=request.user)
        business_data_to_delete.delete()
        return redirect("businessdata:addbusinessdata")

    else:
      businessdata_app_logger.info("Form submission incorrect. Please enter correct information (e.g., valid JSON in {'question':'answer'} format).")
      messages.error(
        request,
        "Form submission incorrect. Please enter correct information (e.g., valid JSON in {'question':'answer'} format)."
      )

  context = {'form': form}
  # JSON validation should be handled at the form level, no need to submit if it is not good JSON/Dict
  return render(request, 'business/addbusinessdata.html', context)

# update business data
# this route will update the data normally but if it is questions and answers changed will update embeddings
# when embeddings are saved we keep the state of previous question answer data
# so that we can revert database state to it if embeddings fails
# we need to save database update first because the embedding route in agents is getting the question answers from database,
# so it has to be committed here first
@login_required(login_url='users:loginbusinessuser')
@user_passes_test(is_business_user, login_url='users:loginbusinessuser')
def updateBusinessData(request, pk):
  business_data_to_update = get_object_or_404(BusinessUserData, pk=pk, user=request.user)
  form = BusinessUserDataUpdateForm(instance=business_data_to_update)

  # Store the previous state of question_answer_data
  previous_question_answers = business_data_to_update.question_answer_data
  previous_question_answers_length = len(json.dumps(previous_question_answers))

  if request.method == 'POST':
    form = BusinessUserDataUpdateForm(request.POST, instance=business_data_to_update)
    if form.is_valid():
      # Commit the updated data to the database
      updated_data = form.save(commit=False)
      new_question_answers_length = len(json.dumps(updated_data.question_answer_data))

      # Check if `question_answer_data` has changed
      if previous_question_answers_length != new_question_answers_length:
        # `question_answer_data` has changed; trigger embedding logic
        document_title_id = updated_data.id
        embed_data_url = reverse("agents:embed-data", kwargs={"pk": document_title_id})
        full_url = request.build_absolute_uri(embed_data_url)
        session = requests.Session()

        try:
          updated_data.save()  # Commit the new data before embeddings so that agent route gets new data
          # Call embedding route
          response = session.post(full_url, headers={"Content-Type": "application/json"}, cookies=request.COOKIES)

          if response.status_code == 200:
            # Embedding successful
            response_success = response.json()["success"]

            businessdata_app_logger.info(f"Embedding updated successfully: {response_success}")            
            print("Embedding updated successfully:", response_success)

            messages.success(
              request,
              "Data has been updated successfully, and embeddings are valid!"
            )
            return redirect("businessdata:businessdatamanagement")

          elif response.status_code == 302:
            # Unexpected redirect
            error_message = f"Error embedding route, Redirect detected to: {response.headers.get('Location')}"
            
            businessdata_app_logger.info(error_message)
            print(error_message)

            # Rollback to previous state
            updated_data.question_answer_data = previous_question_answers
            updated_data.save()
            businessdata_app_logger.info("Embedding validation failed. Changes have been rolled back.")
            messages.error(
               request,
            "Embedding validation failed. Changes have been rolled back."
            )
            return redirect("businessdata:updatebusinessdata", pk=pk)

          else:
            # Handle embedding failure
            response_error = json.loads(response.text).get("error", "Unknown error occurred.")

            businessdata_app_logger.info(f"Embedding failed: {response_error}")
            print("Embedding failed:", response_error)

            # Rollback to previous state
            updated_data.question_answer_data = previous_question_answers
            updated_data.save()
            messages.error(
              request,
              f"Embedding validation failed. Changes have been rolled back. Error: {response_error}"
            )
            return redirect("businessdata:updatebusinessdata", pk=pk)

        except requests.exceptions.RequestException as e:
          # Request failure
          businessdata_app_logger.info(f"Error during embedding request: {e}")
          print(f"Error during embedding request: {e}")
          # Rollback to previous state
          updated_data.question_answer_data = previous_question_answers
          updated_data.save()
          messages.error(
            request,
            "An error occurred while validating embeddings. Changes have been rolled back."
          )
          return redirect("businessdata:updatebusinessdata", pk=pk)

      else:
        # `question_answer_data` hasn't changed; perform a normal update
        updated_data.save()
        businessdata_app_logger.info("Data has been updated successfully without embedding changes.")
        messages.success(
          request,
          "Data has been updated successfully without embedding changes."
        )
        return redirect("businessdata:businessdatamanagement")

    else:
      businessdata_app_logger.info("Form submission incorrect. Please enter valid data respecting the format. (e.g., JSON or dict)")
      messages.error(
        request,
        "Form submission incorrect. Please enter valid data respecting the format. (e.g., JSON or dict)"
      )

  context = {'form': form}
  return render(request, "business/updatebusinessdata.html", context)


# delete business data
@login_required(login_url="users:loginbusinessuser")
@user_passes_test(is_business_user, login_url='users:loginbusinessuser')
def deleteBusinessData(request, pk):
  business_data_to_delete = get_object_or_404(BusinessUserData, id=pk, user=request.user)

  businessdata_app_logger.info(f"business_data_to_delete: {business_data_to_delete}")
  print("business_data_to_delete: ", business_data_to_delete)

  document_title = business_data_to_delete.document_title
  document_title_id = pk
  '''
  Here get the document title so that we can delete it from the embeddings as it is the collection name.
  '''
  if request.method == "POST":

    # delete from embedding collection
    # Reverse the URL for the 'delete-embedding-collection' route with the given document_title_id (pk)
    delete_embed_data_url = reverse("agents:delete-embedding-collection", kwargs={"pk": document_title_id})
    # Construct the full URL using the request's base URI
    full_url = request.build_absolute_uri(delete_embed_data_url)
    session = requests.Session()

    try:
      # call the route using post request for the moment if we need to add data to payload (which is empty in this code version)
      response = session.post(full_url, headers={"Content-Type": "application/json"}, cookies=request.COOKIES)

      # Check the response status
      if response.status_code == 200:
        response_success = response.json()["success"]

        businessdata_app_logger.info(f"Embedding deleted successfully: {response_success}")
        print("Embedding deleted successfully:", response_success)

        # here no redirect we will just at the end of the function send the success message and redirect once
        # but we can tell user to wait for full deletion
        # we don't redirect here as we still need to delete database data in the next try/except, then we redirect
        messages.success(
          request,
          f"Embeddings data deleted successfully."
        )
      else:
        # here we will redirect has there have been an error
        '''
         Log error to Devops/Security team
        '''
        response_error = json.loads(response)["error"]

        businessdata_app_logger.info(f"Failed to delete embedding. Status code: {response.status_code}, Response: {response_error}")

        messages.error(
          request,
          f"Failed to delete embedding. Status code: {response.status_code}, Response: {response_error}"
        )
        return redirect("businessdata:businessdatamanagement")

    except requests.exceptions.RequestException as e:
      '''
       Log erro to Devops/Security team
      '''
      businessdata_app_logger.info(f"Error making the request: {e}")
      
      messages.error(
        request,
        f"Error making the request: {e}"
      )
      return redirect("businessdata:businessdatamanagement")

    # delete from database now that's embedding are deleted successfully,
    # this won't be triggered if embedding deletion fails, data is safe
    try:
      business_data_to_delete.delete()
      businessdata_app_logger.info("Database data have been successfully deleted.")
      print("Database data have been successfully deleted.")
    except Exception as e:
      businessdata_app_logger.info(f"An error occured while trying to delete data from database: {e}")
      print(f"An error occured while trying to delete data from database: {e}")

  # here we return the confirmation message of data deletion
  businessdata_app_logger.info("Full business data deletion confirmation status: 'successfully deleted'.")
  messages.success(
    request,
    "Full business data deletion confirmation status: 'successfully deleted'."
  )
  return redirect("businessdata:businessdatamanagement")

