<%! title = "Table Football Ladder 3.0" %>
<%! base = "../" %>
<%inherit file="html.mako" />
<div class="container-fluid">
<div class="row">
  <div class="col-md-8">
    <div class="panel panel-default">
      <div class="panel-heading">
        <h1 class="panel-title">${player.name}</h1>
      </div>
      <div class="panel-body">
        <table class="player-stats">
          <tr><th>Skill</th><td class="ladder-skill">${"{:.3f}".format(player.elo)}</td><th>Current Ranking</th><td class="ladder-position">${ladder.getPlayerRank(player.name)}</td><th>Overrated</th><td>${"{:.3f}".format(player.overrated())}</td></tr>
          <tr><th>Total games</th><td>${len(player.games)}</td></tr>
          <tr><th>Wins</th><td>${player.wins}</td><th>Losses</th><td>${player.losses}</td><th>Draws</th><td>${len(player.games) - player.wins - player.losses}</td></tr>
          <tr><th>Goals for</th><td>${player.goalsFor}</td><th>Goals against</th><td>${player.goalsAgainst}</td><th>GD/game</th><td>${"{:.3f}".format(float(player.goalsFor) / player.goalsAgainst)}</td></tr>
        </table>
      </div>
    </div>
    <div class="panel panel-default">
      <div class="panel-heading">
        <h2 class="panel-title">Per-Player Stats</h2>
      </div>
      <div class="panel-body">
        Soon&trade;
      </div>
    </div>
    <div class="panel panel-default">
      <div class="panel-heading">
        <h2 class="panel-title">Skill Chart</h2>
      </div>
      <div class="panel-body">
        Soon&trade;
      </div>
    </div>
  </div>
  <div class="col-md-4">
    <div class="panel panel-default">
      <div class="panel-heading">
        <h2 class="panel-title">Recent Games</h2>
      </div>
      <div class="panel-body">
<%
recentGames = player.games[-5:]
recentGames.reverse()
%>
% for game in recentGames:
    ${self.blocks.render("recentGame", game=game, base=self.attr.base)}
% endfor
      </div>
    </div>
    <div class="panel panel-default">
      <div class="panel-heading">
        <h2 class="panel-title">First Ever Game</h2>
      </div>
      <div class="panel-body">
    ${self.blocks.render("recentGame", game=player.games[0], base=self.attr.base)}
      </div>
    </div>
  </div>
</div>