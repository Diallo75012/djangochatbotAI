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
@login_required(login_url='users:loginclientuser')
@user_passes_test(is_client_user, login_url='users:loginclientuser')
def clientUserChat(request):
    user = request.user
    cache_key = f"chat_{user.id}"

    # Fetch chat messages from cache or database
    chat_messages = cache.get(cache_key)
    if not chat_messages:
        chat_messages = ChatMessages.objects.filter(user=user).order_by('timestamp')
        cache.set(cache_key, list(chat_messages), 3600)

    if request.method == 'POST':
        data = json.loads(request.body)
        message_content = data.get('message')
        chatbot_id = data.get('chatbot_id')
        chatbot_name = data.get('chatbot_name')
        chatbot_age = data.get('chatbot_age')
        chatbot_origin = data.get('chatbot_origin')
        chatbot_dream = data.get('chatbot_dream')
        chatbot_tone = data.get('chatbot_tone')
        chatbot_description = data.get('chatbot_description')
        chatbot_expertise = data.get('chatbot_expertise')

        # Save user message
        chat_msg = ChatMessages.objects.create(
            user=user,
            sender_type='user',
            nickname=user.clientuser.nickname,
            content=message_content,
            timestamp=timezone.now()
        )

        # Update cache with user message
        chat_messages = list(chat_messages) if chat_messages else []
        chat_messages.append(chat_msg)
        cache.set(cache_key, chat_messages, 3600)

        # Create bot response (dummy response for now)
        bot_response_content = f"Echo: {message_content}"
        bot_msg = ChatMessages.objects.create(
            user=user,
            sender_type='bot',
            nickname="ChatBot",
            content=bot_response_content,
            timestamp=timezone.now()
        )

        # Update cache with bot response
        chat_messages.append(bot_msg)
        cache.set(cache_key, chat_messages, 3600)

        # Save bot message to the database
        bot_msg.save()

        return JsonResponse({
            'user_message': message_content,
            'bot_message': bot_response_content,
        })

    # Fetch the default chatbot from the selected document title
    document_titles = BusinessUserData.objects.filter(user=user).values_list('document_title', flat=True)
    print("DOCUMENT TITLES: ", document_titles)
    selected_document = request.GET.get('selected_document')
    default_chatbot = None

    if selected_document:
        business_data = BusinessUserData.objects.filter(user=user, document_title=selected_document).first()
        if business_data and business_data.chat_bot:
            default_chatbot = business_data.chat_bot

    context = {
        'form': ClientUserChatForm(),
        'chat_messages': chat_messages,
        'user_avatar': user.clientuser.picture.url if user.clientuser.picture else None,
        'chatbot_avatar': default_chatbot.avatar.url if default_chatbot and default_chatbot.avatar else '/images/chatbot_dummy.png',
        'default_chatbot': default_chatbot,
        'document_titles': document_titles,
        'selected_document': selected_document,
    }

    return render(request, 'clientchat/clientuserchat.html', context)

