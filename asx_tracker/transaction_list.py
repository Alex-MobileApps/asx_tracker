class TransactionList():

    # Constructor

    def __init__(self):
        self.items = []


    # Length

    def __len__(self):
        return len(self.items)


    # Index

    def __getitem__(self, idx):
        return self.items[idx]


    # Functions

    def add(self, transaction):
        """
        Add a transaction to the transaction list

        Parameters
        ----------
        transaction : Transaction
            Transaction to add
        """

        self.items.append(transaction)


    def remove(self, idx):
        """
        Remove a transaction from the transaction list

        Parameters
        ----------
        idx : int
            Transaction index in the transaction list
        """

        if idx < 0 or idx >= len(self.items):
            return
        self.items.pop(idx)