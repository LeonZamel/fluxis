from django.http.response import (
    HttpResponse,
    HttpResponseBadRequest,
    HttpResponseRedirect,
)
from django.views import View
from requests_oauthlib.oauth2_session import OAuth2Session
from rest_framework import permissions, status
from rest_framework.authentication import SessionAuthentication
from rest_framework.exceptions import APIException
from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    ListCreateAPIView,
    RetrieveDestroyAPIView,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Credentials, DatabaseCredentials, OAuth2Credentials
from .serializers import (
    CredentialsSerializer,
    DatabaseCredentialsSerializer,
    OAuth2CredentialsSerializer,
)
from .services.database.database_providers import DATABASE_PROVIDERS_CHOICE
from .services.oauth2.oauth2_providers import OAUTH2_PROVIDERS, OAUTH2_PROVIDERS_CHOICE
from .services.service_providers import SERVICE_PROVIDERS_CHOICE


class IsOwnerOrReject(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


class CredentialsList(ListAPIView):
    serializer_class = CredentialsSerializer

    def get_queryset(self):
        return Credentials.objects.filter(user=self.request.user)


class CredentialsDetail(RetrieveDestroyAPIView):
    serializer_class = CredentialsSerializer
    queryset = Credentials.objects.all()
    permission_classes = (IsAuthenticated, IsOwnerOrReject)


class DatabaseServiceList(APIView):
    def get(self, request):
        return Response(
            data=[
                {"key": key, "name": name} for (key, name) in DATABASE_PROVIDERS_CHOICE
            ]
        )


class OAuth2ServiceList(APIView):
    def get(self, request):
        return Response(
            data=[{"key": key, "name": name} for (key, name) in OAUTH2_PROVIDERS_CHOICE]
        )


class DatabaseCredentialsCreate(CreateAPIView):
    serializer_class = DatabaseCredentialsSerializer
    queryset = DatabaseCredentials.objects.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class OAuth2Start(APIView):
    def get(self, request, format=None):
        try:
            service_key = request.GET["service_key"]
            provider = OAUTH2_PROVIDERS[service_key]
        except KeyError as e:
            return Response(
                f"Unknown provider {e}",
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            provider = provider()
        except KeyError as e:
            return Response(
                f"Internal error", status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        oauth = OAuth2Session(
            provider.client_id, redirect_uri=provider.redirect_uri, scope=provider.scope
        )
        authorization_url, state = oauth.authorization_url(
            provider.authorize_url, **provider.extra_kwargs
        )

        response = Response(
            data={
                "url": authorization_url,
            }
        )
        request.session["oauth_state"] = state
        request.session["service_key"] = service_key
        return response


class OAuth2Callback(APIView):
    def post(self, request):
        service_key = request.session["service_key"]
        provider = OAUTH2_PROVIDERS[service_key]()
        resp = provider.redirect_uri + request.data.get("code")

        # Create Session, get token
        oauth = OAuth2Session(
            provider.client_id,
            redirect_uri=provider.redirect_uri,
            state=request.session["oauth_state"],
        )
        token = oauth.fetch_token(
            provider.token_url,
            client_secret=provider.client_secret,
            authorization_response=resp,
        )

        OAuth2Credentials.objects.create(
            user=request.user,
            access_token=token["access_token"],
            refresh_token=token.get("refresh_token"),
            token=token,
            service=service_key,
        )

        # Clean up
        response = Response()
        response.delete_cookie("oauth_state")
        response.delete_cookie("service_key")
        return response
