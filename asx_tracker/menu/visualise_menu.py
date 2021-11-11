from asx_tracker.menu.menu import Menu
from asx_tracker.plot import Plot
from asx_tracker.date import Date
from asx_tracker.database.database import Database
from asx_tracker.printer import Printer

class VisualiseMenu(Menu):

    _NOT_SET = 'Not set'
    _DEF_START = Date.MIN
    _DEF_END = Date.MAX
    _DEF_PLT_TYPE = 'Line'
    _VAR_DAILY = 'Daily'
    _VAR_INTRADAY = 'Intraday'
    _DEF_VARIATION = _VAR_DAILY
    _PLT_TYPES = {'Line':'line', 'Candlestick':'candle', 'OHLC':'ohlc', 'Renko':'renko', 'Hollow and filled':'hollow_and_filled'}

    def __init__(self):
        super().__init__(title = 'Visualise')
        self.ticker = None
        self.start = VisualiseMenu._DEF_START
        self.end = VisualiseMenu._DEF_END
        self.plt_type = VisualiseMenu._DEF_PLT_TYPE
        self.variation = VisualiseMenu._DEF_VARIATION
        self.mav = None
        self.set_options()

    def set_options(self):
        fn = lambda a: a if a is not None else VisualiseMenu._NOT_SET
        self.options = [
            f'Set ticker:\t\t{fn(self.ticker)}',
            f'Set start date:\t{Date.timestamp_to_date_str(self.start)}',
            f'Set end date:\t{Date.timestamp_to_date_str(self.end)}',
            f'Set plot type:\t{self.plt_type}',
            f'Data variation:\t{self.variation}',
            f'Moving average:\t{fn(self.mav)}',
            'Visualise',
            'Back'
        ]

    def handle_option(self, controller):
        option = self.select_option(self.options)
        if option == 8:
            return controller.pop()
        print()
        if option == 1:
            self.set_ticker()
        elif option == 2:
            self.set_start()
        elif option == 3:
            self.set_end()
        elif option == 4:
            self.set_plt_type()
        elif option == 5:
            self.set_variation()
        elif option == 6:
            self.set_mav()
        else:
            self.visualise()
        self.set_options()
        controller.display()


    # Ticker

    def set_ticker(self):
        ticker = input('Enter ticker: ').upper()
        if Database.fetch_single_listing(ticker, Database.COL_TICKER):
            self.ticker = ticker
        else:
            Printer.ack(f'{ticker} is not a valid ticker')


    # Start date

    def set_start(self):
        self.start = input('Enter start date: ')


    # End date

    def set_end(self):
        self.end = input('Enter end date: ')


    # Plot type

    def set_plt_type(self):
        options = list(VisualiseMenu._PLT_TYPES.keys())
        Printer.options(options)
        option = self.select_option(options)
        self.plt_type = options[option-1]


    # Daily or Intraday variation

    def set_variation(self):
        options = [VisualiseMenu._VAR_DAILY, VisualiseMenu._VAR_INTRADAY]
        Printer.options(options)
        option = self.select_option(options)
        self.variation = options[option-1]


    # Moving average

    def set_mav(self):
        mav = input('Enter moving averages (0 for None): ')
        try:
            mav = VisualiseMenu._str_to_mav(mav)
            self.mav = None if mav is None else VisualiseMenu._mav_to_str(mav)
        except:
            Printer.ack("Values should be integers, e.g. '3' or '3,5'")

    @staticmethod
    def _str_to_mav(mav):
        mav = mav.replace(' ', '')
        mav = [int(m) for m in mav.split(',')]
        for i in reversed(range(len(mav))):
            if mav[i] <= 0:
                mav.pop(i)
        if len(mav) > 0:
            return mav

    @staticmethod
    def _mav_to_str(mav):
        if mav is not None:
            return ','.join([str(m) for m in mav])

    def visualise(self):
        if self.ticker is None:
            Printer.ack('Ticker is not set')
            return
        print('Close plot to continue')
        kwargs = {}
        if self.mav is not None: kwargs['mav'] = VisualiseMenu._str_to_mav(self.mav)
        fn = Plot.daily if self.variation == VisualiseMenu._VAR_DAILY else Plot.intraday
        fn(self.ticker, self.start, self.end, type=VisualiseMenu._PLT_TYPES[self.plt_type], **kwargs)