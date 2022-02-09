from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic import TemplateView

urlpatterns = [
    path(
        "secret_path_31415926535_admin/", admin.site.urls
    ),  # Of course this isn't secret per se, but just hiding it will already get rid of a bunch of unwanted brute force attacks
    path("api/v1/", include("core.api.urls")),
]
