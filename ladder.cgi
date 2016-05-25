#!/usr/bin/env python

from tntfl.web import serve
from wsgi import ladder_ajax
import cgi

form = cgi.FieldStorage()


if "gamesFrom" in form and "gamesTo" in form:
    fromTime = int(form["gamesFrom"].value)
    toTime = int(form["gamesTo"].value)
    timeRange = (fromTime, toTime)
else:
    timeRange = None

serve(
    ladder_ajax(
        sortCol=form['sortCol'].value if "sortCol" in form else None,
        sortOrder=form["sortOrder"].value if "sortOrder" in form else None,
        showInactive=form["showInactive"].value if "showInactive" in form else 0,
        timeRange=timeRange
    )
)
