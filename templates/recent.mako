<%page args="ladder, base, games, limit=10"/>
<%namespace name="blocks" file="blocks.mako" />
<%!
# from datetime import datetime
%>
<%
  recentGames = [l for l in games if not l.isDeleted()][-limit:]
  recentGames.reverse()
%>
<div class="container-fluid">
    ${blocks.render("gameList", games=recentGames, base=base)}
</div>
