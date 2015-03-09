#!/usr/bin/env python

import cgi
from tntfl.ladder import TableFootballLadder
from tntfl.web import serve_template


form = cgi.FieldStorage()

if "view" in form and form["view"].value == "json":
    ladder = TableFootballLadder("ladder.txt")
    serve_template("ladder.mako", ladder=ladder, base="../")
else:
    print "Status: 404 Not Found"
    print