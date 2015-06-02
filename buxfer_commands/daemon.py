import smtplib

import settings
from command import BuxferCommand


class BuxferDaemon( BuxferCommand ):

    def send_report(self):
        connection = self.do_connect()
        accounts = connection.get_accounts()

        msg = 'Subject: Reporte de gastos\n'
        msg += 'Reporte de gastos\n\n'

        for acc in accounts:
            msg += "%s: $%s\n" % (acc['key-account']['name'],
                acc['key-account']['balance'])

        server = smtplib.SMTP('%s:%s' % (settings.SMTPSERVER,
            settings.SMTPPORT))

        if settings.TLS:
            server.starttls()
            
        server.login(settings.EMAIL_USER, 
            settings.EMAIL_PASS)
        server.sendmail(settings.SENDER, 
            settings.RECIPIENTS, msg)
        server.quit()