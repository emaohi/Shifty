from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Business(models.Model):
    business_name = models.CharField(primary_key=True, max_length=30)

    BUSINESS_TYPE_CHOICES = (
        ('RE', 'Restaurant'), ('CA', 'Cafe'), ('PU', 'Pub')
    )
    business_type = models.CharField(
        max_length=2,
        choices=BUSINESS_TYPE_CHOICES,
        default='CA',
    )

    def __str__(self):
        return self.business_name

    def get_type(self):
        return self.get_business_type_display()


class EmployeeProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    business = models.ForeignKey(Business, on_delete=models.CASCADE)
    phone_num = models.CharField(max_length=30, blank=True)
    home_address = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    started_work_date = models.DateField(null=True, blank=True)

    ROLE_CHOICES = (
        ('MA', 'Manager'), ('WA', 'Waiter'), ('BT', 'Bartender'), ('CO', 'Cook')
    )
    role = models.CharField(
        max_length=2,
        choices=ROLE_CHOICES,
        default='WA',
    )

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def update_employee(sender, instance, created, **kwargs):
    if created:
        b, craeted = Business.objects.update_or_create(business_name='dummy')
        EmployeeProfile.objects.create(user=instance, business=b)
    instance.profile.save()
