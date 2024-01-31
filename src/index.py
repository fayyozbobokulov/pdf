from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.pagesizes import A4
from font import register_fonts
from text import create_wrapped_text, WrapTextOptions
from position import Position
from datetime import datetime
from color import hex_to_rgb
from reportlab.lib.colors import gainsboro, black, Color, grey, HexColor, white
from devider import devider
from text import text
import json

def create_pdf_with_forms(output_path):
    with open('./src/templates/medical.json', 'r') as f:
        data = json.load(f)
    # Create a canvas
    c = Canvas(output_path, pagesize=A4)
    register_fonts(False)
    margin = 50
    left_margin = margin
    right_margin = margin
    top_margin = margin
    bottom_margin = margin
    page_width, page_height = A4
    width = page_width - (left_margin + right_margin)
    height = page_height - (top_margin + bottom_margin)
    text_width = width - (left_margin+right_margin)
    pos = Position(50, 50, margin, page_height, c)
    
    options: WrapTextOptions = {
        "page_width": page_width,
        "page_height": page_height, 
        "text_width": text_width,
        "margin": margin,
        "font_name": 'Roboto-Bold',
        "font_size": 18
    }

    # Title
    c.setFont("Roboto-Bold", 18)
    c.drawString(50, page_height-50, "Medical/Surgical Skills Checklist")
    c.setFont('Roboto-Regular',12)
    pos.y += 30

    options: WrapTextOptions = {
        "page_width": page_width,
        "page_height": page_height, 
        "text_width": text_width,
        "margin": margin,
        "font_name": 'Roboto-Regular',
        "font_size": 12,
        "x": pos.x,
        "y": page_height-pos.y,
        'text_color': grey
    }

    # Subtitle 
    create_wrapped_text(c, options,"This profile is a self evaluation as a healthcare professional in this discipline and speciality. It is an indication of experience in specific clinical areas.");
    pos.y+=30
    c.setFont('Roboto-Regular',12)
    c.drawString(50, page_height-pos.y, "Please enter your full legal name")
    # Define the form
    form = c.acroForm

    # Form fields with positions and sizes
    form_fields = [
        {"name": "fname", "tooltip": "First Name", "x": 50, "y": page_height - pos.y - 55, "width": 240, "height": 20},
        {"name": "lname", "tooltip": "Last Name", "x": 320, "y": page_height - pos.y - 55, "width": 240, "height": 20},
        {"name": "ssn", "tooltip": "SSN", "x": 50, "y": page_height - pos.y - 125, "width": 240, "height": 20},
        {"name": "email", "tooltip": "Email", "x": 50, "y": page_height - pos.y - 195, "width": 240, "height": 20},
        {"name": "phone", "tooltip": "Phone", "x": 320, "y": page_height - pos.y - 195, "width": 240, "height": 20},
    ]
    
    for field in form_fields:
        c.drawString(field['x'], field['y']+30, field["tooltip"])
        form.textfield(name=field['name'], tooltip=field['tooltip'],
                   x=field['x'], y=field['y'], borderStyle='inset',
                   borderColor=black, fillColor=gainsboro, 
                   width=field['width'], height=field['height'],
                   textColor=black, forceBorder=False)

    c.setFont('Roboto-Regular',12)

    # Info about levels
    pos.y += 250
    c.drawString(pos.x + 10, page_height-pos.y, '1. No theory and/or experience')
    pos.y+=20
    c.drawString(pos.x + 10, page_height-pos.y, '2. Limited experience/need supervision and/or support')
    pos.y+=20
    c.drawString(pos.x + 10, page_height-pos.y, '3. Experienced/minimal support needed to perform')
    pos.y+=20
    c.drawString(pos.x + 10, page_height-pos.y, '4. Proficient/can perform independently')
    pos.y+=80

    header_color = hex_to_rgb('#3d265d')
    skills_color = hex_to_rgb('#DCDCDC')
    skills_color2 = hex_to_rgb('#ffffff')
    rec_height = 30    
    # The skills list
    for key, value in data.items():
        pos.y += 20
        print(key)
        title = key.split('medical')[1].upper()
        devider(c, header_color, pos.x, page_height - pos.y, width+10, rec_height)
        c.setFillColor(white)
        c.drawString(pos.x+10, page_height - pos.y + 11, title)

        color = True
        pos.y += 20
        for question in value['questions']:
            pos.y += 20
            devider(c, skills_color if color else skills_color2, pos.x, page_height - pos.y + 11, width + 10, rec_height)
            color = not color
            text(c, black, pos.x, page_height - pos.y + 11, question['description'])
            c.setFont('Roboto-Regular',12)
            c.setFillColor(black)
            c.drawString(pos.x, page_height - pos.y + 11, question['description'])
            
    c.save()

# Usage
output_file_path = f'samples/{datetime.now()}-sample.pdf'
create_pdf_with_forms(output_file_path)
