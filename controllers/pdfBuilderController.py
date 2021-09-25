from .utils.pdfBuilder import PDF

def build_pdf(file_name, invoice_data, pdfs_folder):
    try:
    
        pdf = PDF(invoice_data) # the class, have the header, the footer
        pdf.add_invoice_fields()
        pdf.add_invoice_table()
        signature_position = pdf.render_signature_page()


        pdf.output(pdfs_folder +"/"+ file_name +  '.pdf', 'F')

        return signature_position

    except Exception as e:
        print('something happened in build_pdf', e)
        return False

