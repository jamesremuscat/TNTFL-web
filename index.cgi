#!/usr/bin/env python
import cgi
from tntfl.ladder import TableFootballLadder
from tntfl.web import serve_template

form = cgi.FieldStorage()

if "gamesFrom" in form and "gamesTo" in form:
    fromTime = int(form["gamesFrom"].value)
    toTime = int(form["gamesTo"].value)
    ladder = TableFootballLadder("ladder.txt", timeRange=(fromTime, toTime))
else:
    ladder = TableFootballLadder("ladder.txt")
serve_template("index.mako", ladder=ladder)
