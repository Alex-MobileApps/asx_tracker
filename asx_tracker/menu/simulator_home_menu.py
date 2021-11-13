from asx_tracker.menu.menu import Menu
from asx_tracker.menu.simulator_new_menu import SimulatorNewMenu

class SimulatorHomeMenu(Menu):

    # Constructor

    def __init__(self, **kwargs):
        super().__init__(
            title = 'Trading simulator',
            options = ['New simulation','Load simulation','Delete simulation','Back'])


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
            controller.push(SimulatorNewMenu)
        else:
            return controller.pop()