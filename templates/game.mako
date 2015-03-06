<%! title = "Table Football Ladder 3.0" %>
<%! base = "../../" %>
<%inherit file="html.mako" />
${self.blocks.render("recentGame", game=game, base=self.attr.base)}
<p><a href="json">This game as JSON</a></p>