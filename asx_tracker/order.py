class Order():

    # Static variables

    TYPE_MARKET_BUY     = 'Market BUY'
    TYPE_MARKET_SELL    = 'Market SELL'
    TYPE_LIMIT_BUY      = 'Limit BUY'
    TYPE_LIMIT_SELL     = 'Limit SELL'
    MARKET_PRICE        = 'MARKET'
    ORDER_TYPES         = [TYPE_MARKET_BUY, TYPE_MARKET_SELL, TYPE_LIMIT_BUY, TYPE_LIMIT_SELL]


    # Constructor

    def __init__(self, ticker, order_type, units, price=None):
        self.set_ticker(ticker)
        self.set_order_type(order_type)
        self.set_units(units)
        self.set_price(price)


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


    def set_order_type(self, order_type):
        """
        Set order type

        Parameters
        ----------
        order_type : str
            Order.TYPE_MARKET_BUY : Market buy order
            Order.TYPE_MARKET_SELL : Market sell order
            Order.TYPE_LIMIT_BUY : Limit buy order
            Order.TYPE_LIMIT_SELL : Limit sell order

        Raises
        ------
        ValueError
            Invalid order type
        """

        if order_type in Order.ORDER_TYPES:
            self.order_type = order_type
        else:
            raise ValueError('Invalid order type')


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


    def set_price(self, price):
        """
        Set limit price

        Parameters
        ----------
        price : int
            Limit price x100

        Raises
        ------
        ValueError
            Negative limit price
        """

        if price is None or price >= 0:
            self.price = price
        else:
            raise ValueError('Negative limit price')