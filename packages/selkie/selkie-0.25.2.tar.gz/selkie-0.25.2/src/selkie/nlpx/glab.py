
from ..pyx.com import Main
from .gdev import GDev


class SelkieMain (Main):

    # GDev

    def com_sents (self, fn):
        gdev = GDev(fn)


if __name__ == '__main__':
    SelkieMain()()
