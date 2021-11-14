from datetime import datetime, timedelta
from asx_tracker.utils import Utils
from asx_tracker.date import Date

class StrFormat():

	# Static variables

	_NON_NEG = False


	# Padding

	@staticmethod
	def pad_str(txt, width):
		"""
        Fills a string to a specified width by padding blank characters

        Parameters
        ----------
        txt : str
            Original string
        width : int
            Width to fill to

        Returns
        -------
        str
            Filled string
        """

		len_txt = len(txt)
		if len_txt >= width:
			return txt[:width]
		return txt + (width - len_txt) * ' '


	# From str

	@staticmethod
	def date_str_to_timestamp(txt):
		"""
		Converts a date string to a timestamp integer

		Parameters
		----------
		txt : str
			Date string

		Returns
		-------
		int or None
			int if string can be converted, else None
		"""

		txt = txt.strip()

		# Parse timestamp string
		if Utils.is_float(txt):
			val = int(round(float(txt)))
			if val >= Date.MIN and val <= Date.MAX:
				return val
			return None

        # Now, Min, Max
		txt = txt.upper()
		if txt == Date._NOW:
			now = Date._TZ_SYDNEY_INFO.localize(datetime.now())
			now -= timedelta(seconds=now.second)
			return int(now.timestamp())
		elif txt == Date._MIN:
			return Date.MIN
		elif txt == Date._MAX:
			return Date.MAX

        # Parse text
		txt = txt.split(' ')
		txt = [t for t in txt if t != '']
		time = [0] * 6 # year, month, day, hour, minute, second
		try:
			time[0] = int(txt[2])
			time[1] = Date._MONTH_MAP[txt[1]]
			time[2] = int(txt[0])
			if len(txt) > 3:
				hour, min = txt[3].split(':')
				time[3] = int(hour)
				if min.endswith('PM') and time[3] != 12:
					time[3] += 12
				min = min.replace('AM', '')
				min = min.replace('PM', '')
				time[4] = int(min)
			utc_dt = datetime(*time)
			loc_dt = Date._TZ_SYDNEY_INFO.localize(utc_dt)
			timestamp = int(loc_dt.timestamp())
			if timestamp >= Date.MIN and timestamp <= Date.MAX:
				return timestamp
		except:
			return


	@staticmethod
	def minute_str_to_int(txt, non_neg=_NON_NEG):
		"""
        Converts a time string in minutes to an integer

        Parameters
        ----------
        txt : str
            Time string in minutes
		non_neg : bool, optional
			Whether or not negative numbers are allowed, by default _NON_NEG

        Returns
        -------
        int or None
            int if string can be converted, else None
        """

		txt = txt.replace(' ', '')
		txt = txt.upper()
		txt = txt.replace('MIN', '')

		if not Utils.is_float(txt):
			return

		val = int(round(float(txt)))
		if non_neg and val < 0:
			return
		return val


	@staticmethod
	def percentage_str_to_int(txt, non_neg=_NON_NEG):
		"""
		Converts a percentage string to an integer

		Parameters
		----------
		txt : str
			Percentage string
		non_neg : bool, optional
			Whether or not negative numbers are allowed, by default _NON_NEG

		Returns
		-------
		[type]
			[description]
		"""
		txt = txt.replace(' ', '')
		txt = txt.replace('%', '')
		if not Utils.is_float(txt):
			return

		val = int(round(float(txt)))
		if non_neg and val < 0:
			return
		return val


	@staticmethod
	def currency_str_to_int100(txt, non_neg=_NON_NEG):
		"""
        Converts a currency string to an integer

        Parameters
        ----------
        txt : str
            Currency string
		non_neg : bool, optional
			Whether or not negative numbers are allowed, by default _NON_NEG

        Returns
        -------
        int or None
            int if string can be converted, else None
        """

		txt = txt.replace(' ', '')
		txt = txt.replace('$', '')
		txt = txt.replace(',', '')

		if not Utils.is_float(txt):
			return

		val = float(txt)
		if non_neg and val < 0:
			return
		return int(round(val * 100))


	# To str

	@staticmethod
	def int100_to_currency_str(val):
		"""
        Converts an integer to a currency string

        Parameters
        ----------
        val : int
            Value to convert to a currency string

        Returns
        -------
        str
            Currency string representation of value
        """

		txt = str(abs(val)).zfill(3)
		pref = '-' if val < 0 else ''
		dollars = txt[:-2]
		cents = txt[-2:]
		split_dollars = []
		while len(dollars) >= 3:
			split_dollars.append(dollars[-3:])
			dollars = dollars[:-3]
		if len(dollars) > 0:
			split_dollars.append(dollars)
		dollars = ','.join(reversed(split_dollars))
		return pref + '$' + dollars + '.' + cents