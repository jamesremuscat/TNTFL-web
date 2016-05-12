#!/usr/bin/env python

from tntfl.web import serve
from wsgi import achievements

serve(achievements())
