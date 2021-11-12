from time import time
from datetime import datetime, timedelta
from pytz import timezone
from asx_tracker.utils import Utils

class Date():

    # Static variables

    SECOND          = 1
    MINUTE          = 60
    HOUR            = 3600
    DAY             = 86400
    WEEK            = 604800
    YEAR_365        = 31536000
    MIN             = 0
    MAX             = 253402261199

    _TZ_SYDNEY      = 'Australia/Sydney'
    _TZ_SYDNEY_INFO = timezone(_TZ_SYDNEY)
    _HOUR_CLOSE     = 19
    _DATE_FORMAT    = '%d %b %Y %I:%M%p'
    _MONTH_MAP      = {'JAN': 1, 'FEB': 2, 'MAR': 3, 'APR': 4, 'MAY': 5, 'JUN': 6, 'JUL': 7, 'AUG': 8, 'SEP': 9, 'OCT': 10, 'NOV': 11, 'DEC': 12}
    _NOW            = 'NOW'
    _MIN            = 'MIN'
    _MAX            = 'MAX'

    # Timestamps

    @staticmethod
    def timestamp_now(offset=0):
        """
        Returns the timestamp (seconds) of the current time

        Parameters
        ----------
        offset : int, optional
            Offset the , by default 0

        Returns
        -------
        int
            Timestamp (seconds)
        """

        return int(time() + offset)


    @staticmethod
    def timestamp_30_days(date=None, offset=0):
        """
        Returns the timestamp (seconds) of 30 days before a given date

        Parameters
        ----------
        date : int, optional
            Timestamp of the original date, or timestamp of now (if None)
        offset : int, optional
            Apply an offset (seconds) to the original date, by default 0

        Returns
        -------
        int
            Timestamp of a date (seconds) after subtracting 30 days
        """

        if date is None: date = Date.timestamp_now()
        return offset + date - 30 * Date.DAY


    @staticmethod
    def timestamp_60_days(date=None, offset=0):
        """
        Returns the timestamp (seconds) of 60 days before a given date.
        See Date.timestamp_30_days
        """

        if date is None: date = Date.timestamp_now()
        return offset + date - 60 * Date.DAY


    @staticmethod
    def timestamp_730_days(date=None, offset=0):
        """
        Returns the timestamp (seconds) of 730 days before a given date.
        See Date.timestamp_30_days
        """

        if date is None: date = Date.timestamp_now()
        return offset + date - 730 * Date.DAY


    @staticmethod
    def timestamp_to_datetime(timestamps):
        """
        Converts timestamps to Sydney based datetime objects

        Parameters
        ----------
        timestamps : int or list
            Timestamp or list of timestamps

        Returns
        -------
        datetime or list
            Conversion of timestamps to Sydney based timestamps
        """

        fn = lambda t: datetime.fromtimestamp(t, tz=timezone(Date._TZ_SYDNEY))
        if Utils.has_len(timestamps):
            return [fn(t) for t in timestamps]
        return fn(timestamps)


    @staticmethod
    def timestamp_to_date_str(timestamp):
        """
        Converts a timestamp to a formatted string in Sydney time

        Parameters
        ----------
        timestamp : int
            Timestamp to convert

        Returns
        -------
        str
            String representation of timestamp in Sydney time
        """

        date = Date.timestamp_to_datetime(timestamp)
        return date.strftime(format=Date._DATE_FORMAT)


    @staticmethod
    def date_str_to_timestamp(txt):
        """
        Convert a string to a timestamp

        Parameters
        ----------
        txt : str
            Date string to convert

        Returns
        -------
        int or None
            Timestamp if conversion is successful, else None
        """

        # Parse timestamp string
        if Utils.is_int(txt):
            return int(txt)

        # Now, Min, Max
        txt = txt.upper().strip()
        if txt == Date._NOW:
            now = Date._TZ_SYDNEY_INFO.localize(datetime.now())
            now -= timedelta(seconds=now.second)
            return now.timestamp()
        elif txt == Date._MIN:
            return Date.MIN
        elif txt == Date._MAX:
            return Date.MAX

        # Parse text
        txt = txt.split(' ')
        txt = [t for t in txt if t != '']
        time = [0] * 6 # year, month, day, hour, minute, second
        try:
            time[0] = int(txt[2])
            time[1] = Date._MONTH_MAP[txt[1]]
            time[2] = int(txt[0])
            if len(txt) > 3:
                hour, min = txt[3].split(':')
                time[3] = int(hour)
                if min.endswith('PM') and time[3] != 12:
                    time[3] += 12
                min = min.replace('AM', '')
                min = min.replace('PM', '')
                time[4] = int(min)
            utc_dt = datetime(*time)
            loc_dt = Date._TZ_SYDNEY_INFO.localize(utc_dt)
            return int(loc_dt.timestamp())
        except:
            return None