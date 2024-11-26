from django.forms import ModelForm
from .models import BusinessUserData
from django.contrib.auth.models import User
# as code would be duplicated the JSON validator has been moved to a class mixin in the mixins file
from .mixins import JSONFieldValidationMixin


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
