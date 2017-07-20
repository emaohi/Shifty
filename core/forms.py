import time

import datetime
from django import forms
from django.forms import TextInput

from core.models import ManagerMessage, ShiftSlot


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

    roles = ['waiter', 'bartender', 'cook']

    def __init__(self, *args, **kwargs):
        super(ShiftSlotForm, self).__init__(*args, **kwargs)

        field_to_vals = {'age': forms.IntegerField(required=False,
                                                   widget=forms.NumberInput(attrs={'placeholder': 'Age'})),
                         'months_working': forms.IntegerField(
                             required=False, widget=forms.NumberInput(attrs={'placeholder': 'Working months'})),
                         'gender': forms.ChoiceField(choices=self.GENDER_CHOICES, required=False),
                         'average_rate': forms.FloatField(min_value=0.0, required=False,
                                                          widget=forms.NumberInput(attrs={'placeholder': 'Average rate'}))}
        for role in self.roles:
            for field, val in field_to_vals.iteritems():
                self.fields[role + '_' + field + '__desc_constraint'] = \
                    forms.CharField(required=False, disabled=True, widget=forms.TextInput(attrs={'placeholder': (role + ' ' + field).replace('_', ' ').title()}))
                self.fields[role + '_' + field + '__operation_constraint'] =\
                    forms.ChoiceField(choices=self.OP_CHOICES, disabled=True if field is 'gender' else False, required=False)
                self.fields[role + '_' + field + '__value_constraint'] = val
                self.fields[role + '_' + field + '__applyOn_constraint'] =\
                    forms.IntegerField(min_value=0, widget=forms.NumberInput(attrs={'placeholder': 'Apply on'}), required=False)

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

        for role in self.roles:
            num_of_role = clean_data['num_of_' + role + 's']
            for clean_field in clean_data:
                if role in clean_field and 'apply' in clean_field:
                    if clean_data[clean_field] > num_of_role:
                        msg = 'you must not apply rule of %ss more than the num you declared they will be' % role
                        raise forms.ValidationError(msg)

        end_hour = clean_data['end_hour']
        start_hour = clean_data['start_hour']
        if end_hour < start_hour:
            msg = 'end hour (%s) is not later than start_hour (%s)' % (end_hour, start_hour)
            raise forms.ValidationError(msg)

        # TODO if value has added - apply_on mustn't be empty and vice versa
