from user.models.profile import Profile

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group, User
from django.utils.translation import gettext_lazy as _


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    fk_name = "user"

    fields = ("avatar",)
    readonly_fields = ("avatar",)

    classes = ("grp-collapse grp-open",)
    inline_classes = ("grp-collapse grp-open",)


class CustomUserAdmin(UserAdmin):
    list_display = ("username", "first_name", "last_name", "is_staff", "is_superuser")

    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (_("Personal info"), {"fields": ("first_name", "last_name")}),
        (_("Permissions"), {"fields": ("is_staff", "is_superuser")}),
    )
    readonly_fields = ("username", "first_name", "last_name")

    inlines = (ProfileInline,)

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super().get_inline_instances(request, obj)


admin.site.unregister(Group)
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
