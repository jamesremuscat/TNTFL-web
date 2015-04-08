<%! base = "../" %>
<%inherit file="json.mako" />[
<%
  recentGames = [l for l in ladder.games if not l.isDeleted()][-limit:]
  recentGames.reverse()
%>
% for game in recentGames:
    ${self.blocks.render("game", game=game, base=self.attr.base)}${"," if loop.index < len(recentGames) - 1 else ""}
% endfor
]