from reportlab.pdfgen.canvas import Canvas
from typing import Tuple
from reportlab.lib.colors import white

def devider(c: Canvas, bg_color: Tuple[float, float, float], x: int, y: int, width: int, height: int) -> None:
    c.setFillColorRGB(*bg_color)
    c.setStrokeColorRGB(*bg_color)
    c.rect(x, y, width+10, height, fill=1)
    