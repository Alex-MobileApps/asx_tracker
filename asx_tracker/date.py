from time import time
from datetime import datetime, timedelta
from pytz import timezone

class Date():

    SECOND = 1
    MINUTE = 60
    HOUR = 3600
    DAY = 86400
    WEEK = 604800
    YEAR_365 = 31536000

    _TZ_SYDNEY = 'Australia/Sydney'
    _HOUR_CLOSE = 19

    @staticmethod
    def timestamp_now(offset=0):
        return int(time() + offset)

    @staticmethod
    def timestamp_730_days(date=None, offset=0):
        if date is None: date = Date.timestamp_now()
        return offset + date - 730 * Date.DAY

    @staticmethod
    def timestamp_60_days(date=None, offset=0):
        if date is None: date = Date.timestamp_now()
        return offset + date - 60 * Date.DAY

    @staticmethod
    def timestamp_30_days(date=None, offset=0):
        if date is None: date = Date.timestamp_now()
        return offset + date - 30 * Date.DAY

    @staticmethod
    def timestamp_last_close():
        now = Date.timestamp_now()
        date_now = datetime.fromtimestamp(now, tz=timezone(Date._TZ_SYDNEY)).replace(minute=0, second=0, microsecond=0)
        if date_now.hour < Date._HOUR_CLOSE:
            date_now -= timedelta(days=1)
        date_now = date_now.replace(hour=Date._HOUR_CLOSE)
        return int(date_now.timestamp())
