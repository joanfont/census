# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, jsonify
import requests
from bs4 import BeautifulSoup

from re import compile, search

app = Flask(__name__)

URL_CENS = 'http://cens.palmademallorca.es/cens/dinamic/Consulta.htm'

DEFAULT_FIELDS = {
    'form_name': 'formcenso'
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/consulta')
def consulta():

    def _numero(li):
        regex = compile('(\d+)')
        text = li.text
        res = regex.search(text)
        if res:
            return int(res.group(1).strip())
        else:
            return None

    def _lletra(li):
        regex = compile('(.*): ([a-zA-Z]+)')
        text = li.text
        res = regex.search(text)
        if res:
            return res.group(2).strip()
        else:
            return None

    def _colegi(li):
        regex = compile('(.*):(.*)')
        text = li.text
        res = regex.search(text)
        if res:
            return res.group(2).strip()
        else:
            return None

    def _direccio(li):
        regex = compile('(.*):(.*)')
        text = li.text
        res = regex.search(text)
        if res:
            return res.group(2).strip()
        else:
            return None

    nif = request.args.get('nif')

    if not nif:
        return jsonify({'code': 'bad_request', 'desc': 'El camp NIF és obligatori'}), 400

    post_params = DEFAULT_FIELDS
    post_params.update({
        'nifPersona': nif
    })

    req = requests.post(URL_CENS, post_params)
    response = req.text
    soup = BeautifulSoup(response, 'html.parser')

    if soup.find('table', {'id': 'formcenso-errors'}):
        return jsonify({'code': 'invalid', 'desc': 'El NIF {nif} és invàlid'.format(nif=nif)}), 422

    ul = soup.find('div', {'id': 'mesaInfo'})
    lis = ul.find_all('li')

    districte, seccio, mesa, colegi, direccio = lis

    districte = _numero(districte)
    seccio = _numero(seccio)
    mesa = _lletra(mesa)
    colegi = _colegi(colegi)
    direccio = _direccio(direccio)



    return jsonify({
        'districte': districte,
        'seccio': seccio,
        'mesa': mesa,
        'colegi': colegi,
        'direccio': direccio
    })



if __name__ == '__main__':

    app.run(host='0.0.0.0', port=8000, debug=True)