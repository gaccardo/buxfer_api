import os
import math

from reportlab.pdfgen import canvas
from reportlab.graphics.shapes import Drawing
from reportlab.graphics.charts.piecharts import Pie
from reportlab.graphics.charts.legends import Legend
from reportlab.lib.colors import black, red, purple, green, \
    maroon, brown, pink, white, HexColor
from reportlab.graphics import renderPDF
from reportlab.platypus import Table, TableStyle
from reportlab.lib.units import cm
from reportlab.platypus import PageBreak
import datetime

import settings
from currency_calculator import CurrencyCalculator

class Reporter( object ):

    def __init__(self, accounts, transactions):
        self.accounts     = accounts
        self.transactions = transactions
        self.c            = None
        self.l            = 800

        cc = CurrencyCalculator()
        self.dolar = None
        try:
            self.dolar = cc.get_dolar()['real']
        except:
            self.dolar = settings.DOLAR

        self.pdf_chart_colors = [
            HexColor("#0000e5"),
            HexColor("#1f1feb"),
            HexColor("#5757f0"),
            HexColor("#8f8ff5"),
            HexColor("#c7c7fa"),
            HexColor("#f5c2c2"),
            HexColor("#eb8585"),
            HexColor("#e04747"),
            HexColor("#d60a0a"),
            HexColor("#cc0000"),
            HexColor("#ff0000"),
        ]

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
        self.c.drawString(495, 780, 'Dolar: $%.2f' % self.dolar)
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
        data = [['Cuenta', 'Moneda', 'Saldo']]

        self.l = 630
        
        for acc in self.accounts:
            data.append([acc.name, acc.currency, 
                '$%.2f' % acc.balance])

        t = Table(data)
        t.setStyle(TableStyle([('INNERGRID', (0,0), (-1,-1), 0.25, black),
            ('BOX', (0,0), (-1,-1), 0.25, black),
            ('FONTNAME', (0,0), (-1,0), 'Courier-Bold'),
            ('BACKGROUND', (0,0), (-1,0), HexColor('#efeded')),
            ('BACKGROUND', (0,0), (0,-1), HexColor('#efeded')),
            ('FONTSIZE', (0,0), (-1,0), 12),
            ('FONTSIZE', (0,1), (-1,-1), 8),
            ('FONTNAME', (0,1), (-1,-1), 'Courier')]))

        t.wrapOn(self.c, 30, self.l)
        t.drawOn(self.c, 30, self.l)

        self.l -= 20
        self.c.setFont('Courier', 14)
        self.c.drawString(30, self.l, 'Totales por moneda')
        self.l -= 63
        data2 = [['Moneda', 'Saldo']]

        totals = self.__get_totals_by_currency()
        for currency, amount in totals.iteritems():
            data2.append([currency, amount])

        t2 = Table(data2)
        t2.setStyle(TableStyle([('INNERGRID', (0,0), (-1,-1), 0.25, black),
            ('BOX', (0,0), (-1,-1), 0.25, black),
            ('FONTNAME', (0,0), (-1,0), 'Courier-Bold'),
            ('BACKGROUND', (0,0), (-1,0), HexColor('#efeded')),
            ('BACKGROUND', (0,0), (0,-1), HexColor('#efeded')),
            ('FONTSIZE', (0,0), (-1,0), 12),
            ('FONTSIZE', (0,1), (-1,-1), 8),
            ('FONTNAME', (0,1), (-1,-1), 'Courier')]))

        t2.wrapOn(self.c, 30, self.l)
        t2.drawOn(self.c, 30, self.l)

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

        header = ['Fecha', 'Tipo', 'Cuenta', 'Monto', 'Description']
        data = [header]

        for tra in self.transactions:
            tipo = self.__translate_type(tra.t_type)
            data.append([tra.date, tipo.upper(), tra.account,
                '$%.2f' % tra.amount, tra.description])

        registros = 24
        filas = len(data) / float(registros)
        coheficiente = math.ceil(len(data) / filas)
        look = 0
        datas = list()
        datas_new = list()

        while look < len(data):
            second = int(look+coheficiente)
            datas.append(data[look:second])
            look = int(look+coheficiente)

        datas_new.append(datas[0])

        for dd in datas[1:][::-1]:
            datas_new.append([header] + dd)

        data1 = datas_new[0]
        self.l -= len(data1) * 19
        t = Table(data1)
        t.setStyle(TableStyle([('INNERGRID', (0,0), (-1,-1), 0.25, black),
            ('BOX', (0,0), (-1,-1), 0.25, black),
            ('FONTNAME', (0,0), (-1,0), 'Courier-Bold'),
            ('BACKGROUND', (0,0), (-1,0), HexColor('#efeded')),
            ('BACKGROUND', (0,0), (0,-1), HexColor('#efeded')),
            ('FONTSIZE', (0,0), (-1,0), 12),
            ('FONTSIZE', (0,1), (-1,-1), 8),
            ('FONTNAME', (0,1), (-1,-1), 'Courier')]))
        t.wrapOn(self.c, 30, self.l)
        t.drawOn(self.c, 30, self.l)

        for dd in datas_new[1:][::-1]:
            p = PageBreak()
            p.drawOn(self.c, 0, 1000)
            self.c.showPage()
            self.l = 800 - (len(dd) * 19)

            t2 = Table(dd)
            t2.setStyle(TableStyle([('INNERGRID', (0,0), (-1,-1), 0.25, black),
                ('BOX', (0,0), (-1,-1), 0.25, black),
                ('FONTNAME', (0,0), (-1,0), 'Courier-Bold'),
                ('BACKGROUND', (0,0), (-1,0), HexColor('#efeded')),
                ('BACKGROUND', (0,0), (0,-1), HexColor('#efeded')),
                ('FONTSIZE', (0,0), (-1,0), 12),
                ('FONTSIZE', (0,1), (-1,-1), 8),
                ('FONTNAME', (0,1), (-1,-1), 'Courier')]))
            t2.wrapOn(self.c, 30, self.l)
            t2.drawOn(self.c, 30, self.l)

    def __add_graph(self):
        drawing = Drawing(200, 100)
        data = list()
        labels = list()

        self.c.drawString(370, 730, 
            'Distribucion en pesos'.encode('utf-8'))

        for acc in self.accounts:
            balance = acc.balance
            if acc.currency == 'USD':
                balance = balance * self.dolar

            data.append(balance)
            labels.append(acc.name)

        pie = Pie()
        pie.x = 280
        pie.y = 630
        pie.height = 100
        pie.width = 100
        pie.data = data
        pie.labels = labels
        pie.simpleLabels = 1
        pie.slices.strokeWidth = 1
        pie.slices.strokeColor = black
        pie.slices.label_visible = 0

        legend = Legend()
        legend.x = 400
        legend.y = 680
        legend.dx              = 8
        legend.dy              = 8
        legend.fontName        = 'Helvetica'
        legend.fontSize        = 7
        legend.boxAnchor       = 'w'
        legend.columnMaximum   = 10
        legend.strokeWidth     = 1
        legend.strokeColor     = black
        legend.deltax          = 75
        legend.deltay          = 10
        legend.autoXPadding    = 5
        legend.yGap            = 0
        legend.dxTextSpace     = 5
        legend.alignment       = 'right'
        legend.dividerLines    = 1|2|4
        legend.dividerOffsY    = 4.5
        legend.subCols.rpad    = 30
        n = len(pie.data)
        self.__setItems(n,pie.slices,
            'fillColor',self.pdf_chart_colors)

        legend.colorNamePairs = [(pie.slices[i].fillColor, 
            (pie.labels[i][0:20],'$%0.2f' % pie.data[i])) for i in xrange(n)]


        drawing.add(pie)
        drawing.add(legend)
        x, y = 0, 0
        renderPDF.draw(drawing, self.c, x, y, showBoundary=False)

    def __per_account_statistic(self):

        for acc in self.accounts:
            p = PageBreak()
            p.drawOn(self.c, 0, 1000)
            self.c.showPage()
            self.l = 760

            self.c.setFont('Courier', 14)
            self.c.drawString(30, 800, 'Cuenta: %s' % \
                acc.name)

            header = ['Fecha', 'Tipo', 'Monto', 'Description']
            data   = [header]
            g_data = list()
            g_labe = list()
            total  = 0

            for tra in self.transactions:
                if tra.account == acc.name:
                    if tra.t_type in ['expense', 'transfer']:
                        tipo = self.__translate_type(tra.t_type)
                        data.append([tra.date, tipo.upper(),
                            '$%2.f' % tra.amount, tra.description])
                        total += tra.amount

                        g_data.append(tra.amount)
                        g_labe.append(tra.description.encode('utf-8'))

            data.append(['TOTAL', '', '$%.2f' % total, ''])

            if len(g_data) == 0 or len(g_labe) == 0:
                self.c.setFont('Courier', 12)
                self.c.drawString(30, 770, 'Sin movimientos negativos')
                continue
 
            from_title = 35
            if len(data) != 2:
                self.l -= ((len(data) * len(data)) + len(data)) + from_title

            t = Table(data)
            t.setStyle(TableStyle([('INNERGRID', (0,0), (-1,-1), 0.25, black),
                ('BOX', (0,0), (-1,-1), 0.25, black),
                ('FONTNAME', (0,0), (-1,0), 'Courier-Bold'),
                ('BACKGROUND', (0,0), (-1,0), HexColor('#efeded')),
                ('BACKGROUND', (0,0), (0,-1), HexColor('#efeded')),
                ('FONTSIZE', (0,0), (-1,0), 12),
                ('FONTSIZE', (0,1), (-1,-1), 8),
                ('FONTNAME', (0,1), (-1,-1), 'Courier'),
                ('BACKGROUND', (0,-1), (-1,-1), red),
                ('TEXTCOLOR', (0,-1), (-1,-1), white)]))

            t.wrapOn(self.c, 30, self.l)
            t.drawOn(self.c, 30, self.l)

            drawing = Drawing(200, 100)

            pie = Pie()
            pie.x = 30
            pie.y = self.l - 300
            pie.height = 200
            pie.width = 200
            pie.data = g_data
            pie.labels = g_labe
            pie.simpleLabels = 1
            pie.slices.strokeWidth = 1
            pie.slices.strokeColor = black
            pie.slices.label_visible = 0
            pie.slices.popout        = 1
            #pie.labels   = map(str, pie.data)

            
            legend = Legend()
            legend.x = 250
            legend.y = self.l - 250
            legend.dx              = 8
            legend.dy              = 8
            legend.fontName        = 'Helvetica'
            legend.fontSize        = 7
            legend.boxAnchor       = 'w'
            legend.columnMaximum   = 10
            legend.strokeWidth     = 1
            legend.strokeColor     = black
            legend.deltax          = 75
            legend.deltay          = 10
            legend.autoXPadding    = 5
            legend.yGap            = 0
            legend.dxTextSpace     = 5
            legend.alignment       = 'right'
            legend.dividerLines    = 1|2|4
            legend.dividerOffsY    = 4.5
            legend.subCols.rpad    = 30
            n = len(pie.data)
            self.__setItems(n,pie.slices,
                'fillColor',self.pdf_chart_colors)

            legend.colorNamePairs = [(pie.slices[i].fillColor, 
                (pie.labels[i][0:20],'$%0.2f' % pie.data[i])) for i in xrange(n)]
            

            drawing.add(pie)
            drawing.add(legend)
            x, y = 0, 10

            renderPDF.draw(drawing, self.c, x, y, showBoundary=False)

    def __setItems(self, n, obj, attr, values):
        m = len(values)
        i = m // n
        for j in xrange(n):
            setattr(obj[j],attr,values[j*i % m])

    def __get_tags_statistics(self):
        monto_categorias = dict()
        for tra in self.transactions:
            if len(tra.tags) > 0:
                for tag in tra.tags:
                    if tag in monto_categorias.keys():
                        monto_categorias[tag] += tra.amount
                    else:
                        monto_categorias[tag] = tra.amount

        labels = [lab.encode('utf-8') for lab in monto_categorias.keys()]
        data = monto_categorias.values()

        p = PageBreak()
        p.drawOn(self.c, 0, 1000)
        self.c.showPage()
        self.l = 600

        self.c.setFont('Courier', 14)
        self.c.drawString(30, 800, 'Categorias')

        drawing = Drawing(200, 200)

        pie = Pie()
        pie.x = 30
        pie.y = self.l - 130
        pie.height = 300
        pie.width = 300
        pie.data = data
        pie.labels = labels
        pie.simpleLabels = 1
        pie.slices.strokeWidth = 1
        pie.slices.strokeColor = black
        pie.slices.label_visible = 0

        legend = Legend()
        legend.x = 400
        legend.y = self.l
        legend.dx              = 8
        legend.dy              = 8
        legend.fontName        = 'Helvetica'
        legend.fontSize        = 7
        legend.boxAnchor       = 'w'
        legend.columnMaximum   = 10
        legend.strokeWidth     = 1
        legend.strokeColor     = black
        legend.deltax          = 75
        legend.deltay          = 10
        legend.autoXPadding    = 5
        legend.yGap            = 0
        legend.dxTextSpace     = 5
        legend.alignment       = 'right'
        legend.dividerLines    = 1|2|4
        legend.dividerOffsY    = 4.5
        legend.subCols.rpad    = 30
        n = len(pie.data)
        self.__setItems(n,pie.slices,
            'fillColor',self.pdf_chart_colors)

        legend.colorNamePairs = [(pie.slices[i].fillColor, 
            (pie.labels[i][0:20],'$%0.2f' % pie.data[i])) for i in xrange(n)]

        drawing.add(pie)
        drawing.add(legend)
        x, y = 0, 10

        renderPDF.draw(drawing, self.c, x, y, showBoundary=False)

    def generate_report(self):
        self.__prepare_document()
        self.__generate_header()
        self.__accounts_amount()
        self.__add_graph()
        self.__transactions()
        self.__get_tags_statistics()
        self.__per_account_statistic()
        self.c.showPage()
        self.c.save()
