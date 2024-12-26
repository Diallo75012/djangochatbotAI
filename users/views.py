import os
import json
import logging
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User, Group
from django.shortcuts import get_object_or_404
from django.contrib import messages
from .forms import (
  CreateBusinessUserForm,
  UpdateBusinessUserForm,
  # to create/update
  CreateClientUserForm,
  UpdateClientUserForm
)
from .models import ClientUser
import memcache
from django.http import HttpResponse


# setup logger
users_app_logger = logging.getLogger('users')

# Connecting to Memcached
mc = memcache.Client(['127.0.0.1:11211'], debug=1)

# setup function checks if user is client user
# and use in decorator for checks
def is_client_user(user):
  return user.groups.filter(name='client').exists()


#############################################################
#               BUSINESS USER                               #
#############################################################
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
    
      users_app_logger.info(f"A user with the username '{username}' already exists.")
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

        users_app_logger.info(f"Account has been created for {username}")
        messages.success(request, f"Account has been created for {username}")
        return redirect('users:loginbusinessuser')
      else:
        users_app_logger.info("Authentication failed after registration.")
        messages.error(request, "Authentication failed after registration.")
    else:
      users_app_logger.info("Invalid form submission. Please correct the errors.")
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

            users_app_logger.info('Your profile has been updated successfully.')
            messages.success(request, 'Your profile has been updated successfully.')
            return redirect('businessdata:businessdatamanagement')
        else:
            users_app_logger.info('Please correct the error below.')
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
        users_app_logger.info('User is not a business user. Create a business account, then come back to login here.')
        messages.error(request, 'User is not a business user. Create a business account, then come back to login here.')
    else:
      users_app_logger.info('Username OR Password is incorrect')
      messages.info(request, 'Username OR Password is incorrect')

  context = {}
  return render(request, 'users/loginbusinessuser.html', context)

# logout user
def logoutBusinessUser(request):
  logout(request)
  users_app_logger.info('Business User logged out.')
  return redirect('users:loginbusinessuser')


#############################################################
#               CLIENT USER                                 #
#############################################################

# register user
def registerClientUser(request):

  if request.method == 'POST':
    form = CreateClientUserForm(request.POST)

    # Check if the username already exists before form validation
    username = request.POST.get('username')
    if User.objects.filter(username=username).exists():
    
      users_app_logger.info(f"A user with the username '{username}' already exists.")
      messages.error(request, f"A user with the username '{username}' already exists.")
      form.add_error("username", f"A user with the username '{username}' already exists.")
      context = {'form': form}
      return render(request, 'users/registerclientuser.html', context)

    # Proceed with validating the form
    if form.is_valid():
      # Save the user and log them in
      user = form.save()

      # Add user to 'business' group
      client_group, created = Group.objects.get_or_create(name='client')
      user.groups.add(client_group)

      username = form.cleaned_data.get('username')
      password = form.cleaned_data['password1']
      user = authenticate(username=user.username, password=password)

      if user:
        login(request, user)

        users_app_logger.info(f"Account has been created for {username}")
        messages.success(request, f"Account has been created for {username}")
        return redirect('users:loginclientuser')
      else:
        users_app_logger.info("Authentication failed after registration.")
        messages.error(request, "Authentication failed after registration.")
    else:
      users_app_logger.info("Invalid form submission. Please correct the errors.")
      messages.error(request, "Invalid form submission. Please correct the errors.")
  else:
    # Present an empty registration form by default
    form = CreateClientUserForm()

  context = {'form': form}
  return render(request, 'users/registerclientuser.html', context)


# update user will be used as user settings page to update
@login_required(login_url='users:loginclientuser')
@user_passes_test(is_client_user, login_url='users:loginclientuser')
def updateClientUser(request):
  """
  View to update the logged-in user's information.
  """
  user = get_object_or_404(User, pk=request.user.pk)
  form = UpdateClientUserForm(instance=user)

  if request.method == 'POST':
    # Include request.FILES to handle image uploads
    form = UpdateClientUserForm(request.POST, request.FILES, instance=user)
    if form.is_valid():
      form.save()

      users_app_logger.info('Your profile has been updated successfully.')
      messages.success(request, 'Your profile has been updated successfully.')
      return redirect('clientchat:clientuserchat')
    else:
      users_app_logger.info('Please correct the error below.')
      messages.error(request, 'Please correct the error below.')

  context = {'form': form}
  return render(request, 'users/updateclientuser.html', context)


# login user
def loginClientUser(request):
  # making sure user is redirected to index page when already logged in
  if request.user.is_authenticated:
    return redirect('clientchat:clientuserchat')

  if request.method == 'POST':
    username = request.POST.get('username')
    password = request.POST.get('password')

    user = authenticate(request=request, username=username, password=password)
    if user is not None:
      if is_client_user(user):
        login(request, user)
        users_app_logger.info('Business User logged in.')
        return redirect('clientchat:clientuserchat')
      else:
        users_app_logger.info('User is not a client user. Create a client account, then come back to login here.')
        messages.error(request, 'User is not a client user. Create a client account, then come back to login here.')
    else:
      users_app_logger.info('Username OR Password is incorrect')
      messages.info(request, 'Username OR Password is incorrect')

  context = {}
  return render(request, 'users/loginclientuser.html', context)



# we make sure that when we logout the cache is emptied
def logoutClientUser(request):
  user = request.user
  cache_key = f"chat_{user.id}"
  # clear the cached messges on logout
  mc.delete(cache_key)
  logout(request)
  users_app_logger.info('Business User Logged Out.')
  return redirect('users:loginclientuser')
