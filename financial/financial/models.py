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
        self.transactions = []

    @property
    def credit_transactions(self):
        return sorted([t for t in self.transactions if t.credit])

    @property
    def debit_transactions(self):
        return sorted([t for t in self.transactions if t.debit])

    def add_transaction(self, date, code, in_out, amount, desc, mutation, notes):
        transaction = Transaction(date, code, in_out, amount, desc, mutation, notes)
        self.transactions.append(transaction)
        if transaction.credit:
            self.total_in += amount
        if transaction.debit:
            self.total_out += amount

    def write(self, per_month=False):
        print(self)
        if per_month:
            current_month = None
            month_sum = 0
            for t in self.debit_transactions:
                month = t.date.strftime("%Y-%m")
                if current_month is None:
                    current_month = month
                if current_month != month:
                    print("{}: {}".format(current_month, month_sum))
                    current_month = month
                    month_sum = 0
                month_sum += t.amount
                # print(t)
            print("{}: {}".format(current_month, month_sum))

    def __eq__(self, other):
        return self.account_number == other.account_number

    def __str__(self):
        return "Account({}, {})".format(self.account_number, self.desc)

    def __repr__(self):
        return "Account({})".format(self.account_number)


class Transaction(object):

    def __init__(self, date, code, in_out, amount, desc, mutation, notes):
        self.date = date
        self.code = code
        self.in_out = in_out
        self.amount = amount
        self.desc = desc
        self.mutation = mutation
        self.notes = notes

    @property
    def credit(self):
        return self.in_out in ["Bij", 'Credit']

    @property
    def debit(self):
        return self.in_out in ["Af", 'Debit']

    def __lt__(self, other):
        return self.date < other.date

    def __str(self):
        return "T( {}, {}, {}, {} {} )".format(self.date, self.code, self.in_out, self.amount, self.desc)

    def __repr__(self):
        return self.__str()