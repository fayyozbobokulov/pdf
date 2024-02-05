from os import listdir
from pdf import PDFCreator
from position import Position
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.colors import grey, red, black
import json

INPUT_FIELD_HEIGHT = 20
DEVIDER_HEIGHT = 40

def main ():
    file_names = listdir('./src/templates')
    print(file_names)
    for path in file_names:
        c = Canvas(f'./samples2/{path[:5]}.pdf', pagesize=A4, bottomup=0)
        pos = Position(50, A4, c)
        with open(f'./src/templates/{path}', 'r') as f:
            data = json.load(f)
        pdf = PDFCreator(c, pos, A4, f'./src/templates/{path}')
        
        pdf.header(data["name"])
        pos.y += 150
        pdf.levels()
        pdf.skills(data['skills'])
        certifications = ['BLS', 'ACLS', 'Telemetry Certificate', 'ONS Chemo/Biotherapy Certification', 'Other Chemo Certification']
        pdf.certs(certifications)
        pdf.others(['Other: Specify', 'Other: Specify'])
        pos.y += 50
        pdf.footer()

        c.save()



main()