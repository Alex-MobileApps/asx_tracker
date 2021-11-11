import mplfinance
import pandas as pd
from asx_tracker.date import Date
from asx_tracker.database.database import Database

class Plot():

    # Static variables

    _COL_OPEN = 'Open'
    _COL_HIGH = 'High'
    _COL_LOW = 'Low'
    _COL_CLOSE = 'Close'
    _COL_VOL = 'Volume'
    _DEF_TYPE = 'line'


    # Plot intraday

    @staticmethod
    def intraday(ticker, start, end, **kwargs):
        """
        Plots intraday data for a ticker

        Parameters
        ----------
        ticker : str
            Ticker to plot data for
        start : int
            Timestamp of start date of the plot
        end : int
            Timestamp of end date of the plot
        """

        title = f'{ticker} intraday data'
        Plot._plot_intraday_or_daily(ticker, Database.fetch_single_intraday, start, end, title=title, **kwargs)


    # Plot daily

    @staticmethod
    def daily(ticker, start, end, **kwargs):
        """
        Plots whole day data for a ticker.
        See Plot.intraday
        """

        title = f'{ticker} daily data'
        Plot._plot_intraday_or_daily(ticker, Database.fetch_single_daily, start, end, title=title, **kwargs)


    # Internal

    @staticmethod
    def _plot_intraday_or_daily(ticker, fetch_fn, start, end, **kwargs):
        """
        Plots one of intraday or daily data for a ticker

        Parameters
        ----------
        ticker : str
            Ticker to plot data for
        fetch_fn : function
            Database.fetch_single_intraday : if plotting intraday data
            Database.fetch_single_daily : if plotting daily data
        start : int
            Timestamp of start date of the plot
        end : int
            Timestamp of end date of the plot
        """

        df = Plot._fetch_intraday_or_daily(ticker, fetch_fn, start, end)
        if df is None:
            print(f'No data found for {ticker}')
        else:
            Plot._plot(df, **kwargs)


    @staticmethod
    def _fetch_intraday_or_daily(ticker, fetch_fn, start, end):
        """
        Fetches a DataFrame of intraday or daily data for a ticker

        Parameters
        ----------
        See Plot._plot_intraday_or_daily

        Returns
        -------
        pandas.DataFrame
            DataFrame with intraday or daily data for a ticker
        """

        fetch_cols = [Database.COL_DATE, Database.COL_OPEN, Database.COL_HIGH, Database.COL_LOW, Database.COL_CLOSE, Database.COL_VOL]
        data = fetch_fn(ticker, *fetch_cols, start=start, end=end)
        if len(data) == 0:
            return
        plot_cols = [Database.COL_DATE, Plot._COL_OPEN, Plot._COL_HIGH, Plot._COL_LOW, Plot._COL_CLOSE, Plot._COL_VOL]
        df = pd.DataFrame(data, columns=plot_cols)
        for col in [Plot._COL_OPEN, Plot._COL_HIGH, Plot._COL_LOW, Plot._COL_CLOSE]:
            df[col] /= 100
        df[Database.COL_DATE] = Date.timestamp_to_datetime(df[Database.COL_DATE])
        df.set_index(Database.COL_DATE, inplace=True)
        return df


    @staticmethod
    def _plot(df, block=True, **kwargs):
        """
        Plots a DataFrame using mplfinance

        Parameters
        ----------
        df : pandas.DataFrame
            DataFrame to plot
        block : bool, optional
            Whether or not to block the main thread, by default True
        """

        if 'volume' not in kwargs:
            kwargs['volume'] = True
        if 'type' not in kwargs:
            kwargs['type'] = Plot._DEF_TYPE
        mplfinance.plot(df, block=block, **kwargs)