#!/usr/bin/env python

import cgi
import os
from time import time
from tntfl.ladder import Game, TableFootballLadder
from tntfl.web import redirect_302, serve_template

form = cgi.FieldStorage()

if "method" in form:
    ladder = TableFootballLadder("ladder.txt")
    if form["method"].value == "add":
        if "bluePlayer" in form and "redPlayer" in form:
            redScore = form["redScore"].value if "redScore" in form else 0
            blueScore = form["blueScore"].value if "blueScore" in form else 0
            game = Game(form["redPlayer"].value, redScore, form["bluePlayer"].value, blueScore, time())
            ladder.addAndWriteGame(game)
            if "view" in form and form["view"].value == "json":
                serve_template("wrappedGame.mako", game=game)
            else:
                redirect_302("../")
    elif form["method"].value == "view" and "game" in form:
        gameTime = int(form["game"].value)
        found = False
        for game in ladder.games:
            if game.time == gameTime and not found:
                serve_template("wrappedGame.mako", game=game)
                found = True
        if not found:
            print "Status: 404 Not Found"
            print
    elif form['method'].value == "delete" and "game" in form:
        gameTime = int(form["game"].value)
        found = False
        for game in ladder.games:
            if game.time == gameTime and not found:
                found = True
                if "deleteConfirm" in form and form["deleteConfirm"].value == "true":
                    game.deletedAt = time()
                    game.deletedBy = os.environ["REMOTE_USER"] if "REMOTE_USER" in os.environ else "Unknown"
                    ladder.writeLadder("ladder.txt")
                    redirect_302("../")
                else:
                    print "Content-Type: text/plain"
                    print
                    print form
                    serve_template("deleteGame.mako", game=game)
        if not found:
            print "Status: 404 Not Found"
            print
