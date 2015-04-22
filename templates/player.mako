<%! title = "Table Football Ladder 3.0" %>
<%! base = "../../" %>
<%! from tntfl.ladder import Game %>
<%inherit file="html.mako" />
<%

from tntfl.ladder import PerPlayerStat

pps = {}

winStreak = {
  "from": 0,
  "to": 0,
  "count": 0
}

loseStreak = {
  "from": 0,
  "to": 0,
  "count": 0
}

currentWinStreak = {
  "from": 0,
  "to": 0,
  "count": 0
}

currentLoseStreak = {
  "from": 0,
  "to": 0,
  "count": 0
}

for game in player.games:
    if game.redPlayer == player.name:
        if game.redScore > game.blueScore:
          currentWinStreak['from'] = game.time if currentWinStreak['from'] == 0 else currentWinStreak['from']
          currentWinStreak['to'] = game.time
          currentWinStreak['count'] += 1
        else:
          if currentWinStreak['count'] >= winStreak['count']:
            winStreak['from'] = currentWinStreak['from']
            winStreak['to'] = currentWinStreak['to']
            winStreak['count'] = currentWinStreak['count']
          currentWinStreak = {"from": 0, "to": 0, "count": 0}
        if game.redScore < game.blueScore:
          currentLoseStreak['from'] = game.time if currentLoseStreak['from'] == 0 else currentLoseStreak['from']
          currentLoseStreak['to'] = game.time
          currentLoseStreak['count'] += 1
        else:
          if currentLoseStreak['count'] >= loseStreak['count']:
            loseStreak['from'] = currentLoseStreak['from']
            loseStreak['to'] = currentLoseStreak['to']
            loseStreak['count'] = currentLoseStreak['count']
          currentLoseStreak = {"from": 0, "to": 0, "count": 0}
          
        if game.bluePlayer not in pps:
            pps[game.bluePlayer] = PerPlayerStat(game.bluePlayer)
        pps[game.bluePlayer].append(game.redScore, game.blueScore, -game.skillChangeToBlue)
    elif game.bluePlayer == player.name:
        if game.blueScore > game.redScore:
          currentWinStreak['from'] = game.time if currentWinStreak['from'] == 0 else currentWinStreak['from']
          currentWinStreak['to'] = game.time
          currentWinStreak['count'] += 1
        else:
          if currentWinStreak['count'] >= winStreak['count']:
            winStreak['from'] = currentWinStreak['from']
            winStreak['to'] = currentWinStreak['to']
            winStreak['count'] = currentWinStreak['count']
          currentStreak = {"from": 0, "to": 0, "count": 0}
        if game.blueScore < game.redScore:
          currentLoseStreak['from'] = game.time if currentLoseStreak['from'] == 0 else currentLoseStreak['from']
          currentLoseStreak['to'] = game.time
          currentLoseStreak['count'] += 1
        else:
          if currentLoseStreak['count'] >= loseStreak['count']:
            loseStreak['from'] = currentLoseStreak['from']
            loseStreak['to'] = currentLoseStreak['to']
            loseStreak['count'] = currentLoseStreak['count']
          currentLoseStreak = {"from": 0, "to": 0, "count": 0}
        if game.redPlayer not in pps:
            pps[game.redPlayer] = PerPlayerStat(game.redPlayer)
        pps[game.redPlayer].append(game.blueScore, game.redScore, game.skillChangeToBlue)

if currentWinStreak['count'] > 0:
  currentStreak = currentWinStreak
  currentStreakType = "wins"
elif currentLoseStreak['count'] > 0:
  currentStreak = currentLoseStreak
  currentStreakType = "losses"
else:
  currentStreakType = "(last game was a draw)"
%>
<div class="container-fluid">
  <div class="row">
    <div class="col-md-8">
      <div class="panel panel-default">
        <div class="panel-heading">
          <h1 class="panel-title">${player.name}</h1>
        </div>
        <div class="panel-body">
          <table class="player-stats">
            <tr><th>Skill</th><td class="ladder-skill">${"{:.3f}".format(player.elo)}</td><th>Current Ranking</th>
  <% rank = ladder.getPlayerRank(player.name) %>
            <td class="ladder-position ${"inactive" if rank == -1 else "ladder-first" if rank == 1 else ""}">${rank if rank != -1 else "-"}</td>
            <th>Overrated</th><td>${"{:.3f}".format(player.overrated())}</td></tr>
  <%
    redness = float(player.gamesAsRed) / len(player.games) if len(player.games) > 0 else 0
  %>
            <tr><th>Total games</th><td>${len(player.games)}</td><th>Games today</th><td>${player.gamesToday}</td><th>Side Preference</th><td class="side-preference" style="background-color: rgb(${int(round(redness * 255))}, 0, ${int(round((1 - redness) * 255))})">${"{:.2%}".format(redness if redness >= 0.5 else (1-redness))} ${"red" if redness >= 0.5 else "blue"}</td></tr>
            <tr><th>Wins</th><td>${player.wins}</td><th>Losses</th><td>${player.losses}</td><th>Draws</th><td>${len(player.games) - player.wins - player.losses}</td></tr>
            <tr><th>Goals for</th><td>${player.goalsFor}</td><th>Goals against</th><td>${player.goalsAgainst}</td><th>GD/game</th><td>${"{:.3f}".format(float(player.goalsFor) / player.goalsAgainst) if player.goalsAgainst > 0 else "0"}</td></tr>
            <tr>
              <th>Highest ever skill</th>
              <td>${"{:.3f}".format(player.highestSkill['skill'])}</td>
    % if player.highestSkill['time'] > 0:
              <td>at <a href="${self.attr.base}game/${player.highestSkill['time']}/">${Game.formatTime(player.highestSkill['time'])}</a></td>
    % else:
              <td>before first game</td>
    % endif
              <th>Lowest ever skill</th>
              <td>${"{:.3f}".format(player.lowestSkill['skill'])}</td>
    % if player.lowestSkill['time'] > 0:
              <td>at <a href="${self.attr.base}game/${player.lowestSkill['time']}/">${Game.formatTime(player.lowestSkill['time'])}</a></td>
    % else:
              <td>before first game</td>
    % endif
            </tr>
            <tr>
              <th>Longest Winning Streak</th>
              <td>${winStreak['count']}</td>
