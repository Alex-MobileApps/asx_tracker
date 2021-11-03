import sqlite3

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

    _PATH_DB = 'asx_tracker/database/data/database.db'


    # Execute

    @staticmethod
    def execute(query, values=None, path=_PATH_DB, fetch=True):
        conn = sqlite3.connect(path)
        cursor = conn.cursor()
        if not values: cursor.execute(query)
        else: cursor.executemany(query, values)
        response = cursor.fetchall() if fetch else cursor.rowcount
        conn.commit()
        cursor.close()
        conn.close()
        return response


    # Insert new listings

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

        return Database.execute(query, values=data, fetch=False)


    # Insert daily

    @staticmethod
    def insert_daily(df):
        raise NotImplementedError()


    # Insert intraday

    @staticmethod
    def insert_intraday(df):
        raise NotImplementedError()



