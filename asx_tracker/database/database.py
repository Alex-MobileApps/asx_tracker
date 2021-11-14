import sqlite3
from asx_tracker.date import Date
from asx_tracker.database.sql import Sql

class Database():

    # Static variables

    TAB_LISTING = 'listing'
    TAB_INTRADAY = 'intraday'
    TAB_DAILY = 'daily'
    COL_TICKER = 'ticker'
    COL_NAME = 'name'
    COL_MGMT_PCT = 'mgmt_pct'
    COL_DATE = 'date'
    COL_OPEN = 'open'
    COL_CLOSE = 'close'
    COL_LOW = 'low'
    COL_HIGH = 'high'
    COL_VOL= 'volume'
    COL_LAST_INTRADAY = 'last_intraday'
    COL_LAST_DAILY = 'last_daily'

    _PATH_DB = 'asx_tracker/database/database.db'


    # Create tables

    @staticmethod
    def create_tables():
        """
        Creates the required tables for the program
        """

        Database._execute(Sql.FOREIGN_KEYS, fetch=False)
        Database._execute(Sql.CREATE_TAB_LISTING, fetch=False)
        Database._execute(Sql.CREATE_TAB_INTRADAY, fetch=False)
        Database._execute(Sql.CREATE_TAB_DAILY, fetch=False)


    # Listings

    @staticmethod
    def insert_listings(df):
        """
        Inserts ASX listings into the database

        Parameters
        ----------
        df : pandas.DataFrame
            Listing to insert

        Returns
        -------
        int
            Number of rows inserted
        """

        data = []
        for i in range(len(df)):
            row = df.iloc[i]
            data.append((row[Database.COL_TICKER], row[Database.COL_NAME], int(row[Database.COL_MGMT_PCT])))
        query = f"""
        INSERT OR IGNORE INTO {Database.TAB_LISTING}
        ({Database.COL_TICKER}, {Database.COL_NAME}, {Database.COL_MGMT_PCT})
        VALUES
        (?,?,?)
        """
        return Database._execute(query, values=data, fetch=False)


    @staticmethod
    def fetch_all_listings(*cols):
        """
        Retrieve all ASX listings from the database

        Returns
        -------
        list
            Fetched listings
        """

        sel_cols = Database._set_cols(cols)
        query = f"""
        SELECT {sel_cols} FROM {Database.TAB_LISTING}
        ORDER BY {Database.COL_TICKER}
        """
        return Database._execute(query)


    @staticmethod
    def fetch_single_listing(ticker, *cols):
        """
        Retrieve ASX listing data for a single ticker

        Parameters
        ----------
        ticker : str
            Ticker to fetch

        Returns
        -------
        list
            Fetched listings
        """

        sel_cols = Database._set_cols(cols)
        query = f"""
        SELECT {sel_cols} FROM {Database.TAB_LISTING} WHERE {Database.COL_TICKER} = '{ticker}' LIMIT 1
        """
        return Database._execute(query)


    @staticmethod
    def update_listings_date(ticker, fetched_date, date_col):
        """
        Change when the last save of daily or intraday data happened in the database for a single ticker

        Parameters
        ----------
        ticker : str
            Ticker to update
        fetched_date : int
            Timestamp in the last inserted entry
        date_col
            Database.COL_LAST_INTRADAY : update last intraday save
            Database.COL_LAST_DAILY : update last daily save

        Returns
        -------
        int
            Number of entries modified
        """

        data = [(int(fetched_date),ticker)]
        query = f"""
        UPDATE {Database.TAB_LISTING}
        SET {date_col} = ?
        WHERE {Database.COL_TICKER} = ?
        """
        return Database._execute(query, values=data, fetch=False)


    # Intraday

    @staticmethod
    def insert_intraday(df):
        """
        Inserts ASX intraday data into the database

        Parameters
        ----------
        df : pandas.DataFrame
            Intraday data to insert

        Returns
        -------
        int
            Number of rows inserted
        """

        return Database._insert_intraday_or_daily(df, Database.TAB_INTRADAY)


    @staticmethod
    def fetch_all_intraday(*cols):
        """
        Retrieve all ASX intraday data from the database

        Returns
        -------
        list
            Fetched intraday data
        """

        return Database._fetch_all_intraday_or_daily(Database.TAB_INTRADAY, *cols)


    @staticmethod
    def fetch_single_intraday(ticker, *cols, start=None, end=None):
        """
        Retrieve ASX intraday data for a single ticker

        Parameters
        ----------
        ticker : str
            Ticker to fetch
        start : int
            Timestamp of start date to fetch from
        end : int
            Timestamp of end date to fetch from

        Returns
        -------
        list
            Fetched listings
        """

        return Database._fetch_single_intraday_or_daily(ticker, Database.TAB_INTRADAY, *cols, start=start, end=end)


    # Daily

    @staticmethod
    def insert_daily(df):
        """
        Inserts ASX daily data into the database.
        See Database.insert_intraday
        """

        return Database._insert_intraday_or_daily(df, Database.TAB_DAILY)


    @staticmethod
    def fetch_all_daily(*cols):
        """
        Retrieve all ASX daily data from the database.
        See Database.fetch_all_intraday
        """

        return Database._fetch_all_intraday_or_daily(Database.TAB_DAILY, *cols)


    @staticmethod
    def fetch_single_daily(ticker, *cols, start=None, end=None):
        """
        Retrieve ASX daily data for a single ticker.
        See Database.fetch_single_intraday
        """

        return Database._fetch_single_intraday_or_daily(ticker, Database.TAB_DAILY, *cols, start=start, end=end)


    # Live

    @staticmethod
    def fetch_multiple_live_prices(date, *tickers):
        """
        Fetches multiple live prices

        Parameters
        ----------
        date : int
            Live timestamp

        Returns
        -------
        list
            Live prices for each ticker
        """

        prices = [None] * len(tickers)
        for i, ticker in enumerate(tickers):
            prices[i] = Database.fetch_single_live_price(ticker, date)
        return prices


    @staticmethod
    def fetch_single_live_price(ticker, date):
        """
        Fetches a live price for a single ticker

        Parameters
        ----------
        ticker : str
            Ticker name
        date : int
            Live timestamp

        Returns
        -------
        int or None
            int if a live price is found, else None
        """

        last_intraday = Database._fetch_live_intraday_or_daily(ticker, date, Database.TAB_INTRADAY, Database.COL_DATE, Database.COL_CLOSE)

        # No intraday
        if not last_intraday:
            last_daily = Database._fetch_live_intraday_or_daily(ticker, date, Database.TAB_DAILY, Database.COL_CLOSE)
            return last_daily[0][0] if last_daily else None

        min_date = Date.timestamp_to_datetime(Date.MIN)
        days_since = lambda t: (Date.timestamp_to_datetime(t) - min_date).days

        # Intraday on current day
        intraday_date, intraday_close = last_intraday[0]
        live_day, intraday_day = days_since(date), days_since(intraday_date)
        if live_day == intraday_day:
            return intraday_close

        # No daily
        last_daily = Database._fetch_live_intraday_or_daily(ticker, date, Database.TAB_DAILY, Database.COL_DATE, Database.COL_CLOSE)
        if not last_daily:
            return intraday_close

        # Return intraday if newer, else daily
        daily_date, daily_close = last_daily[0]
        daily_day = days_since(daily_date)
        return intraday_close if intraday_day > daily_day else daily_close


    # Internal

    @staticmethod
    def _execute(query, values=None, path=_PATH_DB, fetch=True):
        """
        Execute an SQLite query

        Parameters
        ----------
        query : str
            Query to execute
        values : list, optional
            List of tuples with values to insert, by default None
        path : str, optional
            Path to the database, by default _PATH_DB
        fetch : bool, optional
            Whether executing a fetch or modification (changes whether fetch data or number of rows modified is returned), by default True

        Returns
        -------
        list or int
            List of values fetched (if fetch=True), else number of rows modified
        """

        conn = sqlite3.connect(path)
        cursor = conn.cursor()
        if not values: cursor.execute(query)
        else: cursor.executemany(query, values)
        response = cursor.fetchall() if fetch else cursor.rowcount
        conn.commit()
        cursor.close()
        conn.close()
        return response


    @staticmethod
    def _insert_intraday_or_daily(df, table):
        data = []
        for i in range(len(df)):
            row = df.iloc[i]
            data.append((row[Database.COL_TICKER], int(row[Database.COL_DATE]), int(row[Database.COL_OPEN]), int(row[Database.COL_CLOSE]), int(row[Database.COL_LOW]), int(row[Database.COL_HIGH]), int(row[Database.COL_VOL])))
        query = f"""
        INSERT OR IGNORE INTO {table}
        ({Database.COL_TICKER}, {Database.COL_DATE}, {Database.COL_OPEN}, {Database.COL_CLOSE}, {Database.COL_LOW}, {Database.COL_HIGH}, {Database.COL_VOL})
        VALUES
        (?,?,?,?,?,?,?)
        """
        return Database._execute(query, values=data, fetch=False)


    @staticmethod
    def _fetch_all_intraday_or_daily(table, *cols):
        sel_cols = Database._set_cols(cols)
        query = f"""
        SELECT {sel_cols} FROM {table}
        ORDER BY {Database.COL_TICKER}, {Database.COL_DATE}
        """
        return Database._execute(query)


    @staticmethod
    def _fetch_single_intraday_or_daily(ticker, table, *cols, start=None, end=None):
        sel_cols = Database._set_cols(cols)
        query = [
            f"SELECT {sel_cols} FROM {table} WHERE {Database.COL_TICKER} = '{ticker}'",
            '',
            f'ORDER BY {Database.COL_DATE}']
        if start is not None and end is not None:
            query[1] = f'AND {Database.COL_DATE} BETWEEN {start} AND {end}'
        query = ' '.join(query)
        return Database._execute(query)


    @staticmethod
    def _fetch_live_intraday_or_daily(ticker, table, date, *cols):
        """
        Retrieve the most recent intraday or daily entry for a single ticker

        Parameters
        ----------
        ticker : str
            Ticker to fetch
        table : str
            Database.COL_INTRADAY : intraday data
            Database.COL_DAILY : daily data
        date : int
            Timestamp of the live date
        """

        sel_cols = Database._set_cols(cols)

        query = f"""
        SELECT {sel_cols} FROM {table}
        WHERE {Database.COL_TICKER} = '{ticker}' AND {Database.COL_DATE} <= {date}
        ORDER BY {Database.COL_DATE} DESC LIMIT 1
        """

        return Database._execute(query)


    @staticmethod
    def _set_cols(cols):
        return "*" if cols is None else ",".join(cols)