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
        fields = ('business_name', 'business_type', 'address', 'logo', 'tip_method', 'deadline_day')

    def __init__(self, *args, **kwargs):
        super(BusinessRegistrationForm, self).__init__(*args, **kwargs)
        for k, v in self.fields.iteritems():
            v.widget.attrs.update({'class': 'form-control'})
        self.fields['logo_url'] = forms.CharField(required=False, widget=forms.HiddenInput)


class BusinessEditForm(forms.ModelForm):
    class Meta:
        model = Business
        fields = ('address', 'business_type', 'tip_method', 'deadline_day', 'logo')
        help_texts = {
            'tip_method': 'Whether your employees get their tips personally or share group tips',
            'deadline_day': 'The day until which shift requests must be submitted by your employees',
            'logo': 'Edit logo'
        }

    def __init__(self, *args, **kwargs):
        super(BusinessEditForm, self).__init__(*args, **kwargs)
        for _, field in self.fields.iteritems():
            field.widget.attrs.update({'class': 'form-control'})


class ManagerSignUpForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(ManagerSignUpForm, self).__init__(*args, **kwargs)

        for fieldname in ['username', 'password1', 'password2']:
            self.fields[fieldname].help_text = None
        for _, v in self.fields.iteritems():
            v.widget.attrs.update({'class': 'form-control'})

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


class DateInput(forms.DateInput):
    input_type = 'date'


class EditProfileForm(forms.ModelForm):

    class Meta:
        model = EmployeeProfile
        fields = ['user', 'started_work_date', 'role', 'phone_num', 'birth_date', 'home_address', 'arriving_method',
                  'rate', 'enable_mailing']
        widgets = {
            'started_work_date': DateInput(),
            'birth_date': DateInput(),
        }
        help_texts = {
            'phone_num': 'in form of 05x-xxxxxxx',
            'enable_mailing': 'It is recommended to enable mailing from Shifty',
            'home_address': 'Exact address will enable checking ETA to work',
            'arriving_method': 'Show you ETA and notification for your next shift'
        }

    def __init__(self, *args, **kwargs):
        requester_is_manager = kwargs.pop('is_manager', None)
        super(EditProfileForm, self).__init__(*args, **kwargs)
        subject_is_manager = self.instance.user.groups.filter(name='Managers').exists()
        fields_to_delete = ()
        fields_to_disable = ()

        if not requester_is_manager and not subject_is_manager:
            fields_to_delete = ('rate', )
            fields_to_disable = ('started_work_date', 'role')
        if requester_is_manager and subject_is_manager:
            fields_to_delete = ('rate', 'role')

        for field in fields_to_delete:
            del self.fields[field]
        for field in fields_to_disable:
            self.fields[field].disabled = True

        self.fields['user'].widget = forms.HiddenInput()
        self.fields['user'].label = ''
        for k, v in self.fields.iteritems():
            if k is not 'enable_mailing':
                v.widget.attrs.update({'class': 'form-control', 'style': 'width: 450px; display: inline'})
            else:
                v.widget.attrs.update({'style': 'display: inline'})

