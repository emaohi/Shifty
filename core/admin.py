from django.contrib import admin
from .models import ShiftsArrangement, Message, EmployeeRequest, BroadcastMessage, ShiftSwapMessage

# Register your models here.
admin.site.register(ShiftsArrangement)

admin.site.register(EmployeeRequest)
admin.site.register(BroadcastMessage)
admin.site.register(ShiftSwapMessage)


class MessageAdmin(admin.ModelAdmin):
    list_display = ("sender", "get_recipients", "subject", "text", "sent_time")

admin.site.register(Message, MessageAdmin)


# class EmployeeRequest(admin.ModelAdmin):
#     list_display = ("")