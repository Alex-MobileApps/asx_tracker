class Controller():

    def __init__(self):
        self.menus = []


    # Add/remove views

    def push(self, menu):
        """
        Pushes a new menu into view

        Parameters
        ----------
        menu : Menu
            New menu
        """

        self.menus.append(menu())
        self.display()


    def pop(self):
        """
        Unwinds from the last menu
        """

        if len(self.menus) > 1:
            self.menus.pop()
            self.display()
        else:
            exit()


    # Display

    def display(self):
        """
        Displays the top-most menu on the screen
        """

        menu = self.menus[-1]
        menu.display()
        menu.handle_option(self)