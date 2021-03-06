from asx_tracker.menu.menu import Menu
from asx_tracker.menu.update_menu import UpdateMenu
from asx_tracker.menu.visualise_menu import VisualiseMenu
from asx_tracker.menu.simulator_home_menu import SimulatorHomeMenu

class HomeMenu(Menu):

    # Constructor

    def __init__(self, **kwargs):
        super().__init__(
            title = "ASX tracker",
            subtitle = "Welcome to the ASX company and ETF tracker",
            options = ["Update data", "Visualise", "Trading simulator", "Exit"])


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
            controller.push(UpdateMenu)
        elif option == 2:
            controller.push(VisualiseMenu)
        elif option == 3:
            controller.push(SimulatorHomeMenu)
        else:
            exit()