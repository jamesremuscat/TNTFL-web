<%! base = "" %>
<%
def accept(game):
    return (not fromTime or game.time >= fromTime) and (not toTime or game.time <= toTime) and (includeDeleted or not g.isDeleted())
games = [g for g in ladder.games if accept(g)]
if limit:
    games = games[-limit:]
%>
<%inherit file="json.mako" />[
% for g in games:
    ${self.blocks.render("game", game=g, base=self.attr.base)}${"," if loop.index < len(games) - 1 else ""}
% endfor
]
