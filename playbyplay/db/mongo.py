#!/usr/bin/env python

import os
import redis
import json

from pymongo import MongoClient


REDIS_URL = os.environ.get('REDIS_URL') or '0.0.0.0:6379'
REDIS = redis.from_url(REDIS_URL)
MONGO_URL = os.environ.get('MONGO_URL')
MONGO_USERNAME = None
MONGO_PASSWORD = None
MONGO_CLIENT = None

if not MONGO_URL:
    MONGO_CLIENT = MongoClient('localhost', 27017)
else:
    MONGO_CLIENT = MongoClient(MONGO_URL)
    MONGO_CLIENT.playbyplay.authenticate(MONGO_USERNAME, MONGO_PASSWORD,
        mechanism='SCRAM-SHA-1')


def persist_play_data():
    db = MONGO_CLIENT.playbyplay
    play_table = db.plays
    player_table = db.players

    for key in REDIS.keys():
        data = json.loads(REDIS.get(key))

        for play in data:

            if len(key.split('|')) < 4:
                continue

            players = play['players']
            del play['players']

            for i, player_list in players.iteritems():
                for player in player_list:
                    if player['playerName']:
                        db_player = {
                            'name': player['playerName'],
                            'clubcode': player['clubcode']
                        }

                        if player_table.count(db_player) < 1:
                            player_table.insert(db_player)

            if play_table.count(play) < 1:
                play_table.insert(play)


if __name__ == '__main__':
    persist_play_data()