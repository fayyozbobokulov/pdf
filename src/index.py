from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.pagesizes import A4
from font import register_fonts
from text import create_wrapped_text, WrapTextOptions
from position import Position
from datetime import datetime
from color import hex_to_rgb
from reportlab.lib.colors import gainsboro, black, Color, grey, HexColor, white, magenta, pink, blue
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
        {"name": "ssn", "tooltip": "SSN", "x": 50, "y": page_height - pos.y - 105, "width": 240, "height": 20},
        {"name": "email", "tooltip": "Email", "x": 50, "y": page_height - pos.y - 155, "width": 240, "height": 20},
        {"name": "phone", "tooltip": "Phone", "x": 320, "y": page_height - pos.y - 155, "width": 240, "height": 20},
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
    skills_color = hex_to_rgb('#DCDCDC')
    skills_color2 = hex_to_rgb('#ffffff')
    rec_height = 30    
    pos.y += 20
    # The skills list
    for key, value in data.items():
        title = key.split('medical')[1].upper()
        devider(c, header_color, pos.x, page_height - pos.y, width+10, rec_height)
        text(c, white, pos.x+10, page_height - pos.y +11, title)

        if len(value['questions'][0]['answer'])>3:
            print(f"IT is TRUE: > {value['questions'][0]['answer']}")
            for i in range(1, 5):
                text(c, white, pos.x + 400 + 20 * i, page_height -pos.y + 11, f'{i}')
        


        color = True
        pos.y += 30
        for question in value['questions']:
            devider(c, skills_color if color else skills_color2, pos.x, page_height - pos.y + 11, width + 10, rec_height-10)
            color = not color
            text(c, black, pos.x, page_height - pos.y + 18, question['description'])
            if len(question['answer'])>3:
                for i in range(1, 5):
                    form.radio(name=question['description'], tooltip='Field radio1',
                        value='value1', selected=True if i==1 else False,
                        x=pos.x + 395 + 20 * i, y=page_height -pos.y + 11, buttonStyle='circle',
                        borderStyle='solid', shape='circle',
                        borderColor=grey, fillColor=white,
                        textColor=HexColor('#72c800'), forceBorder=True)
            if len(question['answer'])<3:
                text(c, black, pos.x+395, page_height -pos.y + 18, 'Yes')
                text(c, black, pos.x+455, page_height -pos.y + 18, 'No')
                form.radio(name=question['description'], tooltip='Field radio1',
                    value='value1', selected=True if i==1 else False,
                    x=pos.x + 395 + 30, y=page_height -pos.y + 11, buttonStyle='circle',
                    borderStyle='solid', shape='circle',
                    borderColor=grey, fillColor=white,
                    textColor=HexColor('#72c800'), forceBorder=True)
                form.radio(name=question['description'], tooltip='Field radio1',
                    value='value1', selected=True if i==1 else False,
                    x=pos.x + 455 + 20, y=page_height -pos.y + 11, buttonStyle='circle',
                    borderStyle='solid', shape='circle',
                    borderColor=grey, fillColor=white,
                    textColor=HexColor('#72c800'), forceBorder=True)

            pos.y += 20
    
    certifications = ['BLS', 'ACLS', 'Telemetry Certificate', 'ONS Chemo/Biotherapy Certification', 'Other Chemo Certification'];
    devider(c, header_color, pos.x, page_height - pos.y, width+10, rec_height)
    text(c, white, pos.x+10, page_height - pos.y +11, 'CERTIFICATIONS')
    pos.y+=30
    
    color = False

    for cert in certifications:
        devider(c, skills_color if color else skills_color2, pos.x, page_height - pos.y + 11, width + 10, rec_height-10)
        text(c, black, pos.x, page_height - pos.y + 18, cert)
        text(c, black, pos.x+350, page_height - pos.y + 18, 'Exp. Date')
        form.textfield(name='date', x=pos.x+410, y=page_height - pos.y+10, borderStyle='inset',
            borderColor=black, fillColor=gainsboro, width=100, height=20, textColor=black, forceBorder=False)
        pos.y+=20
        color = not color

    others = ['Other: Specify', 'Other: Specify'];
    pos.y+=10
    for other in others:
        devider(c, skills_color if color else skills_color2, pos.x, page_height - pos.y + 11, width + 10, rec_height)
        text(c, black, pos.x, page_height - pos.y + 25, other)
        text(c, black, pos.x+350, page_height - pos.y + 25, 'Exp. Date')
        form.textfield(name='date', x=pos.x+130, y=page_height - pos.y+10, borderStyle='inset',
            borderColor=black, fillColor=gainsboro, width=200, height=30, textColor=black, forceBorder=False)
        form.textfield(name='date', x=pos.x+410, y=page_height - pos.y+18, borderStyle='inset',
            borderColor=black, fillColor=gainsboro, width=100, height=20, textColor=black, forceBorder=False)

        pos.y+=30
        color = not color

        
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
    

    c.save()

# Usage
output_file_path = f'samples/{datetime.now()}-sample.pdf'
create_pdf_with_forms(output_file_path)
