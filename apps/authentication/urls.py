# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path
from .views import login_view, register_user, update_user_view, delete_user_view
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path("login/", login_view, name="login"),
    path("register/", register_user, name="register"),
    path("update/", update_user_view, name="update-user"),
    path("delete/", delete_user_view, name="delete-user"),
    path("logout/", LogoutView.as_view(), name="logout"),
]
