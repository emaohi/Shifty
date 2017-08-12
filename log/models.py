from __future__ import unicode_literals, division

from datetime import datetime

from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Business(models.Model):
    business_name = models.CharField(primary_key=True, max_length=30)

    manager = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    BUSINESS_TYPE_CHOICES = (
        ('RE', 'Restaurant'), ('CA', 'Cafe'), ('PU', 'Pub')
    )
    business_type = models.CharField(
        max_length=2,
        choices=BUSINESS_TYPE_CHOICES,
        default='CA',
    )

    TIP_METHOD_CHOICES = (
        ('P', 'Personal'), ('G', 'Group')
    )

    tip_method = models.CharField(max_length=1, choices=TIP_METHOD_CHOICES, default='G')

    DAYS_OF_WEEK = (
        ('1', 'Sunday'),
        ('2', 'Monday'),
        ('3', 'Tuesday'),
        ('4', 'Wednesday'),
        ('5', 'Thursday'),
        ('6', 'Friday'),
        ('7', 'Saturday'),
    )
    deadline_day = models.CharField(max_length=1, choices=DAYS_OF_WEEK, default='7')

    def __str__(self):
        return self.business_name

    def get_type(self):
        return self.get_business_type_display()

    def get_employees(self):
        return self.employeeprofile_set.all()


# noinspection PyTypeChecker
class EmployeeProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    business = models.ForeignKey(Business, on_delete=models.CASCADE)
    phone_regex = RegexValidator(regex=r'^05\d{1}-\d{7}$',
                                 message="Wrong phone number format.")
    phone_num = models.CharField(validators=[phone_regex], blank=True, max_length=16)  # validators should be a list
    # phone_num = models.CharField(max_length=30, blank=True)
    home_address = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    started_work_date = models.DateField(null=True, blank=True)

    GENDER_CHOICES = (
        ('M', 'Male'), ('F', 'Female')
    )
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default='M')

    ROLE_CHOICES = (
        ('MA', 'Manager'), ('WA', 'Waiter'), ('BT', 'Bartender'), ('CO', 'Cook')
    )

    avg_rate = models.FloatField(default=2.5, validators=[MaxValueValidator(5.0), MinValueValidator(0.0)])

    role = models.CharField(
        max_length=2,
        choices=ROLE_CHOICES,
        default='WA',
    )
    enable_mailing = models.BooleanField(default=True)

    def __str__(self):
        return self.user.username

    # noinspection PyTypeChecker
    def get_employment_months(self):
        if self.started_work_date:
            today = datetime.now().date()
            delta = today - self.started_work_date
            return round(delta.days / 30, 1)
        return None

    def get_age(self):
        if self.birth_date:
            today = datetime.now().date()
            delta = today - self.birth_date
            return round(delta.days / 365, 2)
        return None

    def get_manager(self):
        profile_business = self.business
        for profile in profile_business.employeeprofile_set.all():
            if profile.role == 'MA':
                return profile
        return None

    @staticmethod
    def get_filtered_upon_fields():
        return ['birth_date', 'started_work_date', 'gender', 'avg_rate']


@receiver(post_save, sender=User)
def update_employee(sender, instance, created, **kwargs):
    if created:
        b, created2 = Business.objects.update_or_create(business_name='dummy')
        EmployeeProfile.objects.create(user=instance, business=b)
    instance.profile.save()
