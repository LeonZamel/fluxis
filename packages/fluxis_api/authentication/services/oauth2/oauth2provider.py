import datetime
import os

from requests_oauthlib.oauth2_session import OAuth2Session


class OAuth2Provider:
    key: str  # Unique identification key
    name: str  # Human readable name
    authorize_url: str
    access_token_url: str
    refresh_url: str
    scope = []
    extra_kwargs = {}

    def __init__(self):
        # Creates a provider with the client id and secret from environment variables
        name = self.key.upper()
        self.client_id = os.environ[f'{name}_CLIENT_ID']
        self.client_secret = os.environ[f'{name}_CLIENT_SECRET']
        self.redirect_uri = os.environ['OAUTH2_REDIRECT_URI']

    def refresh_token(self, refresh_token):
        extra = {
            'client_id': self.client_id,
            'client_secret': self.client_secret,
        }

        oauth = OAuth2Session(self.client_id)
        return oauth.refresh_token(self.refresh_url, refresh_token=refresh_token, **extra)
