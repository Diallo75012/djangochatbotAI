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
from businessdata.models import BusinessUserData
from users.models import ClientUser
from .models import ChatMessages
import memcache
# just for returning test when debugging other route redirects
#from django.http import HttpResponse


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
        form = ClientUserChatForm(request.POST)
        if form.is_valid():
            user_message = form.cleaned_data['content']
            chatbot_name = request.POST.get('chatbot_name')
            chatbot_age = request.POST.get('chatbot_age')
            chatbot_origin = request.POST.get('chatbot_origin')
            chatbot_dream = request.POST.get('chatbot_dream')
            chatbot_tone = request.POST.get('chatbot_tone')
            chatbot_description = request.POST.get('chatbot_description')
            chatbot_expertise = request.POST.get('chatbot_expertise')

            # Debugging information
            print("User message:", user_message)
            print("Chatbot details:", chatbot_name, chatbot_age, chatbot_origin, chatbot_dream, chatbot_tone, chatbot_description, chatbot_expertise)

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
            return JsonResponse({
                'user_message': user_message,
                'bot_message': bot_response_content
            })

    # Render initial form
    form = ClientUserChatForm()
    context = {
        'form': form,
        'chat_messages': chat_messages,
        'user_avatar': user.clientuser.picture.url if user.clientuser.picture else None,
        'chatbot_avatar': '/images/chatbot_dummy.png',
        'document_titles': BusinessUserData.objects.all().values_list('document_title', flat=True),
        'default_chatbot': None,  # Placeholder for initial render
    }

    return render(request, 'clientchat/clientuserchat.html', context)


