<%! base = "../" %>
<%inherit file="json.mako" />[
<%
  recentGames = ladder.games[-limit:]
  recentGames.reverse()
%>
% for game in recentGames:
    {"href": "${self.attr.base}game/${game.time}/json"}${"," if loop.index < len(recentGames) - 1 else ""}
% endfor
]