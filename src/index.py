from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.pagesizes import A4
from font import register_fonts
from text import create_wrapped_text, WrapTextOptions
from position import Position
from datetime import datetime
from color import hex_to_rgb
from reportlab.lib.colors import gainsboro, black, Color, grey, HexColor, white, magenta, pink, blue, red
from devider import devider
from text import text, required_text
from footer import footer
import json
from typing import Dict

PAGE_WIDTH, PAGE_HEIGHT = A4

def create_pdf_with_forms(output_path):
    with open('./src/templates/medical.json', 'r') as f:
        data = json.load(f)
    # Create a canvas
    c = Canvas(output_path, pagesize=A4, pdfVersion=(1,7))
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
    pos = Position(margin, A4, c)
    
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
    c.setFillColor(grey)
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
    c.setFillColor(black)
    c.drawString(50, page_height-pos.y, "Please enter your full legal name")
    # Define the form
    form = c.acroForm
    # Form fields with positions and sizes
    form_fields = [
        {"name": "fname", "tooltip": "First Name", "x": 50, "y": page_height - pos.y - 55, "width": 240, "height": 20, "required": True},
        {"name": "lname", "tooltip": "Last Name", "x": 320, "y": page_height - pos.y - 55, "width": 240, "height": 20, "required": True},
        {"name": "ssn", "tooltip": "Last 4 digits of SSN", "x": 50, "y": page_height - pos.y - 105, "width": 240, "height": 20, "required": False},
        {"name": "email", "tooltip": "Email", "x": 50, "y": page_height - pos.y - 155, "width": 240, "height": 20, "required": True},
        {"name": "phone", "tooltip": "Phone", "x": 320, "y": page_height - pos.y - 155, "width": 240, "height": 20, "required": True},
    ]
    
    for field in form_fields:
        # c.drawString(field['x'], field['y']+30, field["tooltip"])
        required_text(c, red, field['x'], field['y']+30, field['tooltip'], required=field['required'])
        form.textfield(name=field['name'], tooltip=field['tooltip'],
                   x=field['x'], y=field['y'], borderStyle='inset',
                   borderColor=black, fillColor=gainsboro, 
                   width=field['width'], height=field['height'],
                   textColor=black, forceBorder=False)

    c.setFont('Roboto-Regular',12)

    # Info about levels
    pos.y += 200
    c.drawString(pos.x + 10, page_height-pos.y, '1. No theory and/or experience')
    pos.y+=20
    c.drawString(pos.x + 10, page_height-pos.y, '2. Limited experience/need supervision and/or support')
    pos.y+=20
    c.drawString(pos.x + 10, page_height-pos.y, '3. Experienced/minimal support needed to perform')
    pos.y+=20
    c.drawString(pos.x + 10, page_height-pos.y, '4. Proficient/can perform independently')
    pos.y+=80

    header_color = hex_to_rgb('#3d265d')
    skills_color = hex_to_rgb('#ededed')
    skills_color2 = hex_to_rgb('#ffffff')
    rec_height = 40
    pos.y += 30
    header_size = 12
    # The skills list
    for key, value in data['skills'].items():
        title = key.split('medical')[1].upper()
        devider(c, header_color, pos.x, page_height - pos.y, width+10, rec_height)
        text(c, white, pos.x+5, page_height - pos.y+rec_height/2-header_size/4, title)

        if len(value['questions'][0]['answer'])>3:
            for i in range(1, 5):
                text(c, white, pos.x + 400 + 15 * i, page_height - pos.y+rec_height/2-header_size/4, f'{i}')
        
        color = True
        pos.y += rec_height
        for question in value['questions']:
            devider(c, skills_color if color else skills_color2, pos.x, page_height - pos.y, width + 10, rec_height)
            color = not color
            text(c, black, pos.x+3, page_height - pos.y+rec_height/2-header_size/4, question['description'])
            if len(question['answer'])>3:
                for i in range(1, 5):
                    form.radio(name=question['description'], tooltip='Field radio1',
                        value=f'value{i}', selected=True if i==1 else False,
                        x=pos.x + 398 + 15 * i, y=page_height - pos.y+rec_height/2-header_size/4, buttonStyle='circle',
                        borderStyle='solid', shape='circle', size=15,
                        borderColor=grey, fillColor=white, borderWidth=0,
                        textColor=HexColor('#72c800'), forceBorder=False)
            if len(question['answer'])<3:
                text(c, black, pos.x+395, page_height - pos.y+rec_height/2-header_size/4, 'Yes')
                text(c, black, pos.x+455, page_height - pos.y+rec_height/2-header_size/4, 'No')
                form.radio(name=question['description'], tooltip='Field radio1',
                    value='value1', selected=True if i==1 else False,
                    x=pos.x + 395 + 30, y=page_height - pos.y+rec_height/2-header_size/2, buttonStyle='circle',
                    borderStyle='solid', shape='circle', size=15,
                    borderColor=grey, fillColor=white, borderWidth=0,
                    textColor=HexColor('#72c800'), forceBorder=False)
                form.radio(name=question['description'], tooltip='Field radio1',
                    value='value2', selected=True if i==1 else False,
                    x=pos.x + 455 + 20, y=page_height - pos.y+rec_height/2-header_size/2, buttonStyle='circle',
                    borderStyle='solid', shape='circle', borderWidth=0,
                    borderColor=grey, fillColor=white, size=15,
                    textColor=HexColor('#72c800'), forceBorder=False)

            pos.y += rec_height
    
    certifications = ['BLS', 'ACLS', 'Telemetry Certificate', 'ONS Chemo/Biotherapy Certification', 'Other Chemo Certification'];
    devider(c, header_color, pos.x, page_height - pos.y, width+10, rec_height)
    text(c, white, pos.x+10, page_height - pos.y+rec_height/2-header_size/4, 'CERTIFICATIONS')
    pos.y+=rec_height+10
    
    color = False

    for cert in certifications:
        devider(c, skills_color if color else skills_color2, pos.x, page_height - pos.y + 11, width + 10, rec_height)
        text(c, black, pos.x, page_height - pos.y+rec_height/2+header_size/2, cert)
        text(c, black, pos.x+350, page_height - pos.y+rec_height/2+header_size/2, 'Exp. Date')
        form.textfield(name=cert, x=pos.x+410, y=page_height - pos.y+rec_height/2, borderStyle='inset',
            borderColor=black, fillColor=gainsboro, width=100, height=20, textColor=black, forceBorder=False)
        pos.y+=rec_height
        color = not color

    others = ['Other: Specify', 'Other: Specify'];
    
    for other in others:
        devider(c, skills_color if color else skills_color2, pos.x, page_height - pos.y + 11, width + 10, rec_height)
        text(c, black, pos.x, page_height - pos.y+rec_height/2  + header_size/2, other)
        text(c, black, pos.x+350, page_height - pos.y+rec_height/2 + header_size/2, 'Exp. Date')
        form.textfield(name='input1', x=pos.x+130, y=page_height - pos.y+rec_height/2, borderStyle='inset',
            borderColor=black, fillColor=gainsboro, width=200, height=30, textColor=black, forceBorder=False)
        form.textfield(name='input2', x=pos.x+410, y=page_height - pos.y+rec_height/2, borderStyle='inset',
            borderColor=black, fillColor=gainsboro, width=100, height=20, textColor=black, forceBorder=False)

        pos.y+=rec_height
        color = not color

    footer(c, form, pos, page_height, page_width, margin)
    c.save()

# Usage
output_file_path = f'samples/{datetime.now()}-sample.pdf'
create_pdf_with_forms(output_file_path)
