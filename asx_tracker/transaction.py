from asx_tracker.date import Date

class Transaction():

    # Static variables

    STATUS_SUCCESSFUL   = 'SUCCESSFUL'
    STATUS_FAILED       = 'FAILED'
    STATUS_CANCELLED    = 'CANCELLED'
    STATUS_TYPES        = [STATUS_SUCCESSFUL, STATUS_CANCELLED, STATUS_FAILED]


    # Constructor

    def __init__(self, date, order, unit_price=None, gross=None, tax=None, status=None):
        self.set_date(date)
        self.set_order(order)
        self.set_unit_price(unit_price)
        self.set_gross(gross)
        self.set_tax(tax)
        self.set_status(status)


    # Setters

    def set_date(self, date):
        """
        Set transaction date

        Parameters
        ----------
        date : int
            Timestamp of transaction date

        Raises
        ------
        ValueError
            Invalid date
        """

        if date < Date.MIN or date > Date.MAX:
            raise ValueError('Invalid date')
        self.date = date


    def set_order(self, order):
        """
        Set transaction order

        Parameters
        ----------
        order : Order
            Transaction order
        """

        self.order = order


    def set_unit_price(self, unit_price):
        """
        Set unit price at time of transaction

        Parameters
        ----------
        unit_price : int
            Transaction unit price at time of transaction x100

        Raises
        ------
        ValueError
            Negative unit price
        """

        if unit_price < 0:
            raise ValueError('Negative unit price')
        self.unit_price = unit_price


    def set_gross(self, gross):
        """
        Set the gross transaction fill amount that is transferred

        Parameters
        ----------
        gross : int
            Transaction fill amount x100
        """

        self.gross = gross


    def set_tax(self, tax):
        """
        Set the Capital Gains Tax amount related to the transaction

        Parameters
        ----------
        tax : int
            Capital Gains Tax amount x100
        """
        self.tax = tax


    def set_status(self, status):
        """
        Set transaction completion status

        Parameters
        ----------
        status : str
            Transaction.STATUS_SUCCESSFUL : Successful
            Transaction.STATUS_FAILED : Failed
            Transaction.STATUS_CANCELLED : Cancelled

        Raises
        ------
        ValueError
            Invalid transaction status
        """

        if status is not None and status not in Transaction.STATUS_TYPES:
            raise ValueError('Invalid transaction status')
        self.status = status
