-- Enable foreign keys
-- Do for each connection

PRAGMA foreign_keys = ON;

-- Create tables

CREATE TABLE IF NOT EXISTS listing (
    ticker          TEXT    PRIMARY KEY,
    name            TEXT    NOT NULL,
    mgmt_pct        INTEGER NOT NULL,
    fetched_date    DATE    NOT NULL    DEFAULT '1900-01-01'
);

CREATE TABLE IF NOT EXISTS intraday (
    ticker          TEXT    NOT NULL,
    date            DATE    NOT NULL,
    open            INTEGER NOT NULL,
    close           INTEGER NOT NULL,
    low             INTEGER NOT NULL,
    high            INTEGER NOT NULL,
    volume          INTEGER NOT NULL,
    PRIMARY KEY (ticker, date),
    FOREIGN KEY (ticker) REFERENCES listing (ticker) ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS daily (
    ticker          TEXT    NOT NULL,
    date            DATE    NOT NULL ,
    open            INTEGER NOT NULL,
    close           INTEGER NOT NULL,
    low             INTEGER NOT NULL,
    high            INTEGER NOT NULL,
    volume          INTEGER NOT NULL,
    dividends       INTEGER NOT NULL,
    stock_splits    INTEGER NOT NULL,
    PRIMARY KEY (ticker, date),
    FOREIGN KEY (ticker) REFERENCES listing (ticker) ON UPDATE CASCADE ON DELETE CASCADE
);






-- EXPLAIN QUERY PLAN SELECT * FROM daily WHERE ticker = 'DHHF' AND date >= date('1700-01-01') AND date <= date('2200-01-01');

-- INSERT INTO listing
-- (ticker, name, mgmt_pct, fetched_date)
-- VALUES
-- ('DHHF', 'BetaShares Diversified All Growth ETF', 19, '1800-01-01');

-- INSERT INTO listing
-- (ticker, name, mgmt_pct, fetched_date)
-- VALUES
-- ('VDHG', 'Vanguard High Growth', 26, '1830-34-01');

-- INSERT INTO daily
-- VALUES
-- ('DHHF', '2021-10-08', 3001, 2943, 2930, 3001, 9155, 0, 0);

-- INSERT INTO daily
-- VALUES
-- ('VDHG', '2021-10-08', 3001, 2943, 2930, 3001, 9155, 0, 0);

-- DELETE FROM listing WHERE ticker = 'VDHG';

-- UPDATE listing SET ticker = 'VAS' WHERE ticker = 'VDHG';

-- DELETE FROM daily WHERE ticker = 'VDHG';
-- 
-- DELETE FROM listing WHERE ticker = 'VDHG';

-- VALUES
-- -- ('DHHF', '2021-10-08', 3001, 2943, 2930, 3001, 9155, 0, 0);
-- ('VDHG', '2021-10-08', 3001, 2943, 2930, 3001, 9155, 0, 0);

-- DELETE FROM daily WHERE ticker = 'VDHG';