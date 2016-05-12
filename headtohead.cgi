#!/usr/bin/env python
from tntfl.web import serve, fail_404
from wsgi import head_to_head
import cgi
import sys

form = cgi.FieldStorage()



if "player1" in form:
    if "player2" in form:
        player1 = form["player1"].value.lower()
        player2 = form["player2"].value.lower()
        serve(head_to_head(player1, player2))
        sys.exit(0)
fail_404()
