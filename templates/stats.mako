<%! title = "Stats | Table Football Ladder 3.0" %>
<%! base = "../" %>
<%inherit file="html.mako" />
<% msgs = sorted(ladder.games, key=lambda x: abs(x.skillChangeToBlue), reverse=True) %>
<%
redGoals = 0
blueGoals = 0
for game in ladder.games:
    redGoals += game.redScore
    blueGoals += game.blueScore

activePlayers = 0
for player in ladder.players.values():
    if player.isActive():
      activePlayers += 1
%>
<div class="container-fluid">
  <div class="row">
    <div class="col-md-4">
      <div class="panel panel-default">
        <div class="panel-heading">
          <h2 class="panel-title">Stats</h2>
        </div>
        <div class="panel-body">
          <dl class="dl-horizontal">
            <dt>Total games</dt>
            <dd>${len(ladder.games)}</dd>
            <dt>Total goals by red</dt>
            <dd>${redGoals}</dd>
            <dt>Total goals by blue</dt>
            <dd>${blueGoals}</dd>
            <dt>Total players</dt>
            <dd>${len(ladder.players)}</dd>
            <dt>Active players</dt>
            <dd>${activePlayers} (${"{:.2%}".format(float(activePlayers) / len(ladder.players))})</dd>
          </dl>
        </div>
      </div>
    </div>
    <div class="col-md-4">
      <div class="panel panel-default">
        <div class="panel-heading">
          <h2 class="panel-title">Most Significant Games</h2>
        </div>
        <div class="panel-body">
% for game in msgs[0:5]:
    ${self.blocks.render("recentGame", game=game, base=self.attr.base)}
% endfor
        </div>
      </div>
    </div>
    <div class="col-md-4">
      <div class="panel panel-default">
        <div class="panel-heading">
          <h2 class="panel-title">Least Significant Games</h2>
        </div>
        <div class="panel-body">
% for game in msgs[-5:]:
    ${self.blocks.render("recentGame", game=game, base=self.attr.base)}
% endfor
        </div>
      </div>
    </div>
  </div>
</div>