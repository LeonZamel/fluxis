from .slack.slack_provider import SlackProvider
from .google.google_sheets_provider import GoogleSheetsProvider

OAUTH2_PROVIDERS = {
    SlackProvider.key: SlackProvider,
    GoogleSheetsProvider.key: GoogleSheetsProvider,
}

OAUTH2_PROVIDERS_CHOICE = [(provider.key, provider.name)
                           for provider in OAUTH2_PROVIDERS.values()]
