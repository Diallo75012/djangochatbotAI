import requests
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
      business_data = form.save(commit=False)
      business_data.user = request.user
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
      embed_data_url = reverse("embed-data", kwargs={"pk": document_title_id})
      # Construct the full URL using the request's base URI
      full_url = request.build_absolute_uri(embed_data_url)
      # no payload send as we don't want to have a size limit
      # but will fetch data fom database to create embeddings on the fly using document id
      # document title will be the collection name there, and question/answers will be looped through to create doc to embed
      # with document title as metadata
      try:
        # call the route using post request for the moment if we need to add data to payload (which is empty in this code version)
        response = requests.post(full_url, headers={"Content-Type": "application/json"})
        # Check the response status
        if response.status_code == 200:
          response_success = json.loads(response)["success"]
          print("Embedding created successfully:", response_success)
          messages.success(
            request,
            "Business data added successfully! Wait a for embedding validation."
          )
          return redirect("businessdata:addbusinessdata")
        else:
          '''
           Log error to Devops/Security team
          '''
          response_error = json.loads(response)["error"]
          messages.error(
            request,
            f"Failed to create embedding. Status code: {response.status_code}, Response: {response_error}"
          )
          return redirect("businessdata:addbusinessdata")

      except requests.exceptions.RequestException as e:
        '''
         Log erro to Devops/Security team
        '''
        messages.error(
          request,
          f"Error making the request: {e}"
        )
        return redirect("businessdata:addbusinessdata")

    else:
      messages.error(
        request,
        "Form submission incorrect. Please enter correct information (e.g., valid JSON in {'question':'answer'} format)."
      )

  context = {'form': form}
  # JSON validation should be handled at the form level, no need to submit if it is not good JSON/Dict
  return render(request, 'business/addbusinessdata.html', context)

# update business data
@login_required(login_url='users:loginbusinessuser')
@user_passes_test(is_business_user, login_url='users:loginbusinessuser')
def updateBusinessData(request, pk):
  business_data_to_update = get_object_or_404(BusinessUserData, pk=pk, user=request.user)
  form = BusinessUserDataUpdateForm(instance=business_data_to_update)

  if request.method == 'POST':
    form = BusinessUserDataUpdateForm(request.POST, instance=business_data_to_update)
    if form.is_valid():
      form.save()
      messages.success(
        request,
        "Data has been updated successfully."
      )
      return redirect("businessdata:businessdatamanagement")
    else:
      messages.error(
        request,
        "Form submission incorrect. Please enter correct information respecting the data. eg: JSON format or DICT"
      )
  context = {'form': form}
  return render(request, "business/updatebusinessdata.html", context)


# delete business data
@login_required(login_url="users:loginuser")
@user_passes_test(is_business_user, login_url='users:loginbusinessuser')
def deleteBusinessData(request, pk):
  business_data_to_delete = get_object_or_404(BusinessUserData, id=pk, user=request.user)
  if request.method == "POST":
    business_data_to_delete.delete()
    messages.success(
      request,
      "Business data has been successfully deleted."
    )
    return redirect("businessdata:businessdatamanagement")

