from asx_tracker.menu.menu import Menu
from asx_tracker.scraper.scraper import Scraper
from asx_tracker.printer import Printer
from asx_tracker.utils import Utils

class UpdateMenu(Menu):
    def __init__(self):
        super().__init__(
            title = "Update data",
            options = ["Download new data", "Back"])

    def handle_option(self, controller):
        option = self.select_option(self.options)
        if option == 1:
            UpdateMenu.download(controller)
        else:
            controller.pop()

    @staticmethod
    def download(controller):
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

        # Download daily
        print('Downloading daily data ...')
        UpdateMenu.download_single(Scraper.download_daily)
        print()

        # Complete
        Printer.divider()
        input(f'Press Enter to continue')
        controller.pop()


    @staticmethod
    def download_single(fn, *args):
        try:
            count = fn(*args)
            print(f'{Utils.CLEAR_LINE}  complete ({count} added)')
            return True
        except Exception as e:
            print(f'{Utils.CLEAR_LINE}  FAILED: {e}')
            return False


    @staticmethod
    def set_comp_url():
        print(f'1. Open {Scraper._URL_COM}')
        print("2. Copy the destination URL of the 'ASX LISTED COMPANIES CSV' button")
        print()
        return input('Enter destination URL: ')