<%! title = "Table Football Ladder 3.0" %>
<%inherit file="html.mako" />
<%
  recentGames = ladder.games[-10:]
  recentGames.reverse()
%>
<nav class="navbar navbar-default">
  <div class="container-fluid">
    <!-- Brand and toggle get grouped for better mobile display -->
    <div class="navbar-header">
      <h3 class="navbar-text">Table Football Ladder</h3>
    </div>

    <form class="navbar-form navbar-right game-entry" method="post" action="game/add">
      <div class="form-group">
        <input type="text" name="redPlayer" class="form-control red player" placeholder="Red">
        <input type="text" name="redScore" class="form-control red score" placeholder="0" maxlength="2"> - <input type="text" name="blueScore" class="form-control blue score" placeholder="0" maxlength="2">
        <input type="text" name="bluePlayer" class="form-control blue player" placeholder="Blue">
        <script type="text/javascript">
          $(".red.score").change(function() {
          	$(".blue.score").val(10 - $(".red.score").val());
          })
        </script>
      </div>
      <button type="submit" class="btn btn-default">Add game <span class="glyphicon glyphicon-triangle-right"></span></button>
    </form>
  </div><!-- /.container-fluid -->
</nav>
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
