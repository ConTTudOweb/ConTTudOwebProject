from tenant_schemas.middleware import BaseTenantMiddleware
from tenant_schemas.utils import get_public_schema_name


class TenantMiddleware(BaseTenantMiddleware):
    """
    Selects the proper database schema using the request host. E.g. <my_tenant>.<my_domain>
    """

    def get_tenant(self, model, hostname, request):
        public_schema_name = get_public_schema_name()
        schema_name = request.headers.get('Tenant', public_schema_name)
        print('Tenant: ', schema_name)
        print(hostname, request.headers)
        if schema_name != public_schema_name:
            return model.objects.get(schema_name=schema_name)

        return model.objects.get(domain_url=hostname)
