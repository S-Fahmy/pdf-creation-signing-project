import datetime
import os
import uuid

from cryptography import x509
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.x509.oid import NameOID



'''
the class responsible for creating and saving self signed cert, that will be trusted and used to sign the pdfs via pyhanko library
this will also be the root cert

#NOTE the current code is using this sole cert sign all files, i have not been told much about the use case of this service but 
# if there are use cases that needs different certs for different pdfs this code can be improved further by using cert chain of trust, 
# by creating 1 root cert(self-signed or from a trusted CA), and then different certs will be created and
# signed by the root cert on request (CSR).

docs referance used: https://github.com/pyca/cryptography/blob/main/docs/x509/tutorial.rst
'''
class selfSignedCert():

    def __init__(self, key_name, cert_name):

        self.private_key_file_name = key_name
        self.cert_file_name = cert_name

    def key_create(self):
        key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
        self.save_private_key_pem(key)

        return key



    def save_private_key_pem(self, key):

        with open(self.private_key_file_name, "wb") as keypem:
            keypem.write(key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.TraditionalOpenSSL,
                encryption_algorithm=serialization.BestAvailableEncryption(b'pdf')))


    def generate_self_signed_cert(self, key):

        subject = issuer = x509.Name([
            x509.NameAttribute(NameOID.COUNTRY_NAME, u"US"),
            x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, u"California"),
            x509.NameAttribute(NameOID.LOCALITY_NAME, u"San Francisco"),
            x509.NameAttribute(NameOID.ORGANIZATION_NAME, u"My Company"),
            x509.NameAttribute(NameOID.COMMON_NAME, u"mysite.com"),
        ])

        cert = x509.CertificateBuilder().subject_name(
            subject
        ).issuer_name(
            issuer
        ).public_key(
            key.public_key()
        ).serial_number(
            x509.random_serial_number()
        ).not_valid_before(
            datetime.datetime.utcnow()
        ).not_valid_after(
            # Our certificate will be valid for 10 days
            datetime.datetime.utcnow() + datetime.timedelta(days=10)
        ).add_extension(
            extension=x509.KeyUsage(
                digital_signature=True, key_encipherment=True, content_commitment=True,
                data_encipherment=False, key_agreement=False, encipher_only=False, decipher_only=False,
                key_cert_sign=False, crl_sign=False), critical=True
        ).sign(key, hashes.SHA256())

        self.save_cert(cert)

        return cert


    def save_cert(self, cert):
        with open(self.cert_file_name, "wb") as f:
            f.write(cert.public_bytes(serialization.Encoding.PEM))


    def create(self):
        if not os.path.exists(self.cert_file_name) or not os.path.exists(self.private_key_file_name):
            priv = self.key_create()
            cert = self.generate_self_signed_cert(priv)

        return True

print('Generating certificates')
selfSignedCert(cert_name='certificates/pdfapp.cert.pem', key_name='certificates/pdfapp.key.pem').create()