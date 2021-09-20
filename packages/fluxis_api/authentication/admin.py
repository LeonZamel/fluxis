from django.contrib import admin

from .models import DatabaseCredentials, OAuth2Credentials

# Register your models here.
admin.site.register(DatabaseCredentials)
admin.site.register(OAuth2Credentials)
