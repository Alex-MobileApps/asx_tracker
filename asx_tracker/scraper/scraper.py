import pandas as pd
from time import sleep, time
import requests
from asx_tracker.database.database import Database
from asx_tracker.utils import Utils
from asx_tracker.date import Date

class Scraper():

    # Column names when scraping
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

    # URLs
    _URL_COM            = 'https://www2.asx.com.au/markets/trade-our-cash-market/directory'
    _URL_ETP            = 'https://www2.asx.com.au/markets/trade-our-cash-market/asx-investment-products-directory/etps'

    # Query parameters
    _INTERVAL_DAILY     = '1d'
    _INTERVAL_INTRADAY  = '1m'
    _RANGE_DAILY        = '10y'
    _PARAM_START        = 'period1'
    _PARAM_END          = 'period2'
    _PARAM_RANGE        = 'range'
    _PARAM_INTERVAL     = 'interval'

    # Misc
    _TICKER_EXT         = '.AX'
    _METHOD_DAILY       = 'daily'
    _METHOD_INTRADAY    = 'intraday'
    _SCRAPE_ATTEMPTS    = 2
    _RATE_LIMIT         = 2.0 # Seconds (<1.8 will cause IP banning i.e. 2000 per hour)


    # Scrape ETFs

    @staticmethod
    def download_etfs():
        dfs = pd.read_html(Scraper._URL_ETP, header=0)
        df = pd.concat([df[[Scraper._COL_ETP_TICKER,Scraper._COL_ETP_NAME,Scraper._COL_ETP_MGMT_PCT]][df[Scraper._COL_ETP_TYPE] == 'ETF'] for df in dfs], axis=0)
        df.rename(columns={Scraper._COL_ETP_TICKER: Database.COL_TICKER, Scraper._COL_ETP_NAME: Database.COL_NAME, Scraper._COL_ETP_MGMT_PCT: Database.COL_MGMT_PCT}, inplace=True)
        df[Database.COL_TICKER] = df[Database.COL_TICKER].str.upper()
        df[Database.COL_NAME] = df[Database.COL_NAME].fillna('')
        df[Database.COL_MGMT_PCT] *= 100
        df[Database.COL_MGMT_PCT] = df[Database.COL_MGMT_PCT].astype(int)
        df = df.groupby(Database.COL_TICKER, as_index=False).max()
        return Database.insert_listings(df)


    # Scrape companies

    @staticmethod
    def download_companies(url):
        df = pd.read_csv(url, header=0)[[Scraper._COL_COM_TICKER, Scraper._COL_COM_NAME, Scraper._COL_COM_LIST_DATE]]
        df.dropna(subset=[Scraper._COL_COM_LIST_DATE], inplace=True)
        df.drop(Scraper._COL_COM_LIST_DATE, axis=1, inplace=True)
        df.rename(columns={Scraper._COL_COM_TICKER: Database.COL_TICKER, Scraper._COL_COM_NAME: Database.COL_NAME}, inplace=True)
        df[Database.COL_TICKER] = df[Database.COL_TICKER].str.upper()
        df[Database.COL_NAME] = df[Database.COL_NAME].fillna('')
        df[Database.COL_MGMT_PCT] = 0
        return Database.insert_listings(df)


    # Scrape intraday

    @staticmethod
    def download_intraday():
        """
        Scrapes and saves all intraday data

        Returns
        -------
        int
            Number of entries saved
        """

        return Scraper._download_intraday_or_daily(Scraper._download_ticker_intraday, Database.COL_LAST_INTRADAY, Scraper._INTERVAL_INTRADAY)


    # Scrape daily

    @staticmethod
    def download_daily():
        """
        Scrapes and saves all daily data

        Returns
        -------
        int
            Number of entries saved
        """

        return Scraper._download_intraday_or_daily(Scraper._download_ticker_daily, Database.COL_LAST_DAILY, Scraper._INTERVAL_DAILY)


    # Internal

    @staticmethod
    def _download_intraday_or_daily(scrape_fn, date_col, interval):
        """
        Scrapes and saves all intraday or daily data

        Parameters
        ----------
        scrape_fn : fn
            Scraper._download_ticker_intraday: Scrape intraday data
            Scraper._download_ticker_daily: Scrape daily data
        date_col : str
            Database.COL_LAST_INTRADAY: Scrape intraday data
            Database.COL_LAST_DAILY: Scrape daily data
        interval : str
            Scraper._INTERVAL_INTRADAY: Scrape intraday data
            Scraper._INTERVAL_DAILY: Scrape daily data

        Returns
        -------
        int
            Number of entries saved
        """

        # Setup data
        count = 0
        data = Database.fetch_all_listings(Database.COL_TICKER, date_col)
        len_data = len(data)
        params = {Scraper._PARAM_INTERVAL: interval}

        # Scrape
        for i, (ticker, last_save) in enumerate(data):
            pct_complete = int(100 * i / len_data)
            print(f'{Utils.CLEAR_LINE}  {pct_complete}% ({count} added) - currently downloading {ticker}', end='', flush=True)
            count += scrape_fn(ticker, last_save, params)

        return count


    @staticmethod
    def _download_ticker_intraday(ticker, last_save, params):
        """
        Scrapes and saves all intraday data for a ticker

        Parameters
        ----------
        ticker : str
            Listing's ticker
        last_save : int
            Timestamp of the last saved entry
        params : dict
            See Scraper._url_yfinance for possible values

        Returns
        -------
        int
            Number of entries saved
        """

        # Setup data
        count = 0
        stop = Date.timestamp_now()
        params[Scraper._PARAM_START] = max(last_save + 1, Date.timestamp_30_days(stop, Date.HOUR))

        # Scrape intervals
        while params[Scraper._PARAM_START] <= stop:
            params[Scraper._PARAM_END] = params[Scraper._PARAM_START] + Date.WEEK
            tmp_count = Scraper._save_period(ticker, Database.insert_intraday, params, Database.COL_LAST_INTRADAY)
            if tmp_count is None:
                break
            count += tmp_count
            params[Scraper._PARAM_START] = params[Scraper._PARAM_END] + 1

        return count


    @staticmethod
    def _download_ticker_daily(ticker, last_save, params):
        """
        Scrapes and saves all daily data for a ticker

        Parameters
        ----------
        ticker : str
            Listing's ticker
        last_save : int
            Timestamp of the last saved entry
        params : dict
            See Scraper._url_yfinance for possible values

        Returns
        -------
        int
            Number of entries saved
        """

        # Setup data
        stop = Date.timestamp_now(-Date.DAY)
        params[Scraper._PARAM_START] = last_save + 1
        if params[Scraper._PARAM_START] > stop:
            return 0

        # Scrape intervals
        params[Scraper._PARAM_END] = stop
        count = Scraper._save_period(ticker, Database.insert_daily, params, Database.COL_LAST_DAILY)
        return count if count is not None else 0


    @staticmethod
    def _save_period(ticker, insert_fn, params, date_col):
        """
        Saves a single period of intraday or daily data for a ticker to the database

        Parameters
        ----------
        ticker : str
            Listing's ticker
        insert_fn : fn
            Database.insert_intraday : Save to intraday database table
            Database.insert_daily : Save to daily database table
        params : dict
            See Scraper._url_yfinance for possible values
        date_col : str
            Database.COL_LAST_INTRADAY: Scrape intraday data
            Database.COL_LAST_DAILY: Scrape daily data

        Returns
        -------
        int or None
            Number of entries if scrape was successful, None if not successful
        """

        try:
            df = Scraper._repeat_scrape_period(ticker, params)
            if df is None or len(df) == 0:
                return 0
            last_save = df[Database.COL_DATE].max()
            count = insert_fn(df)
            Database.update_listings_date(ticker, last_save, date_col)
            return count
        except Exception as e:
            print(f'{Utils.CLEAR_LINE}  FAILED: {ticker} - {e} ')


    @staticmethod
    def _repeat_scrape_period(ticker, params, interval=None):
        """
        Repeat attempts to scrape intraday or daily data for a ticker over a single time period

        Parameters
        ----------
        ticker : str
            Listing ticker
        params : dict
            See Scraper._url_yfinance for possible values
        interval : str, optional
            See Scraper._url_yfinance for possible values, by default None (i.e. already in params)

        Returns
        -------
        pandas.DataFrame
            Scraped data over a time period

        Raises
        ------
        RuntimeError
            If unable to scrape data after multiple attempts
        """

        # Add interval
        if interval is not None:
            params[Scraper._PARAM_INTERVAL] = interval

        # Multiple attempts
        last_attempt = Scraper._SCRAPE_ATTEMPTS - 1
        for i in range(Scraper._SCRAPE_ATTEMPTS):
            try:
                return Scraper._scrape_period(ticker, params)
            except RuntimeError as e:
                if i == last_attempt:
                    raise e


    @staticmethod
    def _scrape_period(ticker, params):
        """
        Scrapes intraday or daily data for a ticker over a single time period

        Parameters
        ----------
        ticker : str
            Listing's ticker
        params : dict
            See Scraper._url_yfinance for possible values

        Returns
        -------
        pandas.DataFrame
            Scraped data over a time period

        Raises
        ------
        RuntimeError
            If status code is not 200
            If Yahoo! Finance servers are down
            If JSON cannot be walked successfully
        ValueError
            If Yahoo! Finance returned a custom error
        """

        start_time = time()

        # Scrape
        url = Scraper._url_yfinance(ticker + Scraper._TICKER_EXT, params)
        data = requests.get(url, headers={'User-Agent':Utils.USER_AGENT})

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
        try:
            high = Scraper._get_quote_value(Scraper._COL_API_HIGH, quote, len_dates)
            open = Scraper._get_quote_value(Scraper._COL_API_OPEN, quote, len_dates)
            low = Scraper._get_quote_value(Scraper._COL_API_LOW, quote, len_dates)
            close = Scraper._get_quote_value(Scraper._COL_API_CLOSE, quote, len_dates)
            volume = Scraper._get_quote_value(Scraper._COL_API_VOL, quote, len_dates)
        except Exception as e:
            Scraper._rate_limit(start_time)
            raise e

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
    def _get_quote_value(key, quote, len_timestamps):
        """
        Parses the values for a key in the scraped quote

        Parameters
        ----------
        key : str
            Key in quotes to parse
        quote : dict
            Quote to retrieve key values from
        len_timestamps : int
            Number of timestamps parsed

        Returns
        -------
        list
            List of values for quote[key]

        Raises
        ------
        RuntimeError
            If JSON cannot be walked successfully or the length of the values and timestamps differ
        """

        if key not in quote:
            raise RuntimeError(f'No key "{key}"')
        vals = quote[key]
        if not Utils.has_len(vals):
            raise RuntimeError(f'Value for key "{key}" has no len')
        if len(vals) != len_timestamps:
            raise RuntimeError(f'Length mismatch for timestamps and {key} ({len_timestamps} vs. {len(vals)})')
        return vals


    @staticmethod
    def _rate_limit(start_time):
        """
        Pauses the program to prevent exceeding Yahoo! Finance rate limits

        Parameters
        ----------
        start_time : float
            Last time Yahoo! Finance API was used
        """

        elapsed = time() - start_time
        sleep_time = Scraper._RATE_LIMIT - elapsed
        if sleep_time > 0:
            sleep(sleep_time)


    @staticmethod
    def _url_yfinance(ticker, params):
        """
        Returns the API endpoint to fetch yahoo finance data

        Parameters
        ----------
        ticker : str
            Listing ticker (with .AX extension)
        params : dict
            interval: str
                - 1m:                           Up to last 30 days (7 days per request)
                - 2m, 5m, 15m, 30m, 60m, 90m:   Up to last 60 days (60 days per request)
                - 1h:                           Up to last 730 days (730 days per request)
                - 1d, 5d, 1wk, 1mo, 3mo:        Up to all time (Any days per request)
            Scraper._PARAM_START : int
                - Start timestamp
            Scraper._PARAM_END : int
                - End timestamp

        Returns
        -------
        str
            URL to fetch Yahoo! Finance data
        """

        params_str = '&'.join([f'{k}={v}' for k,v in params.items()])
        return f'https://query2.finance.yahoo.com/v8/finance/chart/{ticker}?{params_str}'