from asx_tracker.database.database import Database
from asx_tracker.str_format import StrFormat

class OrderList():

    # Static variables

    TYPE_MARKET_BUY     = 'Market BUY'
    TYPE_MARKET_SELL    = 'Market SELL'
    TYPE_LIMIT_BUY      = 'Limit BUY'
    TYPE_LIMIT_SELL     = 'Limit SELL'
    ORDER_TYPES = [TYPE_MARKET_BUY, TYPE_MARKET_SELL, TYPE_LIMIT_BUY, TYPE_LIMIT_SELL]


    # Constructor

    def __init__(self):
        self._orders = []


    # Length

    def __len__(self):
        return len(self._orders)


    # Index

    def __getitem__(self, idx):
        return self._orders[idx]


    # Functions

    def add(self, ticker, order_type, units, price=None):
        """
        Add an order to the order list

        Parameters
        ----------
        ticker : str
            Ticker name
        order_type : int
            OrderList.TYPE_MARKET_BUY : Market BUY order
            OrderList.TYPE_MARKET_SELL : Market SELL order
            OrderList.TYPE_LIMIT_BUY : Limit BUY order
            OrderList.TYPE_LIMIT_SELL : Limit SELL order
        units : int
            Number of units
        price : int, optional
            Limit order price, by default None
        """

        self._orders.append((ticker, order_type, units, price))
        self._resort()


    def remove(self, idx):
        """
        Remove an order from the order list

        Parameters
        ----------
        idx : int
            Order index in the order list
        """

        if idx < 0 or idx >= len(self._orders):
            return
        self._orders.pop(idx)


    # Internal

    def _resort(self):
        """
        Resorts the order list in preference order
        """

        orders = {}
        order_pref = [OrderList.TYPE_MARKET_SELL, OrderList.TYPE_LIMIT_SELL, OrderList.TYPE_MARKET_BUY, OrderList.TYPE_LIMIT_BUY]
        for k in order_pref:
            orders[k] = []
        for order in self._orders:
            k = order[1]
            orders[k].append(order)
        self._orders = []
        for k in order_pref:
            self._orders += orders[k]