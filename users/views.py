from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.contrib import messages
from .models import BusinessUserData
from .forms import (
  CreateUserForm,
  UpdateUserForm,
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
  This route will present by default empty registration form.
  When the user posts the form, it will use this same route to create the user.
  '''
  if request.method == 'POST':
    form = CreateUserForm(request.POST)

    # Check if the username already exists before form validation
    username = request.POST.get('username')
    if User.objects.filter(username=username).exists():
      messages.error(request, f"A user with the username '{username}' already exists.")
      form.add_error("username", f"A user with the username '{username}' already exists.")
      context = {'form': form}
      return render(request, 'registration/registeruser.html', context)

    # Proceed with validating the form
    if form.is_valid():
      # Save the user and log them in
      user = form.save()
      password = form.cleaned_data['password1']
      user = authenticate(username=username, password=password)

      if user:
        login(request, user)
        messages.success(request, f"Account has been created for {username}")
        return redirect('users:loginuser')
      else:
        messages.error(request, "Authentication failed after registration.")
    else:
      messages.error(request, "Invalid form submission. Please correct the errors.")
  else:
    # Present an empty registration form by default
    form = CreateUserForm()

  context = {'form': form}
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
  # making sure user is redirected to index page when already logged in
  if request.user.is_authenticated:
    return redirect('users:index')

  if request.method == 'POST':
    username = request.POST.get('username')
    password = request.POST.get('password')

    user = authenticate(request=request, username=username, password=password)
    if user is not None:
      login(request, user)
      return redirect('users:index')
    else:
      messages.info(request, 'Username OR Password is incorrect')

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
      business_data = form.save(commit=False)
      business_data.user = request.user
      print("Business user: ", request.user)
      business_data.save()
      messages.success(
        request,
        "Business data added successfully!"
      )
      return redirect("users:index")
    else:
      messages.error(
        request,
        "Form submission incorrect. Please enter correct information (e.g., valid JSON in {'question':'answer'} format)."
      )
  context = {'form': form}
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
  context = {'form': form}
  return render(request, "business/updatebusinessdata.html", context)


# delete business data
@login_required(login_url="users:loginuser")
def deleteBusinessData(request, pk):
  business_data_to_delete = get_object_or_404(BusinessUserData, id=pk, user=request.user)
  if request.method == "POST":
    business_data_to_delete.delete()
    messages.success(
      request,
      "Business data has been successfully deleted."
    )
    return redirect("users:index")

