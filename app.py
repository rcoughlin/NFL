#!/usr/bin/env python

import os

import redis
import nflgame
import json
import requests

from flask import Flask
from flask import jsonify
from flask import request
from flask.ext.cors import CORS


app = Flask(__name__, static_url_path='/static')
cors = CORS(app)

REDIS_URL = os.environ.get('REDIS_URL') or '0.0.0.0:6379'
REDIS = redis.from_url(REDIS_URL)


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
    name, year, week = parse_request_arguments(request.args)

    games = fetch_games(year, week)
    players = nflgame.combine_game_stats(games)

    messages = []
    for player in players.rushing().sort('rushing_yds'):
        messages.append('{} {} carries for {} yards and {} TDs'.format(
            player, player.rushing_att, player.rushing_yds,
            player.rushing_tds))

    return json.dumps(messages)


@app.route('/plays_by_player.json', methods=['GET'])
def plays_by_player():
    name, year, week = parse_request_arguments(request.args)

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
            print 'IN'
            key = 'plays_by_player|{}|{}'.format(year, week)
            data = REDIS.get(key)
            print 'DATA', data
            if not data:
                data = fetch_plays(name, year, week)
                print 'API'
                REDIS.set(key, json.dumps(list(data)))
                print 'SET'
            else:
                data = json.loads(data)
            for play in data:
                print 'LOOP'
                plays.append(play.data)
        except TypeError as e:
            print e

    return json.dumps(plays)


@app.route('/plays_by_team.json', methods=['GET'])
def plays_by_team():
    name, year, week = parse_request_arguments(request.args)
    team = None

    player = None
    players = fetch_player(name)
    if len(players) > 0:
        player = players[0]
        team = player.team

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
    api_called = False
    if team and year and week:
        try:
            print 'IN', json.loads
            key = 'plays_by_team|{}|{}|{}'.format(player.name, year, week)
            data = REDIS.get(key)
            print 'DATA', type(data)
            if not (data and len(data)):
                print 'HIT REDIS'
                data = nflgame.combine_plays(fetch_games(year, week, team))

                plays = json.dumps([
                    play.data for play in data if team == play.team
                ])
                print 'API'
                REDIS.set(key, plays)
                print 'SET'
            else:
                print 'POST DATA', data
                plays = data
            # for play in data:
            #     print 'LOOP', play
            #     if team == play.team:
            #         plays.append(play.data)
        except TypeError as e: pass

    return plays


def fetch_games(year, week, team = None):
    games = nflgame.games(year, week)
    if team:
        for game in games:
            if game.home == team or game.away == team:
                return [ game ]
    return games


def fetch_player(name):
    return nflgame.find(name)


def fetch_plays(name, year, week):
    player = fetch_player(name)
    if len(player) > 0:
        return player[0].plays(year, week)
    else:
        return None


def parse_request_arguments(args):
    name, year, week = None, None, None

    if len(args.getlist('name')):
        name = args.getlist('name')[0]
    if len(args.getlist('year')):
        year = int(args.getlist('year')[0])
    if len(args.getlist('week')):
        week = int(args.getlist('week')[0])

    return name, year, week


def send_static_file(path):
    return app.send_static_file(path)


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)