import smtplib
import math

import settings
from command import BuxferCommand


class BuxferDaemon( BuxferCommand ):

    def send_report(self):
        if not settings.SEND_EMAIL:
            return False

        connection = self.do_connect()
        accounts = connection.get_accounts()
        transactions = connection.get_transactions()

        msg = 'Subject: Reporte de gastos\n'
        msg += 'Reporte de gastos\n\n'
        for acc in accounts:
            msg += "%s: $%s\n" % (acc.name,
                '%.2f' % acc.balance)

        msg += "\nTransacciones\n\n"
        for tra in transactions:
            msg += "%s: $%.2f %s\n" % (tra.description, 
                math.fabs(tra.expense), tra.t_type.upper())


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
        else:
            print msg