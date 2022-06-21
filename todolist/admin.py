from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.forms import Textarea

from todolist.models import Account


class UserAdminConfig(UserAdmin):
    search_fields = ('email', 'username',)
    ordering = ('-date_joined',)
    list_display = ('username', 'email', 'is_staff', 'is_active')

    fieldsets = (
        (None, {'fields': ('username', 'email',)}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
        ('Personal', {'fields': ('about',)}),
    )

    formfield_overrides = {
        Account.about: {'widget': Textarea(attrs={'rows': 10, 'cols': 40})},
    }

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'is_active', 'is_staff')
        }),
    )


admin.site.register(Account, UserAdminConfig)
