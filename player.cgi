#!/usr/bin/env python

import cgi
from tntfl.ladder import TableFootballLadder
from tntfl.web import fail_404, serve_template


form = cgi.FieldStorage()

if "player" in form:
    ladder = TableFootballLadder("ladder.txt")
    if form["player"].value.lower() in ladder.players:
        player = ladder.players[form["player"].value.lower()]
        if "method" in form:
            if form["method"].value == "games":
                serve_template("playerGames.mako", pageTitle="%s's games" % player.name, games=player.games, ladder=ladder)
        else:
            serve_template("player.mako", player=player, ladder=ladder)
    else:
        fail_404()
        print
