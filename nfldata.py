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

    # TODO commonize
    year = int(request.args.getlist('year')[0])
    week = int(request.args.getlist('week')[0])

    games = fetch_games(inputYear, inputWeek)
    players = nflgame.combine_game_stats(games)

    messages = []
    for player in players.rushing().sort('rushing_yds'):
        messages.append('{} {} carries for {} yards and {} TDs'.format(
            player, player.rushing_att, player.rushing_yds,
            player.rushing_tds))

    return json.dumps(messages)


@app.route('/play_by_play.json', methods=['GET'])
def play_by_play():

    # TODO commonize
    name = request.args.getlist('name')[0]
    year = int(request.args.getlist('year')[0])
    week = int(request.args.getlist('week')[0])

    print 'HERE'

    '''
    Try to perform some arithmetic on our inputs, if they aren't ints, our API
    will throw errors
    '''
    try:
        year = year + 1 - 1
        week = week + 1 - 1
    except TypeError as e:
        return e

    plays = []
    if name and year and week:
        try:
            nfl_game_plays = fetch_plays(name, year, week)
            for play in nfl_game_plays:
                plays.append(play.data)
        except TypeError as e: pass

    return json.dumps(plays)


def fetch_games(year, week):
    return nflgame.games(year, week)


def fetch_player(name):
    return nflgame.find(name)


def fetch_plays(name, year, week):
    player = fetch_player(name)
    if len(player) > 0:
        return player[0].plays(year, week)
    else:
        return None


def send_static_file(path):
    return app.send_static_file(path)


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)