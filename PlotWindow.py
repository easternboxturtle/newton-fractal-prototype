from dataclasses import dataclass


@dataclass
class PlotWindow:
    width_px: int
    height_px: int
    center: complex
    scale: float

    def pixel_to_complex(self, x, y) -> complex:
        real = -(self.width_px/2 - x)*self.scale + self.center.real
        imag = (self.height_px/2 - y)*self.scale + self.center.imag
        return complex(real, imag)