% if winStreak['count'] > 0:
              <td><a href="${self.attr.base}game/${winStreak['from']}/">${Game.formatTime(winStreak['from'])}</a> to <a href="${self.attr.base}game/${winStreak['to']}/">${Game.formatTime(winStreak['to'])}</a></td>
% else:
              <td />
% endif
              <th>Longest Losing Streak</th>
              <td>${loseStreak['count']}</td>
% if loseStreak['count'] > 0:
              <td><a href="${self.attr.base}game/${loseStreak['from']}/">${Game.formatTime(loseStreak['from'])}</a> to <a href="${self.attr.base}game/${loseStreak['to']}/">${Game.formatTime(loseStreak['to'])}</a></td>
% else:
              <td />
% endif
            </tr>
            <tr>
              <th>Current Streak</th>
              <td>${currentStreak['count']} ${currentStreakType}</td>
% if currentStreak['count'] > 0:
              <td><a href="${self.attr.base}game/${currentStreak['from']}/">${Game.formatTime(currentStreak['from'])}</a> to <a href="${self.attr.base}game/${currentStreak['to']}/">${Game.formatTime(currentStreak['to'])}</a></td>
% else:
              <td />
% endif
            </tr>
          </table>
        </div>
      </div>
      <div class="panel panel-default">
        <div class="panel-heading">
          <h2 class="panel-title">Skill Chart</h2>
        </div>
        <div class="panel-body">
          <div id="playerchart">&nbsp;</div>
  <%
  skill = 0
  skillHistory = []
  
  for game in player.games:
    if game.redPlayer == player.name:
      skill -= game.skillChangeToBlue
      skillHistory.append([game.time * 1000, skill])
    elif game.bluePlayer == player.name:
      skill += game.skillChangeToBlue
      skillHistory.append([game.time * 1000, skill])
  %>
          <script type="text/javascript">
            $(function() {
              $.plot("#playerchart", [ ${skillHistory} ], {'legend' : {show: false}, 'xaxis': {mode: 'time'}, grid: {hoverable: true}, colors: ['#0000FF']});
            });
            
            $("<div id='tooltip'></div>").css({
        position: "absolute",
        display: "none",
        border: "1px solid #fdd",
        padding: "2px",
        "background-color": "#fee",
        opacity: 0.80
      }).appendTo("body");
  
      $("#playerchart").bind("plothover", function (event, pos, item) {
  
          if (item) {
            var x = item.datapoint[0].toFixed(2),
              y = item.datapoint[1].toFixed(2);
  
            $("#tooltip").html(y)
              .css({top: item.pageY+5, left: item.pageX+5})
              .fadeIn(200);
          } else {
            $("#tooltip").hide();
          }
      });
          </script>
        </div>
      </div>
  
      <div class="panel panel-default">
        <div class="panel-heading">
          <h2 class="panel-title">Per-Player Stats</h2>
        </div>
        <div class="panel-body">
          <table class="table table-striped table-hover ladder" id="pps">
            <thead>
                <tr>
                  <th>Opponent</th>
                  <th></th>
                  <th>Games</th>
                  <th>Wins</th>
                  <th>Draws</th>
                  <th>Losses</th>
                  <th>Goals scored</th>
                  <th>Goals conceded</th>
                  <th>GD</th>
                  <th>Skill change</th>
                </tr>
            </thead>
            <tbody>
  % for stat in pps.values():
    ${self.blocks.render("perPlayerStat", stat=stat, player=player, base=self.attr.base)}
  % endfor          
            </tbody>
          </table>
          <script type="text/javascript">
          $("#pps").tablesorter({sortList:[[9,1]], 'headers': { 1: { 'sorter': false}}}); 
          </script>
        </div>
      </div>
      
    </div>
    <div class="col-md-4">
  % if len(player.games) > 0:
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
      ${self.blocks.render("game", game=game, base=self.attr.base)}
  % endfor
          <a class="pull-right" href="games/">See all games</a>
        </div>
      </div>
      <div class="panel panel-default">
        <div class="panel-heading">
          <h2 class="panel-title">Most Significant Game</h2>
        </div>
        <div class="panel-body">
      ${self.blocks.render("game", game=player.mostSignificantGame, base=self.attr.base)}
        </div>
      </div>
      <div class="panel panel-default">
        <div class="panel-heading">
          <h2 class="panel-title">First Ever Game</h2>
        </div>
        <div class="panel-body">
      ${self.blocks.render("game", game=player.games[0], base=self.attr.base)}
        </div>
      </div>
  % else:
      <p>This player has not played any games.</p>
  % endif
    </div>
  </div>
</div>