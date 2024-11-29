from django.forms import ModelForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import ChatMessages, ClientUser


# create client user
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

# update business user
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


# client user chat form
class ClientUserChatForm(forms.ModelForm):
  class Meta:
    model = ChatMessages
    fields = ["nickname", "content"]
    labels = {
      "content": "Your Message",
      "image": "Atache an Image",
    }

# create client user
class CreateClientUserForm(UserCreationForm):
  # we set the field
  email = forms.EmailField(required=True)
  nickname = forms.CharField(max_length=40)
  bio = forms.CharField(max_length=255, required=False)

  class Meta:
    # we will use the User model and put what needed in  ClientUser Form
    model = User
    fields = ['nickname', 'email', 'password1', 'password2']

  def save(self, commit=True):
    user = super().save(commit=False)
    user.username = self.cleaned_data['nickname']
    user.email = self.cleaned_data['email']

    if commit:

      user.save()

      client_user = ClientUser.objects.create(
        user=user,
        nickname=self.cleaned_data['nickname'],
        email=self.cleaned_data['email'],
        bio=self.cleaned_data.get('bio', ''),
      )

      client_user.save()

    return user

# update client user
class UpdateClientUserForm(ModelForm):
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

