from pybles import pybles

import settings
from command import BuxferCommand


class ShowBalance( BuxferCommand ):

    def show_accounts(self):
        connection = self.do_connect()
        accounts = connection.get_accounts()

        PB = pybles.Pyble()

        PB.add_column('CUENTA')
        PB.add_column('MONEDA')
        PB.add_column('MONTO')

        for acc in accounts:
            PB.add_line([acc.name, acc.currency, 
                acc.balance])

        PB.show_table()