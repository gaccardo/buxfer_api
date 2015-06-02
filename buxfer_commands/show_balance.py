from api import buxfer
from pybles import pybles

import settings


class ShowBalance( object ):

    def __do_connect(self):
        ba = buxfer.BuxferAPI()
        ba.login(user = settings.USER, 
            password = settings.PASS)

        return ba

    def show_accounts(self):
        connection = self.__do_connect()
        accounts = connection.get_accounts()

        PB = pybles.Pyble()

        PB.add_column('CUENTA')
        PB.add_column('MONEDA')
        PB.add_column('MONTO')

        for acc in accounts:
            PB.add_line([acc['key-account']['name'],
                         acc['key-account']['currency'],
                         acc['key-account']['balance']])

        PB.show_table()