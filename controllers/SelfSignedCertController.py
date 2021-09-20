import datetime
import os

from cryptography import x509
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.x509.oid import NameOID



'''
the class responsible for creating and saving self signed cert, that will be trusted and used to sign the pdfs via pyhanko library
this will also be the root cert

NOTE docs referance used: https://github.com/pyca/cryptography/blob/main/docs/x509/tutorial.rst
'''
class selfSignedCert():

    def __init__(self, key_name, cert_name):

        #init the location of the cert and key pems fiels.
        self.private_key_file_name = key_name
        self.cert_file_name = cert_name



    def key_create(self):
        key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
        self.save_private_key_pem(key)

        return key


    '''
    saves the private key in a .pem file
    this will be used to encrypt the pdf during signing.
    '''
    def save_private_key_pem(self, key):

        with open(self.private_key_file_name, "wb") as keypem:
            keypem.write(key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.TraditionalOpenSSL,
                encryption_algorithm=serialization.BestAvailableEncryption(b'pdf')))



    '''
    generate the self signed cert
    TODO FILL THE ISSUER DATA.
    '''
    def generate_self_signed_cert(self, key):

        subject = issuer = x509.Name([
            x509.NameAttribute(NameOID.COUNTRY_NAME, u"xy"),
            x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, u"zyx"),
            x509.NameAttribute(NameOID.LOCALITY_NAME, u"yzx"),
            x509.NameAttribute(NameOID.ORGANIZATION_NAME, u"xzy"),
            x509.NameAttribute(NameOID.COMMON_NAME, u"xyz.com"),
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

        if not os.path.exists(self.cert_file_name):
            print('Generating self signed cert')

            if not os.path.exists(self.private_key_file_name):
                print('there is no private key found.')
                private_key = self.key_create()
            else:
                print('there is a private key found. loading it.')
            with open(self.private_key_file_name, "rb") as f:
                private_key = serialization.load_pem_private_key(f.read(), b'pdf')
                
            cert = self.generate_self_signed_cert(private_key)

        return True

