#!/usr/bin/env python

from tntfl.ladder import TableFootballLadder
from tntfl.web import serve_template


ladder = TableFootballLadder("ladder.txt")
serve_template("achievements.mako", achievements=sorted(ladder.getAchievements().iteritems(), reverse=True, key=lambda t: t[1]))
