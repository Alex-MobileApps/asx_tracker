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
        warn = False

        # Download new companies
        print('Downloading new company names ...')
        if not UpdateMenu.scrape_single(Scraper.scrape_companies, comp_url):
            warn = True
        print()

        # Download new ETFs
        print('Downloading new ETF names ...')
        if not UpdateMenu.scrape_single(Scraper.scrape_etfs):
            warn = True
        print()

        # Download daily
        print('Downloading daily data ...')
        if not UpdateMenu.scrape_single(Scraper.scrape_daily):
            warn = True
        print()

        # Download intraday
        print('Downloading intraday data ...')
        if not UpdateMenu.scrape_single(Scraper.scrape_intraday):
            warn = True

        # Complete
        Printer.divider()
        warn_txt = 'WARNING: Some downloads failed' if warn else 'Download successful'
        input(f'{warn_txt} (press Enter to continue)')
        controller.pop()


    @staticmethod
    def scrape_single(fn, *args):
        try:
            count = fn(*args)
            print(f'{Utils.CLEAR_LINE}  complete ({count} added)\t\t\t')
            return True
        except Exception as e:
            print('  FAILED', f'({e})')
            return False


    @staticmethod
    def set_comp_url():
        print(f'1. Open {Scraper._URL_COM}')
        print("2. Copy the destination URL of the 'ASX LISTED COMPANIES CSV' button")
        print()
        return input('Enter destination URL: ')