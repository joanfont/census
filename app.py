from flask import Flask, render_template, request, jsonify

from core import BaseError, ElectoralCensus

app = Flask(__name__)

@app.errorhandler(BaseError)
def handle_base_error(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/find')
def find():
    nif = request.args.get('nif')
    voter = ElectoralCensus.find_by_nif(nif)
    response = jsonify(voter.to_dict())
    return response

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
