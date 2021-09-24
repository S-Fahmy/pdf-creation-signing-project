from .utils.pdfBuilder import PDF

def build_pdf(file_name, invoice_data, pdfs_folder, fonts_folder):
    try:
    
        pdf = PDF(fonts_folder) # the class, have the header, the footer
        pdf.add_invoice_fields()
        pdf.add_invoice_table(data_list = invoice_data)
        pdf.output(pdfs_folder +"/"+ file_name +  '.pdf', 'F')

        return True

    except Exception as e:
        print('something happened in build_pdf', e)
        return False

