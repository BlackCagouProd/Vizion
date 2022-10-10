# -*- coding: utf-8 -*-
from flask import Flask , render_template, jsonify
import json
import requests
from api import Population_api_url
from matplotlib.figure import Figure

app = Flask(__name__)

@app.route("/")
def dashboard():
    param = requests.get(Population_api_url)
    content = json.loads(param.content.decode("utf-8"))

    labels = []
    values = []

    for key in content:
        labels.append(key)
        values.append(content[key])

        print(labels)
        print(values)

        # fig = Figure()
        # ax1 = fig.subplots(1, 1)
        # ax1.bar(labels, values)
        # fig.savefig("test.png",format="png")

    if param.status_code != 200:
        return jsonify({
            'status': 'error',
            'message': 'La requête à l\'API n\'a pas fonctionné. Voici le message renvoyé par l\'API : {}'.format(content['message'])
        }), 500
    # else:
    #     return jsonify({
    #         'status': 'ok',
    #         'data': []
    #     })

    return render_template("dashboard.html", content=content)

if __name__ == "__main__":
    app.run(debug=True)