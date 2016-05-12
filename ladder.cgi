#!/usr/bin/env python

from tntfl.web import serve
from wsgi import ladder_ajax
import cgi

form = cgi.FieldStorage()

serve(ladder_ajax(
               sortCol=form['sortCol'].value if "sortCol" in form else None,
               sortOrder=form["sortOrder"].value if "sortOrder" in form else None,
               showInactive=form["showInactive"].value if "showInactive" in form else 0))
