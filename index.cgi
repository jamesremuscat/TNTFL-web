#!/usr/bin/env python
import cgi
from tntfl.ladder import TableFootballLadder
from tntfl.web import serve_template

form = cgi.FieldStorage()

if "to" in form and "from" in form:
    toTime = int(form["to"].value)
    fromTime = int(form["from"].value)
    ladder = TableFootballLadder("ladder.txt", timeRange=(fromTime, toTime))
else:
    ladder = TableFootballLadder("ladder.txt")
serve_template("index.mako", ladder=ladder)
