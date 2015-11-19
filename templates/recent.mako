<%page args="ladder, base, games, limit=10"/>
<%namespace name="blocks" file="blocks.mako" />
<%!
from datetime import datetime
from tntfl.pundit import Pundit
import tntfl.templateUtils as utils
%>
<%
  recentGames = [l for l in games if not l.isDeleted()][-limit:]
  recentGames.reverse()
  pundit = Pundit()
%>
% for game in recentGames:
    ${blocks.render("game", game=game, base=base, punditryAvailable=utils.punditryAvailable(pundit, game, ladder))}
% endfor
<p>Updated at ${datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>
