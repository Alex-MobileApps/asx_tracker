from asx_tracker.menu.menu import Menu
from asx_tracker.menu.update_menu import UpdateMenu
from asx_tracker.menu.visualise_menu import VisualiseMenu

class HomeMenu(Menu):
    def __init__(self):
        super().__init__(
            title = "ASX tracker",
            subtitle = "Welcome to the ASX company and ETF tracker",
            options = ["Update data", "Visualise", "Trading simulation", "Exit"])

    def handle_option(self, controller):
        option = self.select_option(self.options)
        if option == 1:
            controller.push(UpdateMenu)
        elif option == 2:
            controller.push(VisualiseMenu)
        elif option == 3:
            pass
        else:
            exit()