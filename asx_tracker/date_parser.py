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
        if len(txt) == 0:
            return

        # Parse timestamp
        if Utils.is_int(txt):
            return int(txt)

        # Parse string
        # need to allow low, high, now, start, end, hour, minute, day, week, month, year, /, _STR_MAP
        txt = txt.upper()