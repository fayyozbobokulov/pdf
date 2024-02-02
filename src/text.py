from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import Paragraph
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from typing import NamedTuple, List, Dict, Union, Optional
from reportlab.lib.colors import Color
from typing import Tuple
from reportlab.pdfgen.canvas import Canvas, black
from devider import devider
class WrapTextOptions(NamedTuple):
    page_width: int
    page_height: int
    text_width: int
    margin: int
    fonst_size: Optional[int]
    x: int
    y: int
    font_name: Optional[str]
    text_color: Color

def create_wrapped_text(c: canvas.Canvas, options: WrapTextOptions, text: str) -> None:
    # Calculate the text area considering margins
    page_width = options['page_width']
    page_height = options['page_height']
    text_width = options['text_width']
    margin = options['margin']
    x = options['x']
    y = options['y']
    text_color = options['text_color']
    font_size = options.get('font_size', 12)
    font_name = options.get('font_name', 'Roboto_Regular')

    text_width = page_width - 2*margin
    text_height = page_height - 2*margin

    # Define the style for the paragraph
    styles = getSampleStyleSheet()
    style = styles['Normal']
    # Add custom styles if needed
    custom_style = ParagraphStyle(
        'Custom',
        parent=style,
        wordWrap='CJK',  # This allows for word wrapping
        spaceBefore=0,
        spaceAfter=0,
        leftIndent=0,
        rightIndent=0,
        firstLineIndent=0,
        fontName=font_name,
        fontSize=font_size,
        textColor=text_color
    )

    # Create a paragraph object
    paragraph = Paragraph(text, custom_style)

    # Calculate the height of the paragraph and break if it exceeds the available height
    w, h = paragraph.wrap(text_width, text_height)

    # If the text height exceeds the page height, then split the text
    if h > text_height:
        # This is a placeholder for more complex logic that would be needed to split the text
        print(f"Warning: The text is too long to fit into the available space of height: {text_height} points.")
    elif w > text_width:
        print(f"Warning: The text is too long to fit into the available space of width: {text_width} points.")

    # Draw the paragraph on the canvas
    paragraph.drawOn(c, x, y)

def text(c: Canvas, color: Color, x: int, y: int, title: str, font_size=12, font_style='Roboto-Regular'):
    c.setFont(font_style, font_size)
    c.setFillColor(color)
    c.drawString(x, y, title)

def required_text(c: Canvas, color: Color, x: int, y: int, title: str, font_size=12, font_style='Roboto-Regular'):
    text_obj = c.beginText()
    text_obj.setTextOrigin(x, y)
    text_obj.textOut(title)
    text_obj.setFillColor(color)
    text_obj.textOut("*")
    text_obj.setFillColor(black)

    c.drawText(text_obj)