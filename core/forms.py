import time
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
    num_of_waiters = forms.IntegerField()
    num_of_bartenders = forms.IntegerField()
    num_of_cooks = forms.IntegerField()

    OP_CHOICES = (
        ('', 'more/euqal/less than'),
        ('gte', '>'),
        ('lte', '<'),
        ('eq', '=')
    )

    employee_fields_dict = fields_for_model(EmployeeProfile, fields=EmployeeProfile.get_filtered_upon_fields())

    def __init__(self, *args, **kwargs):
        num_of_cook_constraints = kwargs.pop('num_of_cook_constraints', 0)
        num_of_bartender_constraints = kwargs.pop('num_of_bartender_constraints', 0)
        num_of_waiter_constraints = kwargs.pop('num_of_waiter_constraints', 1)
        super(ShiftSlotForm, self).__init__(*args, **kwargs)

        role_to_constraint_num = {'cook': num_of_cook_constraints, 'bartender': num_of_bartender_constraints,
                                  'waiter': num_of_waiter_constraints}

        fields_to_hide = []
        for role in role_to_constraint_num:
            for index in range(role_to_constraint_num[role]):
                str_index = str(index)
                self.fields['%s_constraint_%s_field' % (role, str_index)] = \
                    forms.ChoiceField(choices=[('', 'choose field to filter upon')] +
                                              [(choice, choice) for choice in EmployeeProfile.get_filtered_upon_fields()],
                                      required=False)
                for filtered_name, filtered_field in self.employee_fields_dict.iteritems():
                    new_val_field = '%s_constraint_%s_val_%s' % (role, str_index, filtered_name)
                    self.fields[new_val_field] = filtered_field
                    # self.fields[new_val_field].label = new_val_field
                    fields_to_hide.append(new_val_field)
                self.fields['%s_constraint_%s_op' % (role, str_index)] = forms.ChoiceField(choices=self.OP_CHOICES)
                self.fields['%s_constraint_%s_apply_on' % (role, str_index)] = forms.IntegerField(initial=1)
        for field in fields_to_hide:
            # pass
            self.fields[field].label = ''
            self.fields[field].widget = forms.HiddenInput()
        for k, v in self.fields.iteritems():
            v.widget.attrs.update({'class': 'form-control'})
            if 'num' in k:
                v.widget.attrs.update({'style': 'width: 450px; display: inline',
                                       'class': 'form-control attach-constraint'})

    def clean(self):
        clean_data = super(ShiftSlotForm, self).clean()



