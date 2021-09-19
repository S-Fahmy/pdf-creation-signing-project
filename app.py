from flask import Flask, render_template, request, jsonify, abort, url_for


app = Flask(__name__)

# app.config.from_object('config')


@app.route('/')
def main():

    return render_template('index.html')




if __name__ == '__main__':
    # app.run(host='127.0.0.1', port=8080, debug=True)
    app.run(debug=True)


