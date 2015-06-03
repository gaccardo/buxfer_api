import requests
import settings

from pybles import pybles

from account import Account


class ErrorWithBuxferAPI( Exception ): pass


class BuxferAPIUnauthorized( Exception ): pass


class BuxferAPI( object ):

    def __init__(self):
        self.base_url = settings.BASE_URL
        self.token = None

    def __get_request(self, resource):
        url = "%s/%s?token=%s" % (self.base_url, 
            resource, self.token)
        response = requests.get(url)

        if response.status_code == 400:
            raise BuxferAPIUnauthorized

        if response.status_code != 200:
            raise ErrorWithBuxferAPI

        return response.json()

    def login(self, user, password):
        response = requests.get("%s/login?userid=%s" \
            "&password=%s" % (self.base_url, user, password))

        if response.status_code != 200:
            raise ErrorWithBuferAPI

        token = response.json()
        self.token = token['response']['token']

    def logout(self):
        pass

    def __from_json_accounts_to_objects(self, accounts):
        accounts_list = list()
        for acc in accounts['response']['accounts']:
            acc = acc['key-account']
            accounts_list.append(Account(currency=acc['currency'], 
                balance=acc['balance'], 
                id=acc['id'], 
                bank=acc['bank'], 
                name=acc['name']))

        return accounts_list

    def get_accounts(self):
        response = self.__get_request('accounts')
        return self.__from_json_accounts_to_objects(response)

    def get_transactions(self):
        response = self.__get_request('transactions')
        return response['response']['transactions']

    