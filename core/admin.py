from django.contrib import admin

from .models import EmployeeRequest, ManagerMessage, ShiftSlot, Holiday, ShiftRequest, Shift, ShiftSwap, SavedSlot


class EmployeeRequestAdmin(admin.ModelAdmin):
    list_display = ('get_issuers_string', 'type', 'text', 'status', 'sent_time')
    raw_id_fields = ('issuers',)

admin.site.register(EmployeeRequest, EmployeeRequestAdmin)


class ManagerMessageAdmin(admin.ModelAdmin):
    list_display = ('business', 'get_recipients_string', 'subject', 'text', 'sent_time')

admin.site.register(ManagerMessage, ManagerMessageAdmin)


class ShiftSlotAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'business', 'year', 'week', 'day', 'start_hour', 'end_hour', 'constraints',
                    'holiday', 'get_date', 'get_week_str', 'saved_slot')
admin.site.register(ShiftSlot, ShiftSlotAdmin)


class HolidayAdmin(admin.ModelAdmin):
    list_display = ('name', 'date')
admin.site.register(Holiday, HolidayAdmin)


class ShiftRequestAdmin(admin.ModelAdmin):
    list_display = ('id', 'employee', 'week_range', 'get_slots', 'submission_time')
    raw_id_fields = ('employee',)
admin.site.register(ShiftRequest, ShiftRequestAdmin)


class ShiftAdmin(admin.ModelAdmin):
    list_display = ['slot', 'rank', 'get_employees_string', 'get_date', 'remarks']
    raw_id_fields = ('employees',)
admin.site.register(Shift, ShiftAdmin)


class ShiftSwapAdmin(admin.ModelAdmin):
    list_display = ['id', 'requester', 'responder', 'requester_shift', 'requested_shift',
                    'accept_step', 'updated_at']
admin.site.register(ShiftSwap, ShiftSwapAdmin)


class ShiftSlotInline(admin.StackedInline):
    model = ShiftSlot


class SavedSlotAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'constraints', 'is_mandatory']
    inlines = [
        ShiftSlotInline
    ]
admin.site.register(SavedSlot, SavedSlotAdmin)
