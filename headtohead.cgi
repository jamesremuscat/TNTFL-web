#!/usr/bin/env python
from tntfl.ladder import TableFootballLadder
from tntfl.web import serve_template, fail_404
import tntfl.templateUtils as utils
import cgi

form = cgi.FieldStorage()

ladder = TableFootballLadder("ladder.txt")

depth = 0
if "depth" in form:
    depth = form["depth"].value

try:
    if "player1" in form:
        player1 = ladder.players[form["player1"].value]
        if "player2" in form:
            player2 = ladder.players[form["player2"].value]
            if "method" in form:
                if form["method"].value == "games":
                    games = utils.getSharedGames(player1, player2)
                    pageTitle = "%s vs %s" % (player1.name, player2.name)
                    serve_template("headtoheadgames.mako", pageTitle=pageTitle, games=games, ladder=ladder)
            else:
                serve_template("headtohead.mako", ladder=ladder, player1=player1, player2=player2, depth=2)
        else:
            serve_template("headtohead.mako", ladder=ladder, player1=player1, depth=1)
    else:
        serve_template("headtohead.mako", ladder=ladder, depth=0)
except KeyError:
    fail_404()
