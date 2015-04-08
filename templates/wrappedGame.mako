<%! title = "Table Football Ladder 3.0" %>
<%! base = "../../" %>
<%inherit file="html.mako" />
${self.blocks.render("game", game=game, base=self.attr.base)}
<p><a href="json">This game as JSON</a></p>
% if not game.isDeleted():
<a href="delete" class="btn btn-danger pull-right"><span class="glyphicon glyphicon-lock"></span> Delete game</a>
% endif