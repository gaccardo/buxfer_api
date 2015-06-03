import smtplib
import math

import settings
from command import BuxferCommand
from api.reporter import Reporter


class BuxferDaemon( BuxferCommand ):

    def send_report(self):
        if not settings.SEND_EMAIL:
            return False

        connection = self.do_connect()
        accounts = connection.get_accounts()
        transactions = connection.get_transactions()
        reporter = Reporter(accounts, transactions)
        reporter.generate_report()

        if not settings.DEBUG_EMAIL:
            server = smtplib.SMTP('%s:%s' % (settings.SMTPSERVER,
                settings.SMTPPORT))

            if settings.TLS:
                server.starttls()
                
            server.login(settings.EMAIL_USER, 
                settings.EMAIL_PASS)
            server.sendmail(settings.SENDER, 
                settings.RECIPIENTS, msg)
            server.quit()