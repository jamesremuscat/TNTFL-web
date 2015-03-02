<%! title = "Table Football Ladder 3.0" %>
<%inherit file="html.mako" />
<%namespace name="blocks" file="blocks.mako"/>
<%
  sortedLadder = sorted([p for p in ladder.players.values() if p.isActive()], key=lambda x: x.elo, reverse=True)
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
        <tr>
          <th>Pos</th>
          <th>Player</th>
          <th>For</th>
          <th>Against</th>
          <th>Games</th>
          <th>GD</th>
          <th>Skill</th>
        </tr>
% for player in sortedLadder:
      <tr>
      <td class="ladder-position ${"ladder-first" if loop.index is 0 else "" }">${loop.index + 1}</td>
      <td class="ladder-name">${player.name}</td>
      <td class="ladder-stat">${"{:d}".format(player.goalsFor)}</td>
      <td class="ladder-stat">${"{:d}".format(player.goalsAgainst)}</td>
      <td class="ladder-stat">${"{:d}".format(player.games)}</td>
      <td class="ladder-stat">${"{:.3f}".format(float(player.goalsFor) / player.goalsAgainst)}</td>
      <td class="ladder-stat ladder-skill">${"{:.3f}".format(player.elo)}</td>
      </tr>
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
    ${blocks.render("recentGame", game=game)}
% endfor
      </div>
    </div>
  </div>
</div>
