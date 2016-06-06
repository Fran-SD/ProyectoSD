__author__ = 'cancionesquelopetan'
import twitter
import io
import json

def oauth_login():
    CONSUMER_KEY = '1acp1uEGh2oAf1Be3RmVdF1is'
    CONSUMER_SECRET = 'tO3QaIiMGN12FVuN3jpxIN06uSZ2nP0xrWWDHYc6PPkid81ByV'
    OAUTH_TOKEN = '739877546062405632-Jn7dqdGylY7cbUl9xjroKdnOipw4S1i'
    OAUTH_TOKEN_SECRET = '5Z4dqp2M2e4mXAK9R7uy0GD5aWaOa7p2dz8pTUprNwBHy'

    auth = twitter.oauth.OAuth(OAUTH_TOKEN, OAUTH_TOKEN_SECRET, CONSUMER_KEY, CONSUMER_SECRET)

    twitter_api = twitter.Twitter(auth=auth)
    return twitter_api
