class Position:
    def __init__(self, x, y, margin, max_y, doc):
        self.x = x
        self.margin = margin
        self._y = y
        self.max_y = max_y
        self.doc = doc
        self.min_y = x

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value):
        if value > self.max_y-self.margin:
            self.handle_exceeding_y()
        # if(value < self.min_y):
        #     self.handle_lowering_y()
        else:
            self._y = value

    def handle_exceeding_y(self):
        print(f"The value of y has exceeded {self.max_y}: {self._y}")
        print(f"Exceeded: ${self._y}")

        self._y = 50
        self.doc.showPage()
        print(f"New: ${self._y}")

    def handle_lowering_y(self):
        print(f"The value of y has lowered {self.max_y}: {self._y}")
        print(f"Lowered: ${self._y}")
        self._y = 50
        print(f"New: ${self._y}")

# Usage:
# from reportlab.pdfgen import canvas
# doc = canvas.Canvas('example.pdf')
# position = Position(x=100, y=100, max_y=800, doc=doc)
