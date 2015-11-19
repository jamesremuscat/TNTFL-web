<%page args="ladder, base, games, limit=10"/>
<%namespace name="blocks" file="blocks.mako" />
<%!
from datetime import datetime
from tntfl.pundit import Pundit

def punditryAvailable(pundit, game, ladder):
    red = ladder.getPlayer(game.redPlayer)
    blue = ladder.getPlayer(game.bluePlayer)
    return pundit.anyComment(red, game, blue)
%>
<%
  recentGames = [l for l in games if not l.isDeleted()][-limit:]
  recentGames.reverse()
  pundit = Pundit()
%>
% for game in recentGames:
    ${blocks.render("game", game=game, base=base, punditryAvailable=punditryAvailable(pundit, game, ladder))}
% endfor
<p>Updated at ${datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>
