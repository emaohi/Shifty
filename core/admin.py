from django.contrib import admin

from .models import EmployeeRequest, ManagerMessage, ShiftSlot, TmpHoliday


class EmployeeRequestAdmin(admin.ModelAdmin):
    list_display = ('get_issuers_string', 'text', 'status', 'sent_time')

admin.site.register(EmployeeRequest, EmployeeRequestAdmin)


class ManagerMessageAdmin(admin.ModelAdmin):
    list_display = ('business', 'get_recipients_string', 'subject', 'text', 'sent_time')

admin.site.register(ManagerMessage, ManagerMessageAdmin)


class ShiftSlotAdmin(admin.ModelAdmin):
    list_display = ('business', 'year', 'week', 'day', 'start_hour', 'end_hour', 'constraints')
admin.site.register(ShiftSlot, ShiftSlotAdmin)

admin.site.register(TmpHoliday)
