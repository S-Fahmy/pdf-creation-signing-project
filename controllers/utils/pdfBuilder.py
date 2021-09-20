from fpdf import FPDF, HTMLMixin


class PDF(FPDF, HTMLMixin):


    def __init__(self):
        super().__init__()
                
        self.add_page() #add first new page
        self.set_draw_color(235, 235, 235) #the color of the borders
        self.alias_nb_pages()  # ??
        self.set_font('helvetica', '', 12)

    

# cell(width, height,text, border,line, align, fill, link)

    '''
    header() and footer() builds the page header and footer, they are overloaded functions no need to directly call them.
    '''
    def header(self):
        # Logo
        # self.image('stamp.png', 10, 8, 33)
        # Arial bold 15
        self.set_font('helvetica', 'B', 15)
        # Move to the right
        self.cell(5)
        # Title
        self.cell(5, 10, 'Title Here', 0, 0, 'L')
        # Line break
        self.ln(30)


    # Page footer
    def footer(self):
        # line(self, x1,y1,x2,y2)
        self.line(10.0, 280.0, 193.0, 280.0)
        # Position at 1.5 cm from bottom
        self.set_y(-15)
        # Arial italic 8
        self.set_font('helvetica', 'I', 8)
        # Page number
        self.cell(0, 10, 'Page ' + str(self.page_no()) + '/{nb}', 0, 0, 'C')


    # y = 40

    def add_invoice_fields(self, y = 40):
        ###
        self.set_line_width(0.0)
        # y = 40
        self.set_font('times', '', 10.0)
        self.set_xy(17.0, y)
        self.cell(ln=0, h=6.0, align='L', w=13.0, txt='Name:', border=0)
        self.set_xy(35.0, y)
        self.cell(ln=0, h=6.0, align='L', w=140.0, txt='Test Name', border=0)
        self.set_xy(17.0, y+8)
        self.cell(ln=0, h=6.0, align='L', w=18.0, txt='Address:', border=0)
        self.set_xy(35.0, y+8)
        self.cell(ln=0, h=6.0, align='L', w=125.0, txt='xyz 12345', border=0)
        self.set_xy(17.0, y+16)
        self.cell(ln=0, h=6.0, align='L', w=18.0, txt='Phone:', border=0)
        self.set_xy(35.0, y+16)
        self.cell(ln=0, h=6.0, align='L', w=80.0, txt='+12345678', border=0)
        self.set_xy(115.0, y+16)
        self.cell(ln=0, h=6.0, align='L', w=18.0, txt='City:', border=0)
        self.set_xy(133.0, y+16)
        self.cell(ln=0, h=6.0, align='L', w=42.0, txt='Xyz', border=0)
        self.set_line_width(0.0)
        self.line(10.0, y + 32, 200.0, y + 32)
        # pdf.set_y(y + 40)
        ### 

    def add_invoice_table(self,  data_list, y = 40):
        i = 1
        total_sum = 0
            
        html_table_body = """
        <table border="1" align="center" width="90%">
        <thead bgcolor="#A0A0A0"><tr>
        <th  align = "left" width="10%">Item</th>
        <th align = "left" width="40%">description</th>
        <th align = "left" width="30%">QTY</th>
        <th align = "left" width="20%">Price</th>
        </tr></thead>
        <tbody>
        """


        
        for data_row in data_list:

            tr = """
            <tr>
            <td align = "left">""" + str(i) + """</td>
            <td align = "left">""" + data_row['description'] + """</td>
            <td align = "left">""" + data_row['quantity'] + """ </td>
            <td align = "left">$""" + data_row['price'] + """</td>
            </tr>
            """
            total_sum += int(data_row['price'])

            if i == len(data_list): #add table footer and close the table
                tr = tr + """
                    <tfoot width = "90%">
                        <tr> 
                        <td width = "70%" align="right"> Total: </td> 
                        <td width = "30%" align="center">$""" + str(total_sum) + """</td>
                

                        </tr>
                    </tfoot>
                        </tbody>
                        </table>
                    """
            html_table_body = html_table_body + tr

            i += 1


        self.set_y(y + 37) #y spacing between the start of the table and the start of page

        self.write_html(html_table_body)                             



    def add_table(self, data_list):

        self.add_invoice_fields() #the table headers
        self.add_invoice_table(data_list= data_list) #the actual table body


'''
code i used to generate a multi page table before figuring that fpdf can accept some basic htmls.
delete if not needed.
'''
# pdf.set_xy(17.0, y + 37)
# pdf.cell(ln=0, h=0.0, align='L', w=125.0, txt='Description', border=0)
# pdf.set_xy(160.0, y + 37)
# pdf.cell(ln=0, h=0.0, align='R', w=20.0, txt='Amount', border=0)
# pdf.set_line_width(0.0)
# pdf.line(10.0, y + 40, 200.0, y + 40)
# pdf.set_y(y + 48)
# row_y_position = y + 48
# for i in range(1, 12):
#     if i >= 18 and i % 18 == 0:  # table is continiung to a new page
#         pdf.add_page()
#         row_y_position = y

#     pdf.set_xy(17.0, row_y_position)
#     pdf.cell(0, 10, 'This is row number: ' + str(i), 0, 1)
#     pdf.line(155.0, row_y_position, 155.0, row_y_position + 10)  # line col
#     pdf.line(10, row_y_position + 10, 200.0, row_y_position + 10)  # line row

#     pdf.set_xy(160.0, row_y_position)
#     pdf.cell(ln=0, h=10, align='R', w=20.0, txt='100,00', border=0)

#     row_y_position += 10
