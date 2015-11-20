<%!
title = "Head to Head | "
base = "../../../"
from tntfl.game import Game
import tntfl.templateUtils as utils

def getNumWins(player, games):
    return len([g for g in games if (g.redPlayer == player.name and g.redScore > g.blueScore) or (g.bluePlayer == player.name and g.blueScore > g.redScore)])

def getNumGoals(player, games):
    return sum(g.redScore if g.redPlayer == player.name else g.blueScore for g in games)

def getSkillChange(player, games):
    return sum(g.skillChangeToBlue if g.bluePlayer == player.name else -g.skillChangeToBlue for g in games)

def getHistograms(player1, player2, sharedGames):
    histogramData = {'player1': {}, 'player2': {}}
    for i in range(11):
        histogramData['player1'][i] = 0
        histogramData['player2'][i] = 0
    for game in sharedGames:
        if game.redPlayer == player1.name:
            histogramData['player1'][game.redScore] += 1
            histogramData['player2'][game.blueScore] += 1
        elif game.bluePlayer == player1.name:
            histogramData['player1'][game.blueScore] += 1
            histogramData['player2'][game.redScore] += 1
    player1Histogram = []
    player2Histogram = []
    for goals, tally in histogramData['player1'].iteritems():
        player1Histogram.append([goals, tally])
    for goals, tally in histogramData['player2'].iteritems():
        player2Histogram.append([goals, tally * -1])
    return {'player1': player1Histogram, 'player2': player2Histogram}
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
    sharedGames = utils.getSharedGames(player1, player2)
    draws = len([g for g in sharedGames if g.redScore == g.blueScore])
    player1wins = getNumWins(player1, sharedGames)
    player2wins = len(sharedGames) - draws - player1wins
    player1goals = getNumGoals(player1, sharedGames)
    player2goals = getNumGoals(player2, sharedGames)
    player1yellowStripes = utils.getNumYellowStripes(player1, sharedGames)
    player2yellowStripes = utils.getNumYellowStripes(player2, sharedGames)
    swingToPlayer1 = getSkillChange(player1, sharedGames)
    histograms = getHistograms(player1, player2, sharedGames)
    predict = ladder.predict(player1, player2) * 10
%>
          <div class="row">
            <div class="col-md-4">
            ${self.blocks.render("headtoheadplayer", base=self.attr.base, player=player1, colour="red")}
              <div class="panel panel-default">
                <div class="panel-heading">
                  <h2 class="panel-title">Recent Encounters</h2>
                </div>
                <div class="panel-body">
                  ${self.blocks.render("recent", base=self.attr.base, games=sharedGames, limit=5)}
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
                      <td ${"class='red-player'" if player1wins >= player2wins else ""}>${player1wins}</td>
                      <th>Wins</small></th>
                      <td ${"class='blue-player'" if player2wins >= player1wins else ""}>${player2wins}</td>
                    </tr>
                    <tr>
                      <td ${"class='red-player'" if player1yellowStripes >= player2yellowStripes else ""}>${player1yellowStripes}</td>
                      <th>10-0 Wins</th>
                      <td ${"class='blue-player'" if player2yellowStripes >= player1yellowStripes else ""}>${player2yellowStripes}</td>
                    </tr>
                    <tr>
                      <td ${"class='red-player'" if player1goals >= player2goals else ""}>${player1goals}</td>
                      <th>Goals</th>
                      <td ${"class='blue-player'" if player2goals >= player1goals else ""}>${player2goals}</td>
                    </tr>
                    <tr>
                      <td class="red-player">${"{:.0f}".format(10 - predict)}</td>
                      <th>Predicted Result</th>
                      <td class="blue-player">${"{:.0f}".format(predict)}</td>
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
                  $(function() {
                    $.plot("#histogram", [ ${histograms['player1']}, ${histograms['player2']} ], {'legend' : {show: false}, 'xaxis': {'ticks': 10}, grid: {hoverable: true}, colors: ['#FF0000', '#0000FF'], 'series' : {'bars' : {'show': true, 'align': 'center'}}});
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
