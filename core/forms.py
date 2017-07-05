from django import forms
from django.forms import TextInput

from core.models import ManagerMessage


class BroadcastMessageForm(forms.ModelForm):
    class Meta:
        model = ManagerMessage
        fields = ('subject', 'text')

    def __init__(self, *args, **kwargs):
        super(BroadcastMessageForm, self).__init__(*args, **kwargs)
        for _, v in self.fields.iteritems():
            v.widget = TextInput(attrs={'class': 'form-control'})
