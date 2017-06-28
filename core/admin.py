from django.contrib import admin
from .models import ShiftsArrangement, EmployeeRequest, ShiftSwapMessage, ManagerMessage

# Register your models here.
admin.site.register(ShiftsArrangement)

admin.site.register(EmployeeRequest)
admin.site.register(ManagerMessage)
admin.site.register(ShiftSwapMessage)
