<%! title = "Table Football Ladder 3.0" %>
<%inherit file="html.mako" />
<%
  recentGames = ladder.games[-10:]
  recentGames.reverse()
%>

<div class="container-fluid">
<div class="row">
  <div class="col-md-8">
    <div class="panel panel-default">
      <div class="panel-body" id="ladderHolder">
        ${self.blocks.render("ladder", base=self.attr.base)}
      </div>
      <script type="text/javascript">
        setInterval(function() {$("#ladderHolder").load("ladder.cgi")}, 60000);
      </script>
    </div>
  </div>
  <div class="col-md-4">
    <div class="panel panel-default">
      <div class="panel-heading">
        <h2 class="panel-title">Recent Games</h2>
      </div>
      <div class="panel-body">
% for game in recentGames:
    ${self.blocks.render("recentGame", game=game, base=self.attr.base)}
% endfor
      </div>
    </div>
  </div>
</div>
