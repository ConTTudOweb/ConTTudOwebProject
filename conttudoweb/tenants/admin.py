from django.contrib import admin
from django_tenants.admin import TenantAdminMixin

from .models import Client, Domain

public_admin_site = admin.AdminSite(name="public-admin")


class ClientAdmin(TenantAdminMixin, admin.ModelAdmin):
    list_display = ['name']


class DomainAdmin(admin.ModelAdmin):
    list_display = ('domain', 'tenant', 'is_primary')


public_admin_site.register(Client, ClientAdmin)
public_admin_site.register(Domain, DomainAdmin)
