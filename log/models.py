from __future__ import unicode_literals, division

from datetime import datetime

from django.core.validators import MaxValueValidator, MinValueValidator
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

    tip_method = models.CharField(
        max_length=1, choices=TIP_METHOD_CHOICES, default='G'
    )

    def get_curr_arrangement(self):
        return self.shiftsArrangement_set.order_by('-id')[0]

    def __str__(self):
        return self.business_name

    def get_type(self):
        return self.get_business_type_display()


# noinspection PyTypeChecker
class EmployeeProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    business = models.ForeignKey(Business, on_delete=models.CASCADE)
    phone_num = models.CharField(max_length=30, blank=True)
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

    def __str__(self):
        return self.user.username

    # noinspection PyTypeChecker
    def get_employment_time(self):
        if self.started_work_date:
            today = datetime.now().date()
            delta = today - self.started_work_date
            return delta.days
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


@receiver(post_save, sender=User)
def update_employee(sender, instance, created, **kwargs):
    if created:
        b, created2 = Business.objects.update_or_create(business_name='dummy')
        EmployeeProfile.objects.create(user=instance, business=b)
    instance.profile.save()
