from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin, GroupAdmin
from django.contrib.auth.models import Group as authGroup
from django.contrib.contenttypes.models import ContentType

from .forms import MyUserChangeForm, MyUserCreationForm
from .models import User, Permission, Group, LogEntry


# TODO: Precisa criar um esquema que crie o usuário com senha aleatória e solicite a troca no primeiro acesso.
@admin.register(User)
class MyUserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = MyUserChangeForm
    add_form = MyUserCreationForm
    filter_horizontal = ('groups', 'user_permissions')

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('email', 'date_of_birth', 'is_active', 'is_staff', 'is_superuser')
    list_filter = ('is_active', 'is_staff', 'is_superuser')
    fieldsets = (
        ('Geral', {'fields': ('email', 'password')}),
        ('Dados pessoais', {'fields': ('date_of_birth', 'first_name', 'last_name')}),
        ('Permissões', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        # ('Preferências', {'fields': ('entity',)}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (
            'Geral',
            {
                'classes': ('wide',),
                'fields': ('email', 'password1', 'password2')
            }
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)


@admin.register(LogEntry)
class LogEntryAdmin(admin.ModelAdmin):
    date_hierarchy = 'action_time'

    list_filter = [
        'user',
        'content_type',
        'action_flag'
    ]

    search_fields = [
        'object_repr',
        'change_message'
    ]

    list_display = [
        'action_time',
        'user',
        'content_type',
        'object_repr',
        'action_flag',
    ]

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_view_permission(self, request, obj=None):
        return request.user.is_superuser


admin.site.unregister(authGroup)
admin.site.register(Group, GroupAdmin)

admin.site.register(ContentType)
admin.site.register(Permission)
