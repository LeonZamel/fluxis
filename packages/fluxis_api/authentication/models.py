from django.db import models

import uuid

from django.contrib.auth import get_user_model
from django.contrib.postgres.fields import JSONField
from django.db import models

from polymorphic.models import PolymorphicModel

from .services.oauth2.oauth2_providers import OAUTH2_PROVIDERS, OAUTH2_PROVIDERS_CHOICE
from .services.database.database_providers import DATABASE_PROVIDERS, DATABASE_PROVIDERS_CHOICE
from .services.service_providers import SERVICE_PROVIDERS, SERVICE_PROVIDERS_CHOICE


class Credentials(PolymorphicModel):
    # This is a class for generic credentials
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50)  # User given name
    service = models.CharField(choices=SERVICE_PROVIDERS_CHOICE, max_length=50)

    # The user that the credentials belong to
    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE
    )

    # These are generic credential information
    credentials = JSONField(default=dict)


class DatabaseCredentials(Credentials):
    class Meta:
        verbose_name = 'Database Credentials'
        verbose_name_plural = 'Database Credentials'

    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    host = models.CharField(max_length=100)
    port = models.IntegerField()
    database = models.CharField(max_length=100)


class OAuth2Credentials(Credentials):
    class Meta:
        verbose_name = 'OAuth2 Credentials'
        verbose_name_plural = 'OAuth2 Credentials'

    # The actual access token
    access_token = models.CharField(max_length=500)

    # Refresh token
    refresh_token = models.CharField(
        max_length=500, blank=True, null=True, default=None)

    # The full response token
    token = JSONField()

    def __str__(self):
        return f'{self.user} {self.service} credentials'
