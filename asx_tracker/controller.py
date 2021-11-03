class Controller():

    def __init__(self):
        self.menus = []

    def push(self, menu):
        self.menus.append(menu())
        self.display()

    def pop(self):
        if len(self.menus) > 1:
            self.menus.pop()
            self.display()
        else:
            exit()

    def display(self):
        menu = self.menus[-1]
        menu.display()
        menu.handle_option(self)