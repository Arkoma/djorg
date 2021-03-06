"""djorg URL Configuration

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
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

from rest_framework import routers
from notes.api import NoteViewSet
from rest_framework.authtoken import views
from graphene_django.views import GraphQLView

from importlib import import_module

from django.conf.urls import include, url, re_path

from allauth.socialaccount import providers

# from . import app_settings

router = routers.DefaultRouter()
router.register(r'notes', NoteViewSet)

urlpatterns = [
    path('', TemplateView.as_view(template_name='djorg_base.html')),
    path('graphql/', GraphQLView.as_view(graphiql=True)),
    path('api/', include(router.urls)),
    path('bookmarks/', include('bookmarks.urls')),
    path('admin/', admin.site.urls),
    path('accounts/profile/', include('bookmarks.urls')),
    url(r'^', include('allauth.account.urls')),
    re_path(r'^api-token-auth/', views.obtain_auth_token),
]

# if app_settings.SOCIALACCOUNT_ENABLED:
#    urlpatterns += [url(r'^social/', include('allauth.socialaccount.urls'))]

for provider in providers.registry.get_list():
    try:
        prov_mod = import_module(provider.get_package() + '.urls')
    except ImportError:
        continue
    prov_urlpatterns = getattr(prov_mod, 'urlpatterns', None)
    if prov_urlpatterns:
        urlpatterns += prov_urlpatterns
