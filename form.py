from reportlab.lib import colors
# Helper function to create form text fields
def create_form_text_field(c, name, x, y, width, height, value=''):
    c.drawString(x, y + height + 3, name)
    c.rect(x, y, width, height, stroke=1, fill=0)
    c.acroForm.textField(name=name, tooltip=name, x=x, y=y, width=width, height=height,
                            borderColor=colors.black, fillColor=colors.white, textColor=colors.black,
                            forceBorder=True, value=value)
