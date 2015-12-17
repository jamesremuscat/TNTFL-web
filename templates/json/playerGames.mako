<%!
base = "../../../"
%>
<%inherit file="json.mako" />
[
% for game in games:
  ${self.blocks.render("game", game=game, base=self.attr.base)}${"," if loop.index < length - 1 else ""}
% endfor
]
