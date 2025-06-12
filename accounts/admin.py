from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from .forms import CustomUserCreationForm
from django.utils.translation import gettext_lazy as _

# Custom admin class for managing CustomUser model via Django admin
class CustomUserAdmin(UserAdmin):
    # Specify the custom form used for creating users
    add_form = CustomUserCreationForm

    # Associate this admin with the CustomUser model
    model = CustomUser

    # Fields to display in the user list view in admin panel
    list_display = ('email', 'name', 'mobile_no', 'work_status', 'is_staff', 'is_active')

    # Filters to be shown in the sidebar of the user list view
    list_filter = ('is_staff', 'is_active', 'work_status')

    # Default ordering in admin list view
    ordering = ('email',)

    # Fieldsets to control the layout of the user detail/edit page in admin
    fieldsets = (
        (None, {'fields': ('email', 'password')}),  # Basic login info
        (_('Personal Info'), {'fields': ('name', 'mobile_no', 'work_status')}),  # Personal details
        (_('Permissions'), {'fields': (
            'is_active', 'is_staff', 'is_superuser',
            'groups', 'user_permissions'
        )}),  # Permissions-related settings
        (_('Important Dates'), {'fields': ('last_login', 'date_joined')}),  # Metadata
    )

    # Layout for the "Add user" form in the admin
    add_fieldsets = (
        (None, {
            'classes': ('wide',),  # Makes form wide
            'fields': (
                'name', 'mobile_no', 'email', 'work_status',
                'password1', 'password2', 'is_staff', 'is_active'
            ),
        }),
    )

    # Allow searching users by email or name in the admin panel
    search_fields = ('email', 'name')

# Register the CustomUser model with the custom admin configuration
admin.site.register(CustomUser, CustomUserAdmin)
