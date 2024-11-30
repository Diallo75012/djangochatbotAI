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
@login_required(login_url='users:loginclientuser')
@user_passes_test(is_client_user, login_url='users:loginclientuser')
def clientUserChat(request):
    """
    View to handle client user chat, fetch document titles, chatbot details, etc.
    """
    user = request.user
    cache_key = f"chat_{user.id}"

    # Fetch chat messages from cache or database
    chat_messages = mc.get(cache_key)
    if not chat_messages:
        chat_messages = ChatMessages.objects.filter(user=user).order_by('timestamp')
        mc.set(cache_key, list(chat_messages), time=3600)

    # Fetch all document titles available from the database
    document_titles = BusinessUserData.objects.values_list('document_title', flat=True).distinct().order_by('document_title')
    
    # Select the first document title alphabetically if none is selected by the client user
    selected_document = request.GET.get('selected_document', document_titles.first() if document_titles else None)
    default_chatbot = None
    business_user = None

    if selected_document:
        # Fetch the business data associated with the selected document title
        business_data = BusinessUserData.objects.filter(document_title=selected_document).first()
        if business_data:
            # Get the business user from business data
            business_user = business_data.user

            # Get the default chatbot if it exists for the selected document title
            if business_data.chat_bot:
                default_chatbot = business_data.chat_bot

    if request.method == 'POST':
        form = ClientUserChatForm(request.POST)
        if form.is_valid():
            # Save user message
            user_message = form.cleaned_data['message']
            chat_msg = ChatMessages.objects.create(
                user=user,
                sender_type='user',
                nickname=user.clientuser.nickname,
                content=user_message,
                timestamp=timezone.now()
            )

            # Save in database and update cache
            chat_messages = list(chat_messages)
            chat_messages.append(chat_msg)
            mc.set(cache_key, chat_messages, time=3600)

            # Dummy chat response until we plug in LLM agents
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
            mc.set(cache_key, chat_messages, time=3600)

            # Save bot message in the database as well
            bot_msg.save()

            # Reload page to show new messages
            return redirect('clientchat:clientuserchat')
    else:
        form = ClientUserChatForm()

    # Now, let's pass all that to the WebUI context
    context = {
        'form': form,
        'chat_messages': chat_messages,
        'user_avatar': user.clientuser.picture.url if user.clientuser.picture else None,
        'chatbot_avatar': '/images/chatbot_dummy.png',
        'document_titles': document_titles,
        'selected_document': selected_document,
        'default_chatbot': default_chatbot,
        'business_user': business_user,
    }

    return render(request, 'clientchat/clientuserchat.html', context)

