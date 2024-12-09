import os
import json
import requests
# import rust library her efor the moment but we might create a helper file with this inside or put it in common app so that all apps can call it from central point
import rust_lib
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User, Group
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.utils import timezone
from django.core.cache import cache  # Using Django's cache framework for simplicity
from django.urls import reverse
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
from agents.app_utils import ai_personality
from agents.graph import retrieval_agent_graph
from dotenv import load_dotenv


# load env vars
load_dotenv(dotenv_path='.env', override=False)
load_dotenv(dotenv_path=".vars.env", override=True)

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
        # get user_message and set env var
        user_message = data.get('message')
        # set user initial query
        set_key(".vars.env", "USER_INITIAL_QUERY", user_message)
        load_dotenv(dotenv_path=".vars.env", override=True)

        # we need also the document_title for future llm call (RAG retrieval)
        document_title_id = data.get('document_title_id')
        print("Document Title Id: ", document_title_id)
        # set env var for document title for Ai agent team to know what doc to retrieve from
        set_key(".vars.env", "DOCUMENT_TITLE", document_title)
        load_dotenv(dotenv_path=".vars.env", override=True)

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
        
        # make a function that is going to handle ai personality and use default values if field not field by client user of business user settings
        ai_traits_dict = {
          "chatbot_name": chatbot_name,
          "chatbot_description": chatbot_description,
          "chatbot_age": chatbot_age,
          "chatbot_origin": chatbot_origin,
          "chatbot_dream": chatbot_dream,
          "chatbot_tone": chatbot_tone,
          "chatbot_expertise": chatbot_expertise,
        }
        # here we will just set the environment variable personality trait of the ai with all fields filled
        # using default values if fields are not filled
        ai_personality_traits =  ai_personality.personality_trait_formatting(ai_traits_dict)
        # set environment variable that will have those trait stored for AI agent team
        set_key(".vars.env", "AI_PERSONALITY_TRAITS", ai_personality_traits)
        load_dotenv(dotenv_path=".vars.env", override=True)

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
        # we need to replace this with agent team by doing a call to the route url of agent app "retrieve-data"
        # /agents/retrieve-data
        # response coming from it is already json.dumped 
        # so we need to json.load to check if there is no error 
        # and json.dump it again to send to javascript frontend
        retriever_url = reverse("retrieve-data")
        retriever_response = requests.get(request.build_absolute_uri(retriever_url))
        if retriever_response.status_code == 200:
          # we can now load the json data to check for error and save to database if not. key for answer is: "answer"
          agent_retrieved_data_response_json = json.loads(retriever_response)
          # here we check if the Agent AI Team flow had an error
          for k,v in agent_retrieved_data_response_json.items():
            if "err" in k:
              error = agent_retrieved_data_response_json[k]
              # log the error specifying that it has been catch here in clientchat app views to Devops/Security team
              error_message = f"An error occured while running Retriever Agent Team: {error}"
              print(error_message)
              messages.error("The AI Team had some issues, please try later. We are doing our best to fix it.")
              return HttpResponse(json.dumps({"error": error_message}), content_type="applicatiion/json", status=500)
          else:
            # from here we can handle the response if partial response or if retrieved response above thresold
            # we keep it simple and just return answer partial or not but could do for k,v in .... and handle cases
            bot_response_content = agent_retrieved_data_response_json["answer"]
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
            return HttpResponse(json.dumps(response_json), content_type="applicatiion/json", status=200)
        else:
          # log also here for Devops/Security 
          error_message = f"An error occured while trying to get retrieved data from clientchat view: {retriever_response.status_code}"
          print(error_message)
          return HttpResponse(json.dumps({"error": error_message}), content_type="applicatiion/json", status=500)
        
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
        '''

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



