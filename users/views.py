from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import BusinessUserData
from .forms import (
  CreateUserForm,
  BusinessUserDataForm,
  BusinessUserDataUpdateForm
)


# user index page
@login_required(login_url='users:loginuser')
def index(request):
  data = BusinessUserData.objects.filter(user=request.user).values("id", "document_title")
  context = {"data": data}
  return render(request, 'users/main.html', context)
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
# register user
def registerUser(request):
  '''
    This route will present by default empty registration form
    When the user post the form it will use this same route to create user
  '''
  if request.method == 'POST':
    form = CreateUserForm(request.POST)
    if form.is_valid():
      username = form.cleaned_data['username']

      # check if user already exists
      if form._meta.model.objects.filter(username=username).exists():
        messages.error(request, f"A user with the username '{username}' already exists.\nPlease try login page if it is you with you password.")
        return redirect('user:registeruser')

      # save the user and log them in
      user = form.save()
      password = form.cleaned_data['password1']
      user = authenticate(username=username, password=password)

      if user:
        login(request, user)
        message.success(request, f"Account has been created for {username}")
        # this will pass the login page and redirect to the opened interface for business users
        # as this route will check if user is logged in or notm if user is logged in it won't show the login form but login page
        return redirect('users:loginuser')
      else:
        messages.error(request, "Authentication failed after registration.")

    # here if form is not valid
    else:
      messages.error(request, "Invalid form subnission.Please correct the errors.")
  else:
    # otherwise by default we present user form empty to be registred
    form = CreateUserForm()

  context = {'usercreationform': form}
  return render(request, 'registration/registeruser.html', context)

# update user
@login_required(login_url='users:loginuser')
def updateUser(request):
    """
    View to update the logged-in user's information.
    """
    user = get_object_or_404(User, pk=request.user.pk)
    form = UpdateUserForm(instance=user)

    if request.method == 'POST':
        form = UpdateUserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated successfully.')
            return redirect('users:index')
        else:
            messages.error(request, 'Please correct the error below.')

    context = {'form': form}
    return render(request, 'users/updateuser.html', context)

# login user
def loginUser(request):
  if request.method == 'POST':
    username = request.POST.get('username')
    password = request.POST.get('password')

    user = authenticate(request, username, password=password)
    if iser is not None:
      login(request, user)
      return redirect('users:index')
    else:
      message.info(request, 'Username OR Password is incorrect')

  context = {}
  return render(request, 'accounts/loginuser.html', context)

# logout user
def logoutUser(request):
  logout(request)
  return redirect('users:loginuser')

# add business data
@login_required(login_url='users:loginuser')
def addBusinessData(request):
  '''
    Handle adding business daa with JSONField validation.
  '''

  form = BusinessUserDataForm()
  if request.method == 'POST':
    form = BusinessUserDataForm(request.POST)
    if form.is_valid():
      form.save()
      messages.success(
        request,
        "Business data added successfully!"
      )
      # we just return to same page if user need to add more 
      # otherwise user will use navigation to go somewhere else
      return redirect("users:addbusinessdata")
    else:
      messages.error(
        request,
        "Form submission incorrect. Please enter correct information (JSON) {'question':'answer',...}"
      )
  context = {'adddatafrom': form}
  # JSON validation should be handled at the form level, no need to submit if it is not good JSON/Dict
  return render(request, 'business/addbusinessdata.html', context)

# update business data
@login_required(login_url='users:loginuser')
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
      return redirect("users:index")
    else:
      messages.error(
        request,
        "Form submission incorrect. Please enter correct information respecting the data. eg: JSON format or DICT"
      )
  context = {'businessdataupdateform': form}
  return render(request, "business/updatebusinessdata.html", context)


# delete business data
@login_required(login_url="users:loginuser")
def deleteBusinessData(request, pk):
  business_data_to_delete = get_objects_or_404(BusinessUserData, id=pk, user=request.user)
  if request.method == "POST":
    business_data_to_delete.delete()
    messages.success(
      request,
      "Business data has been successfully deleted."
    )
    return redirect("users:index")

