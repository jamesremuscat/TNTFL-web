<%! title = "Table Football Ladder 3.0" %>
<%inherit file="html.mako" />
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
          <th>Overrated</th>
          <th>Skill</th>
        </tr>
% for player in sortedLadder:
    ${self.blocks.render("ladderEntry", player=player, index=loop.index)}
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
    ${self.blocks.render("recentGame", game=game)}
% endfor
      </div>
    </div>
  </div>
</div>
