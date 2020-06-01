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
from django.views.generic import RedirectView
from rest_framework import routers

from .core.views import FederativeUnitViewSet, PeopleViewSet, CityViewSet

admin.site.site_title = settings.ADMIN_SITE_TITLE
admin.site.site_header = settings.ADMIN_SITE_HEADER
admin.site.index_title = settings.ADMIN_INDEX_TITLE
admin.site.empty_value_display = '---'

router = routers.DefaultRouter(trailing_slash=True)
router.register('federative-unit', FederativeUnitViewSet)
router.register('city', CityViewSet)
router.register('people', PeopleViewSet)

urlpatterns = [path('', admin.site.urls),

               path('api/', include(router.urls)),
               path('api-auth/', include('rest_framework.urls')),
               path('rest-auth/', include('rest_auth.urls')),

               path('favicon.ico', RedirectView.as_view(url=staticfiles_storage.url('assets/img/favicon.png')))
               ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ]
