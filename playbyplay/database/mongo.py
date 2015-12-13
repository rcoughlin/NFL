#!/usr/bin/env python

import os
import redis
import uuid
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

            key_list = key.split('|')
            if len(key_list) < 4: continue

            redis_key_prefix, name, play['year'], play['week'] = key_list

            players = play['players']
            del play['players']

            db_players = []
            for i, player_list in players.iteritems():
                for player in player_list:
                    if player['playerName']:
                        player_uuid = str(uuid.uuid4())
                        name = player['playerName']
                        team = player['clubcode']

                        db_player = {
                            '_id': player_uuid,
                            'name': name,
                            'team': team
                        }

                        if player_table.find(
                            {'name': name, 'team': team}
                        ).count() < 1:
                            db_players.append(player_table.insert(db_player))
                        else: db_players.append(player_uuid)

            play['players'] = db_players
            if play_table.find({
                'year': play['year'],
                'week': play['week'],
                'qtr': play['qtr'],
                'posteam': play['posteam'],
                'time': play['time']
            }).count() < 1:
                play['_id'] = str(uuid.uuid4())
                play_table.insert(play)

if __name__ == '__main__':
    persist_play_data()