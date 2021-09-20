from .utils.pdfBuilder import PDF

def build_pdf(file_name, invoice_data, pdfs_folder):
    try:
    
        pdf = PDF() # the class, have the header, the footer
        pdf.add_table(invoice_data)
        pdf.output(pdfs_folder +"/"+ file_name +  '.pdf', 'F')

        return True

    except Exception as e:
        print('something happened in build_pdf', e)
        return False

