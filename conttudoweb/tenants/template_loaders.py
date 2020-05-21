from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.db import connection
from ordered_set import OrderedSet
from tenant_schemas.postgresql_backend.base import FakeTenant
from tenant_schemas.template_loaders import FilesystemLoader


class CustomFilesystemLoader(FilesystemLoader):
    def get_dirs(self):
        dirs = OrderedSet(super(FilesystemLoader, self).get_dirs())

        if connection.tenant and not isinstance(connection.tenant, FakeTenant):
            try:
                template_dirs = settings.MULTITENANT_TEMPLATE_DIRS
            except AttributeError:
                raise ImproperlyConfigured(
                    "To use %s.%s you must define the MULTITENANT_TEMPLATE_DIRS"
                    % (__name__, FilesystemLoader.__name__)
                )

            for template_dir in reversed(template_dirs):
                dirs.update(
                    [
                        template_dir % (connection.tenant.schema_name,)
                        if "%s" in template_dir
                        else template_dir,
                    ]
                )

        return [each for each in reversed(dirs)]
