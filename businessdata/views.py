from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.contrib import messages
from .models import BusinessUserData
from .forms import (
  BusinessUserDataForm,
  BusinessUserDataUpdateForm
)


# setup function that checks if user is business 
# and use in decorator for group filtering views
def is_business_user(user):
  return user.groups.filter(name='business').exists()

# user index page
@login_required(login_url='users:loginbusinessuser')
@user_passes_test(is_business_user, login_url='users:loginbusinessuser')
def businessDataManagement(request):
  data = BusinessUserData.objects.filter(user=request.user).values("id", "document_title")
  context = {"data": data}
  return render(request, 'business/businessdatamanagement.html', context)
  # for API later on we might use jsonResponse
  '''
  return JsonResponse({'business_data': list(data)})
  # which will output (good for frontend REACT...)
  {
    "business_data": [
      {"id": 1, "document_title": "Title1"},
      {"id": 2, "document_title": "Title2"}
    ]
  }
  '''

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
        "Business data added successfully!"
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

