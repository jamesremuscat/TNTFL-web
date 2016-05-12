#!/usr/bin/env python

from tntfl.ladder import TableFootballLadder
from tntfl.web import serve_template


ladder = TableFootballLadder("ladder.txt")
serve_template("stats.mako", ladder=ladder)
