import smtplib

import settings
from api import buxfer


class BuxferDaemon( object ):

    def __do_connect(self):
        ba = buxfer.BuxferAPI()
        ba.login(user = settings.USER,
            password = settings.PASS)

        return ba

    def send_report(self):
        connection = self.__do_connect()
        accounts = connection.get_accounts()

        msg = 'Subject: Reporte de gastos\n'
        msg += 'Reporte de gastos\n\n'

        for acc in accounts:
            msg += "%s: $%s\n" % (acc['key-account']['name'],
                acc['key-account']['balance'])

        server = smtplib.SMTP('smtp.gmail.com:587')
        server.starttls()
        server.login(settings.EMAIL_USER, 
            settings.EMAIL_PASS)
        server.sendmail(settings.SENDER, 
            settings.RECIPIENTS, msg)
        server.quit()