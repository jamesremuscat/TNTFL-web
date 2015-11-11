<%!
title = "Head to Head | "
base = "../../../"
from tntfl.game import Game
%>
<%inherit file="html.mako" />
<%
self.attr.base = "../../" if depth == 1 else "../../../" if depth == 2 else "../"
%>

<div class="container-fluid">
  <div class="row">
    <div class="col-md-12">
      <div class="panel panel-default">
        <div class="panel-heading">
          <h1 class="panel-title">Head to Head</h1>
        </div>
        <div class="panel-body container-fluid">
%if player1 and player2:
<%
  sharedGames = sorted([g for g in player1.games if g.redPlayer == player2.name or g.bluePlayer == player2.name], key=lambda g:g.time, reverse=True)
  swingToPlayer1 = 0
  player1wins = 0
  draws = 0
  player1goals = 0
  player2goals = 0
  player1doughnuts = 0
  player2doughnuts = 0

  histogramData = {'player1': {}, 'player2': {}}

  for i in range(11):
      histogramData['player1'][i] = 0
      histogramData['player2'][i] = 0

  for game in sharedGames:
      if game.redPlayer == player1.name:
          swingToPlayer1 -= game.skillChangeToBlue
          player1goals += game.redScore
          player2goals += game.blueScore
          histogramData['player1'][game.redScore] += 1
          histogramData['player2'][game.blueScore] += 1
          if game.redScore > game.blueScore:
              player1wins += 1
          if game.redScore == 10 and game.blueScore == 0:
              player1doughnuts += 1
          if game.redScore == 0 and game.blueScore == 10:
              player2doughnuts += 1
      elif game.bluePlayer == player1.name:
          swingToPlayer1 += game.skillChangeToBlue
          player1goals += game.blueScore
          player2goals += game.redScore
          histogramData['player1'][game.blueScore] += 1
          histogramData['player2'][game.redScore] += 1
          if game.redScore < game.blueScore:
              player1wins += 1
          if game.redScore == 0 and game.blueScore == 10:
              player1doughnuts += 1
          if game.redScore == 10 and game.blueScore == 0:
              player2doughnuts += 1
      if game.redScore == game.blueScore:
          draws += 1
player2wins = len(sharedGames) - draws - player1wins
%>
          <div class="row">
            <div class="col-md-4">
            ${self.blocks.render("headtoheadplayer", base=self.attr.base, player=player1, colour="red")}
              <div class="panel panel-default">
                <div class="panel-heading">
                  <h2 class="panel-title">Recent Encounters</h2>
                </div>
                <div class="panel-body">
        %for game in sharedGames[0:5]:
            ${self.blocks.render("game", game=game, base=self.attr.base)}
        %endfor
                </div>
              </div>
            </div>
            <div class="col-md-4">
              <div class="panel panel-default">
                <div class="panel-heading">
                  <h2 class="panel-title">Statistics</h2>
                </div>
                <div class="panel-body">
                  <p>Matches played: ${len(sharedGames)} (${draws} draws)</p>
                  <table class="table headtohead">
                    <tr>
                      <th>${player1.name}</th>
                      <td></td>
                      <th>${player2.name}</th>
                    </tr>
                    <tr>
       %if swingToPlayer1 >= 0:
                      <td class="red-player">${"{:.3f}".format(swingToPlayer1)}</td>
                      <th>Points Swing</th>
                      <td></td>
       %else:
                      <td></td>
                      <th>Points Swing</th>
                      <td class="blue-player">${"{:.3f}".format(-swingToPlayer1)}</td>
       %endif
                    </tr>
                    <tr>
                      <td ${"class=\"red-player\"" if player1wins >= player2wins else ""}>${player1wins}</td>
                      <th>Wins</small></th>
                      <td ${"class=\"blue-player\"" if player2wins >= player1wins else ""}>${player2wins}</td>
                    </tr>
                    <tr>
                      <td ${"class=\"red-player\"" if player1doughnuts >= player2doughnuts else ""}>${player1doughnuts}</td>
                      <th>10-0 Wins</th>
                      <td ${"class=\"blue-player\"" if player2doughnuts >= player1doughnuts else ""}>${player2doughnuts}</td>
                    </tr>
                    <tr>
                      <td ${"class=\"red-player\"" if player1goals >= player2goals else ""}>${player1goals}</td>
                      <th>Goals</th>
                      <td ${"class=\"blue-player\"" if player2goals >= player1goals else ""}>${player2goals}</td>
                    </tr>
       <% predict = 10 / (1 + 10 ** ((player2.elo - player1.elo) / 180)) %>
                    <tr>
                      <td class="red-player">${"{:.0f}".format(predict)}</td>
                      <th>Predicted Result</th>
                      <td class="blue-player">${"{:.0f}".format(10 - predict)}</td>
                    </tr>
                  </table>
                </div>
              </div>
            </div>
            <div class="col-md-4">
            ${self.blocks.render("headtoheadplayer", base=self.attr.base, player=player2, colour="blue")}
              <div class="panel panel-default">
                <div class="panel-heading">
                  <h2 class="panel-title">Goal Distribution</h2>
                </div>
                <div class="panel-body">
                  <div id="histogram">
                  </div>
                  <script type="text/javascript">
<%
player1Histogram = []
player2Histogram = []
for goals, tally in histogramData['player1'].iteritems():
  player1Histogram.append([goals, tally])
for goals, tally in histogramData['player2'].iteritems():
  player2Histogram.append([goals, tally * -1])
%>
          $(function() {
            $.plot("#histogram", [ ${player1Histogram}, ${player2Histogram} ], {'legend' : {show: false}, 'xaxis': {'ticks': 10}, grid: {hoverable: true}, colors: ['#FF0000', '#0000FF'], 'series' : {'bars' : {'show': true, 'align': 'center'}}});
          });
                  </script>
                </div>
              </div>
            </div>
          </div>
%else:
<p>Choose two players to view head-to-head information!</p>
%endif
        </div>
      </div>
    </div>
  </div>
</div>
