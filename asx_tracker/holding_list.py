from asx_tracker.holding import Holding

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

    def add(self, ticker, units, unit_price):
        """
        Add a holding to the holding list

        Parameters
        ----------
        ticker : str
            Ticker name
        units : int
            Number of units
        unit_price
            Unit price x100

        Returns
        -------
        bool
            Whether or not the add was successful
        """

        if ticker in self.items:
            self.items[ticker].add(units, unit_price)
        else:
            self.items[ticker] = Holding(ticker, units, unit_price)
        return True



    def remove(self, ticker, units):
        """
        Remove a number of units from a holding in the holding list

        Parameters
        ----------
        ticker : str
            Ticker name
        units : int
            Number of units

        Returns
        -------
        bool
            Whether or not the remove was successful
        """

        if ticker not in self.items or self.items[ticker].units < units:
            return False
        if self.items[ticker].units == units:
            del self.items[ticker]
        else:
            self.items[ticker].units -= units
        return True


    def tickers(self):
        """
        Returns a sorted list of tickers in the holding list

        Returns
        -------
        list
            List of tickers
        """

        return sorted(self.items.keys())