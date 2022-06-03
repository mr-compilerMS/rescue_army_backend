from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from imagekit.admin import AdminThumbnail
from .models import User


# Register your models here.
@admin.register(User)
class UserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (
            _("Personal info"),
            {"fields": ("first_name", "last_name", "email", "phone", "avatar")},
        ),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "username",
                    "phone",
                    "email",
                    "first_name",
                    "last_name",
                    "password1",
                    "password2",
                ),
            },
        ),
    )
    list_display = (
        "username",
        "phone",
        "email",
        "first_name",
        "last_name",
        "is_staff",
        "avatar_thumbnail",
    )
    avatar_thumbnail = AdminThumbnail(image_field="avatar_thumbnail")
    search_fields = ("username", "phone", "first_name", "last_name", "email")
    list_per_page = 10
