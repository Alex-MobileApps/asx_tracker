from asx_tracker.menu.menu import Menu
from asx_tracker.scraper.scraper import Scraper
from asx_tracker.database.database import Database
from asx_tracker.printer import Printer

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
        print('Downloading new company names ... ', end='', flush=True)
        fn = lambda: Database.insert_listings(Scraper.scrape_companies(comp_url))
        if not UpdateMenu.download_single(fn):
            warn = True

        # Download new ETFs
        print('Downloading new ETF names ... ', end='', flush=True)
        fn = lambda: Database.insert_listings(Scraper.scrape_etfs())
        if not UpdateMenu.download_single(fn):
            warn = True

        # Download daily
        print('Downloading daily data ... ', end='', flush=True)
        fn = lambda: Database.insert_daily(Scraper.scrape_daily())
        if not UpdateMenu.download_single(fn):
            warn = True

        # Download intraday
        print('Downloading intraday data ... ', end='', flush=True)
        fn = lambda: Database.insert_intraday(Scraper.scrape_intraday())
        if not UpdateMenu.download_single(fn):
            warn = True

        # Complete
        Printer.divider()
        warn_txt = 'WARNING: Some downloads failed' if warn else 'Download successful'
        input(f'{warn_txt} (press Enter to continue)')
        controller.pop()


    @staticmethod
    def download_single(fn):
        try:
            count = fn()
            print(f'complete ({count} added)')
            return True
        except:
            print('FAILED')
            return False


    @staticmethod
    def set_comp_url():
        print(f'1. Open {Scraper._URL_COM}')
        print("2. Copy the destination URL of the 'ASX LISTED COMPANIES CSV' button")
        print()
        return input('Enter destination URL: ')