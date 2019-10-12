class Client(object):

    def __init__(self, name, account_numbers):
        super(Client, self).__init__()
        self.name = name
        self.account_numbers = account_numbers if isinstance(account_numbers, list) else [account_numbers]
        self.accounts = []

    def has_account_number(self, account_number):
        return account_number in self.account_numbers

    def get_account(self, account_number):
        return next((a for a in self.accounts if a.account_number == account_number), None)

    def add_account(self, account):
        self.accounts.append(account)

    @property
    def total_in(self):
        return sum(a.total_in for a in self.accounts)

    @property
    def total_out(self):
        return sum(a.total_out for a in self.accounts)

    def __str__(self):
        return "Client({})".format(self.name)

    def __repr__(self):
        return "Client({})".format(self.name)


class Account(object):

    def __init__(self, account_number, desc):
        super(Account, self).__init__()
        self.account_number = account_number
        self.desc = desc
        self.total_in = 0
        self.total_out = 0

    def add_transaction(self, date, code, in_out, amount, mutation, notes):
        if in_out == 'Bij':
            self.total_in += amount
        if in_out == 'Af':
            self.total_out += amount

    def __eq__(self, other):
        return self.account_number == other.account_number

    def __str__(self):
        return "Account({}, {})".format(self.account_number, self.desc)

    def __repr__(self):
        return "Account({})".format(self.account_number)


