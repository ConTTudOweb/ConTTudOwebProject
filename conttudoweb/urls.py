"""conttudoweb URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.storage import staticfiles_storage
from django.urls import path, include
from django.views.generic import RedirectView, TemplateView
from rest_framework import routers
from rest_framework.schemas import get_schema_view

from .core.views import FederativeUnitViewSet, PeopleViewSet, CityViewSet
from .inventory.views import UnitOfMeasureViewSet, CategoryViewSet, SubcategoryViewSet, \
    ProductSizeRegisterViewSet, ProductViewSet, PackagingTypeViewSet
from .sale.views import SaleOrderViewSet

admin.site.site_title = settings.ADMIN_SITE_TITLE
admin.site.site_header = settings.ADMIN_SITE_HEADER
admin.site.index_title = settings.ADMIN_INDEX_TITLE
admin.site.empty_value_display = '---'


class API(routers.APIRootView):
    """
    Para mais detalhes visite a [documentação][doc].

    [doc]:../api-doc
    """


class Router(routers.DefaultRouter):
    APIRootView = API


router = Router(trailing_slash=True)
# core
router.register('federative-unit', FederativeUnitViewSet)
router.register('city', CityViewSet)
router.register('people', PeopleViewSet)
# inventory
router.register('unit-of-measure', UnitOfMeasureViewSet)
router.register('category', CategoryViewSet)
router.register('subcategory', SubcategoryViewSet)
router.register('product-size-register', ProductSizeRegisterViewSet)
router.register('packaging-type', PackagingTypeViewSet)
router.register('product', ProductViewSet)
# sale
router.register('sale-order', SaleOrderViewSet)

urlpatterns = [path('', admin.site.urls),

               path('api/', include(router.urls)),
               path('api-auth/', include('rest_framework.urls')),
               path('rest-auth/', include('rest_auth.urls')),

               path('openapi', get_schema_view(
                   title="Documentação da API",
                   description=settings.ADMIN_SITE_HEADER,
                   version="1.0.0"
               ), name='openapi-schema'),

               path('api-doc/', TemplateView.as_view(
                   template_name='swagger-ui.html',
                   extra_context={'schema_url': 'openapi-schema'}
               ), name='swagger-ui'),

               path('favicon.ico', RedirectView.as_view(url=staticfiles_storage.url('assets/img/favicon.png')))
               ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ]
