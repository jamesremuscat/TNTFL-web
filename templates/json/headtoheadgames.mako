<%!
base = "../../../../"
%>
<%inherit file="json.mako" />
[
% for game in games:
  ${self.blocks.render("game", game=game, base=base)}${"," if loop.index < len(games) - 1 else ""}
% endfor
]
