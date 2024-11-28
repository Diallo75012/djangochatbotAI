from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.utils import timezone
from .forms import (
  CreateBusinessUserForm,
  UpdateBusinessUserForm,
  # to create/update
  ClientUserChatForm,
)
# from chatbotsettings.models import ChatBotSettings
from .models import ClientUser, ChatUserMessage
import hashlib
import memcache


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


#############################################################
#               CLIENT USER                                 #
#############################################################
@login_required(login_url='users:loginindex') #loginindex to be created
@user_passes_test(is_client_user, login_url='users:loginclientuser') # url to be created
def clientUserChat(request):
  user = request.user
  cache_key = f"chat_{user.id}"

  # fetch chat messages from cache or database
  chat_messages = mc.get(cache_key)
  if not chat_messages:
    chat_messages = ChatMessages.objects.filter(
      user=user
    ).order_by('timestamp')
    # this is how in memecached you record data with ttl 1h
    mc.set(cache_key, list(chat_messages), time=3600)

  if request.method == 'POST':
    form = ClientUserChatForm(request.POST)
    if form.is_valid():
      # save user message
      user_message = form.cleaned_dat['message']
      chat_msg = ChatMessage.objects.create(
        user=user,
        sender_type='user',
        nickname=user.clientuser.nickname,
        content=user_message,
        timestamp=timezone.now()
      )

      # save in database and update cache
      # convert QuerySet to list if not already done
      chat_messages = list(chat_messages)
      chat_messages.apped(chat_msg)
      mc.set(cache_key, chat_messages, time=36000)

      # dummy chat response until we plugin LLM Agents
      bot_response_content = f"Echo: {user_message}"
      bot_msg = ChatMessage.objects.create(
        user=user,
        sender_type='bot',
        nickname="ChatBot",
        content=bot_response_content,
        timestamp=timezone.now()
      )

      # update cache with bot response
      chat_messages.append(bot_msg)
      mc.set(cache_key, chat_messages, time=36000)

      # or use django native session states to set messages
      # request.session['chat_state'] = list(chat_messages)
      # and retrieve later using
      # chat_messages = request.session.get('chat_state', [])

      # save bot message in the database as well
      bot_msg.save()

      # reload page to show new messages
      return redirect('clientuserchat')
  else:
    form = ClientUserChatForm()

  # now lets pass all that to WebUI context
  context = {
    'form': form,
    'chat_messages': chat_messages,
    'user_avatar': user.clientuser.picturl.url if user.clientuser.picture else None,
    'chatbot_avatar': 'dummy/url/image.png'
  }

  return render(request, 'users/clientuserchat.html', context)


# we make sure that when we logout the cache is emptied
def clientUserLogout(request):
  user = request.user
  cache_key = f"chat_{user.id}"
  # clear the cached messges on logout
  mc.delete(cache_key)
  logout(request)
  # rotue to be created
  return redirect('users:loginclientuser')
