from rest_framework.serializers import ModelSerializer

from .models import OAuth2Credentials, Credentials, DatabaseCredentials


class OAuth2CredentialsSerializer(ModelSerializer):
    class Meta:
        model = OAuth2Credentials
        fields = ('id', 'service')
        read_only_fields = ('id', 'service')


class FullOAuth2CredentialsSerializer(ModelSerializer):
    class Meta:
        model = OAuth2Credentials
        fields = ('id', 'service', 'access_token', 'refresh_token', 'token')
        read_only_fields = ('id', 'service')


class CredentialsSerializer(ModelSerializer):
    class Meta:
        model = Credentials
        fields = ('id', 'service')
        read_only_fields = ('id', 'service')


class DatabaseCredentialsSerializer(ModelSerializer):
    class Meta:
        model = DatabaseCredentials
        fields = ('id', 'service', 'username',
                  'password', 'host', 'port', 'database')
        read_only_fields = ('id', )
