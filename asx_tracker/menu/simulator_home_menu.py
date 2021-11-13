from asx_tracker.menu.menu import Menu

class SimulatorHomeMenu(Menu):

    # Constructor

    def __init__(self):
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
        if option == 4:
            return controller.pop()