from django.contrib import admin

from .models import Business, EmployeeProfile


class BusinessAdmin(admin.ModelAdmin):
    list_display = ("business_name", "business_type", "tip_method", "manager", "deadline_day",
                    "slot_request_enabled", "logo")
admin.site.register(Business, BusinessAdmin)


class EmployeeProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "business", "role", "phone_num", "enable_mailing", "menu_score", 'rate', 'arriving_method')

admin.site.register(EmployeeProfile, EmployeeProfileAdmin)
