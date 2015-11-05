#!/usr/bin/env python

import nfldb
import nflvid.vlc

db = nfldb.connect()
q = nfldb.Query(db)

import pdb; pdb.set_tace()

q.game(season_year=2012, season_type='Regular')
q.player(full_name='Adrian Peterson').play(rushing_yds__ge=50)

nflvid.vlc.watch(db, q.as_plays(), '/m/nfl/coach/pbp')