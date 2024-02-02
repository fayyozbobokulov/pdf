from typing import Tuple
from reportlab.pdfgen.canvas import Canvas
class Position:
    def __init__(self, margin: int, page_size: Tuple[float, float], c: Canvas):
        self.page_width, self.page_height = page_size
        self.x = margin
        self.margin = margin
        self._y = margin
        self.max_y = self.page_height - 2*self.margin
        self.doc = c
        self.min_y = margin

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value):
        if value > self.max_y-30:
            self.handle_exceeding_y()
        else:
            self._y = value

    def handle_exceeding_y(self):
        print(f"The value of y has exceeded {self.max_y}: {self._y}")
        print(f"Exceeded: ${self._y}")

        self._y = 70
        self.doc.showPage()
        print(f"New: ${self._y}")


# Usage:
# from reportlab.pdfgen import canvas
# doc = canvas.Canvas('example.pdf')
# position = Position(x=100, y=100, max_y=800, doc=doc)
