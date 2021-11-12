from asx_tracker.date import Date
from asx_tracker.utils import Utils

class DateParser():

    # Static variables

    _STR_MAP = {
        'JANUARY': 'JAN',
        'FEBRUARY': 'FEB',
        'MARCH': 'MAR',
        'APRIL': 'APR',
        'JUNE': 'JUN',
        'JULY': 'JUL',
        'AUGUST': 'AUG',
        'SEPTEMBER': 'SEP',
        'OCTOBER': 'OCT',
        'NOVEMBER': 'NOV',
        'DECEMBER': 'DEC'
    }


    # Parse string

    @staticmethod
    def parse(txt):
        """
        Parse a user input string into a timestamp

        Parameters
        ----------
        txt : str
            User input string

        Returns
        -------
        int or None
            int if the string can be converted, else None
        """

        if len(txt) == 0:
            return

        # Parse timestamp
        if Utils.is_int(txt):
            return int(txt)

        # Parse string
        return Date.date_str_to_timestamp(txt)