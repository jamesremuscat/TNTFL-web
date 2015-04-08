#!/usr/bin/env python

import cgi
import os
from time import time
from tntfl.ladder import TableFootballLadder
from tntfl.web import redirect_302, serve_template

form = cgi.FieldStorage()


ladder = TableFootballLadder("ladder.txt")
if "game" in form:
    gameTime = int(form["game"].value)
    found = False
    for game in ladder.games:
        if game.time == gameTime and not found:
            found = True
            if "deleteConfirm" in form and form["deleteConfirm"].value == "true":
                game.deletedAt = time()
                game.deletedBy = os.environ["REMOTE_USER"] if "REMOTE_USER" in os.environ else "Unknown"
                ladder.writeLadder("ladder.txt")
                redirect_302("./")
            else:
                serve_template("deleteGame.mako", game=game)
    if not found:
        print "Status: 404 Not Found"
        print
