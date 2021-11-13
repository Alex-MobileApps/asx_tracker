from shutil import get_terminal_size
from asx_tracker.utils import Utils

class Table():

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
        return '|' + '|'.join([Utils.pad_str(c, cell_width) for c in cells]) + '|'


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