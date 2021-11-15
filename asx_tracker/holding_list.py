from asx_tracker.database.database import Database
from asx_tracker.str_format import StrFormat

class HoldingList():

    # Constructor

    def __init__(self):
        self._holdings = {}


    # Length

    def __len__(self):
        return len(self._holdings)


    # Index

    def __getitem__(self, ticker):
        return self._holdings[ticker]


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
        if ticker in self._holdings:
            self._holdings[ticker] += units
        else:
            self._holdings[ticker] = units


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

        if units < 0 or ticker not in self._holdings:
            return
        old_units = self._holdings[ticker]
        if old_units == units:
            del self._holdings[ticker]
        elif old_units > units:
            self._holdings[ticker] -= units


    def tickers(self):
        """
        Returns a sorted list of tickers in the holding list

        Returns
        -------
        list
            List of tickers
        """

        return sorted(self._holdings.keys())