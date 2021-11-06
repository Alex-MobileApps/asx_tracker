from asx_tracker.menu.menu import Menu
from asx_tracker.scraper.scraper import Scraper
from asx_tracker.printer import Printer
from asx_tracker.utils import Utils

class UpdateMenu(Menu):
    def __init__(self):
        super().__init__(
            "Update data",
            None,
            ["Download new data (ETA: <time>)", "Back"])

    def handle_option(self, controller):
        option = self.select_option()
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
        UpdateMenu.scrape_single(Scraper.scrape_companies, comp_url)
        print()

        # Download new ETFs
        print('Downloading new ETF names ...')
        UpdateMenu.scrape_single(Scraper.scrape_etfs)
        print()

        # Download daily
        print('Downloading daily data ...')
        UpdateMenu.scrape_single(Scraper.scrape_daily)
        print()

        # Download intraday
        print('Downloading intraday data ...')
        UpdateMenu.scrape_single(Scraper.scrape_intraday)

        # Complete
        Printer.divider()
        input(f'Press Enter to continue')
        controller.pop()


    @staticmethod
    def scrape_single(fn, *args):
        try:
            count = fn(*args)
            print(f'{Utils.CLEAR_LINE}  complete ({count} added)\t\t\t')
            return True
        except Exception as e:
            print('  FAILED:', e)
            return False


    @staticmethod
    def set_comp_url():
        print(f'1. Open {Scraper._URL_COM}')
        print("2. Copy the destination URL of the 'ASX LISTED COMPANIES CSV' button")
        print()
        return input('Enter destination URL: ')