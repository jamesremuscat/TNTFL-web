#!/usr/bin/env python

import cgi
from time import time
from tntfl.ladder import Game, TableFootballLadder
from tntfl.web import redirect_302

form = cgi.FieldStorage()

if "method" in form:
    if form["method"].value == "add":
        if "bluePlayer" in form and "redPlayer" in form and "redScore" in form and "blueScore" in form:
            game = Game(form["redPlayer"].value, form["redScore"].value, form["bluePlayer"].value, form["blueScore"].value, time())
            ladder = TableFootballLadder("ladder.txt")
            ladder.addAndWriteGame(game)
            if "view" in form and form["view"].value == "json":
                pass
            else:
                redirect_302("index.cgi")
    elif form["method"] is "view":
        pass
