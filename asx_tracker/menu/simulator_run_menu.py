from asx_tracker.database.database import Database
from asx_tracker.menu.menu import Menu
from asx_tracker.printer import Printer
from asx_tracker.str_format import StrFormat
from asx_tracker.table import Table
from asx_tracker.date import Date
from asx_tracker.utils import Utils
from asx_tracker.holding_list import HoldingList
from asx_tracker.order_list import OrderList

class SimulatorRunMenu(Menu):

    # Constructor

    def __init__(self, **kwargs):
        super().__init__(options=[
            'Buy or Sell',
            'Cancel order',
            'Visualise',
            'Advance',
            'Save',
            'End'
        ])

        # Settings
        self.now = kwargs['start']
        self.broke = kwargs['broke']
        self.balance = kwargs['balance']
        self.delay = kwargs['delay']
        self.step_min = kwargs['step_min']
        self.cgt = kwargs['cgt']

        self.holdings = HoldingList()
        self.orders = OrderList()
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

        delay_date = self.now - self.delay * Date.MINUTE
        total_cash = f'Cash:\t\t{StrFormat.int100_to_currency_str(self.balance)}'
        total_asx = f'ASX holdings:\t{"$17,005.31"}'
        total = f'Total:\t\t{"$27,005.31"}'
        self.subtitle = total_cash + '\n' + total_asx + '\n' + total
        if self.holdings:
            self.subtitle += '\n\nASX holdings:\n' + Table.holdings(self.holdings, delay_date)
        if self.orders:
            self.subtitle += '\n\nPending orders:\n' + Table.orders(self.orders)


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
        if option == 6:
            return controller.pop()
        print()
        if option == 1:
            self.buy_sell()
        elif option == 2:
            self.cancel_order()
        elif option == 3:
            self.visualise()
        elif option == 4:
            self.advance()
        else:
            self.save()
        self.set_title()
        self.set_subtitle()
        controller.display()


    # Buy / Sell

    def buy_sell(self):
        """
        Handles buy or sell trades
        """

        # Order type
        order_types = OrderList.ORDER_TYPES + ['Back']
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
        if not Utils.is_int(units):
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

        OrderList.TYPE_MARKET_BUY
        options = [f"Cancel {a[1]} {a[0]} x {a[2]} @ {OrderList.MARKET_PRICE if a[3] is None else StrFormat.int100_to_currency_str(a[3])}" for a in self.orders] + ['Back']
        Printer.options(options)
        option = Menu.select_option(options)
        if option == len(options):
            return
        self.orders.remove(option-1)


    # Visualise

    def visualise(self):

        # Ticker
        ticker = input('Enter Ticker: ').strip().upper()
        if not Database.fetch_single_listing(ticker, Database.COL_TICKER):
            return Printer.ack(f'{ticker} is not valid')

        print()
        options = ['1 Day', '5 Days', '1 Month', '6 Months', '1 Year', '5 Years', 'Max']
        Printer.options(options)
        option = Menu.select_option(options)


        raise NotImplementedError()


    # Advance

    def advance(self):
        """
        Advances the simulator date
        """

        nxt = min(self.now + self.step_min * Date.MINUTE, Date.MAX)
        # NOTE: Handle orders here between now and nxt
        self.now = nxt


    # Save

    def save(self):
        raise NotImplementedError()


    # Internal

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

        self._market_order(ticker, units, OrderList.TYPE_MARKET_BUY)


    def _market_sell(self, ticker, units):
        """
        Adds a market sell order to the order list.
        See SimulatorRunMenu._market_buy
        """

        self._market_order(ticker, units, OrderList.TYPE_MARKET_SELL)


    def _limit_buy(self, ticker, units):
        """
        Adds a limit buy order to the order list.
        See SimulatorRunMenu._market_buy
        """

        self._limit_order(ticker, units, OrderList.TYPE_LIMIT_BUY)


    def _limit_sell(self, ticker, units):
        """
        Adds a limit sell order to the order list.
        See SimulatorRunMenu._market_buy
        """

        self._limit_order(ticker, units, OrderList.TYPE_LIMIT_SELL)


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
            OrderList.TYPE_MARKET_BUY : Market buy order
            OrderList.TYPE_MARKET_SELL : Market sell order
        """

        message = f'Confirm {order_type} {ticker} x {units} @ {OrderList.MARKET_PRICE} ({StrFormat.int100_to_currency_str(self.broke)} brokerage)'
        if Utils.confirm(message):
            self.orders.add(ticker, order_type, units)


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
            OrderList.TYPE_LIMIT_BUY : Limit buy order
            OrderList.TYPE_LIMIT_SELL : Limit sell order
        """

        txt = input('Enter limit price: ')
        val = StrFormat.currency_str_to_int100(txt, non_neg=True)
        print()
        message = f'Confirm {order_type} {ticker} x {units} @ {StrFormat.int100_to_currency_str(val)} ({StrFormat.int100_to_currency_str(self.broke)} brokerage)'
        if Utils.confirm(message):
            self.orders.add(ticker, order_type, units, val)