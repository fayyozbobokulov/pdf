from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors

def create_pdf_with_forms(output_path):
    # Create a canvas
    c = canvas.Canvas(output_path, pagesize=A4)
    left_margin = 50
    right_margin = 50
    top_margin = 50
    bottom_margin = 50
    width, height = letter  # Get the dimensions of the letter size
    w2, h2 = A4

    print(f"WIDTH : > ${width} HEIGHT : > ${height}")
    print(f"WIDTH2 : > ${w2} HEIGHT2 : > ${h2}")
    # Title
    c.setFont("Helvetica-Bold", 18)
    c.drawString(50, height - 50, "Medical/Surgical Skills Checklist")

    # Subtitle
    c.setFont("Helvetica-Oblique", 12)
    c.drawString(50, height - 70, ("This profile is a self evaluation as a healthcare professional "
                                    "in this discipline and speciality. It is an indication of "
                                    "experience in specific clinical areas."))

    # Define the form
    c.acroForm

    # Helper function to create form text fields
    def create_form_text_field(name, x, y, width, height, value=''):
        c.drawString(x, y + height + 3, name)
        c.rect(x, y, width, height, stroke=1, fill=0)
        c.acroForm.textField(name=name, tooltip=name, x=x, y=y, width=width, height=height,
                             borderColor=colors.black, fillColor=colors.white, textColor=colors.black,
                             forceBorder=True, value=value)

    # Form fields with positions and sizes
    form_fields = [
        {"name": "First Name", "x": 50, "y": height - 155, "width": 240, "height": 20},
        {"name": "Last Name", "x": 320, "y": height - 155, "width": 240, "height": 20},
        {"name": "SSN", "x": 50, "y": height - 195, "width": 240, "height": 20},
        {"name": "Email", "x": 50, "y": height - 235, "width": 240, "height": 20},
        {"name": "Phone", "x": 320, "y": height - 235, "width": 240, "height": 20},
    ]

    # Create form fields
    for field in form_fields:
        create_form_text_field(field['name'], field['x'], field['y'], field['width'], field['height'])

    # Experience Level Descriptions
    c.setFont("Helvetica", 10)
    experience_levels = [
        "1. No theory and/or experience",
        "2. Limited experience/need supervision and/or support",
        "3. Experienced/minimal support needed to perform",
        "4. Proficient/can perform independently"
    ]
    for i, level in enumerate(experience_levels, start=1):
        c.drawString(50, height - 280 - (i * 20), level)

    # Save the PDF
    c.save()

# Usage
output_file_path = 'Medical_Surgical_Skills_Checklist.pdf'
create_pdf_with_forms(output_file_path)
