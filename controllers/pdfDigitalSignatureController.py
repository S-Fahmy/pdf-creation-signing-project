

from pyhanko import stamp
from pyhanko.pdf_utils import text, images
from pyhanko.pdf_utils.font import opentype
from pyhanko.pdf_utils.incremental_writer import IncrementalPdfFileWriter
from pyhanko.sign import signers, fields
from pyhanko.sign.general import load_cert_from_pemder
from pyhanko_certvalidator import ValidationContext
from pyhanko.pdf_utils.reader import PdfFileReader
from pyhanko.sign.validation import validate_pdf_signature


def sign_pdf_file():
    signer = signers.SimpleSigner.load(
        '../certificates/pdfapp.key.pem', '../certificates/pdfapp.cert.pem',
        key_passphrase=b'pdf'
    )

    with open('sign.pdf', 'rb') as inf:
        w = IncrementalPdfFileWriter(inf)
        fields.append_signature_field(
            w, sig_field_spec=fields.SigFieldSpec(
                'Signature', box=(200, 600, 400, 660)
            )
        )

        meta = signers.PdfSignatureMetadata(field_name='Signature')
        pdf_signer = signers.PdfSigner(
            meta, signer=signer, stamp_style=stamp.TextStampStyle(
                # the 'signer' and 'ts' parameters will be interpolated by pyHanko, if present
                stamp_text='This is custom text!\nSigned by: %(signer)s\nTime: %(ts)s',
                background=images.PdfImage('stamp.png')
            ),
        )
        with open('output.pdf', 'wb') as outf:
            pdf_signer.sign_pdf(w, output=outf)


def validated_pdf_file():
    root_cert = load_cert_from_pemder('certificates/pdfapp.cert.pem')
    vc = ValidationContext(trust_roots=[root_cert])

    with open('output.pdf', 'rb') as doc:
        r = PdfFileReader(doc)
        sig = r.embedded_signatures[0]
        status = validate_pdf_signature(sig, vc)
        print(status.pretty_print_details())
