import logging
from django import forms
from django.forms import TextInput

from core.date_utils import get_birth_day_from_age, get_started_month_from_month_amount, get_next_week_num
from core.models import ManagerMessage, ShiftSlot, ShiftRequest
from core.utils import get_cached_non_mandatory_slots
from log.models import EmployeeProfile

logger = logging.getLogger('cool')


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
    start_hour = forms.TimeField(widget=forms.DateInput(attrs={'type': 'time'}), initial='06:00')
    end_hour = forms.TimeField(widget=forms.DateInput(attrs={'type': 'time'}), initial='23:59')

    name = forms.ChoiceField(choices=('', 'Choose name'), required=False)

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

    # slot_name = None
    # business = None

    mandatory = forms.BooleanField(initial=False, help_text='Is this slot mandatory for your employees', required=False)
    save_as = forms.CharField(required=False, help_text=' Optional: save this slot with name')

    def __init__(self, *args, **kwargs):

        self.business = kwargs.pop('business')
        self.slot_names = kwargs.pop('names', (()))

        super(ShiftSlotForm, self).__init__(*args, **kwargs)

        self.fields["name"].choices = self.slot_names
        self.fields["name"].choices.append(('', '---'))
        self.fields["name"].initial = ''

        field_to_vals = {'age': forms.IntegerField(required=False,
                                                   widget=forms.NumberInput(attrs={'placeholder': 'Age'})),
                         'months_working': forms.IntegerField(
                             required=False, widget=forms.NumberInput(attrs={'placeholder': 'Working months'})),
                         'gender': forms.ChoiceField(choices=self.GENDER_CHOICES, required=False, initial=''),
                         'average_rate': forms.FloatField(min_value=0.0, required=False,
                                                          widget=forms.NumberInput(
                                                              attrs={'placeholder': 'Average rate'}))}
        for role in self.roles:
            for field, val in field_to_vals.iteritems():
                self.fields[role + '_' + field + '__desc_constraint'] = \
                    forms.CharField(required=False, disabled=True,
                                    widget=forms.TextInput(
                                        attrs={'placeholder': (role + ' ' + field).replace('_', ' ').title()}))
                self.fields[role + '_' + field + '__operation_constraint'] = \
                    forms.ChoiceField(choices=self.OP_CHOICES, disabled=True if field is 'gender' else False,
                                      required=False, initial='eq' if field is 'gender' else '')
                self.fields[role + '_' + field + '__value_constraint'] = val
                self.fields[role + '_' + field + '__applyOn_constraint'] = \
                    forms.IntegerField(min_value=0,
                                       widget=forms.NumberInput(attrs={'placeholder': 'Apply on'}), required=False)

        for name, field in self.fields.iteritems():
            field.widget.attrs.update({'class': 'form-control', 'form': 'theForm'})
            if 'num' in name:
                field.widget.attrs.update({'style': 'width: 450px; display: inline',
                                           'class': 'form-control attach-con'})
            if 'mandatory' in name:
                field.widget.attrs.update({'style': 'width: 50px; display: inline'})
        self.field_order = sorted(self.fields)

    def clean(self):
        clean_data = super(ShiftSlotForm, self).clean()

        self.validate_enough_of_role(clean_data)
        self.validate_apply_less_than_role_num(clean_data)
        self.validate_end_after_start(clean_data)
        self.validate_no_partial_empty_constraints(clean_data)
        self.validate_constraints_can_be_fulfilled(clean_data)
        self.validate_slot_not_overlaping(clean_data)

    def validate_enough_of_role(self, clean_data):
        for role in self.roles:
            role_reverse = dict((v, k) for k, v in EmployeeProfile.ROLE_CHOICES)
            requested_num_of_role = int(clean_data['num_of_' + role + 's'])
            real_num_of_role = EmployeeProfile.objects.filter(business=self.business,
                                                              role=role_reverse[role.title()]).count()

            if requested_num_of_role > real_num_of_role:
                msg = 'you cant request %s %ss, there are only %s' % (requested_num_of_role, role,
                                                                      real_num_of_role)
                logger.error(msg)
                raise forms.ValidationError(msg)

    def validate_no_partial_empty_constraints(self, clean_data):
        for group in self.get_constraint_groups():
            group_list = [val for key, val in clean_data.iteritems() if group in key and 'desc' not in key and
                          'gender__operation' not in key]
            if not self.validate_all_none_or_not_none(group_list):
                msg = 'you cannot leave parts of %s constraint empty' % group
                logger.error(msg)
                raise forms.ValidationError(msg)

    def get_constraint_groups(self):
        return self.remove_duplicates([f.split('__')[0] for f in self.fields if '__' in f])

    def validate_apply_less_than_role_num(self, clean_data):
        for role in self.roles:
            num_of_role = clean_data['num_of_' + role + 's']
            for clean_field in clean_data:
                if role in clean_field and 'apply' in clean_field:
                    if clean_data[clean_field] > num_of_role:
                        msg = 'you must not apply rule of %ss more than the num you declared they will be' % role
                        logger.error(msg)
                        raise forms.ValidationError(msg)

    def validate_constraints_can_be_fulfilled(self, clean_data):
        for group in self.get_constraint_groups():
            role = group.split('_')[0]
            field = group.split('_')[1]
            operation = clean_data[group + '__operation_constraint']
            value = clean_data[group + '__value_constraint']
            apply_on = clean_data[group + '__applyOn_constraint']
            if not self.validate_constraint_group(role, field, operation, value, apply_on):
                msg = 'There are not %s or more %ss whose %s are %s than/to %s' % \
                      (apply_on, role, field, operation, value)
                logger.error(msg)
                raise forms.ValidationError(msg)

    def validate_constraint_group(self, role, field, operation, value, apply_on):
        if not value:
            return True
        if field == 'age':
            field = 'birth_date'
            try:
                value = get_birth_day_from_age(int(value))
            except OverflowError as e:
                msg = 'age is not valid: ' + e.message
                logger.error(msg)
                raise forms.ValidationError(msg)
            operation = self.swap_op(operation)
        if field == 'months':
            field = 'started_work_date'
            value = get_started_month_from_month_amount(int(value))
            operation = self.swap_op(operation)
        if operation == 'eq':
            operation = 'exact'
        lookup = '%s__%s' % (field, operation)
        role_reverse = dict((v, k) for k, v in EmployeeProfile.ROLE_CHOICES)
        filtered_emps = EmployeeProfile.objects \
            .filter(**{'business__business_name': self.business.business_name, 'role': role_reverse[role.title()],
                       lookup: value})
        return len(filtered_emps) >= apply_on

    @staticmethod
    def validate_slot_not_overlaping(clean_data):
        next_week_slots = ShiftSlot.objects.filter(week=get_next_week_num(), day=clean_data['day']) \
            .order_by('start_hour')
        if not next_week_slots:
            return
        ordered_start_time = next_week_slots.order_by('start_hour')
        ordered_end_time = next_week_slots.order_by('end_hour')
        if list(ordered_start_time) != list(ordered_end_time):
            raise forms.ValidationError('weird error: slot not ok even before your slot :( check them')

        sorted_start_times = [slot.start_hour for slot in ordered_start_time]
        sorted_end_times = [slot.end_hour for slot in ordered_end_time]
        if clean_data['start_hour'] in sorted_start_times or clean_data['end_hour'] in sorted_end_times:
            raise forms.ValidationError('slot overlap')

        sorted_start_times.append(clean_data['start_hour'])
        sorted_start_times.sort()
        sorted_end_times.append(clean_data['end_hour'])
        sorted_end_times.sort()

        curr_start_index = sorted_start_times.index(clean_data['start_hour'])
        curr_end_index = sorted_end_times.index(clean_data['end_hour'])
        if curr_start_index != curr_end_index:
            raise forms.ValidationError('slot overlap')

        curr_index = curr_start_index
        if (curr_index != 0 and sorted_start_times[curr_index] < sorted_end_times[curr_index - 1]) \
                or (curr_index != len(sorted_start_times) - 1 and
                            sorted_end_times[curr_index] > sorted_start_times[curr_index + 1]):
            raise forms.ValidationError('slot overlap')

    @staticmethod
    def swap_op(op):
        if op == 'lte':
            return 'gte'
        elif op == 'gte':
            return 'lte'
        return op

    @staticmethod
    def extract_constraint_parts(constraint_data):
        constraint_splitted = constraint_data.split('__')
        role_and_field = constraint_splitted[0]
        part = constraint_splitted[1].split('_')[0]
        role = role_and_field.split('_')[0]
        field = role_and_field.split('_')[1]
        return role, field, part

    @staticmethod
    def validate_end_after_start(clean_data):
        end_hour = clean_data['end_hour']
        start_hour = clean_data['start_hour']
        if end_hour < start_hour:
            msg = 'end hour (%s) is not later than start_hour (%s)' % (end_hour, start_hour)
            raise forms.ValidationError(msg)

    @staticmethod
    def validate_all_none_or_not_none(elements):

        none_list = [None, '']
        return all([(elem in none_list) for elem in elements]) or \
               all([(elem not in none_list) for elem in elements])

    @staticmethod
    def remove_duplicates(seq):
        seen = set()
        seen_add = seen.add
        return [x for x in seq if not (x in seen or seen_add(x))]


class SelectSlotsForm(forms.ModelForm):
    class Meta:
        model = ShiftRequest
        exclude = ('employee', 'submission_time')

    def __init__(self, *args, **kwargs):
        self.business = kwargs.pop('business')
        week = kwargs.pop('week')
        super(SelectSlotsForm, self).__init__(*args, **kwargs)
        self.fields['requested_slots'].queryset = get_cached_non_mandatory_slots(self.business, week)
        logger.info("query set is %s", self.fields['requested_slots'].queryset)
        self.fields['requested_slots'].widget.attrs['class'] = 'selectpicker'

    def clean(self):
        super(SelectSlotsForm, self).clean()

        if not self.business.slot_request_enabled:
            raise forms.ValidationError('Slots request is currently unavailable')
