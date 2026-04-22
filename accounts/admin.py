from django.contrib import admin
from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.db import connection
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from foundations.admin import BaseAdminView
from . models import User, UserProfile


# Custom form for creating new users
class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'role', 'phone_number', 'username')

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


# Custom form for changing users (for use in Django Admin)
class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('email', 'password', 'first_name', 'last_name', 'role', 'phone_number', 'is_active', 'is_staff', 'is_superadmin', 'is_deleted')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here because the field contains hashed data.
        return self.initial["password"]


class UserAdminView(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    prepopulated_fields = {}
    list_display = ('id', 'email', 'username', 'role', 'phone_number', )
    list_display_links = BaseAdminView.list_display_links + ('email', 'username')
    ordering = ('role',)
    list_filter = []
    filter_horizontal = ('groups', 'user_permissions')
    search_fields = BaseAdminView.search_fields + ('email', 'username', 'phone_number')

    def get_fieldsets(self, request, obj=None):
        fieldsets = super().get_fieldsets(request, obj)
        # Check if the current schema is a tenant schema; connection from django.db
        # [request will fetch db connection first]
            # Remove "superuser status", "is admin", "is superadmin" for tenant schemas
        fieldsets = [
            (name,
             {'fields': [f for f in fields['fields'] if f not in {'is_superuser', 'is_admin', 'is_superadmin'}]})
            for name, fields in fieldsets
        ]

        return fieldsets
    fieldsets = (
        ('User Details', {
            'fields': (
                'email', 'username', 'first_name', 'last_name', 'phone_number', 'role',
            )
        }),
        ('Roles & Permissions', {
            'fields': (
                'is_superuser', 'groups', 'user_permissions', 'is_admin', 'is_active', 'is_staff', 'is_superadmin',
                'is_deleted'
            ),
            'classes': ('collapse',),
        }),
        ('Password', {'fields': ('password',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email', 'first_name', 'last_name', 'username', 'role', 'phone_number', 'password1', 'password2'
            ),
        }),
    )


admin.site.register(User, UserAdminView)


class UserProfileAminView(BaseAdminView):
    model = UserProfile
    prepopulated_fields = {}
    list_display = BaseAdminView.list_display + ('user', 'state', 'country', 'zip_code',)
    list_display_links = BaseAdminView.list_display_links + ('user',)
    ordering = BaseAdminView.ordering + ('user',)
    search_fields = BaseAdminView.search_fields + ('user', 'state', 'country', 'zip_code')
    fieldsets = BaseAdminView.fieldsets + (
        ('User Profile', {
            'fields': (
                'user', 'address_line_1', 'address_line_2', 'address_line_3',
                'district', 'state', 'country', 'zip_code', 'is_organization', 'organization_name'
            )
        }),
        ('Profile Medias', {
            'fields': ('profile_image', 'cover_image',),
            'classes': ('collapse',),
        }),
    )


admin.site.register(UserProfile, UserProfileAminView)
