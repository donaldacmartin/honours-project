from graphs.base import BaseGraph

class BaseChart(BaseGraph):
    def __init__(self, width, height):
        super(BaseChart, self).__init__(width, height)

    def draw_axis(self):
        img_width, img_height = self.image.size
        origin = (self.image.size[0] * 0.9, self.imag)
        x1 = self.image.size[0] * 0.1
        y1 = self.image.size[1] * 0.1

        self.draw_line()
