import sqlite3
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
    COL_DIV = 'dividends'
    COL_SPL = 'stock_splits'
    COL_FETCHED_DATE = 'fetched_date'

    _PATH_DB = 'asx_tracker/database/database.db'


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
        Database._execute(Sql.FOREIGN_KEYS, fetch=False)
        Database._execute(Sql.CREATE_TAB_LISTING, fetch=False)
        Database._execute(Sql.CREATE_TAB_INTRADAY, fetch=False)
        Database._execute(Sql.CREATE_TAB_DAILY, fetch=False)


    # Listings

    @staticmethod
    def insert_listings(df):
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
    def fetch_listings(*cols):
        sel_cols = "*" if cols is None else ",".join(cols)
        query = f"""
        SELECT {sel_cols} FROM {Database.TAB_LISTING} ORDER BY {Database.COL_TICKER}
        """
        return Database._execute(query)

    @staticmethod
    def update_listings_date(ticker, fetched_date):
        data = [(int(fetched_date),ticker)]
        query = f"""
        UPDATE {Database.TAB_LISTING}
        SET {Database.COL_FETCHED_DATE} = ?
        WHERE {Database.COL_TICKER} = ?
        """
        return Database._execute(query, values=data, fetch=False)


    # Intraday

    @staticmethod
    def insert_intraday(df):
        data = []
        for i in range(len(df)):
            row = df.iloc[i]
            data.append((row[Database.COL_TICKER], int(row[Database.COL_DATE]), int(row[Database.COL_OPEN]), int(row[Database.COL_CLOSE]), int(row[Database.COL_LOW]), int(row[Database.COL_HIGH]), int(row[Database.COL_VOL])))
        query = f"""
        INSERT OR IGNORE INTO {Database.TAB_INTRADAY}
        ({Database.COL_TICKER}, {Database.COL_DATE}, {Database.COL_OPEN}, {Database.COL_CLOSE}, {Database.COL_LOW}, {Database.COL_HIGH}, {Database.COL_VOL})
        VALUES
        (?,?,?,?,?,?,?)
        """
        return Database._execute(query, values=data, fetch=False)


    # Daily

    @staticmethod
    def insert_daily(df):
        raise NotImplementedError()



