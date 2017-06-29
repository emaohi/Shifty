from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django import forms
from django.contrib.auth.models import User

from log.models import Business, EmployeeProfile


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

    def __init__(self, *args, **kwargs):
        super(BusinessEditForm, self).__init__(*args, **kwargs)
        self.fields['business_type'].widget.attrs \
            .update({
            'class': 'form-control'
        })
        self.fields['tip_method'].widget.attrs \
            .update({
            'class': 'form-control'
        })


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
            self.fields['employee_{index}_firstName'.format(index=index)] = \
                forms.CharField()
            self.fields['employee_{index}_lastName'.format(index=index)] = \
                forms.CharField()
            self.fields['employee_{index}_email'.format(index=index)] = \
                forms.EmailField()
            self.fields['employee_{index}_role'.format(index=index)] = \
                forms.ChoiceField(choices=(('WA', 'waiter'), ('BT', 'bartender'), ('CO', 'cook')))
            self.fields['employee_{index}_dateJoined'.format(index=index)] = \
                forms.DateField()


class EditProfileForm(forms.ModelForm):

    class Meta:
        model = EmployeeProfile
        fields = ['user', 'started_work_date', 'role', 'phone_num', 'birth_date', 'home_address',
                  'avg_rate', 'enable_mailing']

    def __init__(self, *args, **kwargs):
        is_manager = kwargs.pop('is_manager', None)
        super(EditProfileForm, self).__init__(*args, **kwargs)
        fields_to_delete = ()
        fields_to_disable = ()
        if not is_manager:
            fields_to_delete = ('avg_rate', )
            fields_to_disable = ('role', 'started_work_date')
        for field in fields_to_delete:
            del self.fields[field]
        for field in fields_to_disable:
            self.fields[field].disabled = True
        self.fields['user'].widget = forms.HiddenInput()
        self.fields['user'].label = ''
        for k, v in self.fields.iteritems():
            if k is not 'enable_mailing':
                v.widget.attrs.update({'class': 'form-control', 'style': 'width: 450px'})
            else:
                v.widget.attrs.update({'style': 'display: inline'})

