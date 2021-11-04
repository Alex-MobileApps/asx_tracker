from asx_tracker.utils import Utils
from asx_tracker.printer import Printer

class Menu():

    # Constructor

    def __init__(self, title, subtitle, options):
        self.title = title
        self.subtitle = subtitle
        self.options = options


    # Functionality

    def display(self):
        Utils.clear()
        if self.title:
            Printer.header(self.title)
        if self.subtitle:
            print(self.subtitle)
            print()
        if self.options:
            for i, s in enumerate(self.options):
                print(f'{i+1}. {s}')
            Printer.divider()

    def select_option(self):
        len_options = len(self.options)
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