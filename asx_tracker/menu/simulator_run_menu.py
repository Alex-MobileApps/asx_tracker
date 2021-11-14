from asx_tracker.database.database import Database
from asx_tracker.menu.menu import Menu
from asx_tracker.printer import Printer
from asx_tracker.str_format import StrFormat
from asx_tracker.table import Table
from asx_tracker.date import Date
from asx_tracker.utils import Utils

class SimulatorRunMenu(Menu):

    # Static variables

    _HEADER_HOLDINGS = ['Ticker','Units','Unit price']
    _HEADER_LIMITS = ['Ticker','Type','Units','Limit price','Current price','Status']
    _ORDER_TYPES = ['Market BUY','Market SELL','Limit BUY','Limit SELL','Back']


    # Constructor

    def __init__(self, **kwargs):
        super().__init__(options=[
            'Buy or Sell',
            'Cancel limit order',
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
        self.holdings = []
        self.limits = []

        # Limits demo
        self.limits = [
            ('DHHF', 'BUY', 150, 2950),
            ('VDHG', 'SELL', 30, 6300)
        ]

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

        holdings_table = Table.table(header=SimulatorRunMenu._HEADER_HOLDINGS, rows=self._holdings_to_rows())
        limits_table = Table.table(header=SimulatorRunMenu._HEADER_LIMITS, rows=self._limits_to_rows())
        total_cash = f'Cash:\t\t{StrFormat.int100_to_currency_str(self.balance)}'
        total_asx = f'ASX holdings:\t{"$17,005.31"}'
        total = f'Total:\t\t{"$27,005.31"}'
        self.subtitle = total_cash + '\n' + total_asx + '\n' + total
        if self.holdings:
            self.subtitle += '\n\nASX holdings:\n' + holdings_table
        if self.limits:
            self.subtitle += '\n\nActive limit orders:\n' + limits_table


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
            self.cancel_limit_order()
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
        Printer.options(SimulatorRunMenu._ORDER_TYPES)
        order_type = Menu.select_option(SimulatorRunMenu._ORDER_TYPES)
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
        if order_type == 1:
            self._market_buy(ticker, units)
        elif order_type == 2:
            self._market_sell(ticker, units)
        elif order_type == 3:
            self._limit_buy(ticker, units)
        else:
            self._limit_sell(ticker, units)


    # Cancel limit order

    def cancel_limit_order(self):
        """
        Cancels an active limit order
        """

        options = [f'Cancel {l[1]} {l[0]} x {l[2]} @ {StrFormat.int100_to_currency_str(l[3])}' for l in self.limits] + ['Back']
        Printer.options(options)
        option = Menu.select_option(options)
        if option == len(options):
            return
        self.limits.pop(option-1)


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
        # NOTE: Handle limit orders here between now and nxt
        self.now = nxt


    # Save

    def save(self):
        raise NotImplementedError()


    # Internal

    def _market_buy(self, ticker, units):
        """
        Handles market buy orders

        Parameters
        ----------
        ticker : str
            Ticker name
        units : int
            Number of units to purchase
        """

        # Get price
        unit_price = Database.fetch_single_live_price(ticker, self.now)
        if unit_price is None:
            return Printer.ack('No recent unit price')
        price = unit_price * units + self.broke

        # Insufficient funds
        if price > self.balance:
            return Printer.ack('Insufficient funds')

        # Buy
        print()
        message = f'Confirm Market BUY {ticker} x {units} @ {StrFormat.int100_to_currency_str(unit_price)} + {StrFormat.int100_to_currency_str(self.broke)} brokerage = {StrFormat.int100_to_currency_str(price)}'
        if Utils.confirm(message):
            self.balance -= price
            self.holdings.append((ticker,units))


    def _market_sell(self, ticker, units):
        raise NotImplementedError()


    def _limit_buy(self, ticker, units):
        raise NotImplementedError()


    def _limit_sell(self, ticker, units):
        raise NotImplementedError


    def _holdings_to_rows(self):
        """
        Converts the current holdings to a format that can input into a table

        Returns
        -------
        list
            List of tuples with cells for each row in the table
        """

        return [(r[0], str(r[1]), '$39.24') for r in self.holdings]


    def _limits_to_rows(self):
        """
        Converts the current limit orders to a format that can input into a table

        Returns
        -------
        list
            List of tuples with cells for each row in the table
        """

        limits = [None] * len(self.limits)
        for i, l in enumerate(self.limits):
            l1 = l[0]
            l2 = l[1]
            l3 = str(l[2])
            l4 = StrFormat.int100_to_currency_str(l[3])
            l5 = '$99.99'
            l6 = 'PENDING'
            limits[i] = (l1,l2,l3,l4,l5,l6)
        return limits