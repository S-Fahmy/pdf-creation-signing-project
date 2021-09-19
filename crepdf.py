from fpdf import FPDF


# cell(width, height,text, border,line, align, fill, link)

class PDF(FPDF):
    def header(self):
        # Logo
        # self.image('stamp.png', 10, 8, 33)
        # Arial bold 15
        self.set_font('Arial', 'B', 15)
        # Move to the right
        self.cell(5)
        # Title
        self.cell(5, 10, 'Title Here', 0, 0, 'L')
        # Line break
        self.ln(10)

        # self.rect(10.0, 30.0, 190.0, 250.0, 'B')  #rect( x,y,w,h,style='')


    # Page footer
    def footer(self):
        # line(self, x1,y1,x2,y2)
        self.line(10.0, 280.0, 193.0, 280.0)
        # Position at 1.5 cm from bottom
        self.set_y(-15)
        # Arial italic 8
        self.set_font('Arial', 'I', 8)
        # Page number
        self.cell(0, 10, 'Page ' + str(self.page_no()) + '/{nb}', 0, 0, 'C')

# Instantiation of inherited class
pdf = PDF()
pdf.set_draw_color(235, 235, 235)

pdf.alias_nb_pages() #??
pdf.add_page()
pdf.set_font('Times', '', 12)

###
pdf.set_line_width(0.0)
# pdf.line(15.0, 57.0, 185.0, 57.0)
y = 40
pdf.set_font('times', '', 10.0)
pdf.set_xy(17.0, y)
pdf.cell(ln=0, h=6.0, align='L', w=13.0, txt='Name:', border=0)
pdf.set_xy(35.0, y)
pdf.cell(ln=0, h=6.0, align='L', w=140.0, txt='Test Name', border=0)
pdf.set_xy(17.0, y+8)
pdf.cell(ln=0, h=6.0, align='L', w=18.0, txt='Address:', border=0)
pdf.set_xy(35.0, y+8)
pdf.cell(ln=0, h=6.0, align='L', w=125.0, txt='xyz 12345', border=0)
pdf.set_xy(17.0, y+16)
pdf.cell(ln=0, h=6.0, align='L', w=18.0, txt='Phone:', border=0)
pdf.set_xy(35.0, y+16)
pdf.cell(ln=0, h=6.0, align='L', w=80.0, txt='+12345678', border=0)
pdf.set_xy(115.0, y+16)
pdf.cell(ln=0, h=6.0, align='L', w=18.0, txt='City:', border=0)
pdf.set_xy(133.0, y+16)
pdf.cell(ln=0, h=6.0, align='L', w=42.0, txt='Xyz', border=0)
pdf.set_line_width(0.0)
pdf.line(10.0, y + 32, 200.0, y + 32)
# pdf.set_y(y + 40)
###


pdf.set_xy(17.0, y + 37)
pdf.cell(ln=0, h=0.0, align='L', w=125.0, txt='Description', border=0)
pdf.set_xy(160.0, y + 37)
pdf.cell(ln=0, h=0.0, align='R', w=20.0, txt='Amount', border=0)
pdf.set_line_width(0.0)
pdf.line(10.0,y + 40, 200.0, y + 40)
pdf.set_y(y + 48)
row_y_position = y + 48
for i in range(1, 12):
    if i >= 18 and i % 18 == 0: #table is continiung to a new page
        pdf.add_page()
        row_y_position = y

    pdf.set_xy(17.0, row_y_position)
    pdf.cell(0, 10, 'This is row number: ' + str(i), 0, 1)
    pdf.line(155.0, row_y_position, 155.0, row_y_position + 10) # line col
    pdf.line(10, row_y_position +10, 200.0, row_y_position + 10) # line row

    pdf.set_xy(160.0, row_y_position)
    pdf.cell(ln=0, h=10, align='R', w=20.0, txt='100,00', border=0)


    row_y_position += 10

pdf.output('tuto2.pdf', 'F')