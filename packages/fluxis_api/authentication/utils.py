import datetime


def token_expired(token, buffer_period=0):
    """ 
    Check if token is expired given a buffer period
    :param token: this is a first param
    :param buffer_period: buffer period in seconds
    :returns: if token is expired
    :raises keyError: If token has no expiration date
    """
    if 'expires_at' not in token:
        # Might not have gotten an expiration and refresh token, assume it does not expire
        return False
    return datetime.datetime.fromtimestamp(int(token['expires_at']) - buffer_period) < datetime.datetime.now()
