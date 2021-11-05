class Sql():

    FOREIGN_KEYS = f"""
    PRAGMA foreign_keys = ON
    """

    CREATE_TAB_LISTING = f"""
    CREATE TABLE IF NOT EXISTS listing (
        ticker          TEXT    PRIMARY KEY,
        name            TEXT    NOT NULL,
        mgmt_pct        INTEGER NOT NULL,
        last_intraday   INTEGER NOT NULL    DEFAULT 0,
        last_daily      INTEGER NOT NULL    DEFAULT 0
    )
    """

    CREATE_TAB_INTRADAY = f"""
        CREATE TABLE IF NOT EXISTS intraday (
        ticker          TEXT    NOT NULL,
        date            INTEGER NOT NULL,
        open            INTEGER NOT NULL,
        close           INTEGER NOT NULL,
        low             INTEGER NOT NULL,
        high            INTEGER NOT NULL,
        volume          INTEGER NOT NULL,
        PRIMARY KEY (ticker, date),
        FOREIGN KEY (ticker) REFERENCES listing (ticker) ON UPDATE CASCADE ON DELETE CASCADE
    )
    """

    CREATE_TAB_DAILY = f"""
    CREATE TABLE IF NOT EXISTS daily (
        ticker          TEXT    NOT NULL,
        date            INTEGER NOT NULL ,
        open            INTEGER NOT NULL,
        close           INTEGER NOT NULL,
        low             INTEGER NOT NULL,
        high            INTEGER NOT NULL,
        volume          INTEGER NOT NULL,
        PRIMARY KEY (ticker, date),
        FOREIGN KEY (ticker) REFERENCES listing (ticker) ON UPDATE CASCADE ON DELETE CASCADE
    )
    """