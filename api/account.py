
class Account( object ):

    def __init__(self, currency=None, balance=None, 
        id=None, bank=None, name=None):
        self.currency = currency
        self.balance  = balance
        self.id       = id
        self.bank     = bank.encode('utf-8')
        self.name     = name.encode('utf-8')

    def __str__(self):
        string = "<Account(currency=%s, balance=%s, id=%s, " % \
            (self.currency,
             self.balance,
             self.id)
        string += "bank=%s, name=%s)>" % (self.bank, self.name)

        return string 