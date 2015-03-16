#!/usr/bin/env python

import cgi
from tntfl.ladder import TableFootballLadder
from tntfl.web import serve_template


form = cgi.FieldStorage()

ladder = TableFootballLadder("ladder.txt")
serve_template("ladder.mako", ladder=ladder, base="../")
