# coding: utf-8

from os import name
import os
from fpdf import FPDF, HTMLMixin


class PDF(FPDF, HTMLMixin):


    '''
    initialize the data that will be needed to print the pdf
    currently invoice_table_data is dynamic the rest is hard coded, the plan is to pass 1 dict that contains the 3 dicts, and assign them accordingly here
    '''
    def __init__(self, invoice_table_data):
        super().__init__()

        self.the_blue_rgb = (14, 125, 172) # the titles blue color.

        # company informations, for the pages header, currently hardcoded
        self.company_info_dict = {'Tel': '+31 10 307 27 52', 'E-mail': 'mailto:finance@vipahelda.com',
                                  'Website': 'www.vipahelda.com', 'IBAN': 'NL18INGB0005876441', 'BIC': 'INGBNL2A', 'KvK': '53952944', 'BTW nr': 'NL823980534B04'}
        
        # company informations, currently hardcoded
        self.invoice_info_dict = {'company_name': 'cn name', 'address': 'street, location', 'project': 'project name', 'Contact person': 'Quintin Doest', 'quote date': '26-9-2021', 'quote number': '16100003', 'expiry date': '21-09-2021'}

        self.invoice_data = invoice_table_data #table data
        self.set_margins(15, 5, 15) #set the page margins

        self.add_page()  # add first new page

        # this is always set to true by default by fpdf but i increased the bottom margin so the page breaks before the new footer content.
        self.set_auto_page_break(True, margin=40)

        self.set_font('helvetica', size=11)
        self.set_draw_color(81, 81, 81)  # the color of the borders

    '''
    header() and footer() builds the page header and footer, they are overloaded functions no need to directly call them.
    '''

    def header(self):
     
        self.set_font('helvetica', size=8)

        # Move to the right
        self.set_xy(-70, 15)
        self.image(name=os.getcwd() + "/pdfs/icons/1.png", w=50)

        self.set_y(self.get_y() + 5)
        self.write(h=self.font_size, txt='15-09-2021')
        self.ln(5)
        self.set_font(style="B")
        self.set_text_color(*self.the_blue_rgb)
        self.write(h=self.font_size, txt='Quote 16100003')
        self.set_font(style="")
        self.set_text_color(*(0, 0, 0))

        self.set_xy(-60, self.get_y() - self.font_size * 2)
        self.multi_cell(w=50, h=self.font_size + 0.5, txt='VipaHelda B.V.\nCypresbaan 16A\n2908 LT Capelle a/d IJssel\nNederland', ln=2)
        self.set_y(self.get_y() + self.font_size * 2)

        self.render_cells_data_from_dict(self.company_info_dict, x = -70)

        self.set_line_width(0)
        self.line(self.l_margin, self.get_y() + self.font_size * 2, self.w - self.r_margin, self.get_y() + self.font_size * 2)
        self.ln()
        self.header_height = self.get_y() # TO be used to position any content coming after the header


    # Page footer

    def footer(self):
        self.set_font('helvetica', '', 10)
        self.set_text_color(0, 0, 0)
        self.line(self.l_margin, 272.0, self.w - self.r_margin, 272.0)
        self.set_y(-20)
        self.write(h=5, txt="We request that you pay this invoice within 14 days of the invoice date, stating the invoice number,  to be paid to bank account number NL18INGB0005876441 in the name of VipaHelda BV in Capelle aan den IJssel")




    '''
    append data from the invoice info dict.
    '''
    def add_invoice_fields(self, y=40):
        y = self.header_height + 10
        info = self.invoice_info_dict

        self.set_font_size(11)
        self.set_font(style="")
        self.set_y(y)
        
        curr_y_pos = self.get_y()
        #1st block
        company = {'Company:': info['company_name'], 'Address:': info['address']}
        self.render_cells_data_from_dict(company, self.get_x(), 30, 1, 'B', '', True)
        
        self.set_y(self.get_y() - (self.get_y() - curr_y_pos)) #just going up to the prev y pos
        #end block
        company = {'Project:': info['project'], 'Contact person:': info['Contact person']}
        self.render_cells_data_from_dict(company, -85, 35, 1, 'B', '', True)

        self.set_y(self.get_y() + self.font_size * 1.5)
        #3rd block
        company = {'Quote date:': info['quote date'], 'Quote number:': info['quote number'], 'Expiry date:': info['expiry date']}
        self.render_cells_data_from_dict(company, self.l_margin, 30, 1, 'B', '', True)

        self.invoice_fields_height = self.get_y() #should be used by any content coming after this section

        


    '''
    loops over a given key:value info and append rows given x position.
    '''
    def render_cells_data_from_dict(self,dict, x, col_space = 15, height = 0.5, style_key = "", style_value = "", text_color_key = False):
        for key in dict:
            self.set_font(style=style_key)
            if text_color_key: self.set_text_color(*self.the_blue_rgb) #make it blue
            self.set_x(x) # reset x pos
            self.cell(w=15, txt=key,  ln=0) # ln 0 means the next cell will be position to the right of this
            self.set_x(x + col_space)  # move cursor a bit to the right to add the value

            if text_color_key: self.set_text_color(*(0,0,0)) #reset

            self.set_font(style=style_value)
            if key not in ['Website', 'E-mail']:
                self.cell(w=20, h=self.font_size + height, txt=dict[key],  ln=2)
            else: #link
                self.set_text_color(*(17,85,205))
                self.cell(w=20, h=self.font_size + height, txt= dict[key].replace('mailto:', ''), link=self.company_info_dict[key],  ln=2)
                self.set_text_color(*(0,0,0))

        self.set_font(style="") #reset



    '''
    initialize data related to the
    '''
    def init_table(self):
        self.columns_names = ("Omschrijving", "Amount","Bedrag", "Totaal")  # hardcoded
        self.table_body_data = self.invoice_data

        self.cols_width = {0: self.epw * 0.5, 1: self.epw * 0.17, 2: self.epw * 0.17, 3: self.epw * 0.17}

        # self.set_font("Helvetica", size= 16)
        self.set_font('helvetica', size=11)
        self.line_height = self.font_size * 2.5

        # € symbol
        self.currency = chr(128)
        self.vat = 0.14
        # self.set_x(0)

    def render_table_header(self, new_page=False):
        try:

            if(new_page):
                self.add_page(same=True)
                self.set_y( self.header_height + 10)

            else:
                self.set_y( self.invoice_fields_height + 10)

            self.set_fill_color(*self.the_blue_rgb)  # blue
            self.set_text_color(*(255, 255, 255))
            self.c_margin = 2  # this is affecting the left padding of cells

            self.set_font(style="B")
            cell_num = 0
            for col_name in self.columns_names:
                self.cell(
                    self.cols_width[cell_num], self.line_height*1.3, col_name, border=1, fill=1)
                cell_num += 1

            self.ln(self.line_height)
            self.set_font(style="")  # disabling bold text
            self.set_text_color(*(0, 0, 0))

            # setting the y pos for the table body by adding some white space so its not stuck/overlapping with the header or have space between the borders and the header
            self.add_table_white_space(4, 0.5)

        except Exception as e:
            print('something happened in render_table_header()', e)


    '''
    adds the body of the table along with calculating totals
    Totaal cell per item row is the item price (i'm assuming Bedrag is the price of 1 item) x the quantity 
    '''

    def render_table_body(self):
        self.total_excl_vat = 0.0  # used to calculated the total sum for each item totaal

        for row_columns in self.table_body_data:  # rows
            row_columns['totaal'] = ""  # placeholder

            self.item_quantity = 1  # used to calculated totaal per item
            self.price_per_item = 1  # used to calculated totaal per item
            # used to make the cell height dynamic in case there is a long multi line string
            self.cell_height = self.line_height

            col_num = 0
            for column_type in row_columns:

                text = self.calculate_get_cell_value(
                    column_type, row_columns[column_type])

                # aligns the last col to the right
                alignement = 'R' if column_type == 'totaal' else 'L'

                self.multi_cell(self.cols_width[col_num], self.cell_height, txt=text,
                                border='R,L',  align=alignement, ln=3, max_line_height=self.font_size)

                col_num += 1

            self.ln(self.cell_height)

    '''
    calculate totals for the last 3 cells from the right and/or return the display text to be passed as a cell() txt paramater
    '''

    def calculate_get_cell_value(self, key, value):

        if key == 'quantity':  # Amount

            self.item_quantity = int(value)
            text = value + 'x'

        elif key == 'price':  # Bedrag
            # store it for totaal loop iter
            self.price_per_item = float(value)

            text = self.currency + '' + value

        elif key == 'totaal':  # totaal
            total_per_item = round(self.price_per_item * self.item_quantity, 2)

            self.total_excl_vat += total_per_item

            text = self.currency + '' + str(total_per_item)

        elif key == 'description':  # Omschrijving
            text = value

            # calculates how many lines the text will need to fit inside the cell, and based on that calculate the new cell height
            # this is the first cell/column in the data dict so this cell height will be applied for the next cells/cols in this row.
            # currently only doing this check on the item desc cell.

            # with split_only set to true it will only calculate return an array of lines contents that will fit in the cell.
            num_lines = len(self.multi_cell(
                self.cols_width[0], txt=text, split_only=True))

            # NOTE this way the cell height will fit exactly the number of lines, no extra spaces on the top and bottom, if there is it text doesn't look accurate,
            #  there is no align content in a cell vertically in fpdf unless it's source code is updated.
            self.cell_height = num_lines * self.font_size if num_lines > 1 else self.line_height

            # if the height of this cell will span to a new page, add a new page with the table header.
            if self.will_page_break(self.cell_height):

                text = '\n' + text  # add some spacing between the first row and the table header
                # compensate for that new line added above.
                self.cell_height += self.font_size

                self.render_table_header(new_page=True)

        return text

    '''
    footer has 2 rows, each row, no vat and vat, only have data in the last 2 cells the others are empty
    '''

    def render_table_footer(self):
        try: 
            cols_count = len(self.table_body_data[0])
            whitespace = 2 #the count of the extra white space you see above the total excl vat row 

            #first, check if this whole footer section will break the page. (whitespace height + total excl vat height + total all height)
            #line_height is the height that will be passed to the cells() height paramter.
            if self.will_page_break( (self.line_height * whitespace) + (self.line_height * 2) + self.line_height):

                self.render_table_header(new_page=True)

            self.add_table_white_space(cols_count, whitespace) # n rows worth of whitespace

            for row in range(2):

                for cell_num in range(cols_count):

                    if row == 0:  # total excluding vat row

                        if cell_num == cols_count - 2:  # add Total
                            self.draw_dash_line(self.cols_width[cell_num])

                            self.multi_cell(self.cols_width[cell_num], self.line_height*2, '\nTotal \n(excl.VAT)',
                                            border='L', ln=3, max_line_height=self.font_size, align="C")

                        elif cell_num == cols_count - 1:

                            self.draw_dash_line(self.cols_width[cell_num])

                            total_excl_vat = round(self.total_excl_vat, 2)
                            self.multi_cell(self.cols_width[cell_num], self.line_height*2, self.currency + '' + str(
                                total_excl_vat), border='L,R', ln=3, max_line_height=self.font_size, align="R")

                        else:  # empty cells

                            self.multi_cell(
                                self.cols_width[cell_num], self.line_height*2, '', border='L', ln=3, max_line_height=self.font_size)

                    else:  # total row

                        if cell_num == cols_count - 2:  # add Total
                            self.set_font(style="B")

                            self.cell(
                                self.cols_width[cell_num], self.line_height, txt='Total due', border='T,B,L', fill=1)
                        elif cell_num == cols_count - 1:

                            self.set_text_color(0, 0, 0)

                            total_with_vat = str(
                                round(self.total_excl_vat + (self.total_excl_vat * self.vat), 2))

                            self.cell(self.cols_width[cell_num], self.line_height, txt=self.currency +
                                    '' + total_with_vat, border='T,B,L,R',  align="R", fill=1)

                        else:  # empty cells
                            self.cell(
                                self.cols_width[cell_num], self.line_height, '', border='T,B,L', fill=1)


                # the total row colors
                self.set_fill_color(238, 238, 238)
                self.set_text_color(81, 81, 81)
                self.ln(self.line_height*2)

        except Exception as e:
            print('something happened in render_table_footer()', e)
            
            return False


            

    '''
    draws a dash link in the current pos with a given width
    '''

    def draw_dash_line(self, width):
        self.set_line_width(0.4)
        self.dashed_line(self.get_x() + 2, self.get_y(), (self.get_x() +
                         width) - 2, self.get_y(),  space_length=1, dash_length=1.5)
        self.set_line_width(0)

    '''
    adds n rows worth of white space to the table, by drawing empty cells with height in each column 
    '''

    def add_table_white_space(self, cols_count, white_space):

        for col in range(cols_count):
            border = 'L'
            if col == cols_count - 1:
                border = 'L,R'

            self.cell(
                self.cols_width[col], self.line_height * white_space, '', border=border)

        self.ln(self.line_height * white_space) #affected by the line height which is pre calculated using the current used fontsize

    '''
    adds the final values where the signature will also be,  returns y pos and page num for the signature to be appended
    '''

    def render_signature_page(self, y=40):
        self.add_page(same=True)
        self.set_text_color(0, 0, 0)

        self.set_font(style="")
        self.set_font_size(11)
        self.line_height = self.font_size * 2
        self.set_y(self.header_height + 10)

        self.write_text("Made On:", "26/9/2021")
        self.write_text("In:", "26/9/2021")
        self.write_text("In:", "Street address number 1, second floor.")
        self.write_text("Signed By: ", "", 0)

        # returns where the signature field should start on the y axis and the page number.
        # pyhanko count the full page height as 850, compared to 275 here, so i calc a ratio
        # y1 = 850 - (current_y_position * ratio).
        return (round(850 - (self.get_y() * (750 / (self.eph + self.t_margin))), 1), self.page_no())

    def write_text(self, title, value, white_space=2):

        # the write function is a wrapper around the cell() function
        self.write(txt=title)
        self.ln(self.line_height)
        self.write(txt=value)
        self.ln(self.line_height * white_space)


   #####
    def add_invoice_table(self):
        
        # self.set_draw_color(30, 63, 240)
        self.init_table()

        self.render_table_header()

        self.render_table_body()

        self.render_table_footer()














#old unused html code
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

