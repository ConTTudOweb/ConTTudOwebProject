from django.db import models
from tenant_schemas.models import TenantMixin


class Client(TenantMixin):
    domain_url = models.CharField(max_length=128, unique=True, help_text='cliente.conttudoweb.com.br')
    name = models.CharField(max_length=100)


    auto_drop_schema = True

    class Meta:
        default_permissions = ()


# tenant1 = Client(schema_name='tenant1')  # "Client" is a tenant model
#
# with tenant_context(tenant1):
#     User.objects.create_superuser(username='admin1', password='123', email='')
