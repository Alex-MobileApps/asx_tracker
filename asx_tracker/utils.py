import os

class Utils():

    # Static variables

    USER_AGENT = 'Mozilla/5.0'
    CLEAR_LINE = '\x1b[2K\r'


    # Functions

    @staticmethod
    def clear():
        """
        Clears the terminal output
        """

        os.system('cls' if os.name == 'nt' else 'clear')

    @staticmethod
    def has_len(*M):
        """
        Returns whether or not objects have a length

        Returns
        -------
        bool
            Whether or not objects have a length
        """

        try:
            for m in M:
                len(m)
            return True
        except:
            return False


    @staticmethod
    def is_int(*M):
        """
        Returns whether or not objects can be converted to integers

        Returns
        -------
        bool
            Whether or not objects can be converted to integers
        """

        for m in M:
            try: int(m)
            except: return False
        return True