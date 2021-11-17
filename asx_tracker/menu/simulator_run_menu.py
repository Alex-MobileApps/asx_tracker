from asx_tracker.database.database import Database
from asx_tracker.menu.menu import Menu
from asx_tracker.printer import Printer
from asx_tracker.str_format import StrFormat
from asx_tracker.table import Table
from asx_tracker.date import Date
from asx_tracker.transaction import Transaction
from asx_tracker.utils import Utils
from asx_tracker.holding_list import HoldingList
from asx_tracker.order_list import OrderList
from asx_tracker.transaction_list import TransactionList
from asx_tracker.order import Order
from asx_tracker.plot import Plot

class SimulatorRunMenu(Menu):

    # Constructor

    def __init__(self, **kwargs):
        super().__init__(options=[
            'Buy or Sell',
            'Cancel order',
            'Visualise',
            'Add / remove cash',
            'Advance',
            'Advance to date',
            'Pay Tax',
            'Transaction history',
            'End'
        ])

        # Settings
        self.now = kwargs['start']
        self.broke = kwargs['broke']
        self.balance = kwargs['balance']
        self.delay = kwargs['delay']
        self.step_min = kwargs['step_min']
        self.cgt = kwargs['cgt']
        self.tax = 0

        self.holdings = HoldingList()
        self.orders = OrderList()
        self.transactions = TransactionList()
        self.set_title()
        self.set_subtitle()


    # Menu title

    def set_title(self):
        """
        Sets the main menu's title
        """

        self.title = Date.timestamp_to_date_str(self.now)


    # Menu subtitle

    def set_subtitle(self):
        """
        Sets the main menu's subtitle
        """

        # Tickers and amounts
        holdings_tickers = self.holdings.tickers()
        orders_tickers = self.orders.tickers()
        tickers = list(set(holdings_tickers + orders_tickers))
        prices = Database.fetch_multiple_live_prices(self._delayed_time(), *tickers)
        asx_value = sum([self.holdings[t].units * prices[t] for t in holdings_tickers])

        # Subtitle
        total_cash = f'Cash:\t\t{StrFormat.int100_to_currency_str(self.balance)}'
        total_asx = f'ASX holdings:\t{StrFormat.int100_to_currency_str(asx_value)}'
        total = f'Total:\t\t{StrFormat.int100_to_currency_str(self.balance + asx_value)}'
        tax = f'Tax owed:\t{StrFormat.int100_to_currency_str(self.tax)}'
        self.subtitle = total_cash + '\n' + total_asx + '\n' + total + '\n' + tax
        if self.holdings:
            self.subtitle += '\n\nASX holdings:\n' + Table.holdings(self.holdings, prices)
        if self.orders:
            self.subtitle += '\n\nPending orders:\n' + Table.orders(self.orders, prices)


    # Menu options

    def handle_option(self, controller):
        """
        Handles selection of a menu option

        Parameters
        ----------
        controller : Controller
            Controller that is managing the program
        """

        option = Menu.select_option(self.options)
        if option == 9:
            return controller.pop()
        print()
        if option == 1:
            self.buy_sell()
        elif option == 2:
            self.cancel_order()
        elif option == 3:
            self.visualise()
        elif option == 4:
            self.add_remove_cash()
        elif option == 5:
            self.advance()
        elif option == 6:
            self.advance_to_date()
        elif option == 7:
            self.pay_tax()
        elif option == 8:
            self.transaction_history()
        self.set_title()
        self.set_subtitle()
        controller.display()


    # Buy / Sell

    def buy_sell(self):
        """
        Handles buy or sell trades
        """

        # Order type
        order_types = Order.ORDER_TYPES + ['Back']
        Printer.options(order_types)
        order_type = Menu.select_option(order_types)
        if order_type == 5:
            return

        # Ticker
        print()
        ticker = input('Enter Ticker: ').strip().upper()
        if not Database.fetch_single_listing(ticker, Database.COL_TICKER):
            return Printer.ack(f'{ticker} is not a valid Ticker')

        # Units
        print()
        units = input('Number of units: ')
        if not Utils.is_int(units) or int(units) < 0:
            return Printer.ack(f'{units} is not a valid number of units')
        units = int(units)

        # Handle order
        print()
        if order_type == 1:
            self._market_buy(ticker, units)
        elif order_type == 2:
            self._market_sell(ticker, units)
        elif order_type == 3:
            self._limit_buy(ticker, units)
        else:
            self._limit_sell(ticker, units)


    # Cancel order

    def cancel_order(self):
        """
        Cancels an active order
        """

        options = [f'Cancel {order}' for order in self.orders] + ['Back']
        Printer.options(options)
        option = Menu.select_option(options)
        if option == len(options):
            return
        idx = option - 1
        order = self.orders[idx]
        print()
        if Utils.confirm(f'Confirm cancel {order}'):
            self.transactions.add(Transaction(self.now, order, status=Transaction.STATUS_CANCELLED))
            self.orders.remove(idx)


    # Visualise

    def visualise(self):

        # Ticker
        ticker = input('Enter Ticker: ').strip().upper()
        if not Database.fetch_single_listing(ticker, Database.COL_TICKER):
            return Printer.ack(f'{ticker} is not valid')
        print()
        options = Plot.PERIOD_OPTIONS + ['Back']
        Printer.options(options)
        option = Menu.select_option(options)
        if option == 9:
            return
        args = (ticker, self._delayed_time())
        if option == 1:
            Plot.period_1d(*args)
        elif option == 2:
            Plot.period_1w(*args)
        elif option == 3:
            Plot.period_1m(*args)
        elif option == 4:
            Plot.period_6m(*args)
        elif option == 5:
            Plot.period_ytd(*args)
        elif option == 6:
            Plot.period_1y(*args)
        elif option == 7:
            Plot.period_2y(*args)
        elif option == 8:
            Plot.period_max(*args)


    # Add / remove cash

    def add_remove_cash(self):
        txt = input('Add/remove cash: ')
        val = StrFormat.currency_str_to_int100(txt)
        if val is None:
            return Printer.ack(f'{txt} is not valid')
        print()
        if Utils.confirm(f'Confirm change cash balance by {StrFormat.int100_to_currency_str(val)}'):
            self.balance += val


    # Advance

    def advance(self):
        """
        Advances the simulator by the step interval
        """

        self._advance_and_fill(self.now + self.step_min * Date.MINUTE)


    # Advance to date

    def advance_to_date(self):
        """
        Advances the simulator to a specific date
        """

        txt = input('Advance to date: ')
        val = StrFormat.date_str_to_timestamp(txt)
        if val is None:
            return Printer.ack(f'{txt} is not valid')
        self._advance_and_fill(val)


    # Pay tax

    def pay_tax(self):
        """
        Handles the remaining tax balance
        """

        if self.tax > self.balance:
            return Printer.ack(f'Insufficient funds')
        self.balance -= self.tax
        self.tax = 0


    # Transaction history

    def transaction_history(self):
        """
        Prints the history of completed transactions
        """

        history = Table.transactions(self.transactions)
        print('Transaction history:')
        print(history)
        print()
        Printer.ack('')


    # Internal


    def _delayed_time(self):
        """
        Returns the delayed simulator time

        Returns
        -------
        int
            Timestamp of delayed time
        """

        return self.now - self.delay * Date.MINUTE


    def _market_buy(self, ticker, units):
        """
        Adds a market buy order to the order list

        Parameters
        ----------
        ticker : str
            Ticker name
        units : int
            Number of units
        """

        self._market_order(ticker, units, Order.TYPE_MARKET_BUY)


    def _market_sell(self, ticker, units):
        """
        Adds a market sell order to the order list.
        See SimulatorRunMenu._market_buy
        """

        self._market_order(ticker, units, Order.TYPE_MARKET_SELL)


    def _limit_buy(self, ticker, units):
        """
        Adds a limit buy order to the order list.
        See SimulatorRunMenu._market_buy
        """

        self._limit_order(ticker, units, Order.TYPE_LIMIT_BUY)


    def _limit_sell(self, ticker, units):
        """
        Adds a limit sell order to the order list.
        See SimulatorRunMenu._market_buy
        """

        self._limit_order(ticker, units, Order.TYPE_LIMIT_SELL)


    def _market_order(self, ticker, units, order_type):
        """
        Adds a market order to the order list

        Parameters
        ----------
        ticker : str
            Ticker name
        units : int
            Number of units
        order_type : str
            Order.TYPE_MARKET_BUY : Market buy order
            Order.TYPE_MARKET_SELL : Market sell order
        """

        order = Order(ticker, order_type, units)
        message = f'Confirm {order} ({StrFormat.int100_to_currency_str(self.broke)} brokerage)'
        if Utils.confirm(message):
            self.orders.add(order)


    def _limit_order(self, ticker, units, order_type):
        """
        Adds a limit order to the order list

        Parameters
        ----------
        ticker : str
            Ticker name
        units : int
            Number of units
        order_type : str
            Order.TYPE_LIMIT_BUY : Limit buy order
            Order.TYPE_LIMIT_SELL : Limit sell order
        """

        txt = input('Enter limit price: ')
        val = StrFormat.currency_str_to_int100(txt, non_neg=True)
        print()
        order = Order(ticker, order_type, units, val)
        message = f'Confirm {order} ({StrFormat.int100_to_currency_str(self.broke)} brokerage)'
        if Utils.confirm(message):
            self.orders.add(order)


    def _advance_and_fill(self, date):
        """
        Handles advancing to a date and filling orders

        Parameters
        ----------
        date : int
            Timestamp of date to advance to
        """

        # End date
        nxt = min(Date.MAX, date)
        if not Date.market_open(nxt):
            nxt = Date.timestamp_next_open(nxt)

        while self.now < nxt:

            # Market closed
            if not Date.market_open(self.now):
                self.now = Date.timestamp_next_open(self.now)

            # No orders
            elif len(self.orders) == 0:
                self.now = nxt

            # Fill orders
            else:
                tickers = self.orders.tickers()
                prices = Database.fetch_multiple_live_prices(self.now, *tickers)
                self._fill_all_orders(prices)
                self.now += Date.MINUTE


    def _fill_all_orders(self, prices):
        """
        Attempt to fill all orders in the order list

        Parameters
        ----------
        prices : dict
            Live price for each ticker in the order list
        """

        filled = []
        for i, order in enumerate(self.orders):
            price = prices[order.ticker]
            if price is None:
                continue # No previous entry
            transaction = self._fill_single_order(order, price)
            if transaction is not None:
                self.transactions.add(transaction)
                filled.append(i)
        for i in reversed(filled):
            self.orders.remove(i)


    def _fill_single_order(self, order, price):
        """
        Attempt to fill a single order

        Parameters
        ----------
        order : Order
            Order to fill
        price : int
            Live price for the ticker in the order

        Returns
        -------
        Transaction or None
            Transaction if order filled successfully, else None
        """

        if order.order_type == Order.TYPE_MARKET_BUY:
            return self._fill_market_buy(order, price)
        elif order.order_type == Order.TYPE_MARKET_SELL:
            return self._fill_market_sell(order, price)
        elif order.order_type == Order.TYPE_LIMIT_BUY:
            return self._fill_limit_buy(order, price)
        else:
            return self._fill_limit_sell(order, price)


    def _fill_market_buy(self, order, price):
        """
        Attempt to fill a market buy order.
        See SimulatorRunMenu._fill_single_order
        """

        gross = order.units * price + self.broke
        transaction = Transaction(self.now, order, price)
        if gross <= self.balance:
            self.balance -= gross
            self.holdings.add(order.ticker, order.units, price)
            return Transaction(self.now, order, price, gross, status=Transaction.STATUS_SUCCESSFUL)
        return Transaction(self.now, order, price, status=Transaction.STATUS_FAILED)


    def _fill_market_sell(self, order, price):
        """
        Attempt to fill a market sell order.
        See SimulatorRunMenu._fill_single_order
        """

        gross = order.units * price - self.broke
        if order.ticker in self.holdings.items and order.units <= self.holdings[order.ticker].units:
            buy_price = self.holdings[order.ticker].unit_price * order.units
            tax = self._cgt_amount(buy_price, gross)
            self.tax += tax
            self.balance += gross
            self.holdings.remove(order.ticker, order.units)
            return Transaction(self.now, order, price, gross, tax, status=Transaction.STATUS_SUCCESSFUL)
        return Transaction(self.now, order, price, status=Transaction.STATUS_FAILED)


    def _fill_limit_buy(self, order, price):
        """
        Attempt to fill a limit buy order.
        See SimulatorRunMenu._fill_single_order
        """

        # Not at limit
        if price > order.price:
            return

        # At limit
        gross = order.units * price + self.broke
        if gross <= self.balance:
            self.balance -= gross
            self.holdings.add(order.ticker, order.units, price)
            return Transaction(self.now, order, price, gross, status=Transaction.STATUS_SUCCESSFUL)


    def _fill_limit_sell(self, order, price):
        """
        Attempt to fill a limit sell order.
        See SimulatorRunMenu._fill_single_order
        """

        # Not at limit
        if price < order.price:
            return

        # At limit
        gross = order.units * price - self.broke
        if order.ticker in self.holdings.items and order.units <= self.holdings[order.ticker].units:
            buy_price = self.holdings[order.ticker].unit_price * order.units
            tax = self._cgt_amount(buy_price, gross)
            self.tax += tax
            self.balance += gross
            self.holdings.remove(order.ticker, order.units)
            return Transaction(self.now, order, price, gross, tax, status=Transaction.STATUS_SUCCESSFUL)


    def _cgt_amount(self, buy, sell):
        """
        Returns the Capital Gains Tax amount for a profit or loss

        Parameters
        ----------
        buy : int
            Buy price
        sell : int
            Sell price

        Returns
        -------
        int
            Capital Gains Tax amount
        """

        profit = sell - buy
        return int(round(profit * self.cgt / 100))