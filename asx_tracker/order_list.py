from asx_tracker.order import Order

class OrderList():

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

    def add(self, order):
        """
        Add an order to the order list

        Parameters
        ----------
        order : Order
            Order to add
        """

        self.items.append(order)
        self._resort()


    def remove(self, idx):
        """
        Remove an order from the order list

        Parameters
        ----------
        idx : int
            Order index in the order list
        """

        if idx < 0 or idx >= len(self.items):
            return
        self.items.pop(idx)


    def tickers(self):
        """
        Returns a sorted list of tickers in the order list

        Returns
        -------
        list
            List of tickers
        """

        return sorted(set([order.ticker for order in self.items]))


    # Internal

    def _resort(self):
        """
        Resorts the order list in preference order
        """

        orders = {}
        order_pref = [Order.TYPE_MARKET_SELL, Order.TYPE_LIMIT_SELL, Order.TYPE_MARKET_BUY, Order.TYPE_LIMIT_BUY]
        for k in order_pref:
            orders[k] = []
        for order in self.items:
            orders[order.order_type].append(order)
        self.items = []
        for k in order_pref:
            self.items += orders[k]