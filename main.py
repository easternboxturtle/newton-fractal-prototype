from NewtonFractalPlot import *
from PlotWindow import *
from poly import *
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

    nf = NewtonFractalPlot(poly(coefficients), PlotWindow(800, 600, complex(0, 0), 1/200))
    nf.iterate_frame()
