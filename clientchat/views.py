import json
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User, Group
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.utils import timezone
from django.core.cache import cache  # Using Django's cache framework for simplicity
from .forms import (
  ClientUserChatForm,
)
from chatbotsettings.models import ChatBotSettings
from businessdata.models import BusinessUserData
from users.models import ClientUser
from .models import ChatMessages
import memcache
# just for returning test when debugging other route redirects
from django.http import HttpResponse, JsonResponse


# Connecting to Memcached
mc = memcache.Client(['127.0.0.1:11211'], debug=1)

# setup function checks if user is client user
# and use in decorator for checks
def is_client_user(user):
  return user.groups.filter(name='client').exists()

# client user chat route
@login_required(login_url='users:loginclientuser')
@user_passes_test(is_client_user, login_url='users:loginclientuser')
def clientUserChat(request):
    user = request.user
    cache_key = f"chat_{user.id}"

    # Fetch chat messages from cache or database
    chat_messages = mc.get(cache_key)
    if not chat_messages:
        chat_messages = ChatMessages.objects.filter(user=user).order_by('timestamp')
        mc.set(cache_key, list(chat_messages), time=3600)

    if request.method == 'POST':
        print("REQUEST SEND BY AJAX: ", request.body)
        data = json.loads(request.body)
        print("Data send from javascript: ", data)
        chatbot_name = data.get('chatbot_name')
        chatbot_description = data.get('chatbot_description')

        form = ClientUserChatForm(request.POST)
        if form.is_valid():
            # user message will be used for llm agents calls
            user_message = form.cleaned_data['content']
            chatbot_name = request.POST.get('chatbot_name')
            chatbot_description = request.POST.get('chatbot_description')

            # Check if required chatbot fields are missing
            if not chatbot_name or not chatbot_description:
                print("chatbot_name or chatbot_description missing.")
                messages.error(request, "AI personality 'Name' and 'Description' are mandatory.")
                return json({'error': 'Chatbot name and description are required.'})

            # Gather other chatbot fields
            chatbot_age = request.POST.get('chatbot_age', '')
            chatbot_origin = request.POST.get('chatbot_origin', '')
            chatbot_dream = request.POST.get('chatbot_dream', '')
            chatbot_tone = request.POST.get('chatbot_tone', '')
            chatbot_expertise = request.POST.get('chatbot_expertise', '')

            # Debugging information
            print("User message:", user_message)
            print(
              "Chatbot details:", 
                chatbot_name,
                chatbot_age,
                chatbot_origin,
                chatbot_dream,
                chatbot_tone,
                chatbot_description,
                chatbot_expertise
            )

            # Create and save user message
            chat_msg = ChatMessages.objects.create(
                user=user,
                sender_type='user',
                nickname=user.clientuser.nickname,
                content=user_message,
                timestamp=timezone.now()
            )

            # Update chat messages in cache
            chat_messages = list(chat_messages)
            chat_messages.append(chat_msg)
            mc.set(cache_key, chat_messages, time=36000)

            # Create a dummy response for now
            bot_response_content = f"Echo: {user_message}"
            bot_msg = ChatMessages.objects.create(
                user=user,
                sender_type='bot',
                nickname="ChatBot",
                content=bot_response_content,
                timestamp=timezone.now()
            )

            # Update cache with bot response
            chat_messages.append(bot_msg)
            mc.set(cache_key, chat_messages, time=36000)

            # Save bot message in the database
            bot_msg.save()

            # Return response to JavaScript
            return json({'bot_message': bot_response_content})

    # Render initial form
    form = ClientUserChatForm()

    # get any default chatbot settings
    business_data_first_document_title = BusinessUserData.objects.all().values_list('document_title', flat=True).order_by('-document_title').first()
    try: 
      chatbot_name = BusinessUserData.objects.filter(document_title=business_data_first_document_title).values_list('chat_bot__name')[0][0]
      if chatbot_name:
        default_chatbot = ChatBotSettings.objects.get(name=chatbot_name)
        print("default chatbot: ", default_chatbot)
      else:
        default_chatbot = ""
    except IndexError as e:
      print(f"Error while trying to get the chatbot name, probably no chatbot records: {e}")
      default_chatbot = ""

    context = {
        'form': form,
        'chat_messages': chat_messages,
        'user_avatar': user.clientuser.picture.url if user.clientuser.picture else '/images/clientuser_dummy_hachiko.png',
        'chatbot_avatar': '/images/chatbot_dummy.png',
        'business_data': BusinessUserData.objects.all(),
        'default_chatbot': default_chatbot,
    }

    return render(request, 'clientchat/clientuserchat.html', context)



