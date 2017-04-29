from django.contrib import admin

from .models import *
admin.site.register(Business)


class EmployeeProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "role")

    def has_change_permission(self, request, obj=None):
        if request.user.is_super_user():
            # allow superusers to edit all profiles
            return True
        if obj is None:
            # The docs say that the method should handle obj=None
            # Don't allow user to edit profiles in general
            return False
        # Let the user edit the package if they are the owner.
        return obj.user == request.user

admin.site.register(EmployeeProfile, EmployeeProfileAdmin)
