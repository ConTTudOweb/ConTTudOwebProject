from decouple import config
from django.db import models
from django_tenants.models import TenantMixin, DomainMixin
from django_tenants.signals import post_schema_sync
from django_tenants.utils import tenant_context

from conttudoweb.authentication.models import MyUser


class Client(TenantMixin):
    domain_url = models.CharField(max_length=128, unique=True, help_text='cliente.conttudoweb.com.br')
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    auto_drop_schema = True

    class Meta:
        default_permissions = ()
        verbose_name = 'cliente'


class Domain(DomainMixin):
    class Meta:
        verbose_name = 'domínio'


def create_super_user_and_admin(sender, tenant, **kwargs):
    with tenant_context(tenant):
        superuser_email = config('SUPERUSER_EMAIL')
        superuser_password = config('SUPERUSER_PASSWORD')
        MyUser.objects.create_superuser(email=superuser_email, password=superuser_password)


post_schema_sync.connect(create_super_user_and_admin, sender=TenantMixin)

# tenant1 = Client(schema_name='tenant1')  # "Client" is a tenant model
#
# with tenant_context(tenant1):
#     User.objects.create_superuser(username='admin1', password='123', email='')
