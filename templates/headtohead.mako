<%! title = "Head to Head | Table Football Ladder 3.0" 
base = "../../../"
from tntfl.ladder import Game %>
<%inherit file="html.mako" />
<%
self.attr.base = "../../" if depth == 1 else "../../../" if depth == 2 else "../"
%>
<%def name="playerPanel(player, colour)">
              <div class="panel panel-default headtohead">
                  <h1 class="${colour}-player panel-title">${player.name}</h1>
                  <div class="panel-body">
                  <% rank = ladder.getPlayerRank(player.name) %>
                  <table class="player-stats">
                    <tr>
                      <th>Rank</th><td class="ladder-position ${"inactive" if rank == -1 else "ladder-first" if rank == 1 else ""}">${rank if rank != -1 else "-"}</td>
                      <th>Skill</th><td class="ladder-skill">${"{:.3f}".format(player.elo)}</td>
                    </tr>
                              <tr>
          <th>Highest ever skill</th>
          <td>${"{:.3f}".format(player.highestSkill['skill'])}<br />
% if player.highestSkill['time'] > 0:
          at <a href="${self.attr.base}game/${player.highestSkill['time']}/">${Game.formatTime(player.highestSkill['time'])}</a></td>
% else:
          before first game</td>
% endif
          <th>Lowest ever skill</th>
          <td>${"{:.3f}".format(player.lowestSkill['skill'])}<br />
% if player.lowestSkill['time'] > 0:
          at <a href="${self.attr.base}game/${player.lowestSkill['time']}/">${Game.formatTime(player.lowestSkill['time'])}</a></td>
% else:
          before first game</td>
% endif
          </tr>
                  </table>
                  </div>
              </div>
</%def><div class="container-fluid">
  <div class="row">
    <div class="col-md-12">
      <div class="panel panel-default">
        <div class="panel-heading">
          <h1 class="panel-title">Head to Head</h1>
        </div>
        <div class="panel-body container-fluid">
          <div class="row">
            <div class="col-md-4">
%if player1:
${self.playerPanel(player1, "red")}
%endif
            </div>
            <div class="col-md-4">
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
  
  for game in sharedGames:
      if game.redPlayer == player1.name:
          swingToPlayer1 -= game.skillChangeToBlue
          player1goals += game.redScore
          player2goals += game.blueScore
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
%endif
            </div>
            <div class="col-md-4">
%if player2:
${self.playerPanel(player2, "blue")}
%endif
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</div>