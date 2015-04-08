<%page args="ladder, base, limit=10"/>
<%namespace name="blocks" file="blocks.mako" />
<%! from datetime import datetime %>
<%
  recentGames = [l for l in ladder.games if not l.isDeleted()][-limit:]
  recentGames.reverse()
%>
% for game in recentGames:
    ${blocks.render("game", game=game, base=base)}
% endfor
<p>Updated at ${datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>