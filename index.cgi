#!/usr/bin/env python
from mako.template import Template

print "Content-Type: text/html"
print

print(Template("hello ${data}!").render(data="world"))
