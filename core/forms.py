from django import forms
from django.forms import TextInput

from core.models import ManagerMessage


class BroadcastMessageForm(forms.ModelForm):
    class Meta:
        model = ManagerMessage
        fields = ('subject', 'text')

    def __init__(self, *args, **kwargs):
        super(BroadcastMessageForm, self).__init__(*args, **kwargs)
        self.fields['subject'].widget = TextInput(attrs={
            'class': 'form-control'
        })
        self.fields['text'].widget = TextInput(attrs={
            'class': 'form-control'
        })
