import os
from flask import Flask, render_template, request, jsonify, abort, url_for
from controllers import pdfBuilderController
from controllers import pdfDigitalSignatureController
import base64


app = Flask(__name__)
app.config.from_object('config')


@app.route('/')
def main():

    return render_template('index.html')


@app.route('/pdf/create', methods=["POST"])
def create_a_pdf():
    try:
        data = request.json

        #TODO: more customized/detailed validations...
        if data is None or data.get('invoiceData' , None) is None or data.get('pdfName', None) is None or data['pdfName'] == '':
            print('data incomplete')
            return jsonify({'success': False, 'message': 'data incorrect'}), 500

        # print(data.get('invoiceData'))
        pdf_name = data['pdfName']
        invoice_data = data['invoiceData']

        #build the pdf file first
        if pdfBuilderController.build_pdf(pdf_name, invoice_data, app.config.get('PDFS_LOCATION'), app.config.get('FONTS_PATH')):
            #sign it
            success = pdfDigitalSignatureController.sign_pdf_file(pdf_name + '.pdf', app.config.get('CERTS_LOCATION'), app.config.get('PDFS_LOCATION'))

            if not success:
                return jsonify({'success': False, 'message': 'error during signing file'}), 500
        
        return jsonify({'success': True}), 200

    except Exception as e:
        print('something happened in create_a_pdf', e)
        return jsonify({'success': False, 'message': 'error'}), 500



'''
takes pdf name as a parameter, and calls the signature validation function on it
currently just return valid true or false
'''
@app.route('/pdf/validate/<string:pdf_name>', methods = ['GET', 'POST'])
def validate_a_pdf(pdf_name):
    try:

        valid = pdfDigitalSignatureController.validated_pdf_file(pdf_name, app.config.get('CERTS_LOCATION'), app.config.get('PDFS_LOCATION'))
        if valid is False:
            
            return jsonify({'valid': False}), 200

        return jsonify({'valid': True}), 200

    except Exception as e:

        print('something happened in validate_a_pdf', e)
        return jsonify({'valid': False, 'message': 'error'}), 500


@app.route('/signature/save', methods = ['POST'])
def save_signature():
    try:
        signatureImgData =  request.json.split(',')[1]

        with open("signature.png", "wb") as image:
            image.write(base64.b64decode(signatureImgData))
        
        return jsonify({'success': True}), 200

    except Exception as e:

        print('something happened in save_signature', e)
        return jsonify({'valid': False, 'message': 'error'}), 500


@app.route('/signature/load', methods = ['GET'])
def get_existing_signature():
    if not os.path.exists('signature.png'):
        print('no existing sig images found')
        return jsonify({'success': False}), 200


    img_data = ""
    with open("signature.png", "rb") as image:
        data = base64.b64encode(image.read())
        img_data = data.decode()

    return jsonify({'success': True, 'img_data': img_data}), 200

if __name__ == '__main__':
    # app.run(host='127.0.0.1', port=8080, debug=True)
    app.run(debug=True)


