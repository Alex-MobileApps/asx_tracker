from shutil import get_terminal_size

class Printer():

    _DIV_BOLD = '======================================'
    _DIV_REG = '--------------------------------------'


    # Headers

    @staticmethod
    def header(txt=None, top=True, bottom=True):
        Printer._headers(txt, top, bottom, True)

    @staticmethod
    def subheader(txt, top=False, bottom=True):
        Printer._headers(txt, top, bottom, False)

    @staticmethod
    def _headers(txt, top, bottom, bold):
        if top: Printer.divider(bold)
        if txt: print(txt)
        if bottom: Printer.divider(bold)


    # Dividers

    @staticmethod
    def divider(bold=False):
        size = get_terminal_size().columns
        if bold:
            print('=' * size)
        else:
            print('-' * size)
        #print(Printer._DIV_BOLD if bold else Printer._DIV_REG)

    
    