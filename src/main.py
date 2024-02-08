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
    file_names = listdir('./src/full')
    print(file_names)
    # file_names = ['cardinter.json']
    i = 0
    for path in file_names:
        c = Canvas(f'./samples2/{path[:-5]}.pdf', pagesize=A4, bottomup=0)
        pos = Position(50, A4, c)

        with open(f'./src/full/{path}', 'r') as f:
            data = json.load(f)
        i+=1
        print(f"n: {i}, file: {path}")
        pdf = PDFCreator(c, pos, A4)
        pdf.header(data["title"])
        pos.y += 150
        pdf.levels()
        pdf.skills(data['skills'])
        pdf.certs(data['certifications'])
        pos.y += 50
        pdf.footer()
        pos.page
        pdf.save()



main()