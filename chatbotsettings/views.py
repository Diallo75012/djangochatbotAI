from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.contrib import messages
from .models import ChatBotSettings
from .forms import (
  ChatBotSettingsForm,
  ChatBotSettingsUpdateForm
)
from businessdata.models import BusinessUserData


def is_business_user(user):
  return user.groups.filter(name='business').exists()


@login_required(login_url='users:loginbusinessuser')
@user_passes_test(is_business_user, login_url='users:loginbusinessuser')
def ChatBotSettingsManagement(request):
  # we fetch all and then will fetch only what we need after having seen how it looks like in webui
  # adding `.values("<model field>", "<other model field>")`
  data = ChatBotSettings.objects.filter(business_user=request.user)
  context = {"data": data}
  return render(request, 'chatbotsettings/chatbotsettingsmanagement.html', context)

# add chatbot settings
@login_required(login_url='users:loginbusinessuser')
@user_passes_test(is_business_user, login_url='users:loginbusinessuser')
def addChatBotSettings(request):
  '''
    Handle adding chatbot settings.
  '''

  form = ChatBotSettingsForm()
  if request.method == 'POST':
    form = ChatBotSettingsForm(request.POST, request.FILES)
    if form.is_valid():
      chatbotsettings_data = form.save(commit=False)
      chatbotsettings_data.business_user = request.user

      # Check if the avatar already exists for this user
      avatar = request.FILES.get('avatar')
      if avatar:
        try:
          # Check if an existing ChatBotSettings has the same avatar for the same user
          existing_avatar = ChatBotSettings.objects.get(
            business_user=request.user,
            avatar__contains=avatar.name
          )
          messages.error(
            request,
            "This image has already been used. Please upload a different one."
          )
          return redirect("chatbotsettings:addchatbotsettings")
        except ChatBotSettings.DoesNotExist:
          # No duplicate avatar exists, continue to save
          print("Image double name doesn't exist")
          pass

      # Set the business_user_uuid using the user's related BusinessUserData uuid
      try:
        business_user_data = BusinessUserData.objects.get(user=request.user)
        chatbotsettings_data.business_user_uuid = business_user_data
      except Exception as e:
        message.error(
          request,
          "Before creating any ChatBot Setting, you need to have uploaded Business Data"
        )
        return redirect("businessdata:addbusinessdata")

      chatbotsettings_data.save()
      messages.success(
        request,
        "ChatBot settings added successfully!"
      )
      return redirect("chatbotsettings:addchatbotsettings")
    else:
      messages.error(
        request,
        "Form submission incorrect. Please enter correct information."
      )
  context = {'form': form}
  return render(request, 'chatbotsettings/addchatbotsettings.html', context)

# update chatbotsettings
@login_required(login_url='users:loginbusinessuser')
@user_passes_test(is_business_user, login_url='users:loginbusinessuser')
def updateChatBotSettings(request, pk):
  chatbot_settings_to_update = get_object_or_404(ChatBotSettings, pk=pk, business_user=request.user)
  form = ChatBotSettingsUpdateForm(instance=chatbot_settings_to_update)

  if request.method == 'POST':
    form = ChatBotSettingsUpdateForm(request.POST, request.FILES, instance=chatbot_settings_to_update)
    if form.is_valid():
      # Check if the avatar already exists for this user
      avatar = request.FILES.get('avatar')
      if avatar:
        try:
          # Check if an existing ChatBotSettings has the same avatar for the same user
          existing_avatar = ChatBotSettings.objects.get(
            business_user=request.user,
            avatar__contains=avatar.name
          )
          messages.error(
            request,
            "This image has already been used. Please upload a different one."
          )
          return redirect("chatbotsettings:addchatbotsettings")
        except ChatBotSettings.DoesNotExist:
          # No duplicate avatar exists, continue to save
          pass

      form.save()
      messages.success(
        request,
        "ChatBot has been updated successfully."
      )
      return redirect("chatbotsettings:chatbotsettingsmanagement")
    else:
      messages.error(
        request,
        "Form submission incorrect. Please enter correct information."
      )
  context = {'form': form}
  return render(request, "chatbotsettings/updatechatbotsettings.html", context)


# delete chatbot settings
@login_required(login_url="users:loginbusinessuser")
@user_passes_test(is_business_user, login_url='users:loginbusinessuser')
def deleteChatBotSettings(request, pk):
  chatbot_settings_to_delete = get_object_or_404(ChatBotSettings, id=pk, business_user=request.user)
  if request.method == "POST":
    chatbot_settings_to_delete.delete()
    messages.success(
      request,
      "ChatBot settings has been successfully deleted."
    )
    return redirect("chatbotsettings:chatbotsettingsmanagement")
