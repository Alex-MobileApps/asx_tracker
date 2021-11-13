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


    # Currency

    @staticmethod
    def int100_to_currency_str(val):
        """
        Converts an integer to a currency string
        """

        txt = str(val)
        dollars = txt[:-2]
        cents = txt[-2:]
        if dollars == '':
            dollars = '0'
        else:
            split_dollars = []
            while len(dollars) >= 3:
                split_dollars.append(dollars[-3:])
                dollars = dollars[:-3]
            if len(dollars) > 0:
                split_dollars.append(dollars)
            dollars = ','.join(reversed(split_dollars))
        return '$' + dollars + '.' + cents


    # String formatting

    @staticmethod
    def pad_str(txt, width):
        """
        Fills a string to a specified width

        Parameters
        ----------
        txt : str
            Text in the string
        width : int
            Width to fill to

        Returns
        -------
        str
            New string with set width
        """

        len_txt = len(txt)
        if len_txt >= width:
            return txt[:width]
        return txt + (width - len_txt) * ' '