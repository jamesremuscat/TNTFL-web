<%page args="ladder, base, limit=10"/>
<%namespace name="blocks" file="blocks.mako" />
<%
  recentGames = ladder.games[-limit:]
  recentGames.reverse()
%>
% for game in recentGames:
    ${blocks.render("recentGame", game=game, base=base)}
% endfor