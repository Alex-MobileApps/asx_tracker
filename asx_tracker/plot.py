import mplfinance
import pandas as pd
from asx_tracker.date import Date
from asx_tracker.database.database import Database
from asx_tracker.printer import Printer
from asx_tracker.utils import Utils

class Plot():

    # Static variables

    _COL_OPEN       = 'Open'
    _COL_HIGH       = 'High'
    _COL_LOW        = 'Low'
    _COL_CLOSE      = 'Close'
    _COL_VOL        = 'Volume'
    _DEF_TYPE       = 'line'

    _PERIOD_1D      = '1 day'
    _PERIOD_1W      = '1 week'
    _PERIOD_1M      = '1 month'
    _PERIOD_6M      = '6 months'
    _PERIOD_YTD     = 'Year to date'
    _PERIOD_1Y      = '1 year'
    _PERIOD_2Y      = '2 years'
    _PERIOD_MAX     = 'Max'
    PERIOD_OPTIONS  = [_PERIOD_1D,_PERIOD_1W,_PERIOD_1M,_PERIOD_6M,_PERIOD_YTD,_PERIOD_1Y,_PERIOD_2Y,_PERIOD_MAX]


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

        Plot._plot_intraday_or_daily(ticker, Database.fetch_single_intraday, start, end, title=ticker, **kwargs)


    # Plot daily

    @staticmethod
    def daily(ticker, start, end, **kwargs):
        """
        Plots daily data for a ticker.
        See Plot.intraday
        """

        Plot._plot_intraday_or_daily(ticker, Database.fetch_single_daily, start, end, title=ticker, **kwargs)


    # Periods

    @staticmethod
    def period_1d(ticker, end, **kwargs):
        """
        Plots data for a ticker over a single day

        Parameters
        ----------
        ticker : str
            Ticker name
        end : int
            Timestamp of end date
        """

        start = Date.timestamp_to_day_start(end)
        Plot.intraday(ticker, start, end, **kwargs)


    @staticmethod
    def period_1w(ticker, end, **kwargs):
        """
        Plots data for a ticker over 1 week.
        See Plot.period_1d
        """

        start = Date.timestamp_to_day_start(end) - Date.WEEK
        Plot._plot_period_long(ticker, start, end, **kwargs)


    @staticmethod
    def period_1m(ticker, end, **kwargs):
        """
        Plots data for a ticker over 31 days.
        See Plot.period_1d
        """

        start = Date.timestamp_to_day_start(end) - Date.MONTH_31
        Plot._plot_period_long(ticker, start, end, **kwargs)


    @staticmethod
    def period_6m(ticker, end, **kwargs):
        """
        Plots data for a ticker over 6 months.
        See Plot.period_1d
        """

        start = Date.timestamp_to_day_start(end) - Date.HALF_YEAR_365
        Plot._plot_period_long(ticker, start, end, **kwargs)


    @staticmethod
    def period_ytd(ticker, end, **kwargs):
        """
        Plots data for a ticker for the current year
        See Plot.period_1d
        """

        start = Date.timestamp_to_year_start(end)
        Plot._plot_period_long(ticker, start, end, **kwargs)


    @staticmethod
    def period_1y(ticker, end, **kwargs):
        """
        Plots data for a ticker over 1 year.
        See Plot.period_1d
        """

        start = Date.timestamp_to_day_start(end) - Date.YEAR_365
        Plot._plot_period_long(ticker, start, end, **kwargs)


    @staticmethod
    def period_2y(ticker, end, **kwargs):
        """
        Plots data for a ticker over 2 years.
        See Plot.period_1d
        """

        start = Date.timestamp_to_day_start(end) - 2 * Date.YEAR_365
        Plot._plot_period_long(ticker, start, end, **kwargs)


    @staticmethod
    def period_max(ticker, end, **kwargs):
        """
        Plots full history of data for a ticker.
        See Plot.period_1d
        """

        start = Date.MIN
        Plot._plot_period_long(ticker, start, end, **kwargs)


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

        Returns
        -------
        bool
            Whether or not data was found for the specified ticker and dates
        """

        df = Plot._fetch_intraday_or_daily(ticker, fetch_fn, start, end)
        if df is None:
            Printer.ack(f'No data found for {ticker} between the specified dates')
        else:
            print('Close plot to continue')
            Plot._plot(df, **kwargs)


    @staticmethod
    def _plot_period_long(ticker, start, end, **kwargs):
        """
        Plots data across a period for a ticker

        Parameters
        ----------
        ticker : str
            Ticker to plot data for
        start : int
            Timestamp of start date of the plot
        end : int
            Timestamp of end date of the plot
        """

        # Market closed = Daily only
        if not Date.market_open(end):
            end = Date.timestamp_to_day_end(end) if Date.after_close(end) else Date.timestamp_to_prev_day_end(end)
            return Plot.daily(ticker, start, end, **kwargs)

        # Market open
        intraday_date, intraday_price = Database.fetch_single_live_intraday(ticker, end)
        if intraday_date is None or not Date.same_day(end, intraday_date):
            end = Date.timestamp_to_prev_day_end(end)
            return Plot.daily(ticker, start, end, **kwargs)

        # TODO: show during day
        return Plot.intraday(ticker, start, end, **kwargs)


    @staticmethod
    def _fetch_intraday_or_daily(ticker, fetch_fn, start, end):
        """
        Fetches a DataFrame of intraday or daily data for a ticker

        Parameters
        ----------
        See Plot._plot_intraday_or_daily

        Returns
        -------
        pandas.DataFrame or None
            DataFrame with intraday or daily data for a ticker if data is found, else None
        """

        fetch_cols = [Database.COL_DATE, Database.COL_OPEN, Database.COL_HIGH, Database.COL_LOW, Database.COL_CLOSE, Database.COL_VOL]
        data = fetch_fn(ticker, *fetch_cols, start=start, end=end)
        if len(data) == 0:
            return
        plot_cols = [Database.COL_DATE, Plot._COL_OPEN, Plot._COL_HIGH, Plot._COL_LOW, Plot._COL_CLOSE, Plot._COL_VOL]
        df = pd.DataFrame(data, columns=plot_cols)
        for col in [Plot._COL_OPEN, Plot._COL_HIGH, Plot._COL_LOW, Plot._COL_CLOSE]:
            df[col] /= 100
        new_dates = Date.timestamp_to_datetime(*df[Database.COL_DATE])
        df[Database.COL_DATE] = new_dates if Utils.has_len(new_dates) else [new_dates]
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