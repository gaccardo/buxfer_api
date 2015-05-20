import requests
import settings

from pybles import pybles


class ErrorWithBuferAPI( Exception ): pass


class BuxferAPI( object ):

    def __init__(self):
        self.base_url = settings.BASE_URL
        self.token = None

    def login(self, user, password):
        response = requests.get("%s/login?userid=%s" \
            "&password=%s" % (self.base_url, user, password))

        if response.status_code != 200:
            raise ErrorWithBuferAPI

        token = response.json()
        self.token = token['response']['token']

    def get_accounts(self):
        response = requests.get("%s/accounts?token=%s" % (self.base_url, 
            self.token))

        if response.status_code != 200:
            raise ErrorWithBuferAPI

        response = response.json()
        return response['response']['accounts']