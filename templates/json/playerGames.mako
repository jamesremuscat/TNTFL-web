<%! base = "../../../" %>
<%inherit file="json.mako" />[
% for game in player.games:
    ${self.blocks.render("game", game=game, base=self.attr.base, json=True)}${"," if loop.index < len (player.games) - 1 else ""}
% endfor
]