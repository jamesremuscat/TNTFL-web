<%! title = "Table Football Ladder 3.0" %>
<%inherit file="html.mako" />
<%
  recentGames = ladder.games[-10:]
  recentGames.reverse()
%>

<div class="container-fluid">
<p>Ladder has ${len(ladder.games)} games</p>
<div class="row">
  <div class="col-md-8">
    <div class="panel panel-default">
      <div class="panel-body">
        ${self.blocks.render("ladder")}
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
