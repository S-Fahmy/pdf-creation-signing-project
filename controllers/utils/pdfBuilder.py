# coding: utf-8

from fpdf import FPDF, HTMLMixin


class PDF(FPDF, HTMLMixin):

    def __init__(self, font_path):
        super().__init__()
        # self.add_font('DejaVu', fname= font_path + '/DejaVuSansMono.ttf', uni=True) #DejaVu looks bad but i'll keep this line in case you need to add your font.
        self.add_page()  # add first new page

        self.set_font('helvetica', size=14)
        self.set_margins(15, 5, 25)

        self.set_draw_color(81, 81, 81)  # the color of the borders
        self.alias_nb_pages()  # ??

    '''
    header() and footer() builds the page header and footer, they are overloaded functions no need to directly call them.
    '''

    def header(self):
        # Logo
        # self.image('stamp.png', 10, 8, 33)
        # Arial bold 15
        # self.set_font('helvetica', 'B', 15)
        self.set_font('helvetica', size=14)

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
        self.set_y(-30)
        # self.cell(80, 0, "We request that you pay this invoice within 14 days of the invoice date, stating the invoice number, to be paid to bank account number NL18INGB0005876441 in the name of VipaHelda BV in Capelle aan den IJssel", align="C", center=True)
        self.set_y(-15)
        # Arial italic 8
        self.set_font('helvetica', 'I', 8)

        # Page number
        self.cell(0, 10, 'Page ' + str(self.page_no()) + '/{nb}', 0, 0, 'C')

    # y = 40

    def add_invoice_fields(self, y=40):
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


    def add_invoice_table(self,  data_list, y=40):
        # self.set_draw_color(30, 63, 240)
        self.init_table(data_list)

        self.render_table_header(y)

        self.render_table_body()

        self.render_table_footer()



    def init_table(self, data_list):
        self.columns_names = ("Omschrijving", "Amount", "Bedrag", "Totaal") #hardcoded

        # self.TABLE_DATA = (
        #     ("Item test", 34, "5.20", ""),
        #     ("test Item test Item test  Item test Item test Item test Item test test Item test Item test  Item test Item test Item test Item test test Item test Item test  Item test Item test Item test Item test", 45, "1.5", ""),
        #     ("Item test", 19, "17.99", ""),
        #     ("Item test m", 31, "1.0", ""),
        #     ("wow test mItem test mItem test mItem test mItem test mItem test mItem test mItem test mItem test mItem test mItem test mItem test m", 500, "13.0", ""),
        # )
        self.TABLE_DATA = data_list
        
        self.cols_width = {0: self.epw / 2, 1: self.epw / 7, 2: self.epw / 6, 3: self.epw / 4.5}

        # self.set_font("Helvetica", size= 16)
        self.set_font('helvetica', size=12)
        self.line_height = self.font_size * 2.5

        # only working way i found to render € symbol with the built in fpdf fonts encoding without changing things.
        self.currency = chr(128)
        self.vat = 0.14
        self.set_x(0)


    def render_table_header(self, y=40, new_page=False):
        

        if(new_page):
            self.add_page(same=True)
            self.set_y(40)

        else:
            self.set_y(y+40)

        self.set_fill_color(14, 125, 172)  # blue
        self.set_text_color(*(255, 255, 255))
        self.c_margin = 3  # this is affecting the left padding of cells

        self.set_font(style="B")

        cell_num = 0
        for col_name in self.columns_names:
            self.cell(
                self.cols_width[cell_num], self.line_height*1.3, col_name, border=1, fill=1)
            cell_num += 1

        self.ln(self.line_height)
        self.set_font(style="")  # disabling bold text
        self.set_text_color(*(0, 0, 0))

        # cells pos
        if new_page:
            self.set_y(y + (self.line_height + 3))
        else:
            self.set_y(y + 40 + (self.line_height + 3))



    '''
    adds the body of the table along with calculating totals
    Totaal cell per item row is the item price (i'm assuming Bedrag is the price of 1 item) x the quantity 
    '''

    def render_table_body(self):
        self.total_excl_vat = 0.0 #used to calculated the total sum for each item totaal
        # for _ in range(8):  # repeat data rows
        for row_columns in self.TABLE_DATA:  # rows
            row_columns['totaal'] = "" #placeholder

            self.item_quantity = 1 #used to calculated totaal per item
            self.price_per_item = 1 #used to calculated totaal per item
            self.cell_height = self.line_height #used to make the cell height dynamic in case there is a long multi line string

            # cell_num = 0

            # for cell_value in row_columns:  # columns/cells

            #     text = self.calculate_get_cell_value(cell_num, cell_value, len(row_columns))

            #     # aligns the last col to the right
            #     alignement = 'R' if cell_num == len(row_columns) - 1 else 'L'

            #     self.multi_cell(self.cols_width[cell_num], self.cell_height, txt= text, border='R,L',  align=alignement, ln=3, max_line_height=self.font_size)

            #     cell_num += 1

            col_num = 0
            for key in row_columns:  # 3 columns

                text = self.calculate_get_cell_value(key, row_columns[key])

                # aligns the last col to the right
                alignement = 'R' if key == 'totaal' else 'L'

                self.multi_cell(self.cols_width[col_num], self.cell_height, txt= text, border='R,L',  align=alignement, ln=3, max_line_height=self.font_size)

                col_num += 1



            self.ln( self.cell_height)

    '''
    calculate totals for the last 3 cells from the right and/or return the display text to be passed as a cell() txt paramater
    '''

    def calculate_get_cell_value(self, key, value):

        if key == 'quantity':

            self.item_quantity = int(value)  # store it for totaal loop iter
            text = value + 'x'

        elif key == 'price':  # Bedrag
            # store it for totaal loop iter
            self.price_per_item = float(value)

            text = self.currency + '' + value

        elif key ==  'totaal':  # totaal
            total_per_item = round(self.price_per_item * self.item_quantity, 2)

            self.total_excl_vat += total_per_item

            text = self.currency + '' + str(total_per_item)

        elif key == 'description':  # desc cell
            text = value


            #checks if this is the item desc cell, and calculate how many lines the text will need to fit, and based on that calculate the new cell height
            #since this is the first cell, the new cell height will be applied for the next cell in this row.
            #currently only doing this check on the item desc cell.

            

            #with split_only set to true it will only calculate return an array of lines contents that will fit in the cell.
            num_lines = len(self.multi_cell(self.cols_width[0], txt=text, split_only=True))

            #NOTE this way the cell height will fit exactly the number of lines, no extra spaces on the top and bottom, if there is it text doesn't look accurate,
            #  there is no align content in a cell vertically in fpdf unless it's source code is updated.
            self.cell_height = num_lines * self.font_size  if num_lines > 1 else self.line_height 

            if self.will_page_break(self.cell_height): #if the height of this cell will span to a new page, add a new page with the table header.

                text = '\n' + text #add some spacing between the first row and the table header
                self.cell_height += self.font_size #compensate for that new line added above.

                self.render_table_header(new_page=True)

                    
            

        return text


    '''
    footer has 2 rows, each row, no vat and vat, only have data in the last 2 cells the others are empty
    '''
    def render_table_footer(self):

        cols_count = len(self.TABLE_DATA[0])
        # makes the borders of this area slightly thicker
        self.set_line_width(0.4)

        for row in range(2):

            for cell_num in range(cols_count):

                if row == 0:  # total excluding vat row

                    if cell_num == cols_count - 2:  # add Total
                        self.multi_cell(self.cols_width[cell_num], self.line_height*2, '\nTotal \n(excl.VAT)', border='T,L', ln=3, max_line_height=self.font_size, align="C")
                    
                    elif cell_num == cols_count - 1:
                        total_excl_vat =  round(self.total_excl_vat, 2)
                        self.multi_cell(self.cols_width[cell_num], self.line_height*2, self.currency + '' + str(total_excl_vat), border='T,L,R', ln=3, max_line_height=self.font_size, align="R")

                    else: #empty cells

                        self.multi_cell(
                            self.cols_width[cell_num], self.line_height*2, '', border='L', ln=3, max_line_height=self.font_size)

                else:  # total row

                    if cell_num == cols_count - 2:  # add Total
                        self.set_font(style="B")

                        self.cell(
                            self.cols_width[cell_num], self.line_height, txt='Total due', border='T,B,L', fill=1)
                    elif cell_num == cols_count - 1:

                        self.set_text_color(0, 0, 0)

                        total_with_vat = str(round(self.total_excl_vat + (self.total_excl_vat * self.vat), 2))

                        self.cell(self.cols_width[cell_num], self.line_height, txt=self.currency + '' + total_with_vat, border='T,B,L,R',  align="R", fill=1)

                    else: #empty cells
                        self.cell(self.cols_width[cell_num], self.line_height, '', border='T,B,L', fill=1)

            self.ln(self.line_height*2)

            # the total row colors
            self.set_fill_color(238, 238, 238)
            self.set_text_color(81, 81, 81)









    # def add_table(self, data_list):
    #     print(data_list)
    #     self.add_invoice_fields()

        # self.add_invoice_table(data_list=data_list)  # the actual table body


        # i = 1
        # total_sum = 0

        # html_table_body = """
        # <font color="#00ff00"><p>hello in green</p></font>
        # <font color="#336677"><p>hello in blue</p></font>
        # <table border="1" align="center" width="90%">
        #     <thead>
        #         <tr bgcolor = "#0e7dac" height="90">
        #             <th  align = "left" width="10%"><font color="#ffffff"><p>hello <br /></font></th>
        #             <th align = "left" width="40%">description</th>
        #             <th align = "left" width="30%">QTY</th>
        #             <th align = "left" width="20%">Price</th>
        #         </tr>
        #     </thead>
        # <tbody>
        # """

        # for data_row in data_list:

        #     tr = """
        #     <tr>
        #     <font color="#000000"><td align = "left">""" + str(i) + """</td></font>
        #     <font color="#000000"><td align = "left">""" + data_row['description'] + """</td></font>
        #     <td align = "left">""" + data_row['quantity'] + """x</td>
        #     <td align = "left">$""" + data_row['price'] + """</td>
        #     </tr>
        #     """
        #     total_sum += int(data_row['price'])

        #     if i == len(data_list):  # add table footer and close the table
        #         tr = tr + """
        #             <tfoot width = "90%" border>
        #                 <tr bgcolor = "#eeeeee">
        #                 <td width = "70%" align="right"> Total: </td>
        #                 <td width = "30%" align="center">$""" + str(total_sum) + """</td>

        #                 </tr>
        #             </tfoot>
        #                 </tbody>
        #                 </table>
        #             """
        #     html_table_body = html_table_body + tr

        #     i += 1

        # # y spacing between the start of the table and the start of page
        # self.set_y(y + 100)

        # self.write_html(html_table_body)


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
