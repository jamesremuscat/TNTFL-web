#!/usr/bin/env python
from tntfl.web import serve
from wsgi import index

serve(index())
