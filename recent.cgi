#!/usr/bin/env python

import cgi
from tntfl.ladder import TableFootballLadder
from tntfl.web import serve_template


form = cgi.FieldStorage()

ladder = TableFootballLadder("ladder.txt")
serve_template("recent.mako", ladder=ladder, base="../", limit=form["limit"].value if "limit" in form else 10)
