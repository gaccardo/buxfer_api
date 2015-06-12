import urllib2
from htmldom import htmldom

import settings

class CurrencyCalculator( object ):

    def __get_dom(self, url):
        site = urllib2.urlopen(url)
        data = site.read()
        site.close()

        return htmldom.HtmlDom().createDom(data)

    def __return_data(self, compra, venta):
        promedio = (compra + venta) / 2
        promedio = float('%.2f' % promedio)

        return {'compra': compra, 'venta': venta,
                'promedio': promedio, 'real': promedio-0.10}

    def get_dolar_from_argentinadolar(self):
        url = "http://argentinadolar.com/"
        dom = self.__get_dom(url)

        compra = dom.domNodes['h3'][2].getText()
        compra = compra.split('$\n')[-1]
        compra = compra.replace(',','.')
        compra = float(compra)

        venta = dom.domNodes['h3'][3].getText()
        venta = venta.split('$\n')[-1]
        venta = venta.replace(',','.')
        venta = float(venta)

        return self.__return_data(compra, venta)

    def get_dolar_from_dolarblue(self):
        url = "http://www.preciodolarblue.com.ar/"
        dom = self.__get_dom(url)

        compra = dom.domNodes['td'][3].getText()
        compra = float(compra)

        venta = dom.domNodes['td'][4].getText()
        venta = float(venta) 

        return self.__return_data(compra, venta)

    def get_dolar(self):
        dolar = getattr(self, 
            'get_dolar_from_%s' % settings.DOLAR_SOURCE)
        return dolar()
