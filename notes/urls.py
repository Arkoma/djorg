from django.conf.urls import re_path
from rest_framewor.authtoken import views as drf_views
from .apiviews import UserCreate

urlpatterns = [
    re_path(r'^auth$', drf_views.obtain_auth_token, name='auth'),
    path("users/", UserCreate.as_view(), name="user_create"),
]
