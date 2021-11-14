from asx_tracker.menu.menu import Menu
from asx_tracker.date import Date
from asx_tracker.printer import Printer
from asx_tracker.utils import Utils
from asx_tracker.str_format import StrFormat
from asx_tracker.menu.simulator_run_menu import SimulatorRunMenu

class SimulatorNewMenu(Menu):

    # Static variables

    _DEF_START          = 0
    _DEF_BROKE          = 950
    _DEF_BALANCE        = 1000000
    _DEF_DELAY_MIN      = 20
    _DEF_STEP_MIN       = 5
    _DEF_CGT            = 45


    # Constructor

    def __init__(self, **kwargs):
        super().__init__(title = 'New simulator')
        self.start = SimulatorNewMenu._DEF_START
        self.broke = SimulatorNewMenu._DEF_BROKE
        self.balance = SimulatorNewMenu._DEF_BALANCE
        self.delay = SimulatorNewMenu._DEF_DELAY_MIN
        self.step_min = SimulatorNewMenu._DEF_STEP_MIN
        self.cgt = SimulatorNewMenu._DEF_CGT
        self.set_options()


    # Menu options

    def set_options(self):
        """
        Sets the main menu's options, including the current settings for each option
        """

        c = lambda x: StrFormat.int100_to_currency_str(x)
        self.options = [
            f'Set start date:\t\t\t{Date.timestamp_to_date_str(self.start)}',
            f'Set simulator step interval:\t\t{self.step_min} min',
            f'Set starting balance:\t\t{c(self.balance)}',
            f'Set brokerage fee:\t\t\t{c(self.broke)}',
            f'Set ASX data delay:\t\t\t{self.delay} min',
            f'Set Capital Gains Tax percentage:\t{self.cgt}%',
            'Begin',
            'Back'
        ]


    def handle_option(self, controller):
        """
        Handles selection of a menu option

        Parameters
        ----------
        controller : Controller
            Controller that is managing the program
        """

        option = Menu.select_option(self.options)
        if option == 8:
            return controller.pop()
        elif option == 7:
            return controller.push(SimulatorRunMenu, start=self.start, broke=self.broke, balance=self.balance, delay=self.delay, step_min=self.step_min, cgt=self.cgt)
        print()
        if option == 1:
            self.set_start()
        elif option == 2:
            self.set_step_min()
        elif option == 3:
            self.set_balance()
        elif option == 4:
            self.set_brokerage()
        elif option == 5:
            self.set_delay()
        elif option == 6:
            self.set_cgt()
        self.set_options()
        controller.display()


    # Start date

    def set_start(self):
        """
        Sets the simulator start date as a timestamp
        """

        txt = input('Enter start date: ')
        val = StrFormat.date_str_to_timestamp(txt)
        if val is None:
            return Printer.ack(f'{txt} is not valid')
        self.start = val


    # Time advance interval

    def set_step_min(self):
        """
        Sets the simulator time advance step interval
        """

        txt = input('Enter simulator step interval: ')
        val = StrFormat.minute_str_to_int(txt, non_neg=True)
        if val is None:
            return Printer.ack(f'{txt} is not valid')
        self.step_min = val


    # Cash balance

    def set_balance(self):
        """
        Sets the simulator cash balance
        """

        txt = input('Enter starting balance: ')
        val = StrFormat.currency_str_to_int100(txt, non_neg=True)
        if val is None:
            return Printer.ack(f'{txt} is not valid')
        self.balance = val


    # Brokerage

    def set_brokerage(self):
        """
        Sets the simulator brokerage fee
        """

        txt = input('Enter brokerage fee: ')
        val = StrFormat.currency_str_to_int100(txt, non_neg=True)
        if val is None:
            return Printer.ack(f'{txt} is not valid')
        self.broke = val


    # Data delay

    def set_delay(self):
        """
        Sets the simulator ASX data retrieval delay
        """

        txt = input('Enter ASX data delay: ')
        val = StrFormat.minute_str_to_int(txt, non_neg=True)
        if val is None:
            return Printer.ack(f'{txt} is not valid')
        self.delay = val


    # Capital gains

    def set_cgt(self):
        """
        Sets the simulator capital gains tax bracket used when selling
        """

        txt = input('Enter Capital Gains Tax percentage: ')
        val = StrFormat.percentage_str_to_int(txt, non_neg=True)
        if val is None:
            return Printer.ack(f'{txt} is not valid')
        self.cgt = val