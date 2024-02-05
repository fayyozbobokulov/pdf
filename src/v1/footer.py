from v1.textext import WrapTextOptions
from position import Position
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.colors import black, gainsboro, HexColor
from v1.textext import create_wrapped_text, text
from reportlab.pdfbase.acroform import AcroForm



def footer(c: Canvas, form: AcroForm, pos: Position, page_height: int, page_width: int, margin: int):

    options: WrapTextOptions = {
        "page_width": page_width,
        "page_height": page_height, 
        "text_width": page_width - 2*margin,
        "margin": margin,
        "font_name": 'Roboto-Bold',
        "font_size": 18
    }
    pos.y += 60
    options["x"] = pos.x+25
    options['text_color'] = black
    options["y"] = page_height - pos.y
    options["font_size"] = 14
    title = 'Please read and agree to the statements below by marking the checkbox.'
    create_wrapped_text(c, options, title)
    
    pos.y += 50
    options["y"] = page_height - pos.y
    
    options["font_size"] = 10
    options["font_name"] = "Roboto-Regular"
    title = 'I attest that the information I have given is true and accurate to the best of my knowledge and that I am the individual completing this form. I hereby authorize the release of this Skills Checklist to the Client facilities in relation to consideration of employment as a Healthcare Professional with those facilities.'
    create_wrapped_text(c, options, title)
    
    form.checkbox(name='cb1', tooltip='Field cb1',
                  x=pos.x, y=page_height - pos.y + 10, buttonStyle='check',
                  fillColor=gainsboro,
                  textColor=HexColor('#3d265d'), forceBorder=True)
    pos.y += 40

    form.textfield(name='fullname', x=pos.x+40, y=page_height - pos.y, borderStyle='inset',
                borderColor=black, fillColor=gainsboro, width=300, height=20, textColor=black, forceBorder=False)
    form.textfield(name='date', x=pos.x+400, y=page_height - pos.y, borderStyle='inset',
                borderColor=black, fillColor=gainsboro, width=100, height=20, textColor=black, forceBorder=False)
    c.setFillColor(black)
    c.line(x1=pos.x+40, y1=page_height - pos.y, x2=pos.x+340, y2=page_height - pos.y)
    text(c, black, pos.x+170, page_height - pos.y-10, "(Signature)", 8, "Roboto-Italic")
    c.line(x1=pos.x+400, y1=page_height - pos.y, x2=pos.x+500, y2=page_height - pos.y)
    text(c, black, pos.x+430, page_height - pos.y-10, "(Date)", 8, "Roboto-Italic")