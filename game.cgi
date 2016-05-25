#!/usr/bin/env python

import cgi
from time import time
from tntfl.ladder import Game, TableFootballLadder
from tntfl.web import serve
from wsgi import game_add, game_show


form = cgi.FieldStorage()

if "method" in form:
    if form["method"].value == "add":
        serve(game_add())
    elif form["method"].value == "view" and "game" in form:
        gameTime = int(form["game"].value)
        serve(game_show(gameTime))
