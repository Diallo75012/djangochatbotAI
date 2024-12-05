import os
import json
# import rust library her efor the moment but we might create a helper file with this inside or put it in common app so that all apps can call it from central point
import rust_lib
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
from dotenv import load_dotenv


load_dotenv()

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

        # extract chatbot information
        chatbot_name = data.get('chatbot_name')
        chatbot_description = data.get('chatbot_description')
        user_message = data.get('message')
        # we need also the document_title for future llm call (RAG retrieval)
        document_title_id = data.get('document_title_id')
        print("Document Title Id: ", document_title_id)

        # Check if required chatbot fields are missing
        if not chatbot_name or not chatbot_description:
          print("chatbot_name or chatbot_description missing.")
          messages.error(request, "AI personality 'Name' and 'Description' are mandatory.")
          return json({'error': 'Chatbot name and description are required.'})

        # Gather other chatbot fields
        chatbot_age = data.get('chatbot_age', '')
        chatbot_origin = data.get('chatbot_origin', '')
        chatbot_dream = data.get('chatbot_dream', '')
        chatbot_tone = data.get('chatbot_tone', '')
        chatbot_expertise = data.get('chatbot_expertise', '')

        # Create and save user message
        user_chat_msg = ChatMessages.objects.create(
          user=user,
          sender_type='user',
          nickname=user.clientuser.nickname,
          content=user_message,
          timestamp=timezone.now()
        )

        # Update chat messages in cache
        chat_messages = list(chat_messages)
        chat_messages.append(user_chat_msg)
        mc.set(cache_key, chat_messages, time=36000)

        # Create a dummy response for now
        # so here instead of dummy answer we will implement Rust LLM Call library
        '''
          - use all variables above to fill in a prompt. so we will need a `prompts.py` module on the side
          - call LLMs like (boilerplate):
           response = rust_lib.call_llm_api(
             api_url=API_URL, # we will use env vars
             api_key=API_KEY,
             paylaod=<our prompts variable loaded with all necesary vars or default if those vars are empty>
           )
          - use the `response` to send it back to the webui
          We will start small like that with a simple API call
          before introducing the llm agents from a side module imported here
        '''
        response = rust_lib.call_llm_api(
          api_url = os.getenv("GROQ_API_URL"),
          api_key = os.getenv("GROQ_API_KEY"),
          message_content = user_message,
          model = "mixtral-8x7b-32768",
        )
        # let replace the dummy message with the Rust fowarded API call response to test
        bot_response_content = response #f"AI dummy response form backend: Yo! looks like we are connected now!"
        print("Bot Response Content: ", bot_response_content)
        bot_chat_msg = ChatMessages.objects.create(
          user=user,
          sender_type='bot',
          nickname="ChatBot",
          content=bot_response_content,
          timestamp=timezone.now()
        )

        # Update cache with bot response
        chat_messages.append(bot_chat_msg)
        mc.set(cache_key, chat_messages, time=36000)

        # Save bot/user message in the database
        bot_chat_msg.save()
        user_chat_msg

        # format the response
        response_data = {
          'bot_message': bot_response_content,
        }
        response_json = json.dumps(response_data)

        # Return response to JavaScript using HttpResponse 
        # and not JsonResponse which will destroy the webui and just show the message
        # we just want a nice message sent to the javascript frontend handler
        return HttpResponse(response_json, content_type='application/json')


    # get a default chatbot settings (first in desc order)
    business_data_first_document_title = BusinessUserData.objects.all().values_list(
      'document_title', flat=True
      ).order_by(
        # `-` to have it in desc order
        '-document_title'
      ).first()
    
    # setup defaut_chatbot for webui sidebar if any
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

    # get default avatar if nothing set
    user_default_avatar = user.clientuser.picture.url if user.clientuser.picture else '/images/clientuser_dummy_hachiko.png'
    chatbot_default_avatar = default_chatbot.avatar.url if default_chatbot.avatar else '/images/chatbot_dummy.png'
    # get business data to use jinja fields
    business_data = BusinessUserData.objects.all()

    context = {
        'chat_messages': chat_messages,
        'user_avatar': user_default_avatar,
        'chatbot_avatar': chatbot_default_avatar,
        'business_data': business_data,
        'default_chatbot': default_chatbot,
    }

    return render(request, 'clientchat/clientuserchat.html', context)



