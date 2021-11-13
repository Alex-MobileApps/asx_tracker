from asx_tracker.menu.menu import Menu
from asx_tracker.scraper.scraper import Scraper
from asx_tracker.printer import Printer
from asx_tracker.utils import Utils

class UpdateMenu(Menu):

    # Constructor

    def __init__(self, **kwargs):
        super().__init__(
            title = "Update data",
            options = ["Download new data", "Back"])


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
        if option == 1:
            UpdateMenu.download()
        controller.pop()


    # Download data

    @staticmethod
    def download():
        """
        Downloads new ASX data to the database
        """

        # Get company CSV URL
        print()
        comp_url = UpdateMenu.set_comp_url()
        print()

        # Download new companies
        print('Downloading new company names ...')
        UpdateMenu.download_single(Scraper.download_companies, comp_url)
        print()

        # Download new ETFs
        print('Downloading new ETF names ...')
        UpdateMenu.download_single(Scraper.download_etfs)
        print()

        # Download intraday
        print('Downloading intraday data ...')
        UpdateMenu.download_single(Scraper.download_intraday)
        print()

        # Download daily
        print('Downloading daily data ...')
        UpdateMenu.download_single(Scraper.download_daily)

        # Complete
        Printer.divider()
        input(f'Press Enter to continue')


    @staticmethod
    def download_single(fn, *args):
        """
        Performs a database insert function after a download

        Parameters
        ----------
        fn : function
            Function that inserts into the database

        Returns
        -------
        bool
            Whether or not the insert was successful
        """

        try:
            count = fn(*args)
            print(f'{Utils.CLEAR_LINE}  complete ({count} added)')
            return True
        except Exception as e:
            print(f'{Utils.CLEAR_LINE}  FAILED: {e}')
            return False


    @staticmethod
    def set_comp_url():
        """
        Retrieves the URL that contains the ASX's CSV of company information

        Returns
        -------
        str
            ASX company CSV URL
        """

        print(f'1. Open {Scraper._URL_COM}')
        print("2. Copy the destination URL of the 'ASX LISTED COMPANIES CSV' button")
        print()
        return input('Enter destination URL: ')