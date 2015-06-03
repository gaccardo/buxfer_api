import os

from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
import datetime

import settings

class Reporter( object ):

    def __init__(self, accounts, transactions):
        self.accounts     = accounts
        self.transactions = transactions
        self.c            = None
        self.l            = 800

    def __prepare_document(self):
        file_path = os.path.join(settings.REPORT_TMP, 
            settings.REPORT_NAME)
        self.c    = canvas.Canvas(file_path)

    def __generate_header(self):
        self.c.setFont('Helvetica', 28)
        self.c.drawString(30, self.l, 'Estado general de cuentas')
        self.c.setFont('Courier', 11)

        hoy = datetime.datetime.now()
        hoy = hoy.strftime('%d/%m/%Y')

        self.c.drawString(30, 780, 'Fecha: %s' % hoy)
        self.c.line(20,775,580,775)

    def __get_totals_by_currency(self):
        totals = dict()

        for acc in self.accounts:
            if acc.currency not in totals:
                totals[acc.currency] = acc.balance
            else:
                totals[acc.currency] += acc.balance

        return totals

    def __accounts_amount(self):
        self.c.setFont('Courier', 14)
        self.c.drawString(30, 750, 'Cuentas')

        line_number = 735
        decrease = 15
        self.c.setFont('Courier', 11)
        for acc in self.accounts:
            self.c.drawString(35, line_number, "%s (%s): $%.2f" % \
                (acc.name, acc.currency, acc.balance))
            line_number = line_number - decrease

        self.l = line_number
        self.l -= 20
        self.c.setFont('Courier', 14)
        self.c.drawString(30, self.l, 'Totales por moneda')
        self.l -= 15
        self.c.setFont('Courier', 11)

        totals = self.__get_totals_by_currency()
        decrease = 15
        for currency, amount in totals.iteritems():
            self.c.drawString(35, self.l, '%s: $%.2f' % \
                (currency, amount))
            self.l -= decrease

    def __translate_type(self, tipo):
        types = dict()
        types['income']   = 'ingreso'
        types['expense']  = 'gasto'
        types['transfer'] = 'tranferencia'

        return types[tipo]
 
    def __transactions(self):
        self.l -= 20
        self.c.setFont('Courier', 14)
        self.c.drawString(30, self.l, 'Movimientos')

        decrease = 15
        self.l -= 15
        self.c.setFont('Courier', 10)
        for tra in self.transactions:
            tipo = self.__translate_type(tra.t_type)
            if tipo == 'ingreso':
                self.c.setFillColorRGB(0,255,0)
            elif tipo == 'gasto':
                self.c.setFillColorRGB(255,0,0)
            elif tipo == 'tranferencia':
                self.c.setFillColorRGB(0,0,255)
            self.c.drawString(35, self.l, '%s %s %s $%.2f | %s' % \
                (tra.date, tipo.upper(), tra.account,
                 tra.amount, tra.description))
            self.l -= decrease

    def generate_report(self):
        self.__prepare_document()
        self.__generate_header()
        self.__accounts_amount()
        self.__transactions()
        self.c.save()
