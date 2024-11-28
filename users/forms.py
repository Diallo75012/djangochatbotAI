from django.forms import ModelForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import ChatMessage


# create user
class CreateBusinessUserForm(UserCreationForm):
  business_group = forms.CharField(
    initial='business',
    disabled=True,
    # Use HiddenInput if you don't want to show the group field
    widget=forms.HiddenInput()
  )
  class Meta:
    model = User
    fields = ('username', 'email', 'password1', 'password2')

# update user
class UpdateBusinessUserForm(ModelForm):
    """
    Form to update user's information like username, email, and first/last name.
    """
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}),
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError('A user with this email already exists.')
        return email


class ClientUserChatForm(forms.ModelForm):
  class Meta:
    model = ChatMessage
    fields = ["content", "image"]
    labels = {
      "content": "Your Message",
      "image": "Atache an Image",
    }



