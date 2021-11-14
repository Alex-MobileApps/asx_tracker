from asx_tracker.menu.menu import Menu
from asx_tracker.str_format import StrFormat
from asx_tracker.table import Table
from asx_tracker.date import Date

class SimulatorRunMenu(Menu):

    # Static variables

    _HEADER_HOLDINGS = ['Ticker','Units','Unit price']
    _HEADER_LIMITS = ['Ticker','Type','Units','Limit price','Current price','Status']


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
        self.start = kwargs['start']
        self.broke = kwargs['broke']
        self.balance = kwargs['balance']
        self.delay = kwargs['delay']
        self.step_min = kwargs['step_min']
        self.cgt = kwargs['cgt']
        self.holdings = []
        self.limits = []

        # Holdings demo
        #self.holdings = [
        #    ('DHHF', 571),
        #    ('VDHG', 154)
        #]
        self.limits = [
            ('DHHF', 150, 2950),
            ('VDHG', -30, 6300)
        ]

        self.set_title()
        self.set_subtitle()


    def set_title(self):
        self.title = Date.timestamp_to_date_str(self.start)

    def set_subtitle(self):
        holdings_table = Table.table(header=SimulatorRunMenu._HEADER_HOLDINGS, rows=self._holdings_to_rows())
        limits_table = Table.table(header=SimulatorRunMenu._HEADER_LIMITS, rows=self._limits_to_rows())
        total_cash = f'Cash:\t\t{"$10,000.00"}'
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
        controller.pop()


    # Internal

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
            l2 = 'BUY' if l[1] >= 0 else 'SELL'
            l3 = str(abs(l[1]))
            l4 = StrFormat.int100_to_currency_str(l[2])
            l5 = '$99.99'
            l6 = 'PENDING'
            limits[i] = (l1,l2,l3,l4,l5,l6)
        return limits