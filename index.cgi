#!/usr/bin/env python
from mako.lookup import TemplateLookup
from mako import exceptions

tl = TemplateLookup(directories=['templates'])


def serve_template(templatename, **kwargs):
    mytemplate = tl.get_template(templatename)
    print(mytemplate.render(**kwargs))

try:
    serve_template("index.mako")
except:
    print(exceptions.text_error_template().render())
