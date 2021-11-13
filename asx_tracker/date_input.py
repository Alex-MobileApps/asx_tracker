from asx_tracker.date import Date
from asx_tracker.printer import Printer

class DateInput():

    @staticmethod
    def get_date(prompt):
        """
        Returns a timestamp from a user's input date

        Parameters
        ----------
        prompt : str
            Prompt provided to user

        Returns
        -------
        int or None
            Timestamp if conversion is successful, else None
        """''

        txt = input(prompt)
        date = Date.date_str_to_timestamp(txt)
        if date is None:
            Printer.ack(f'{txt} is not a valid date')
        elif date < Date.MIN or date > Date.MAX:
            Printer.ack(f'Date must be between {Date.timestamp_to_date_str(Date.MIN)} and {Date.timestamp_to_date_str(Date.MAX)}')
        else:
            return date