import time

import datetime
from django import forms
from django.forms import TextInput
from django.forms.models import fields_for_model

from core.models import ManagerMessage, ShiftSlot
from log.models import EmployeeProfile


class BroadcastMessageForm(forms.ModelForm):
    class Meta:
        model = ManagerMessage
        fields = ('subject', 'text')

    def __init__(self, *args, **kwargs):
        super(BroadcastMessageForm, self).__init__(*args, **kwargs)
        for _, v in self.fields.iteritems():
            v.widget = TextInput(attrs={'class': 'form-control'})


class ShiftSlotForm(forms.Form):
    day = forms.ChoiceField(choices=ShiftSlot.DAYS_OF_WEEK)
    start_hour = forms.TimeField(widget=forms.DateInput(attrs={'type': 'time'}))
    end_hour = forms.TimeField(widget=forms.DateInput(attrs={'type': 'time'}))

    # constraints
    num_of_waiters = forms.IntegerField(initial=1)
    num_of_bartenders = forms.IntegerField(initial=1)
    num_of_cooks = forms.IntegerField(initial=1)

    OP_CHOICES = (
        ('', 'more/equal/less than'),
        ('gte', '>'),
        ('lte', '<'),
        ('eq', '=')
    )
    GENDER_CHOICES = (
        ('', 'Gender'),
        ('M', 'Male'),
        ('F', 'Female'),
    )

    def __init__(self, *args, **kwargs):

        super(ShiftSlotForm, self).__init__(*args, **kwargs)

        roles = ['waiter', 'bartender', 'cook']
        field_to_vals = {'age': forms.IntegerField(required=False,
                                                   widget=forms.NumberInput(attrs={'placeholder': 'Age'})),
                         'months_working': forms.IntegerField(
                             required=False, widget=forms.NumberInput(attrs={'placeholder': 'Working months'})),
                         'gender': forms.ChoiceField(choices=self.GENDER_CHOICES, required=False, initial=''),
                         'average_rate': forms.FloatField(min_value=0.0,
                                                          widget=forms.NumberInput(attrs={'placeholder': 'Average rate'}))}
        for role in roles:
            for field, val in field_to_vals.iteritems():
                self.fields[role + '_' + field + '__desc_constraint'] = \
                    forms.CharField(required=False, disabled=True,
                                    widget=forms.TextInput(
                                        attrs={'placeholder': (role + ' ' + field).replace('_', ' ').title()}))
                self.fields[role + '_' + field + '__operation_constraint'] =\
                    forms.ChoiceField(choices=self.OP_CHOICES, disabled=True if field is 'gender' else False,
                                      required=False, initial='eq' if field is 'gender' else '')
                self.fields[role + '_' + field + '__value_constraint'] = val
                self.fields[role + '_' + field + '__applyOn_constraint'] =\
                    forms.IntegerField(min_value=0,
                                       widget=forms.NumberInput(attrs={'placeholder': 'Apply on'}), required=False)

        for name, field in self.fields.iteritems():
            field.widget.attrs.update({'class': 'form-control', 'form': 'theForm'})
            if 'num' in name:
                field.widget.attrs.update({'style': 'width: 450px; display: inline',
                                           'class': 'form-control attach-con'})
        self.field_order = sorted(self.fields)

    def get_constraint_groups(self):
        return self.remove_duplicates([f.split('__')[0] for f in self.fields if '__' in f])

    @staticmethod
    def remove_duplicates(seq):
        seen = set()
        seen_add = seen.add
        return [x for x in seq if not (x in seen or seen_add(x))]

    def clean(self):
        clean_data = super(ShiftSlotForm, self).clean()



        # TODO if value has added - apply_on&op mustn't be empty and vice versa
        # TODO also it's possible to check emp values to identify bigger than max / smaller than min cases
