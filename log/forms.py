from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django import forms
from django.contrib.auth.models import User

from log.models import Business


class LoginForm(AuthenticationForm):
    username = forms.CharField(label="Username", max_length=30,
                               widget=forms.TextInput(attrs={'class': 'form-control', 'name': 'username'}))
    password = forms.CharField(label="Password", max_length=30,
                               widget=forms.PasswordInput(attrs={'class': 'form-control', 'name': 'password'}))


class BusinessRegistrationForm(forms.ModelForm):
    class Meta:
        model = Business
        fields = ('business_name', 'business_type', 'tip_method')


class BusinessEditForm(forms.ModelForm):
    class Meta:
        model = Business
        fields = ('business_type', 'tip_method')


class ManagerSignUpForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)

        for fieldname in ['username', 'password1', 'password2']:
            self.fields[fieldname].help_text = None

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'email')


class AddEmployeesForm(forms.Form):

    def __init__(self, *args, **kwargs):
        extra_fields = kwargs.pop('extra', 0)

        super(AddEmployeesForm, self).__init__(*args, **kwargs)

        for index in range(int(extra_fields)):
            # generate extra fields in the number specified via extra_fields
            self.fields['employee_{index}_first_name'.format(index=index)] = \
                forms.CharField()
            self.fields['employee_{index}_last_name'.format(index=index)] = \
                forms.CharField()
            self.fields['employee_{index}_email'.format(index=index)] = \
                forms.EmailField()
