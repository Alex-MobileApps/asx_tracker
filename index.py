from asx_tracker.menu.home_menu import HomeMenu
from asx_tracker.controller import Controller
from asx_tracker.database.database import Database

if __name__ == "__main__":
    try:
        Database.create_tables()
        controller = Controller()
        controller.push(HomeMenu)
    except KeyboardInterrupt:
        pass