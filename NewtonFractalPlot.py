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
        tolerance = self.window.scale
        max_iter = len(self.polynomial)*10
        for n in range(0, max_iter):
            denominator = self.derivative.eval(z)
            if denominator == 0:
                return 0, 0, 0
            z = z - self.polynomial.eval(z)/denominator
            for r in range(0, len(self.roots)):
                epsilon = distance_sq(z, self.roots[r])
                if epsilon < tolerance:
                    factor = shading_weight(n, max_iter, epsilon, tolerance)
                    return shade_color(self.colors[r], factor)
        return 0, 0, 0

    def iterate_frame(self):
        start_time = time.time()
        plot = Image.new("RGB", (self.window.width_px, self.window.height_px), (0, 0, 0))
        pool = Pool(4)
        top_left_corner = self.window.pixel_to_complex(0, 0)
        # These values, dr and di, are just small adjustments for multisampling each pixel
        dr = complex(self.window.scale * 0.5, 0)
        di = complex(0, -self.window.scale * 0.5)
        progress = 0
        delta_progress = 100/(self.window.width_px*self.window.height_px)
        last_print = 0
        for x in range(0, self.window.width_px):
            for y in range(0, self.window.height_px):
                z1 = top_left_corner + complex(self.window.scale*x, -self.window.scale*y)
                z2 = z1 + dr
                z3 = z1 + di
                z4 = z1 + dr + di
                colors = pool.map(self.iterate_point, [z1, z2, z3, z4])
                color = average_colors(colors)
                plot.putpixel((x, y), tuple(color))
                progress += delta_progress
                if progress > last_print + 1:
                    round_progress = math.floor(progress)
                    elapsed = time.time() - start_time
                    estimate = int(math.ceil(elapsed/progress*100-elapsed))
                    print("{}% ... est {} seconds left".format(round_progress, estimate))
                    last_print = round_progress
        pool.close()
        plot.save("output.png")
        plot.show()
        end_time = time.time()
        print("100% ... Time elapsed: {} seconds".format(int(math.ceil(end_time-start_time))))




