<%!
title = ""
base = "../../../"
from tntfl.game import Game
%>
<%inherit file="html.mako" />
<div class="container-fluid">
  <div class="row">
    <div class="col-md-8">
      <div class="panel panel-default">
        <div class="panel-heading">
          <h1 class="panel-title">${player.name}'s games</h1>
        </div>
        <div class="panel-body">
          ${self.blocks.render("gameList", games=reversed(player.games), base=self.attr.base)}
        </div>
      </div>
    </div>
  </div>
</div>
