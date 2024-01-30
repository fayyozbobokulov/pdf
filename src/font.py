from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont


def register_fonts(dev):

    pdfmetrics.registerFont(TTFont('Roboto-Regular', './fonts/Roboto-Regular.ttf'))
    pdfmetrics.registerFont(TTFont('Roboto-Bold', './fonts/Roboto-Medium.ttf'))
    pdfmetrics.registerFont(TTFont('Roboto-Italic', './fonts/Roboto-Italic.ttf'))
    pdfmetrics.registerFont(TTFont('Roboto-BoldItalic', './fonts/Roboto-MediumItalic.ttf'))
    if dev: 
        c = canvas.Canvas('samples/fonts.pdf', pagesize=letter)
        c.setFont('Roboto-Regular', 32)
        c.drawString(10, 10, "Some text encoded in Roboto-Regular")
        c.drawString(10, 60, "In the Roboto-Regular TT Font!")

        c.setFont('Roboto-Bold', 32)
        c.drawString(10, 70, "Some text encoded in Roboto-Bold")
        c.drawString(10, 120, "In the Roboto-Bold TT Font!")

        c.setFont('Roboto-Italic', 32)
        c.drawString(10, 130, "Some text encoded in Roboto-Italic")
        c.drawString(10, 180, "In the Roboto-Italic' TT Font!")

        c.setFont('Roboto-BoldItalic', 32)
        c.drawString(10, 190, "Some text encoded in Roboto-BoldItalic")
        c.drawString(10, 240, "In the Roboto-BoldItalic TT Font!")

        c.save()
