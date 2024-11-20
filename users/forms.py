from django.forms import ModelForm
from .models import BusinessUserData
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
# as code would be duplicated the JSON validator has been moved to a class mixin in the mixins file
from .mixins import JSONFieldValidationMixin

# create user
class CreateUserForm(UserCreationForm):
  class Meta:
    model = User
    fields = ('username', 'email', 'password1', 'password2')

# update user
class UpdateUserForm(forms.ModelForm):
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


# BusinessUserData record form
class BusinessUserDataForm(ModelForm, JSONFieldValidationMixin):
  class Meta:
    model = BusinessUserData
    fields = ['document_title', 'question_answer_data'] 

# BusinessUserData Update data records
class BusinessUserDataUpdateForm(ModelForm, JSONFieldValidationMixin):
  class Meta:
    model = BusinessUserData
    # here need to list fields that need to be updated,
    #the user won't be updated it will be binded to the user logged in who have access to this data
    fields = ['document_title', 'question_answer_data']
