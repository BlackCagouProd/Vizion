# -*- coding: utf-8 -*-
# from io import BytesIO
from flask import Flask, render_template, Response, jsonify
import json
import requests
from api import Population_api_url, meteo_api

# from matplotlib.figure import Figure
# from matplotlib.backends.backend_agg import FigureCanvasAgg as VC


app = Flask(__name__)


@app.route("/")
def dashboard():
    return render_template("dashboard.html")


@app.route("/api/meteo")
def meteo():
    m = requests.get(meteo_api)
    m_m = json.loads(m.content.decode("utf-8"))
    if m.status_code != 200:
        return jsonify(dict(status='error',
                            message='La requête à l\'API météo n\'a pas fonctionné. Voici le message renvoyé par l\'API : {}'.format(
                                m_m['message']))), 500

    data = []  # On initialise une liste vide
    for prev in m_m["weather"]:
        datetime = m_m['dt']
        weather = m_m['weather'][0]["main"]
        temperature = m_m['main']['temp'] - 273.15  # Conversion de Kelvin en °c
        temperature = round(temperature, 2)
        name = m_m['name']
        data.append([name, weather, datetime, temperature])
    return jsonify({
        'status': 'ok',
        'data': data
    })


@app.route("/api/popnc")
def get_pop():
    p = requests.get(Population_api_url)
    p_p = json.loads(p.content.decode('utf-8'))
    if p.status_code != 200:
        return jsonify(dict(status='error',
                            message='La requête à l\'API météo n\'a pas fonctionné. Voici le message renvoyé par l\'API : {}'.format(
                                p_p['message']))), 500

    data = []
    for i in p_p['records']:
        title = i['datasetid']
        year = i['fields']['column_6']
        commune = i['fields']['commune']
        data.append([title, year, commune])
    return jsonify({
        'status': 'ok',
        'data': data
    })
    return p_p






if __name__ == "__main__":
    app.run(debug=True)
