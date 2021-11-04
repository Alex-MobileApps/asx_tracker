from asx_tracker.menu.menu import Menu
from asx_tracker.menu.update_menu import UpdateMenu
from asx_tracker.menu.visualise_menu import VisualiseMenu
from asx_tracker.utils import Utils

class HomeMenu(Menu):
    def __init__(self):
        super().__init__(
            "ASX tracker",
            "Welcome to the ASX company and ETF tracker",
            ["Update data (required within <time>)", "Visualise", "Paper trade", "Exit"])

    def handle_option(self, controller):
        option = self.select_option()
        if option == 1:
            controller.push(UpdateMenu)
        elif option == 2:
            controller.push(VisualiseMenu)
        elif option == 3:
            pass
        else:
            Utils.quit()