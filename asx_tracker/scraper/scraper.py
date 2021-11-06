import pandas as pd
from time import sleep, time
import requests
from asx_tracker.database.database import Database
from asx_tracker.utils import Utils
from asx_tracker.date import Date

class Scraper():

    # Static variables

    _RATE_LIMIT         = 1.9 # Seconds (<1.8 will cause IP banning i.e. 2000 per hour)
    _COL_ETP_TICKER     = 'ASX Code'
    _COL_ETP_MGMT_PCT   = 'Management Cost %'
    _COL_ETP_NAME       = 'Exposure'
    _COL_ETP_TYPE       = 'Type'
    _COL_COM_TICKER     = 'ASX code'
    _COL_COM_NAME       = 'Company name'
    _COL_COM_LIST_DATE  = 'Listing date'
    _COL_API_DATE       = 'timestamp'
    _COL_API_HIGH       = 'high'
    _COL_API_OPEN       = 'open'
    _COL_API_LOW        = 'low'
    _COL_API_CLOSE      = 'close'
    _COL_API_VOL        = 'volume'
    _INTERVAL_DAILY     = '1d'
    _INTERVAL_INTRADAY  = '1m'
    _URL_COM            = 'https://www2.asx.com.au/markets/trade-our-cash-market/directory'
    _URL_ETP            = 'https://www2.asx.com.au/markets/trade-our-cash-market/asx-investment-products-directory/etps'
    _TICKER_EXT         = '.AX'
    _METHOD_DAILY        = 'daily'
    _METHOD_INTRADAY     = 'intraday'


    # Scrape all listings

    @staticmethod
    def scrape_all_listings(comp_url):
        return pd.concat([Scraper.scrape_etfs(), Scraper.scrape_companies(comp_url)])


    # Scrape ETFs

    @staticmethod
    def scrape_etfs():
        dfs = pd.read_html(Scraper._URL_ETP, header=0)
        df = pd.concat([df[[Scraper._COL_ETP_TICKER,Scraper._COL_ETP_NAME,Scraper._COL_ETP_MGMT_PCT]][df[Scraper._COL_ETP_TYPE] == 'ETF'] for df in dfs], axis=0)
        df.rename(columns={Scraper._COL_ETP_TICKER: Database.COL_TICKER, Scraper._COL_ETP_NAME: Database.COL_NAME, Scraper._COL_ETP_MGMT_PCT: Database.COL_MGMT_PCT}, inplace=True)
        df[Database.COL_MGMT_PCT] *= 100
        df[Database.COL_MGMT_PCT] = df[Database.COL_MGMT_PCT].astype(int)
        df = df.groupby(Database.COL_TICKER, as_index=False).max()
        return Database.insert_listings(df)


    # Scrape companies

    @staticmethod
    def scrape_companies(url):
        df = pd.read_csv(url, header=0)[[Scraper._COL_COM_TICKER, Scraper._COL_COM_NAME, Scraper._COL_COM_LIST_DATE]]
        df.dropna(subset=[Scraper._COL_COM_LIST_DATE], inplace=True)
        df.drop(Scraper._COL_COM_LIST_DATE, axis=1, inplace=True)
        df.rename(columns={Scraper._COL_COM_TICKER: Database.COL_TICKER, Scraper._COL_COM_NAME: Database.COL_NAME}, inplace=True)
        df[Database.COL_NAME] = df[Database.COL_NAME].fillna('')
        df[Database.COL_MGMT_PCT] = 0
        return Database.insert_listings(df)


    # Scrape intraday

    @staticmethod
    def scrape_intraday():
        return Scraper._scrape_intraday_or_daily(Scraper._scrape_intraday_internal, Database.COL_LAST_INTRADAY)


    # Scrape daily

    @staticmethod
    def scrape_daily():
        return Scraper._scrape_intraday_or_daily(Scraper._scrape_daily_internal, Database.COL_LAST_DAILY)


    # Internal

    @staticmethod
    def _scrape_intraday_or_daily(fn, date_col):

        # Setup data
        data = Database.fetch_listings(Database.COL_TICKER, date_col)
        len_data = len(data)
        count = 0
        close = Date.timestamp_last_close()

        # Scrape
        for i, (ticker, fetched_date) in enumerate(data):
            count += fn(ticker, fetched_date, close, date_col)
            print(f'{Utils.CLEAR_LINE}  {int(100 * (i+1) / len_data)}% ({count} added) - last update: {ticker} ', end='', flush=True)
        return count


    @staticmethod
    def _scrape_daily_internal(ticker, fetched_date, close, date_col):
        start = fetched_date + 1
        if start >= close:
            return 0
        count = Scraper._insert_interval(ticker, Database.insert_daily, Scraper._INTERVAL_DAILY, start, close, date_col)
        return count if count is not None else 0


    @staticmethod
    def _scrape_intraday_internal(ticker, fetched_date, close, date_col):
        count = 0
        start = max(fetched_date + 1, Date.timestamp_30_days(offset=Date.HOUR))
        while start < close:
            end = min(close, start + Date.WEEK)
            tmp_count = Scraper._insert_interval(ticker, Database.insert_intraday, Scraper._INTERVAL_INTRADAY, start, end, date_col)
            if tmp_count is not None:
                count += tmp_count
            else:
                break
            start = end + 1
        return count


    @staticmethod
    def _insert_interval(ticker, insert_fn, interval, start, end, date_col):
        try:
            df = Scraper._repeat_scrape_single_interval(ticker, interval, start, end)
            count = insert_fn(df) if df is not None else 0
            Database.update_listings_date(ticker, end, date_col)
            return count
        except Exception as e:
            print(f'{Utils.CLEAR_LINE}  FAILED: {ticker} - {e} ')


    @staticmethod
    def _repeat_scrape_single_interval(ticker, interval, start, end):
        get_df = lambda: Scraper._scrape_single_interval(ticker, interval, start, end)
        try: df = get_df()
        except RuntimeError: df = get_df()
        return df


    @staticmethod
    def _scrape_single_interval(ticker, interval, start, end):
        start_time = time()
        # Scrape
        url = Scraper._url_yfinance(ticker + Scraper._TICKER_EXT, interval, start, end)
        data = requests.get(url, headers={'User-Agent':Utils._USER_AGENT})

        # Failed request
        if data.status_code != 200:
            Scraper._rate_limit(start_time)
            raise RuntimeError(f'Status code not 200 ({data.status_code})')

        # Servers down
        if 'Will be right back' in data.text:
            Scraper._rate_limit(start_time)
            raise RuntimeError('Yahoo! Finance servers are currently down')

        data = data.json()
        if 'chart' not in data:
            Scraper._rate_limit(start_time)
            raise RuntimeError('No key "chart"')
        data = data['chart']

        # Error message
        if 'error' in data:
            error = data['error']
            if error and 'description' in error:
                Scraper._rate_limit(start_time)
                raise ValueError(error['description'])

        if 'result' not in data:
            Scraper._rate_limit(start_time)
            raise RuntimeError('No key "result"')
        data = data['result']
        if not Utils.has_len(data):
            Scraper._rate_limit(start_time)
            raise RuntimeError('Value for key "result" has no len')
        if len(data) != 1:
            Scraper._rate_limit(start_time)
            raise RuntimeError('Value for key "result" is not of length 1')
        data = data[0]

        # Dates
        if Scraper._COL_API_DATE not in data:
            Scraper._rate_limit(start_time)
            return None # No values
        dates = data[Scraper._COL_API_DATE]
        if not Utils.has_len(dates):
            Scraper._rate_limit(start_time)
            raise RuntimeError(f'Value for key "{Scraper._COL_API_DATE}" has no len')
        len_dates = len(dates)
        if len_dates == 0:
            Scraper._rate_limit(start_time)
            return None # No values

        # Quotes
        if 'indicators' not in data:
            Scraper._rate_limit(start_time)
            raise RuntimeError('No key "indicators"')
        quote = data['indicators']
        if 'quote' not in quote:
            Scraper._rate_limit(start_time)
            raise RuntimeError('No key "quote"')
        quote = quote['quote']
        if not Utils.has_len(quote):
            Scraper._rate_limit(start_time)
            raise RuntimeError('Value for key "quote" has no len')
        if len(quote) != 1:
            Scraper._rate_limit(start_time)
            raise RuntimeError('Value for key "quote" is not of length 1')
        quote = quote[0]

        # Values
        high = Scraper._get_quote_value(Scraper._COL_API_HIGH, quote, len_dates)
        open = Scraper._get_quote_value(Scraper._COL_API_OPEN, quote, len_dates)
        low = Scraper._get_quote_value(Scraper._COL_API_LOW, quote, len_dates)
        close = Scraper._get_quote_value(Scraper._COL_API_CLOSE, quote, len_dates)
        volume = Scraper._get_quote_value(Scraper._COL_API_VOL, quote, len_dates)

        # DataFrame
        df = pd.DataFrame({Database.COL_DATE: dates, Database.COL_HIGH: high, Database.COL_OPEN: open, Database.COL_LOW: low, Database.COL_CLOSE: close, Database.COL_VOL: volume})
        df.dropna(how='any', inplace=True)
        for col in [Database.COL_HIGH, Database.COL_OPEN, Database.COL_LOW, Database.COL_CLOSE]:
            df[col] = round(df[col] * 100).astype(int)
        df[Database.COL_VOL] = df[Database.COL_VOL].astype(int)
        df[Database.COL_TICKER] = ticker
        Scraper._rate_limit(start_time)
        return df


    @staticmethod
    def _rate_limit(start_time):
        elapsed = time() - start_time
        sleep_time = Scraper._RATE_LIMIT - elapsed
        if sleep_time > 0:
            sleep(sleep_time)


    @staticmethod
    def _url_yfinance(ticker, interval, start, end=None):
        """
        Returns the API endpoint to fetch yahoo finance data

        Parameters
        ----------
        ticker : str
            Listing ticker (with .AX extension)
        interval : str
            Frequency of updates. Valid intervals:
            - 1m:                           Up to last 30 days (7 days per request)
            - 2m, 5m, 15m, 30m, 60m, 90m:   Up to last 60 days (60 days per request)
            - 1h:                           Up to last 730 days (730 days per request)
            - 1d, 5d, 1wk, 1mo, 3mo:        Up to all time (Any days per request)
        start : int
            Start date
        end : int, optional
            End date, by default None

        Returns
        -------
        str
            URL to fetch yahoo finance data
        """

        if end is None:
            end = Date.timestamp_now()
        return f'https://query2.finance.yahoo.com/v8/finance/chart/{ticker}?interval={interval}&period1={start}&period2={end}'


    @staticmethod
    def _get_quote_value(key, quote, len_timestamps):
        if key not in quote :
            raise RuntimeError(f'No key "{key}"')
        vals = quote[key]
        if not Utils.has_len(vals):
            raise RuntimeError(f'Value for key "{key}" has no len')
        if len(vals) != len_timestamps:
            raise RuntimeError(f'Length mismatch for timestamps and {key} ({len_timestamps} vs. {len(vals)})')
        return vals