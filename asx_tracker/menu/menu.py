from asx_tracker.utils import Utils
from asx_tracker.printer import Printer

class Menu():

    # Constructor

    def __init__(self, title=None, subtitle=None, options=None):
        self.title = title
        self.subtitle = subtitle
        self.options = options


    # Functionality

    def display(self):
        Utils.clear()
        if self.title is not None:
            Printer.header(self.title)
        if self.subtitle is not None:
            print(self.subtitle)
        if self.options is not None:
            if self.subtitle is not None:
                print()
            Printer.options(self.options)
        Printer.divider()

    def select_option(self, options):
        len_options = len(options)
        while True:
            val = input('Select an option: ')
            try:
                val = int(val)
                if val > len_options or val < 1:
                    Menu._invalid(len_options)
                else:
                    return val
            except:
                Menu._invalid(len_options)

    def _invalid(n):
        print(f'{Utils.CLEAR_LINE}Please select an option from 1 to {n}')