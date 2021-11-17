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
    MONTH_31        = 2678400
    HALF_YEAR_365   = 15768000
    YEAR_365        = 31536000
    MIN             = -36000
    MAX             = 253402232400
    HOUR_OPEN       = 10
    HOUR_CLOSE      = 16
    MAX_OPEN        = 253402210800

    _TZ_SYDNEY      = 'Australia/Sydney'
    _TZ_SYDNEY_INFO = timezone(_TZ_SYDNEY)
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
    def same_day(date1, date2):
        """
        Returns whether or not two dates are on the same day

        Parameters
        ----------
        date1 : int
            Timestamp of the first date
        date2 : int
            Timestamp of the first date

        Returns
        -------
        bool
            Whether or not both dates are on the same day
        """

        d1, d2 = Date.timestamp_to_datetime(date1, date2)
        return d1.day == d2.day and d1.month == d2.month and d1.year == d2.year


    @staticmethod
    def market_open(date):
        """
        Returns whether or not the market is open at a given date

        Parameters
        ----------
        date : int
            Timestamp of the date

        Returns
        -------
        bool
            Whether or not the market is open
        """

        d = Date.timestamp_to_datetime(date)
        if d.weekday() >= 5 or d.hour < Date.HOUR_OPEN or d.hour > Date.HOUR_CLOSE:
            return False
        if d.hour == Date.HOUR_CLOSE:
            return d.minute == 0
        return True


    @staticmethod
    def after_close(date):
        """
        Returns whether or not the market has already closed for a given date

        Parameters
        ----------
        date : int
            Timestamp of the date

        Returns
        -------
        bool
            Whether or not the market has already closed
        """

        d = Date.timestamp_to_datetime(date)
        if d.weekday() >= 5 or d.hour > Date.HOUR_CLOSE:
            return True
        if d.hour == Date.HOUR_CLOSE:
            return d.minute == 0
        return False


    @staticmethod
    def before_open(date):
        """
        Returns whether or not the market has yet to open for a given date

        Parameters
        ----------
        date : int
            Timestamp of the date

        Returns
        -------
        bool
            Whether or not the market has yet to open
        """

        d = Date.timestamp_to_datetime(date)
        return d.weekday() >= 5 or d.hour < Date.HOUR_OPEN


    @staticmethod
    def timestamp_next_open(date):
        """
        Returns to next next market open as a timestamp

        Parameters
        ----------
        date : int
            Current date

        Returns
        -------
        int
            Timestamp of the next market open
        """

        if date > Date.MAX_OPEN:
            return Date.MAX_OPEN

        d = Date.timestamp_to_datetime(date)
        if d.hour >= Date.HOUR_OPEN:
            d += timedelta(days=1)
        d = d.replace(hour=Date.HOUR_OPEN)
        weekday = d.weekday()
        days = 0 if weekday < 5 else 7 - weekday
        d = d.replace(hour=Date.HOUR_OPEN, minute=0, second=0, microsecond=0) + timedelta(days=days)
        return int(d.timestamp())


    @staticmethod
    def timestamp_to_day_end(date):
        """
        Converts a date to time 23:59:00 on the same day

        Parameters
        ----------
        date : int
            Timestamp of the date

        Returns
        -------
        int
            Converted timestamp
        """

        d = Date.timestamp_to_datetime(date)
        d = d.replace(hour=23, minute=59, second=0, microsecond=0)
        return int(d.timestamp())


    @staticmethod
    def timestamp_to_day_start(date):
        """
        Converts a date to time 00:00:00 on the same day.
        See Date.timestamp_to_day_end
        """

        d = Date.timestamp_to_datetime(date)
        d = d.replace(hour=0, minute=0, second=0, microsecond=0)
        return int(d.timestamp())


    @staticmethod
    def timestamp_to_prev_day_end(date):
        """
        Converts a date to time 23:59:00 on the previous day.
        See Date.timestamp_to_day_end
        """

        return Date.timestamp_to_day_start(date) - Date.MINUTE


    @staticmethod
    def timestamp_to_next_day_start(date):
        """
        Converts a date to time 00:00:00 on the next day.
        See Date.timestamp_to_day_end
        """

        return Date.timestamp_to_day_end(date) + Date.MINUTE


    @staticmethod
    def timestamp_to_year_start(date):
        """
        Converts a date to 1 JAN 00:00:00 for the same year.
        See Date.timestamp_to_day_end
        """

        d = Date.timestamp_to_datetime(date)
        d = d.replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
        return int(d.timestamp())


    @staticmethod
    def timestamp_to_datetime(*timestamps):
        """
        Converts timestamps to Sydney based datetime objects

        Returns
        -------
        datetime or list
            Conversion of timestamps to Sydney based timestamps
        """

        fn = lambda t: datetime.fromtimestamp(t, tz=Date._TZ_SYDNEY_INFO)
        if len(timestamps) > 1:
            return [fn(t) for t in timestamps]
        return fn(timestamps[0])


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
            return int(now.timestamp())
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