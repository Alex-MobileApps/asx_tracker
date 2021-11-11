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
        """
        Refreshes the screen with updated content
        """

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


    @staticmethod
    def select_option(options):
        """
        Retrieves a user's selection from a list of options

        Parameters
        ----------
        options : list
            Sequence of options as strings to select from

        Returns
        -------
        int
            Number of the option selected
        """

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
                Printer.invalid_option(len_options)