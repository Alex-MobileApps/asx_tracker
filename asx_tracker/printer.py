from shutil import get_terminal_size
from asx_tracker.utils import Utils

class Printer():

    # Headers

    @staticmethod
    def header(title, top=True, bottom=True):
        """
        Prints header text to the terminal

        Parameters
        ----------
        title : str
            Title of the header
        top : bool, optional
            Whether or not print a divider above the header text, by default True
        bottom : bool, optional
            Whether or not print a divider below the header text, by default True
        """

        Printer._headers(title, top, bottom, True)


    @staticmethod
    def subheader(title, top=False, bottom=True):
        """
        Prints subheader text to the terminal.
        See Printer.header
        """

        Printer._headers(title, top, bottom, False)


    # Dividers

    @staticmethod
    def divider(bold=False):
        """
        Prints a divider to the terminal

        Parameters
        ----------
        bold : bool, optional
            Whether or not to print a wide or narrow divider, by default False
        """

        size = get_terminal_size().columns
        if bold:
            print('=' * size)
        else:
            print('-' * size)


    # Error messages

    @staticmethod
    def ack(message):
        """
        Prints a message and waits for the user to acknolwedge it before resuming the main thread

        Parameters
        ----------
        message : str
            Message to print
        """

        input(f'{message} (Press Enter to continue)')


    # Options

    @staticmethod
    def options(opts):
        """
        Prints a sequence of enumerated options to the terminal

        Parameters
        ----------
        opts : list
            Sequence of strings to print as options
        """

        for i, s in enumerate(opts):
            print(f'{i+1}. {s}')


    def invalid_option(n):
        """
        Prints a message stating that a selected option was invalid

        Parameters
        ----------
        n : int
            Number of options to select from
        """
        print(f'{Utils.CLEAR_LINE}Please select an option from 1 to {n}')


    # Internal

    @staticmethod
    def _headers(title, top, bottom, bold):
        """
        Handles printing of headers and subheaders to the terminal

        Parameters
        ----------
        title : str
            Title of the header
        top : bool
            Whether or not print a divider above the text
        bottom : bool
            Whether or not print a divider below the text
        bold : bool
            Whether or not to print a wide or narrow divider
        """

        if top: Printer.divider(bold)
        print(title)
        if bottom: Printer.divider(bold)