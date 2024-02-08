from reportlab.pdfgen.canvas import Canvas
from font import register_fonts
from position import Position
from reportlab.lib.colors import Color, HexColor, black, white,gainsboro, grey, red, green
from typing import Tuple
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import Paragraph
from color import hex_to_rgb
from typing import Dict, Any, List
import math

INPUT_FIELD_HEIGHT = 20
DEVIDER_HEIGHT = 40
HEADER_COLOR = hex_to_rgb('#3d265d')
COLOR1 = hex_to_rgb('#ededed')
COLOR2 = hex_to_rgb('#ffffff')
HEADER_SIZE = 12

class PDFCreator:
    def __init__(self, canvas: Canvas, pos: Position, pagesize: Tuple[float, float]) -> None:
        register_fonts(False)
        self.c = canvas
        self.page_width, self.page_height = pagesize
        self.form = self.c.acroForm
        self.margin = 50
        self.pos = pos
        self.height = self.page_height - 2*self.margin
        self.color = True
    
    def header(self, header: str):
        self.text(header, color=grey, font_size=18, font_style='Roboto-Bold')
        self.pos.y += 30
        text = "This profile is a self evaluation as a healthcare professional in this discipline and speciality. It is an indication of experience in specific clinical areas."
        self.wrapped_text(text, text_color=grey)
        self.pos.y += 50
        self.text("Please enter your full legal name")

        self.pos.y += 30
        
        form_fields = [
            {"name": "fname", "tooltip": "First Name", "x": self.pos.x, "y": self.pos.y, "width": 240, "height": 20, "required": True},
            {"name": "lname", "tooltip": "Last Name", "x": self.pos.x + 270, "y": self.pos.y, "width": 240, "height": 20, "required": True},
            {"name": "ssn", "tooltip": "Last 4 digits of SSN", "x": self.pos.x, "y": self.pos.y+50, "width": 240, "height": 20, "required": False},
            {"name": "email", "tooltip": "Email", "x": self.pos.x, "y": self.pos.y+100, "width": 240, "height": 20, "required": True},
            {"name": "phone", "tooltip": "Phone", "x": self.pos.x + 270, "y": self.pos.y+100, "width": 240, "height": 20, "required": True},
        ]
        # self.pos.y += 140
        for field in form_fields:
            self.text(field['tooltip'], required=field['required'], x=field['x'], y=field['y'])
            self.form.textfield(name=field['name'], tooltip=field['tooltip'],
                          x=field['x'], y=self.page_height - field['y'] - 25,
                          height=INPUT_FIELD_HEIGHT, textColor=black, 
                          width=field['width'])
    
    def textfield(self, name:str, width: int, height: int, 
                  text_color: Color=black, x: int = None, y: int = None):
        if x is None:
            x = self.pos.x
        if y is None:
            y = self.pos.y
        
        self.form.textfield(name=name, textColor=text_color, 
                            x=x, y=y, borderStyle='inset', fillColor=gainsboro,
                            width=width, height=height, forceBorder=False, multiline=True)

    def devider(self, color: Tuple[float, float, float], height: int, width: int):
        self.c.setFillColorRGB(*color)
        self.c.setStrokeColorRGB(*color)
        self.c.rect(self.pos.x, self.pos.y, width, height, fill=1)

    def text(self, text: str, x: int = None, y: int = None, required=False, 
             color: Color = black, font_size=12, font_style='Roboto-Regular'):
        
        if x is None:
            x = self.pos.x
        if y is None:
            y = self.pos.y

        if required:
            text_obj = self.c.beginText()
            text_obj.setTextOrigin(x, y)
            text_obj.textOut(text)
            text_obj.setFillColor(red)
            text_obj.textOut("*")
            text_obj.setFillColor(color)
            self.c.drawText(text_obj)
        else: 
            self.c.setFont(font_style, font_size)
            self.c.setFillColor(color)
            self.c.drawString(x, y, text)
        self.c.setFillColor(black)
        self.c.setFont('Roboto-Regular', 12)

    def from_text(self, width: int, height: int, name: str, value='', 
                  x: int = None, y: int = None):
        if x is None:
            x = self.pos.x
        if y is None:
            y = self.pos.y
        self.c.rect(x, y, width, height, stroke=1, fill=0)
        self.form.textField(name=name, tooltip=name, x=x, y=y, width=width, height=height,
                            borderColor= black, fillColor= white, textColor= black,
                            forceBorder=True, value=value)
    
    def wrapped_text(self, text: str, width: int = None, height: int = None, 
                     x: int = None, y: int = None, text_color: Color = black, 
                     font_size: int = 12, font_name: str = 'Roboto-Regular'):
        # Calculate the text area considering margins
        if width is None: 
            width = self.page_width - 2*self.margin
        if height is None:
            height = self.page_height - 2*self.margin
        if x is None:
            x = self.pos.x
        if y is None:
            y = self.pos.y

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
        w, h = paragraph.wrap(width, height)
        # If the text height exceeds the page height, then split the text
        if h > height:
            # This is a placeholder for more complex logic that would be needed to split the text
            print(f"Warning: The text is too long to fit into the available space of height: {height} points.")
        if w > width:

            print(f"Warning: The text is too long to fit into the available space of width: {width} points.")

        # Draw the paragraph on the canvas
        paragraph.drawOn(self.c, x, y if h<=font_size else y - font_size*(h/font_size-1))
    
    def levels(self):
        # Info about levels
        self.pos.y += 20
        self.c.drawString(self.pos.x + 10,self.pos.y, '1. No theory and/or experience')
        self.pos.y+=20
        self.c.drawString(self.pos.x + 10,self.pos.y, '2. Limited experience/need supervision and/or support')
        self.pos.y+=20
        self.c.drawString(self.pos.x + 10,self.pos.y, '3. Experienced/minimal support needed to perform')
        self.pos.y+=20
        self.c.drawString(self.pos.x + 10,self.pos.y, '4. Proficient/can perform independently')
        self.pos.y+=30

    def skills(self, skills: Dict[str, Any]):
        for key, value in skills.items():
            title = value.get('title', '').upper()
            
            self.devider(HEADER_COLOR, DEVIDER_HEIGHT, self.page_width - 2*self.margin + 10)
            self.text(title,x=self.pos.x + 5, y=self.pos.y + DEVIDER_HEIGHT/2+HEADER_SIZE/3,color=white)

            if value.get('type', '') == 'ratingsTable':
                if len(value['questions'][0]['answer']) == 4:
                    for i in range(1, 5):
                        self.text(f'{i}', x=self.pos.x + 400 + 15 * i, y=self.pos.y + DEVIDER_HEIGHT/2+HEADER_SIZE/3,color=white)

                for question in value['questions']:
                    self.pos.y+=DEVIDER_HEIGHT
                    self.devider(COLOR1 if self.color else COLOR2, DEVIDER_HEIGHT, self.page_width - 2*self.margin + 10)
                    self.color = not self.color
                    if question['description'] == "EMR Conversion":
                        print(question)

                    self.text(question['description'],x=self.pos.x + 5, y=self.pos.y + DEVIDER_HEIGHT/2+HEADER_SIZE/3,color=black)
                    if len(question['answer'])==4:
                        for i in range(1, 5):
                            self.form.radio(name=question['description'], tooltip='Field radio1',
                                value=f'value{i}', selected=True if i==1 else False,
                                x=self.pos.x + 398 + 15 * i, y=self.page_height - self.pos.y-DEVIDER_HEIGHT/2-HEADER_SIZE/2, buttonStyle='circle',
                                borderStyle='solid', shape='circle', size=15,
                                borderColor=grey, fillColor=white, borderWidth=0,
                                textColor=HexColor('#72c800'), forceBorder=False)
                    if len(question['answer'])==2:
                        self.text('Yes', self.pos.x+395, self.pos.y + DEVIDER_HEIGHT/2+HEADER_SIZE/3, black)
                        self.text('No', self.pos.x+455, self.pos.y + DEVIDER_HEIGHT/2+HEADER_SIZE/3, black)
                        self.form.radio(name=question['description'], tooltip='Field radio1',
                            value='value1', selected=True if i==1 else False,
                            x=self.pos.x + 395 + 30, y=self.page_height - self.pos.y-DEVIDER_HEIGHT/2-HEADER_SIZE/2, buttonStyle='circle',
                            borderStyle='solid', shape='circle', size=15,
                            borderColor=grey, fillColor=white, borderWidth=0,
                            textColor=HexColor('#72c800'), forceBorder=False)
                        self.form.radio(name=question['description'], tooltip='Field radio1',
                            value='value2', selected=True if i==1 else False,
                            x=self.pos.x + 455 + 20, y=self.page_height - self.pos.y-DEVIDER_HEIGHT/2-HEADER_SIZE/2, buttonStyle='circle',
                            borderStyle='solid', shape='circle', borderWidth=0,
                            borderColor=grey, fillColor=white, size=15,
                            textColor=HexColor('#72c800'), forceBorder=False)
            elif value.get('type', '') == 'checkbox':
                code = ord('A')
                for i in range(9):
                    letter = chr(code+i)
                    self.text(letter, x=self.pos.x + 350 + 15 * i, y=self.pos.y + DEVIDER_HEIGHT/2+HEADER_SIZE/3,color=white)
                qs = value['questions']
                for q in qs:
                    self.pos.y += DEVIDER_HEIGHT + 10
                    self.devider(COLOR1 if self.color else COLOR2, DEVIDER_HEIGHT+10, self.page_width - 2*self.margin + 10)
                    self.wrapped_text(q['description'], width=(self.page_width - 2*self.margin)*0.6, 
                                      height=DEVIDER_HEIGHT, x=self.pos.x+5, y=self.pos.y + HEADER_SIZE+5)
                    for i in range(9):
                        self.form.checkbox(False, "check", "square", fillColor=HexColor('#ededed') if self.color else HexColor('#ffffff'), textColor=HexColor('#72c800'), x=self.pos.x + 348 + i*15, y=self.page_height - self.pos.y-DEVIDER_HEIGHT*2/3, size=10 )

                    self.color = not self.color
            elif value.get("type", '') == 'categories':
                print(value['type'])
                print(key)
                qs = value['questions']
                length = len(qs)
                max_loop = math.ceil(length/2)
                for b in range(max_loop):
                    self.pos.y += DEVIDER_HEIGHT
                    self.devider(COLOR1 if self.color else COLOR2, DEVIDER_HEIGHT, self.page_width - 2*self.margin + 10)
                    self.color = not self.color
                    self.text(qs[b], x=self.pos.x + 5, y=self.pos.y + DEVIDER_HEIGHT/2+HEADER_SIZE/3,color=black)
                    if length-1>=b+max_loop:
                        self.text(qs[b+max_loop], x=self.pos.x + 5 + self.page_width/2, y=self.pos.y + DEVIDER_HEIGHT/2+HEADER_SIZE/3,color=black)
                self.pos.y += DEVIDER_HEIGHT/2
                self.wrapped_text(text=value['reminder'], width=self.page_width-2*self.margin + 10, font_size=10, y=self.pos.y + DEVIDER_HEIGHT, text_color=grey)

            self.pos.y += DEVIDER_HEIGHT

            if value.get('items', False):
                x = 0
                for item in value['items']:
                    # self.pos.y += DEVIDER_HEIGHT

                    self.devider(COLOR1 if self.color else COLOR2, DEVIDER_HEIGHT, self.page_width - 2*self.margin + 10)
                    self.wrapped_text(item['title'],width=(self.page_width - 2*self.margin)*0.6, x=self.pos.x + 5, y=self.pos.y + DEVIDER_HEIGHT/2+HEADER_SIZE/2)
                    self.color = not self.color
                    if item.get('valueIdentifier'):
                        self.pos.y += DEVIDER_HEIGHT
                        self.form.textfield(name=item['valueIdentifier'], x=self.page_width/2, y=self.page_height - self.pos.y + DEVIDER_HEIGHT/2-HEADER_SIZE, borderStyle='inset',
                            borderColor=black, fillColor=gainsboro, width=195, height=20, textColor=black, forceBorder=False, fontSize=8)
                        
                    if item.get('customTitleIdentifier', False):
                        self.pos.y += DEVIDER_HEIGHT
                        self.form.textfield(name=item['customTitleIdentifier'], x=self.page_width/2, y=self.page_height - self.pos.y + DEVIDER_HEIGHT/2-HEADER_SIZE, borderStyle='inset',
                                             borderColor=black, fillColor=gainsboro, width=150, height=20, textColor=black, forceBorder=False, fontSize=8)
                        for i in range(1, 5):
                            self.form.radio(name=f"{item['title']}{x}", tooltip='Field radio1',
                                value=f'value{i}', selected=True if i==1 else False,
                                x=self.pos.x + 398 + 15 * i, y=self.page_height - self.pos.y+DEVIDER_HEIGHT/2-HEADER_SIZE/2, buttonStyle='circle',
                                borderStyle='solid', shape='circle', size=15,
                                borderColor=grey, fillColor=white, borderWidth=0,
                                textColor=HexColor('#72c800'), forceBorder=False)
                        x+=1
                    if item.get('inputIdentifier', False):
                        self.pos.y += DEVIDER_HEIGHT
                        self.text(item.get('inputTitle', ''),x=self.pos.x + 250-len(item.get('valueTitle', '')), y=self.pos.y + DEVIDER_HEIGHT/2+HEADER_SIZE/3,color=black)
                        
            self.pos.y += 10
    
    def certs(self, certs: List[Dict[str, Any]]):

        self.devider(HEADER_COLOR, DEVIDER_HEIGHT, self.page_width - 2*self.margin + 10)
        self.text('CERTIFICATIONS',x=self.pos.x + 5, y=self.pos.y + DEVIDER_HEIGHT/2+HEADER_SIZE/3,color=white)
        self.pos.y+=DEVIDER_HEIGHT
        i = 1
        for cert in certs:
            self.devider(COLOR1 if self.color else COLOR2, DEVIDER_HEIGHT, self.page_width - 2*self.margin + 10)

            self.wrapped_text(cert['title'], width=self.page_width-2*self.margin-50, x=self.pos.x + 5, y=self.pos.y + DEVIDER_HEIGHT/2+HEADER_SIZE/3)
            self.text(cert.get('valueTitle', ''),x=self.pos.x + 350-len(cert.get('valueTitle', '')), y=self.pos.y + DEVIDER_HEIGHT/2+HEADER_SIZE/3,color=black)
            if cert.get('customTitleIdentifier', False):
                self.form.textfield(name=cert['customTitleIdentifier'], x=self.pos.x+180, y=self.page_height - self.pos.y- DEVIDER_HEIGHT, borderStyle='inset',
                    borderColor=black, fillColor=gainsboro, width=150, height=DEVIDER_HEIGHT, textColor=black, forceBorder=False)    
            i+=1
            self.form.textfield(name=F"{cert['title']}{i}", x=self.pos.x+410, y=self.page_height - self.pos.y- DEVIDER_HEIGHT/2-2*HEADER_SIZE/3, borderStyle='inset',
                borderColor=black, fillColor=gainsboro, width=95, height=20, textColor=black, forceBorder=False)    
            self.pos.y += DEVIDER_HEIGHT
            i+=1
            self.color = not self.color

    def others(self, others: List[str]):
        color = False
        i = 1
        for other in others:
            self.devider(COLOR1 if color else COLOR2, DEVIDER_HEIGHT, self.page_width - 2*self.margin + 10)
            self.text(other,x=self.pos.x + 5, y=self.pos.y + DEVIDER_HEIGHT/2+HEADER_SIZE/3,color=black)
            self.text('Exp. Date',x=self.pos.x + 350, y=self.pos.y + DEVIDER_HEIGHT/2+HEADER_SIZE/3,color=black)
            self.form.textfield(name=f'other{i}', x=self.pos.x+130, y=self.page_height - self.pos.y- DEVIDER_HEIGHT, borderStyle='inset',
                borderColor=black, fillColor=gainsboro, width=150, height=DEVIDER_HEIGHT, textColor=black, forceBorder=False)    
            i+=1
            self.form.textfield(name=f'other{i}', x=self.pos.x+410, y=self.page_height - self.pos.y- DEVIDER_HEIGHT/2-2*HEADER_SIZE/3, borderStyle='inset',
                borderColor=black, fillColor=gainsboro, width=95, height=20, textColor=black, forceBorder=False)    
            i+=1
            self.pos.y += DEVIDER_HEIGHT
            color = not color
        
    def footer(self, text_color = black):
        if(self.page_height-50<self.pos.y+158):
            self.pos.y += 158
        title = 'Please read and agree to the statements below by marking the checkbox.'
        self.wrapped_text(text=title, x=self.pos.x+25, y=self.pos.y, text_color=text_color, font_name='Roboto-Bold', font_size=14)
        
        self.pos.y += 14
        title = 'I attest that the information I have given is true and accurate to the best of my knowledge and that I am the individual completing this form. I hereby authorize the release of this Skills Checklist to the Client facilities in relation to consideration of employment as a Healthcare Professional with those facilities.'
        self.wrapped_text(text=title, x=self.pos.x+25, y=self.pos.y+12, text_color=text_color, font_name='Roboto-Regular', font_size=10)
        
        self.form.checkbox(name='cb1', tooltip='Field cb1',
                    x=self.pos.x, y=self.height - self.pos.y+70, buttonStyle='check',
                    fillColor=gainsboro,
                    textColor=HexColor('#3d265d'), forceBorder=False)
        self.pos.y += 75

        self.form.textfield(name='fullname', x=self.pos.x+40, y=self.page_height - self.pos.y, borderStyle='inset',
                    borderColor=black, fillColor=gainsboro, width=300, height=20, textColor=black, forceBorder=False)
        self.form.textfield(name='date', x=self.pos.x+400, y=self.page_height - self.pos.y, borderStyle='inset',
                    borderColor=black, fillColor=gainsboro, width=100, height=20, textColor=black, forceBorder=False)
        self.c.setFillColor(black)
        self.c.line(x1=self.pos.x+40, y1=self.pos.y, x2=self.pos.x+340, y2=self.pos.y)
        self.c.line(x1=self.pos.x+400, y1=self.pos.y, x2=self.pos.x+500, y2=self.pos.y)
        self.pos.y += 8
        self.text("(Signature)", x=self.pos.x + 170, y=self.pos.y, font_size=8, font_style="Roboto-Italic")
        self.text("(Date)", x=self.pos.x+430, y=self.pos.y, font_size=8, font_style="Roboto-Italic")

    def save(self):
        self.c.drawString(self.page_width/2, self.page_height - 30, f'{self.pos.page}')
        self.c.save()
# ["a","b","c","d","e","f","g","h","i","j"]
#                   |                   |     