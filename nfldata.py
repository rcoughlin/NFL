#!/usr/bin/env python

import os

from flask import Flask
from flask import jsonify
from flask import request
from flask.ext.cors import CORS

import nflgame
import json
import requests


app = Flask(__name__, static_url_path='/static')
cors = CORS(app)


@app.route('/', methods=['GET'])
def serve_index_asset():
    return send_static_file('index.html')

@app.route('/plays', methods=['GET'])
def serve_play_by_play_asset():
    return send_static_file('html/plays.html')

@app.route('/<path:path>', methods=['GET'])
def serve_static_assets(path):
    return send_static_file(path)

@app.route('/rushing_yds.json', methods=['GET'])
def rushing_yards():
    inputYear = int(request.args['inputYear'] or \
        request.args.getList('inputYear')[0])
    inputWeek = int(request.args['inputWeek'] or \
        request.args.getList('inputWeek')[0])

    games = nflgame.games(inputYear, inputWeek)
    players = nflgame.combine_game_stats(games)

    messages = []
    for player in players.rushing().sort('rushing_yds'):
        messages.append('{} {} carries for {} yards and {} TDs'.format(
            player, player.rushing_att, player.rushing_yds,
            player.rushing_tds))

    return json.dumps(messages)

def send_static_file(path):
    return app.send_static_file(path)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)