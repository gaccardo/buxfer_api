import urllib2
from htmldom import htmldom

import settings

class CurrencyCalculator( object ):

    def get_dolar_from_argentinadolar(self):
        url = "http://argentinadolar.com/"

        site = urllib2.urlopen(url)
        data = site.read()
        site.close()

        dom = htmldom.HtmlDom().createDom(data)

        compra_raw = dom.domNodes['h3'][2].getText()
        compra_raw = compra_raw.split('$\n')[-1]
        compra_raw = compra_raw.replace(',','.')
        compra_raw = float(compra_raw)

        venta_raw = dom.domNodes['h3'][3].getText()
        venta_raw = venta_raw.split('$\n')[-1]
        venta_raw = venta_raw.replace(',','.')
        venta_raw = float(venta_raw)

        promedio = (compra_raw + venta_raw) / 2
        promedio = float('%.2f' % promedio)

        return {'compra': compra_raw, 'venta': venta_raw,
                'promedio': promedio, 'real': promedio-0.10}

    def get_dolar_from_dolarblue(self):
        url = "http://www.preciodolarblue.com.ar/"

        site = urllib2.urlopen(url)
        data = site.read()
        site.close()

        dom = htmldom.HtmlDom().createDom(data)

        compra_raw = dom.domNodes['td'][3].getText()
        compra_raw = float(compra_raw)

        venta_raw = dom.domNodes['td'][4].getText()
        venta_raw = float(venta_raw) 

        promedio = (compra_raw + venta_raw) / 2
        promedio = float('%.2f' % promedio)

        return {'compra': compra_raw, 'venta': venta_raw,
                'promedio': promedio, 'real': promedio-0.10}

    def get_dolar(self):
        dolar = getattr(self, 
            'get_dolar_from_%s' % settings.DOLAR_SOURCE)
        return dolar()
