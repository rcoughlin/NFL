#!/usr/bin/env python

import numpy as np

from playbyplay.database.mongo import MONGO_CLIENT

# Pull all of our input players
def input_space(year):
    db = MONGO_CLIENT.playbyplay
    play_table = db.plays
    player_table = db.players

    # With our defined year we grab all of the plays in the year
    players = player_table.find({})
    plays = play_table.find({'year': str(year)})

    '''
    Ok, we have all of the players in our input year, and all of the players
    We have no indication of whether we have viable players yet, does our
    player have plays in our input year
    '''
    player_plays = {}
    for play in plays:

        '''
        Who is really responsible for the play? attribute the yards to
        both players, weighting will work out
        TODO kickers and qbs
        '''
        for player in play['players']:
            db_players = list(player_table.find({'_id': player}))
            db_player = None

            if len(db_players):
                db_player = db_players[0]

            if db_player:
                if not player_plays.get(db_player['name'], None):
                    player_plays[db_player['name']] = {
                        'yards': [],
                        'weighted_yards_avg': 0
                    }

                player_plays[db_player['name']]['yards'].append(int(play['ydsnet']))
                player_plays[db_player['name']]['weighted_yards_avg'] = np.average(
                    player_plays[db_player['name']]['yards'])


if __name__ == '__main__':
    input_space(2015)