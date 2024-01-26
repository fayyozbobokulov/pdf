class Position:
    def __init__(self, x, y, max_y, doc):
        self.x = x
        self._y = y
        self.max_y = max_y
        self.doc = doc

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value):
        if value > self.max_y:
            self.handle_exceeding_y()
        self._y = value

    def handle_exceeding_y(self):
        print(f"The value of y has exceeded {self.max_y}: {self._y}")
        self._y = 50
        self.doc.showPage()

# Usage:
# from reportlab.pdfgen import canvas
# doc = canvas.Canvas('example.pdf')
# position = Position(x=100, y=100, max_y=800, doc=doc)
