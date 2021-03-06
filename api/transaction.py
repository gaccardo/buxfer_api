
class Transaction( object ):

    def __init__(self, description=None, account=None, 
        expense=None, amount=None, t_type=None, date=None,
        tags=None):
        self.description = description
        self.account     = account
        self.expense     = expense
        self.amount      = amount
        self.t_type      = t_type
        self.date        = date
        self.tags        = tags

    def __str__(self):
        string = "<Transaction(description=%s, account=%s, " % \
            (self.description, self.account)
        string += "expense=%s, amount=%s, t_type=%s, " % \
            (self.expense, self.amount, self.t_type)
        string += "date=%s, tags=%s)>" % (self.date, self.tags)

        return string
