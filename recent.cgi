#!/usr/bin/env python

import cgi
from tntfl.web import serve
from wsgi import recent_ajax


form = cgi.FieldStorage()


serve(recent_ajax(int(form["limit"].value) if "limit" in form else 10))
