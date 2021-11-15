class HoldingList():

    # Constructor

    def __init__(self):
        self.items = {}


    # Length

    def __len__(self):
        return len(self.items)


    # Index

    def __getitem__(self, ticker):
        return self.items[ticker]


    # Functions

    def add(self, ticker, units):
        """
        Add a number of units to the holdings

        Parameters
        ----------
        ticker : str
            Ticker name
        units : int
            Number of units
        """

        if units < 0:
            return
        if ticker in self.items:
            self.items[ticker] += units
        else:
            self.items[ticker] = units


    def remove(self, ticker, units):
        """
        Remove a number of units from the holdings

        Parameters
        ----------
        ticker : str
            Ticker name
        units : int
            Number of units
        """

        if units < 0 or ticker not in self.items:
            return
        old_units = self.items[ticker]
        if old_units == units:
            del self.items[ticker]
        elif old_units > units:
            self.items[ticker] -= units


    def tickers(self):
        """
        Returns a sorted list of tickers in the holding list

        Returns
        -------
        list
            List of tickers
        """

        return sorted(self.items.keys())