from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from ponytoon.forms import UserAdminChangeForm, UserAdminCreationForm
from accounts.models import User, Profile, Species, TimeZone

class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserAdminChangeForm
    add_form = UserAdminCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('username', 'email', 'is_active', 'is_staff')
    list_filter = ('is_admin', 'is_staff', 'is_active')
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Additional options', {'fields': ('avatar', 'species', 'reputation', 'timezone')}),
        ('Registration info', {'fields': ('last_login', 'date_joined')}),
        ('Premium', {'fields': ('premium', 'premium_date')}),
        ('Permissions', {'fields': ('is_admin', 'is_staff', 'is_active')}),
    )
    readonly_fields = ('premium_date', 'date_joined')
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2')}
        ),
    )
    search_fields = ('username', 'email',)
    ordering = ('username', 'email',)
    filter_horizontal = ()

admin.site.register(User, UserAdmin)

admin.site.register(Species)

admin.site.register(TimeZone)
