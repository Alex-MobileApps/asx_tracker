from asx_tracker.menu.menu import Menu
from asx_tracker.table import Table
from asx_tracker.date import Date

class SimulatorRunMenu(Menu):

    # Static variables

    _TABLE_HEADER = ['Ticker','Units','Unit price']


    # Constructor

    def __init__(self, **kwargs):
        super().__init__()

        # Settings
        self.start = kwargs['start']
        self.broke = kwargs['broke']
        self.balance = kwargs['balance']
        self.delay = kwargs['delay']
        self.step_min = kwargs['step_min']
        self.cgt = kwargs['cgt']

        # Holdings
        self.holdings = [
            ('DHHF', 571),
            ('VDHG', 154)
        ]
        self.limits = [
            ('DHHF', 150, 2950),
            ('VDHG', -30, 6300)
        ]

        #self.print_holdings_table()
        self.set_title()
        self.set_subtitle()
        self.set_options()


    def set_title(self):
        self.title = Date.timestamp_to_date_str(self.start)

    def set_subtitle(self):
        holdings_rows = [(r[0], str(r[1]), '$39.24') for r in self.holdings]
        self.subtitle = Table.table(header=SimulatorRunMenu._TABLE_HEADER, rows=holdings_rows)


    # Menu options

    def set_options(self):
        """
        Sets the main menu's options, including the current settings for each option
        """

        self.options = ['Work in progress (back)']


    def handle_option(self, controller):
        """
        Handles selection of a menu option

        Parameters
        ----------
        controller : Controller
            Controller that is managing the program
        """

        option = Menu.select_option(self.options)
        if option == 1:
            return controller.pop()