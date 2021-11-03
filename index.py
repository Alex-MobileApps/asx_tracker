from asx_tracker.menu.home_menu import HomeMenu
from asx_tracker.controller import Controller

if __name__ == "__main__":
    try:
        controller = Controller()
        controller.push(HomeMenu)
    except KeyboardInterrupt:
        pass