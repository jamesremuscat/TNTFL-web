<%! title = "Table Football Ladder 3.0" %>
<%inherit file="html.mako" />
<%
  sortedLadder = sorted([p for p in ladder.players.values()], key=lambda x: x.elo, reverse=True)
  recentGames = ladder.games[-10:]
  recentGames.reverse()
%>
<div class="container-fluid">
<p>Ladder has ${len(ladder.games)} games</p>
<div class="row">
  <div class="col-md-8">
    <div class="panel panel-default">
      <div class="panel-heading">
        <h2 class="panel-title">Table Football Ladder</h2>
      </div>
      <div class="panel-body">
        <table class="table table-striped table-hover ladder">
% for player in sortedLadder:
      <tr><td class="ladder-position">${loop.index + 1}</td><td>${player.name}</td><td>${"{:.3f}".format(player.elo)}</td></tr>
% endfor
        </table>
      </div>
    </div>
  </div>
  <div class="col-md-4">
    <div class="panel panel-default">
      <div class="panel-heading">
        <h2 class="panel-title">Recent Games</h2>
      </div>
      <div class="panel-body">
% for game in recentGames:
        <div class="recent-game container-fluid">
          <div class="row">
          <div class="col-md-4 red-player">${game.redPlayer}</div>
          <div class="col-md-4">${game.redScore} - ${game.blueScore}</div>
          <div class="col-md-4 blue-player">${game.bluePlayer}</div>
          </div>
          <div class="row">
            <div class="col-md-6">${game.time}</div>
            <div class="col-md-6">${game.skillChangeToBlue}</div>
          </div>
        </div>
% endfor
      </div>
    </div>
  </div>
</div>
