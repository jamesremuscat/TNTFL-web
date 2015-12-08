#!/usr/bin/env python

import cgi
from tntfl.ladder import TableFootballLadder
from tntfl.web import serve_template


form = cgi.FieldStorage()

ladder = TableFootballLadder("ladder.txt")
fromTime = int(form["from"].value) if "from" in form else None
toTime = int(form["to"].value) if "to" in form else None
limit = int(form['limit'].value) if "limit" in form else None
includeDeleted = int(form['includeDeleted'].value) if "includeDeleted" in form else 1
serve_template("games.mako", ladder=ladder, fromTime=fromTime, toTime=toTime, limit=limit, includeDeleted=includeDeleted)
