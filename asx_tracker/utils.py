import os

class Utils():

    _USER_AGENT = 'Mozilla/5.0'
    CLEAR_LINE = '\x1b[2K\r'

    @staticmethod
    def clear():
        os.system('cls' if os.name == 'nt' else 'clear')

    @staticmethod
    def has_len(*M):
        try:
            for m in M:
                len(m)
            return True
        except:
            return False

    @staticmethod
    def quit():
        Utils.clear()
        exit()