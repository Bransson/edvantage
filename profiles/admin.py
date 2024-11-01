from django.contrib import admin

from .models import CustomUser
from django.contrib.auth.admin import UserAdmin


# Register your models here.


class CustomUserAdmin(UserAdmin):
    ordering = ('phone_number',)

    list_display = ('first_name', 'last_name', 'matric_no', 'phone_number','username', 'email', 'date_joined', 'is_staff', 'is_superuser')
    search_fields = ('first_name', 'last_name', "phone_number", "username", "matric_no")
    readonly_fields = ('date_joined', 'phone_number', 'matric_no')
    list_display_links = ('first_name', 'phone_number')
    # list_editable = ('first_name', 'phone_number',)
    add_fieldsets = ((None, {'fields' : ('first_name', 'last_name', 'username', 'matric_no', 'phone_number', 'email', 'password', 'password2', 'is_staff', 'is_superuser', 'is_active')}),)
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()
# admin.site.unregister('Group')


admin.site.register(CustomUser,CustomUserAdmin)
