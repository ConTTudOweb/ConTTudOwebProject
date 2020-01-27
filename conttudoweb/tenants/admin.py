from django.contrib import admin

from .models import Client

public_admin_site = admin.AdminSite(name="public-admin")

# @public_admin_site.register(Client)
class ClientModelAdmin(admin.ModelAdmin):
    list_display = ['name']


public_admin_site.register(Client, ClientModelAdmin)
