import smtplib
import math
from os.path import basename
import os
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.MIMEBase import MIMEBase
from email.utils import COMMASPACE, formatdate
from email import Encoders
import datetime

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
        hoy = datetime.datetime.now()
        hoy = hoy.strftime('%d/%m/%Y')


        msg = MIMEMultipart()
        msg['From'] = settings.SENDER
        msg['To'] = ', '.join(settings.RECIPIENTS)
        msg['Subject'] = "Estado de cuentas: %s" % hoy
        
        reporte = os.path.join(settings.REPORT_TMP, 
            settings.REPORT_NAME)

        part = MIMEBase('application', "octec-stream")
        part.set_payload(open(reporte, "rb").read())
        Encoders.encode_base64(part)

        part.add_header('Content-Disposition', 
            'attachment; filename="%s"' % basename(reporte))
        msg.attach(part)

        server = smtplib.SMTP('%s:%s' % (settings.SMTPSERVER,
            settings.SMTPPORT))
        server.starttls()
        server.login(settings.EMAIL_USER, settings.EMAIL_PASS)
        server.sendmail(settings.SENDER, settings.RECIPIENTS,
            msg.as_string())
        server.close()