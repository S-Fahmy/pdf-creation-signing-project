

from pyhanko import stamp
from pyhanko.pdf_utils import text, images
from pyhanko.pdf_utils.font import opentype
from pyhanko.pdf_utils.incremental_writer import IncrementalPdfFileWriter
from pyhanko.sign import signers, fields
from pyhanko.sign.general import load_cert_from_pemder
from pyhanko_certvalidator import ValidationContext
from pyhanko.pdf_utils.reader import PdfFileReader
from pyhanko.sign.validation import validate_pdf_signature
import os
from controllers.SelfSignedCertController import selfSignedCert




def sign_pdf_file(pdf_name, certs_location, pdfs_location, sig_position):
    validate_cert_existance(certs_location)
    try:
        signer = signers.SimpleSigner.load(
            certs_location + '/pdfapp.key.pem', certs_location + '/pdfapp.cert.pem',
            key_passphrase=b'pdf'
        )

        with open(pdfs_location + '/' + pdf_name, 'rb+') as unsigned:
            pdf_file = IncrementalPdfFileWriter(unsigned)

            #   box() docs: ``ll_x``, ``ll_y``, ``ur_x``, ``ur_y`` format,
            #where ``ll_*`` refers to the lower left and ``ur_*`` to the upper right corner.
            #(x1, y1, x2, y2)
            #sig_position is a tuple (y1, page index)
            fields.append_signature_field(
                pdf_file, sig_field_spec=fields.SigFieldSpec(
                    'Signature', box=(50, sig_position[0], 200, sig_position[0] - 70), on_page = sig_position[1] -1
                )
            )

            meta = signers.PdfSignatureMetadata(field_name='Signature')
            pdf_signer = signers.PdfSigner(
                meta, signer=signer, stamp_style=stamp.TextStampStyle(border_width=0,
                    stamp_text='',
                    background=images.PdfImage('signature.png'),
                    background_opacity = 1
                ),
            )

            pdf_signer.sign_pdf(pdf_file, in_place=True) #sign and overwrite this same file.

            return True

    except Exception as e:
        print('something happened in sign_pdf_file', e)
        return False


'''
this will validate the digital signature in the pdf file
it checks for 2 things, first is that the original signed data have not changed.
second is that the signer identity, currently i'm using a self signed certificate to sign the pdfs, so it'll be added
to pyhanko trusted certs, so it can pass the second step of the validation
'''
def validated_pdf_file(pdf_name, certs_location, pdfs_folder):

    try:
        root_cert = load_cert_from_pemder(certs_location + '/pdfapp.cert.pem')
        
        vc = ValidationContext(trust_roots=[root_cert])
        with open(pdfs_folder + '/' + pdf_name, 'rb') as doc:
            r = PdfFileReader(doc)
            sig = r.embedded_signatures[0]
            status = validate_pdf_signature(sig, vc)

            print(status.pretty_print_details())
            print('verification status botton line: ', status.bottom_line)

            return status.bottom_line #thats a boolean
    except Exception as e:

        print('something happened in validated_pdf_file', e)
        return False

'''
currently checks if the self signed certs exist, if not recreate them

NOTE if cert.pem file got lost but the key.pem file (private key) still there, i made the new cert.pem to be generated
using the same existing private key, thus the cert will have the same public key in it, thus files signed with the old cert will pass validation
'''


def validate_cert_existance(certs_location):
    try:
        if not os.path.exists(certs_location + '/pdfapp.key.pem') or not os.path.exists(certs_location + '/pdfapp.cert.pem'):
            print('pems missing, have to recreate')
            status = selfSignedCert(cert_name=certs_location + '/pdfapp.cert.pem',
                                    key_name=certs_location + '/pdfapp.key.pem').create()
            return True if status else False

        print('pems found')
        return True

    except Exception as e:
        print('something happened in validate_cert_existance', e)
