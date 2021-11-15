from shutil import get_terminal_size
from asx_tracker.order_list import OrderList
from asx_tracker.str_format import StrFormat
from asx_tracker.database.database import Database

class Table():

    # Static variables

    _HEADER_HOLDINGS = ['Ticker','Units','Delayed price']
    _HEADER_ORDERS = ['Ticker','Type','Units','Limit price']


    # Table string

    @staticmethod
    def table(header, rows):
        """
        Returns a table with header and rows as a string

        Parameters
        ----------
        header : list
            Table header cell values
        rows : list
            Table row cell values (list of tuples)

        Returns
        -------
        str
            Table as a string
        """

        h = Table._header(header)
        r = '\n'.join([Table._row(row) for row in rows])
        f = Table._divider(header)
        if r:
            return h + '\n' + r + '\n' + f
        else:
            return h


    # Holding/Order list strings

    @staticmethod
    def holdings(holding_list, date):
        """
        Returns a table of a holding list

        Parameters
        ----------
        holding_list : HoldingList
            Holding list
        date : int
            Timestamp of live date

        Returns
        -------
        str
            Table as a string
        """

        return Table.table(Table._HEADER_HOLDINGS, Table._holdings_rows(holding_list, date))


    @staticmethod
    def orders(order_list):
        """
        Returns a table of an order list

        Parameters
        ----------
        order_list : OrderList
            Order list

        Returns
        -------
        str
            Table as a string
        """

        return Table.table(Table._HEADER_ORDERS, Table._orders_rows(order_list))


    # Internal

    @staticmethod
    def _header(cells):
        """
        Returns a string with the table header

        Parameters
        ----------
        cells : list
            Table header cell values

        Returns
        -------
        str
            Table header string
        """

        return Table._divider(cells) + '\n' + Table._row(cells) + '\n' + Table._divider(cells)


    @staticmethod
    def _row(cells):
        """
        Returns a string with a single row of data

        Parameters
        ----------
        cells : list
            Table row cell values

        Returns
        -------
        str
            Table row string
        """

        # Size
        cell_width = Table._cell_width(cells)

        # Cells
        return '|' + '|'.join([StrFormat.pad_str(c, cell_width) for c in cells]) + '|'


    @staticmethod
    def _divider(cells):
        """
        Returns a string with a table row divider

        Parameters
        ----------
        cells : list
            Table row cell values

        Returns
        -------
        str
            Table divider string
        """

        cell_width = Table._cell_width(cells)
        div = '-' * cell_width
        return '|' + '|'.join([div] * len(cells)) + '|'


    @staticmethod
    def _cell_width(cells):
        """
        Returns the width of each cell in a table

        Parameters
        ----------
        cells : list
            Table row cell values

        Returns
        -------
        int
            Width of each cell
        """

        len_cells = len(cells)
        max_table_width = get_terminal_size().columns
        return int(float(max_table_width - len_cells - 1) / len_cells)


    @staticmethod
    def _holdings_rows(holding_list, date):
        """
        Returns a string with the rows of a holding list

        Parameters
        ----------
        holding_list : HoldingList
            Holding list
        date : int
            Timestamp of live date

        Returns
        -------
        list
            List of row data
        """

        tickers = holding_list.tickers()
        prices = Database.fetch_multiple_live_prices(date, *tickers)
        len_holdings = len(holding_list)
        rows = [None] * len_holdings
        for i in range(len_holdings):
            rows[i] = (tickers[i], str(holding_list[tickers[i]]), StrFormat.int100_to_currency_str(prices[i]))
        return rows


    @staticmethod
    def _orders_rows(order_list):
        """
        Returns a string with the rows of an order list

        Parameters
        ----------
        order_list : OrderList
            Order list

        Returns
        -------
        list
            List of row data
        """

        len_orders = len(order_list)
        rows = [None] * len_orders
        for i in range(len_orders):
            val = order_list[i]
            lim = OrderList.MARKET_PRICE if val[3] is None else StrFormat.int100_to_currency_str(val[3])
            rows[i] = (val[0], val[1], str(val[2]), lim)
        return rows