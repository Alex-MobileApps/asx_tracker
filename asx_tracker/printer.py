class Printer():

    _HEADER = '======================================'
    _SUBHEADER = '--------------------------------------'
    _DIVIDER = '--------------------------------------'


    # Headers

    @staticmethod
    def header(txt=None, top=True, bottom=True):
        Printer._headers(txt, top, bottom, Printer._HEADER)

    @staticmethod
    def subheader(txt, top=False, bottom=True):
        Printer._headers(txt, top, bottom, Printer._SUBHEADER)

    @staticmethod
    def _headers(txt, top, bottom, divider):
        if top: print(divider)
        if txt: print(txt)
        if bottom: print(divider)


    # Dividers

    @staticmethod
    def divider():
        print(Printer._DIVIDER)