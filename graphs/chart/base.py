from graphs.base import BaseGraph

class BaseChart(BaseGraph):
    def __init__(self, width, height):
        super(BaseChart, self).__init__(width, height)

    def draw_axis(self):
        img_width, img_height = self.image.size

        origin     = (img_width * 0.1, img_height * 0.9)
        x_axis_end = (img_width * 0.1, img_height * 0.1)
        y_axis_end = (img_width * 0.9, img_height * 0.9)

        self.draw_line(origin, x_axis_end)
        self.draw_line(origin, y_axis_end)
