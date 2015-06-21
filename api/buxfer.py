import requests
import settings

from pybles import pybles

from account import Account
from transaction import Transaction
from budget import Budget

requests.packages.urllib3.disable_warnings()

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
            error = response.json()
            error = error['error']
            print "ERROR"
            print "* Resource: %s" % resource
            print "* Type: %s" % error['type']
            print "* Request id: %d" % error['request_id']
            print "* Message: %s" % error['message']
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

    def __from_json_transactions_to_objects(self, transactions):
        transactions_list = list()
        for tra in transactions['response']['transactions']:
            tra = tra['key-transaction']
            transactions_list.append(Transaction(description=tra['description'],
                account=tra['accountName'],
                expense=tra['expenseAmount'],
                amount=tra['amount'],
                t_type=tra['transactionType'],
                date=tra['normalizedDate'],
                tags=tra['tagNames']))

        return transactions_list

    def get_transactions(self):
        response = self.__get_request('transactions')
        return self.__from_json_transactions_to_objects(response)

    def __from_json_reminder_to_objects(self, reminders):
        pass

    def get_reminders(self):
        response = self.__get_request('reminders')
        return self.__from_json_reminder_to_objects(response)

    def __from_json_budgets_to_objects(self, budgets):
        budgets_list = list()
        for bud in budgets['response']['budgets']:
            bud = bud['key-budget']
            budgets_list.append(Budget(name=bud['name'], 
                spent=bud['spent'], limit=bud['limit'], 
                balance=bud['balance']))

        return budgets_list

    def get_budgets(self):
        response = self.__get_request('budgets')
        return self.__from_json_budgets_to_objects(response)
