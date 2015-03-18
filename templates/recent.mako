<%page args="ladder, base, limit=10"/>
<%namespace name="blocks" file="blocks.mako" />
<%! from datetime import datetime %>
<%
  recentGames = ladder.games[-limit:]
  recentGames.reverse()
%>
% for game in recentGames:
    ${blocks.render("game", game=game, base=base)}
% endfor
<p>Updated at ${datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>