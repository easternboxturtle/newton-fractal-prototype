from mpmath import mp
from PIL import ImageColor
from colorsys import hls_to_rgb


def inf_close(z1: complex, z2: complex, radius):
    if abs(z1.real - z2.real) < radius:
        if abs(z1.imag - z2.imag) < radius:
            return True
    return False


def inf_metric(z1: complex, z2: complex):
    return max(abs(z1.real - z2.real), abs(z1.imag - z2.imag))

# TODO: add reg metric and use for shading, possibly without square root


def color_palette(num_of_colors):
    colors = list()
    for i in range(0, num_of_colors):
        rgb_float = hls_to_rgb(i/num_of_colors, 0.5, 1.0)
        rgb_255 = [round(v*255) for v in rgb_float]
        colors.append(tuple(rgb_255))
    return colors


def shade_color(color, factor):
    return tuple([int(v * factor) for v in color])


def shading_weight(n, max_iter, epsilon, tolerance):
    x = 1-(n+epsilon/tolerance)/max_iter
    return x*(3+x*(4*x-6))


def average_colors(list_of_colors):
    n = len(list_of_colors)
    return tuple([int(sum([list_of_colors[i][v] for i in range(n)]) / n) for v in range(3)])
