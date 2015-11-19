<%!
title = ""
base = "../../../"
from tntfl.game import Game
from tntfl.pundit import Pundit
import tntfl.templateUtils as utils
%>
<%inherit file="html.mako" />
<%
pundit = Pundit()
%>
<div class="container-fluid">
  <div class="row">
    <div class="col-md-8">
      <div class="panel panel-default">
        <div class="panel-heading">
          <h1 class="panel-title">${player.name}'s games</h1>
        </div>
        <div class="panel-body">
  % for game in reversed(player.games):
      ${self.blocks.render("game", game=game, base=self.attr.base, punditryAvailable=utils.punditryAvailable(pundit, game, ladder))}
  % endfor
        </div>
      </div>
    </div>
  </div>
</div>
