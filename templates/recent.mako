<%page args="ladder, base, limit=10"/>
<%namespace name="blocks" file="blocks.mako" />
<%!
from datetime import datetime
from tntfl.pundit import Pundit
%>
<%
  recentGames = [l for l in ladder.games if not l.isDeleted()][-limit:]
  recentGames.reverse()
  pundit = Pundit()
%>
% for game in recentGames:
<%
  red = ladder.getPlayer(game.redPlayer)
  blue = ladder.getPlayer(game.bluePlayer)
  punditryAvailable = pundit.anyComment(red, game, blue)
%>
    ${blocks.render("game", game=game, base=base, punditryAvailable=punditryAvailable)}
% endfor
<p>Updated at ${datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>
