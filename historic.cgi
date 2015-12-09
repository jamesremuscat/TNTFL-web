#!/usr/bin/env python
import cgi
from tntfl.web import serve_template

form = cgi.FieldStorage()

timeRange=None
if "gamesFrom" in form and "gamesTo" in form:
    fromTime = int(form["gamesFrom"].value)
    toTime = int(form["gamesTo"].value)
    timeRange=(fromTime, toTime)
serve_template("historic.mako", timeRange=timeRange)
