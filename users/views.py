from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.contrib import messages
from .forms import (
  CreateBusinessUserForm,
  UpdateBusinessUserForm,
)

# setup function that checks if user is business 
# and use in decorator for group filtering views
def is_business_user(user):
  return user.groups.filter(name='business').exists()

# register user
def registerBusinessUser(request):
  '''
  This route will present by default empty registration form.
  When the user posts the form, it will use this same route to create the user.
  '''
  if request.method == 'POST':
    form = CreateBusinessUserForm(request.POST)

    # Check if the username already exists before form validation
    username = request.POST.get('username')
    if User.objects.filter(username=username).exists():
      messages.error(request, f"A user with the username '{username}' already exists.")
      form.add_error("username", f"A user with the username '{username}' already exists.")
      context = {'form': form}
      return render(request, 'users/registerbusinessuser.html', context)

    # Proceed with validating the form
    if form.is_valid():
      # Save the user and log them in
      user = form.save()

      # Add user to 'business' group
      business_group, created = Group.objects.get_or_create(name='business')
      user.groups.add(business_group)

      password = form.cleaned_data['password1']
      user = authenticate(username=username, password=password)

      if user:
        login(request, user)
        messages.success(request, f"Account has been created for {username}")
        return redirect('businessdata:loginuser')
      else:
        messages.error(request, "Authentication failed after registration.")
    else:
      messages.error(request, "Invalid form submission. Please correct the errors.")
  else:
    # Present an empty registration form by default
    form = CreateBusinessUserForm()

  context = {'form': form}
  return render(request, 'users/registerbusinessuser.html', context)


# update user
@login_required(login_url='users:loginuser')
@user_passes_test(is_business_user, login_url='users:loginbusinessuser')
def updateBusinessUser(request):
    """
    View to update the logged-in user's information.
    """
    user = get_object_or_404(User, pk=request.user.pk)
    form = UpdateBusinessUserForm(instance=user)

    if request.method == 'POST':
        form = UpdateBusinessUserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated successfully.')
            return redirect('businessdata:businessdatamanagement')
        else:
            messages.error(request, 'Please correct the error below.')

    context = {'form': form}
    return render(request, 'users/updatebusinessuser.html', context)

# login user
def loginBusinessUser(request):
  # making sure user is redirected to index page when already logged in
  if request.user.is_authenticated:
    return redirect('businessdata:businessdatamanagement')

  if request.method == 'POST':
    username = request.POST.get('username')
    password = request.POST.get('password')

    user = authenticate(request=request, username=username, password=password)
    if user is not None:
      if is_business_user(user):
        login(request, user)
        return redirect('businessdata:businessdatamanagement')
      else:
        messages.error(request, 'User is not a business user.')
    else:
      messages.info(request, 'Username OR Password is incorrect')

  context = {}
  return render(request, 'users/loginbusinessuser.html', context)

# logout user
def logoutBusinessUser(request):
  logout(request)
  return redirect('users:loginbusinessuser')


