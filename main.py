from NewtonFractalPlot import *
from PlotWindow import *
from poly import *
import re
import sys


def is_int(s):
    try:
        int(s)
    except ValueError:
        return False
    else:
        return True


if __name__ == '__main__':
    coefficients = [-1, 0, 0, 1]
    width, height = (640, 480)

    # checking if the first argument is a size specification like -800x600
    if len(sys.argv) > 1 and re.match(r"^-\d+x\d+$", sys.argv[1]) is not None:
        width, height = map(int, sys.argv[1][1:].split('x'))
        if width == 0 or height == 0:
            print("Width and height must be greater than 0.")
            exit()
        del sys.argv[1]

    # now that size is handled / removed, check for coefficients
    if len(sys.argv) > 1:
        if all(is_int(c) for c in sys.argv[1:]):
            if len(sys.argv[1:]) >= 4:
                coefficients = [int(c) for c in sys.argv[1:]]
            else:
                print("Polynomial input must be at least cubic, i.e. four or more coefficients.")
                exit()
        else:
            print("Coefficients must be integers.")
            exit()

    nf = NewtonFractalPlot(poly(coefficients), PlotWindow(width, height, complex(0, 0), 1/200))
    nf.iterate_frame()
