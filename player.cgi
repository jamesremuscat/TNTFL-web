#!/usr/bin/env python

import cgi
from tntfl.web import serve
from wsgi import player, player_games


form = cgi.FieldStorage()

if "player" in form:
    playerName = form["player"].value.lower()
    if "method" in form:
        if form["method"].value == "games":
            serve(player_games(playerName))
    else:
        serve(player(playerName))
