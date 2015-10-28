import os

from flask import Flask, send_from_directory
from flask import jsonify
from flask import request
from flask.ext.cors import CORS
import nflgame
import json
import requests

FILE_PATH = os.path.dirname(os.path.realpath('__file__'))

app = Flask(__name__, static_url_path=FILE_PATH)
cors = CORS(app)

@app.route('/index.html', methods=['GET'])
def metrics():
    return send_from_directory(FILE_PATH, 'index.html')

@app.route('/', methods=['GET'])
def hello_world():
    if request.method == 'GET':
        inputYear = request.args['inputYear'] or request.args.getList('inputYear')[0]
        inputWeek = request.args['inputWeek'] or request.args.getList('inputWeek')[0]

        games = nflgame.games(int(inputYear), week=int(inputWeek))
        players = nflgame.combine_game_stats(games)
        messages=[]

        for p in players.rushing().sort('rushing_yds').limit(10):
           msg = '%s %d carries for %d yards and %d TDs' %(p, p.rushing_att, p.rushing_yds, p.rushing_tds)
           messages.append(msg)
        print messages
        return json.dumps(messages)
    return False

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
