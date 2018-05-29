from django.urls import include, path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('account_signup/', include('allauth.urls')),
    path('account_login/', include('allauth.urls')),
]
