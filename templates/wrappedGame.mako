<%!
title = ""
base = "../../"
from tntfl.pundit import Pundit
from random import shuffle
%>
<%inherit file="html.mako" />
<%
pundit = Pundit()
red = ladder.players[game.redPlayer]
blue = ladder.players[game.bluePlayer]
redFacts = pundit.getAllForGame(red, game, blue)
blueFacts = pundit.getAllForGame(blue, game, red)
facts = redFacts + blueFacts
shuffle(facts)
%>
${self.blocks.render("game", game=game, base=self.attr.base)}
<div class="recent-game container-fluid">
  <div class="row achievements">
    <div class="col-md-4">
    % for ach in game.redAchievements:
      ${self.blocks.render("achievement", ach=ach)}
    % endfor
    </div>
    <div class="col-md-4">
      ${self.blocks.render("punditry", facts=facts)}
    </div>
    <div class="col-md-4">
    % for ach in game.blueAchievements:
      ${self.blocks.render("achievement", ach=ach)}
    % endfor
    </div>
  </div>
</div>
<p><a href="json">This game as JSON</a></p>
% if not game.isDeleted():
<a href="delete" class="btn btn-danger pull-right"><span class="glyphicon glyphicon-lock"></span> Delete game</a>
% endif
