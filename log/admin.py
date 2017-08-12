from django.contrib import admin

from .models import Business, EmployeeProfile


class BusinessAdmin(admin.ModelAdmin):
    list_display = ("business_name", "business_type", "tip_method", "manager", "deadline_day")
admin.site.register(Business, BusinessAdmin)


class EmployeeProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "business", "role", "phone_num")

admin.site.register(EmployeeProfile, EmployeeProfileAdmin)
