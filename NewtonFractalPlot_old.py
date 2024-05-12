import time

from PIL import Image, ImageColor
from poly import *
from utils import *
from multiprocessing import Pool
import math
import PlotWindow


class NewtonFractalPlot:

    def __init__(self, polynomial: poly, window: PlotWindow):
        self.polynomial = polynomial
        self.window = window

        self.derivative = polynomial.differentiate()
        self.roots = polynomial.roots()

        self.colors = color_palette(len(self.roots))

    def iterate_point(self, z: complex):
        tolerance = self.window.scale/2
        max_iter = len(self.polynomial)*10
        for n in range(0, max_iter):
            denom = self.derivative.eval(z)
            if denom == 0:
                return 0, 0, 0
            z = z - self.polynomial.eval(z)/denom
            for r in range(0, len(self.roots)):
                epsilon = inf_metric(z, self.roots[r])
                if epsilon < tolerance:
                    return tuple([int(v*(1-(n+epsilon/tolerance)/max_iter)) for v in self.colors[r]])
        return 0, 0, 0

    def iterate_frame(self):
        start_time = time.time()
        plot = Image.new("RGB", (self.window.width_px, self.window.height_px), (0, 0, 0))
        pool = Pool(4)
        top_left_corner = self.window.pixel_to_complex(0, 0)
        dr = complex(self.window.scale * 0.5, 0)
        di = complex(0, -self.window.scale * 0.5)
        progress = 0
        dprogress = 100/(self.window.width_px*self.window.height_px)
        lastprint = 0
        for x in range(0, self.window.width_px):
            for y in range(0, self.window.height_px):
                z1 = top_left_corner + complex(self.window.scale*x, -self.window.scale*y)
                z2 = z1 + dr
                z3 = z1 + di
                z4 = z1 + dr + di
                colors = pool.map(self.iterate_point, [z1, z2, z3, z4])
                color = average_colors(colors)
                plot.putpixel((x, y), tuple(color))
                progress += dprogress
                if progress > lastprint + 1:
                    print("{}% ...".format(math.floor(progress)))
                    lastprint = math.floor(progress)
        pool.close()
        plot.show()
        end_time = time.time()
        print("Time elapsed: {}".format(end_time-start_time))




