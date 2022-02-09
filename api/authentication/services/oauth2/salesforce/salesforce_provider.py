from oauth_client.providers.oauth2provider import OAuth2Provider


class SalesforceProvider(OAuth2Provider):
    key = 'salesforce'
    name = 'Salesforce'
    authorize_url = 'https://login.salesforce.com/services/oauth2/authorize'
    token_url = 'https://login.salesforce.com/services/oauth2/token'
    refresh_url = 'https://login.salesforce.com/services/oauth2/token'
    scope = ['refresh_token', 'api']
