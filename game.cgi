#!/usr/bin/env python

import cgi
from time import time
from tntfl.ladder import Game, TableFootballLadder
from tntfl.web import redirect_302, serve_template

form = cgi.FieldStorage()

if "method" in form:
    ladder = TableFootballLadder("ladder.txt")
    if form["method"].value == "add":
        if "bluePlayer" in form and "redPlayer" in form and "redScore" in form and "blueScore" in form:
            game = Game(form["redPlayer"].value, form["redScore"].value, form["bluePlayer"].value, form["blueScore"].value, time())
            ladder.addAndWriteGame(game)
            if "view" in form and form["view"].value == "json":
                serve_template("json/game.mako", game=game)
            else:
                redirect_302("index.cgi")
    elif form["method"].value == "view" and "game" in form:
        print "AAA"
        gameTime = form["game"].value
        found = False
        for game in ladder.games:
            if game.time == gameTime and not found:
                serve_template("json/game.mako", game=game)
                found = True
        if not found:
            print "404 Not Found"
            print
