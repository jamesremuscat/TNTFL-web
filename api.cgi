#!/usr/bin/env python

from tntfl.web import serve
from wsgi import api

serve_template(api())
