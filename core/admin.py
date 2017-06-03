from django.contrib import admin
from .models import ShiftsArrangement, Message
# Register your models here.
admin.site.register(ShiftsArrangement)


class MessageAdmin(admin.ModelAdmin):
    list_display = ("sender", "get_recipients", "subject", "text", "sent_time")


admin.site.register(Message, MessageAdmin)
