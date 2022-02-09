from authentication.services.oauth2.oauth2provider import OAuth2Provider


class SlackProvider(OAuth2Provider):
    key = 'slack'
    name = 'Slack'
    authorize_url = 'https://slack.com/oauth/v2/authorize'
    token_url = 'https://slack.com/api/oauth.v2.access'
    refresh_url = ''
    scope = ['channels:read', 'chat:write', 'commands']
