class Holding():

    # Constructor

    def __init__(self, ticker, units, unit_price):
        self.set_ticker(ticker)
        self.set_units(units)
        self.set_unit_price(unit_price)


    # Setters

    def set_ticker(self, ticker):
        """
        Set ticker

        Parameters
        ----------
        ticker : str
            Ticker name
        """

        self.ticker = ticker


    def set_units(self, units):
        """
        Set number of units

        Parameters
        ----------
        units : int
            Number of units

        Raises
        ------
        ValueError
            Negative number of units
        """

        if units >= 0:
            self.units = units
        else:
            raise ValueError('Negative number of units')


    def set_unit_price(self, unit_price):
        """
        Set unit price

        Parameters
        ----------
        unit_price : int
            Unit price x100

        Raises
        ------
        ValueError
            Negative unit price
        """

        if unit_price is None or unit_price >= 0:
            self.unit_price = unit_price
        else:
            raise ValueError('Negative unit price')


    def add(self, units, unit_price):
        """
        Add a number of units to the holding

        Parameters
        ----------
        units : int
            Number of units
        unit_price
            Unit price x100
        """

        old_gross = self.units * self.unit_price
        add_gross = units * unit_price
        new_gross = old_gross + add_gross
        new_units = self.units + units
        self.units = new_units
        self.unit_price = new_gross / new_units
