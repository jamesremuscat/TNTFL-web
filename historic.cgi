#!/usr/bin/env python
import cgi
from datetime import date
from tntfl.web import serve
from wsgi import historic_range

form = cgi.FieldStorage()

if "gamesFrom" in form and "gamesTo" in form:
    fromTime = int(form["gamesFrom"].value)
    toTime = int(form["gamesTo"].value)
    timeRange = (fromTime, toTime)
else:
    epoch = date.fromtimestamp(0)
    startdate = date.today().replace(day=1)
    enddate = startdate.replace(month=startdate.month + 1) if startdate.month < 12 else date(startdate.year + 1, 1, 1)
    start = (startdate - epoch).total_seconds()
    end = (enddate - epoch).total_seconds()
    timeRange = (start, end)
serve(historic_range(timeRange))
