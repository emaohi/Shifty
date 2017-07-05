from django.contrib import admin

from .models import EmployeeRequest, ManagerMessage

class EmployeeRequestAdmin(admin.ModelAdmin):
    list_display = ('get_issuers_string', 'text', 'status', 'sent_time')

admin.site.register(EmployeeRequest, EmployeeRequestAdmin)


class ManagerMessageAdmin(admin.ModelAdmin):
    list_display = ('business', 'get_recipients_string', 'subject', 'text', 'sent_time')

admin.site.register(ManagerMessage, ManagerMessageAdmin)
