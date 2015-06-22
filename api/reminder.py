
class Reminder( object ):

    def __init__(self, start_date, description, amount,
        id, account_id):
        self.start_date = start_date
        self.description = description
        self.amount = "%.2f" % amount
        self.id = id
        self.account_id = account_id

    def __str__(self):
        string = "<Reminder(start_date=%s" % start_date
        string += ", description=%s, amount=%2.f" % \
            (self.description, self.amount)
        string += ", id=%s, account_id=%s" % (self.id, 
            self.account_id)
        return string