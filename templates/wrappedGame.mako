<%!
title = ""
base = "../../"
from tntfl.pundit import Pundit
from random import shuffle

def getPunditry(pundit, game, ladder):
    red = ladder.getPlayer(game.redPlayer)
    blue = ladder.getPlayer(game.bluePlayer)
    redFacts = pundit.getAllForGame(red, game, blue)
    blueFacts = pundit.getAllForGame(blue, game, red)
    facts = redFacts + blueFacts
    shuffle(facts)
    return facts
%>
<%inherit file="html.mako" />

<%def name="achievement(ach)">
  <div class="panel panel-default panel-achievement">
    <div class="panel-heading">
      <h3 class="panel-title">${ach.name}</h3>
    </div>
    <div class="panel-body achievement-${ach.__name__}">
      ${ach.description}
    </div>
  </div>
</%def>

<%def name="punditry(facts)">
  <div class="panel panel-default ">
    <div class="panel-heading">
      <h3 class="panel-title">Punditry</h3>
    </div>
    <div class="panel-body">
      % for fact in facts:
        ${fact}
        <br/>
      % endfor
    </div>
  </div>
</%def>

<%
pundit = Pundit()
facts = getPunditry(pundit, game, ladder)
totalActivePlayers = len(ladder.getActivePlayers(game.time-1))
%>

## <div class="panel panel-default">
##   <div class="panel-body">
##     ${self.blocks.render("game", game=game, base=self.attr.base, punditryAvailable=len(facts), totalActivePlayers=totalActivePlayers)}
##     <div class="recent-game container-fluid">
##       <div class="row achievements">
##         <div class="col-md-4">
##         % for ach in game.redAchievements:
##           ${achievement(ach)}
##         % endfor
##         </div>
##         <div class="col-md-4">
##           ${punditry(facts) if len(facts) > 0 else ""}
##         </div>
##         <div class="col-md-4">
##         % for ach in game.blueAchievements:
##           ${achievement(ach)}
##         % endfor
##         </div>
##       </div>
##     </div>
##   </div>
## </div>
## <p><a href="json">This game as JSON</a></p>
## % if not game.isDeleted():
## <a href="delete" class="btn btn-danger pull-right"><span class="glyphicon glyphicon-lock"></span> Delete game</a>
## % endif

<div class="game table-responsive container-fluid">
  <table class="table no-table-boder" style="margin-top: 20px;">
    <tbody>
      ${self.blocks.render("game", game=game, base=self.attr.base, punditryAvailable=len(facts), totalActivePlayers=totalActivePlayers)}
    </tbody>
  </table>
  <div class="recent-game container-fluid">
      <div class="row achievements">
        <div class="col-md-4">
        % for ach in game.redAchievements:
          ${achievement(ach)}
        % endfor
        </div>
        <div class="col-md-4 punditry">
          ${punditry(facts) if len(facts) > 0 else ""}
        </div>
        <div class="col-md-4">
        % for ach in game.blueAchievements:
          ${achievement(ach)}
        % endfor
        </div>
      </div>
    </div>

<p><a href="json">This game as JSON</a></p>
% if not game.isDeleted():
  <a href="delete" class="btn btn-danger pull-right"><span class="glyphicon glyphicon-lock"></span> Delete game</a>
% endif
</div>