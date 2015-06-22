
class Budget( object ):

    def __init__(self, name, spent, limit, balance):
        self.name = name
        self.spent = "%.2f" % spent
        self.limit = "%.2f" % limit
        self.balance = "%.2f" % balance

    def __str__(self):
        string = "<Budget(name=%s, spent=%.2f" % \
            (self.name, self.spent)
        string += ", limit=%.2f, balance=%.2f" % \
            (self.limit, self.balance)
        return string
