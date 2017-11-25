from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from user.models.profile import Profile


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    fk_name = 'user'

    fields = ('avatar', )
    readonly_fields = ('avatar',)

    classes = ('grp-collapse grp-open',)
    inline_classes = ('grp-collapse grp-open',)


class CustomUserAdmin(UserAdmin):
    inlines = (ProfileInline, )

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super().get_inline_instances(request, obj)


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
