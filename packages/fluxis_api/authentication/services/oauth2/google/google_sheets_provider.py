from authentication.services.oauth2.oauth2provider import OAuth2Provider


class GoogleSheetsProvider(OAuth2Provider):
    key = 'google_sheets'
    name = 'Google Sheets'
    authorize_url = 'https://accounts.google.com/o/oauth2/v2/auth'
    token_url = 'https://www.googleapis.com/oauth2/v4/token'
    refresh_url = 'https://oauth2.googleapis.com/token'
    scope = ['https://www.googleapis.com/auth/spreadsheets',
             'https://www.googleapis.com/auth/drive',
             'https://www.googleapis.com/auth/analytics.readonly']
    """
    scope = ['https://www.googleapis.com/auth/spreadsheets',
             'https://www.googleapis.com/auth/drive.readonly',
             'https://www.googleapis.com/auth/analytics.readonly']
    """
    extra_kwargs = {
        # So we receive a refresh token
        'access_type': "offline",

        # So we *always* receive a refresh token, even if we received one before
        'prompt': "consent",
    }
