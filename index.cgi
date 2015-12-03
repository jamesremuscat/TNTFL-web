#!/usr/bin/env python
import cgi
from tntfl.ladder import TableFootballLadder
from tntfl.web import serve_template

form = cgi.FieldStorage()

if "time" in form:
    time = int(form["time"].value)
    ladder = TableFootballLadder("ladder.txt", untilTime=time)
else:
    ladder = TableFootballLadder("ladder.txt")
serve_template("index.mako", ladder=ladder)
