from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic import TemplateView

urlpatterns = [
    path('secret_path_31415926535_admin/', admin.site.urls),
    path('api/v1/', include('core.api.urls')),
]
