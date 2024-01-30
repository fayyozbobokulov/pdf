from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import Paragraph
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from typing import NamedTuple, List, Dict, Union, Optional

class WrapTextOptions(NamedTuple):
    page_width: int
    page_height: int
    text_width: int
    margin: int
    fonst_size: Optional[int]
    x: int
    y: int
    font_name: Optional[str]

def create_wrapped_text(c: canvas.Canvas, options: WrapTextOptions, text: str) -> None:
    # Calculate the text area considering margins
    page_width = options['page_width']
    page_height = options['page_height']
    text_width = options['text_width']
    margin = options['margin']
    x = options['x']
    y = options['y']
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