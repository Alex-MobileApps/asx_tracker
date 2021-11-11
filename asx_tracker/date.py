from time import time
from datetime import datetime
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
