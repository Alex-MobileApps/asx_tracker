from asx_tracker.menu.menu import Menu

class VisualiseMenu(Menu):

    def __init__(self):
        super().__init__(
            'Visualise',
            None,
            [])

    def handle_option(self, controller):
        ticker = input('Ticker: ')
        start = input('Start date (dd/mm/yyyy hh:mm): ')
        end = input('End data (dd/mm/yyyy hh:mm): ')
        controller.pop()
