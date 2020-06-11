from django.conf import settings
from django.db import connection
from django.urls import set_urlconf
from django_tenants.middleware.main import TenantMainMiddleware
from django_tenants.utils import get_public_schema_name
from django_tenants.utils import get_tenant_domain_model, get_tenant_model


class TenantMiddleware(TenantMainMiddleware):
    """
    Selects the proper database schema using the request host. E.g. <my_tenant>.<my_domain>
    """

    def get_tenant_custom(self, domain_model, hostname, request):
        public_schema_name = get_public_schema_name()
        schema_name = request.headers.get('Tenant', public_schema_name)
        if schema_name != public_schema_name:
            model = get_tenant_model()
            return model.objects.get(schema_name=schema_name)

        domain = domain_model.objects.select_related('tenant').get(domain=hostname)
        return domain.tenant

    def process_request(self, request):
        # Connection needs first to be at the public schema, as this is where
        # the tenant metadata is stored.
        connection.set_schema_to_public()
        hostname = self.hostname_from_request(request)

        domain_model = get_tenant_domain_model()
        try:
            tenant = self.get_tenant_custom(domain_model, hostname, request)
        except domain_model.DoesNotExist:
            raise self.TENANT_NOT_FOUND_EXCEPTION('No tenant for hostname "%s"' % hostname)

        tenant.domain_url = hostname
        request.tenant = tenant

        connection.set_tenant(request.tenant)

        # Do we have a public-specific urlconf?
        if hasattr(settings, 'PUBLIC_SCHEMA_URLCONF') and request.tenant.schema_name == get_public_schema_name():
            request.urlconf = settings.PUBLIC_SCHEMA_URLCONF
            set_urlconf(request.urlconf)
