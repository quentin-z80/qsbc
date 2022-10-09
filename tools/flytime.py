import random

from fltk import *

import flytools

class FlyWindow(Fl_Double_Window):
    def __init__(self, w, h, label):
        super().__init__(w, h, label)

if __name__ == "__main__":
    win = FlyWindow(800, 600, "FlyTime")
    win.show()
    Fl.run()
