import sqlite3
from asx_tracker.database.sql import Sql

class Database():

    # Static variables

    _TAB_LISTING = 'listing'
    _TAB_INTRADAY = 'intraday'
    _TAB_DAILY = 'daily'
    _COL_TICKER = 'ticker'
    _COL_NAME = 'name'
    _COL_MGMT_PCT = 'mgmt_pct'
    _COL_DATE = 'date'
    _COL_OPEN = 'open'
    _COL_CLOSE = 'close'
    _COL_LOW = 'low'
    _COL_HIGH = 'high'
    _COL_VOL= 'volume'
    _COL_DIV = 'dividends'
    _COL_SPL = 'stock_splits'
    _COL_FETCHED_DATE = 'fetched_date'

    _PATH_DB = 'asx_tracker/database/data/database.db'


    # Execute

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


    # Create tables

    @staticmethod
    def create_tables():
        Database._execute(Sql._FOREIGN_KEYS, fetch=False)
        Database._execute(Sql._CREATE_TAB_LISTING, fetch=False)
        Database._execute(Sql._CREATE_TAB_INTRADAY, fetch=False)
        Database._execute(Sql._CREATE_TAB_DAILY, fetch=False)


    # Listings

    @staticmethod
    def insert_listings(df):
        data = []
        for i in range(len(df)):
            row = df.iloc[i]
            data.append((row[Database._COL_TICKER], row[Database._COL_NAME], int(row[Database._COL_MGMT_PCT])))
        query = f"""
        INSERT OR IGNORE INTO {Database._TAB_LISTING}
        ({Database._COL_TICKER}, {Database._COL_NAME}, {Database._COL_MGMT_PCT})
        VALUES
        (?,?,?)
        """
        return Database._execute(query, values=data, fetch=False)

    @staticmethod
    def fetch_listings(*cols):
        sel_cols = "*" if cols is None else ",".join(cols)
        query = f"""
        SELECT {sel_cols} FROM {Database._TAB_LISTING} ORDER BY {Database._COL_TICKER}
        """
        return Database._execute(query)

    @staticmethod
    def update_listings_date(ticker, fetched_date):
        data = [(int(fetched_date),ticker)]
        query = f"""
        UPDATE {Database._TAB_LISTING}
        SET {Database._COL_FETCHED_DATE} = ?
        WHERE {Database._COL_TICKER} = ?
        """
        return Database._execute(query, values=data, fetch=False)


    # Intraday

    @staticmethod
    def insert_intraday(df):
        data = []
        for i in range(len(df)):
            row = df.iloc[i]
            data.append((row[Database._COL_TICKER], int(row[Database._COL_DATE]), int(row[Database._COL_OPEN]), int(row[Database._COL_CLOSE]), int(row[Database._COL_LOW]), int(row[Database._COL_HIGH]), int(row[Database._COL_VOL])))
        query = f"""
        INSERT OR IGNORE INTO {Database._TAB_INTRADAY}
        ({Database._COL_TICKER}, {Database._COL_DATE}, {Database._COL_OPEN}, {Database._COL_CLOSE}, {Database._COL_LOW}, {Database._COL_HIGH}, {Database._COL_VOL})
        VALUES
        (?,?,?,?,?,?,?)
        """
        return Database._execute(query, values=data, fetch=False)


    # Daily

    @staticmethod
    def insert_daily(df):
        raise NotImplementedError()



