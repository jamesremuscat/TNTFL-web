#!/usr/bin/env python

import cgi
from tntfl.web import serve
from wsgi import speculate_with

form = cgi.FieldStorage()


if "previousGames" in form:
    serialisedSpecGames = form["previousGames"].value
else:
    serialisedSpecGames = ""

if "bluePlayer" in form and "redPlayer" in form:
    redScore = form["redScore"].value if "redScore" in form else 0
    blueScore = form["blueScore"].value if "blueScore" in form else 0

    serialisedSpecGames += ",{0},{1},{2},{3}".format(form["redPlayer"].value, redScore, blueScore, form["bluePlayer"].value)

if serialisedSpecGames != "" and serialisedSpecGames[0] == ",":
    serialisedSpecGames = serialisedSpecGames[1:]


serve(speculate_with(serialisedSpecGames))
