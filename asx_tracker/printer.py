from shutil import get_terminal_size

class Printer():

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


    # Error message

    @staticmethod
    def ack(message):
        input(f'{message} (Press Enter to continue)')


    # Options

    @staticmethod
    def options(opts):
        for i, s in enumerate(opts):
            print(f'{i+1}. {s}')