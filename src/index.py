from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from font import register_fonts
from text import create_wrapped_text, WrapTextOptions
from position import Position
from datetime import datetime

def create_pdf_with_forms(output_path):
    # Create a canvas
    c = canvas.Canvas(output_path, pagesize=A4)
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
    c.drawString(50, height - 50, "Medical/Surgical Skills Checklist")
    c.setFont('Roboto-Regular',12)
    pos = Position(margin, margin, page_height, c)
    options: WrapTextOptions = {
        "page_width": page_width,
        "page_height": page_height, 
        "text_width": text_width,
        "margin": margin,
        "font_name": 'Roboto-Regular',
        "font_size": 12,
        "x": pos.x,
        "y": page_height-pos.y
    }
    # Subtitle 
    create_wrapped_text(c, options,"This profile is a self evaluation as a healthcare professional in this discipline and speciality. It is an indication of experience in specific clinical areas.");

    # Define the form
    form = c.acroForm

    # Form fields with positions and sizes
    form_fields = [
        {"name": "First Name", "x": 50, "y": height - 155, "width": 240, "height": 20},
        {"name": "Last Name", "x": 320, "y": height - 155, "width": 240, "height": 20},
        {"name": "SSN", "x": 50, "y": height - 195, "width": 240, "height": 20},
        {"name": "Email", "x": 50, "y": height - 235, "width": 240, "height": 20},
        {"name": "Phone", "x": 320, "y": height - 235, "width": 240, "height": 20},
    ]

    form.textfield(
        '',
        
    )

    # # Create form fields
    # for field in form_fields:
    #     create_form_text(field['name'], field['x'], field['y'], field['width'], field['height'])

    # # Experience Level Descriptions
    # c.setFont("Helvetica", 10)
    # experience_levels = [
    #     "1. No theory and/or experience",
    #     "2. Limited experience/need supervision and/or support",
    #     "3. Experienced/minimal support needed to perform",
    #     "4. Proficient/can perform independently"
    # ]
    # for i, level in enumerate(experience_levels, start=1):
    #     c.drawString(50, height - 280 - (i * 20), level)
    # Save the PDF
    c.save()

# Usage
output_file_path = f'samples/{datetime.now()}-sample.pdf'
create_pdf_with_forms(output_file_path)
