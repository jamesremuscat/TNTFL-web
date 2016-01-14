<%page args="sortCol=10, sortOrder=1, showInactive=0"/>
<%!
import re
from datetime import datetime
from tntfl.player import Player
from tntfl.ladder import TableFootballLadder
import tntfl.templateUtils as utils

def rankPlayers(ladder):
    ranked = []
    rank = 1
    for player in ladder.getPlayers():
        if ladder.isPlayerActive(player):
            ranked.append([rank, player])
            rank += 1
        else:
            ranked.append([-1, player])
    return ranked

def idsafe(text):
  return re.sub("[^A-Za-z0-9\-_\:\.]", "_", text)

def getTrend(player):
    trend = []
    size = player.skillBuffer.size()
    for i in range(0, size):
        trend.append([i, player.skillBuffer.getSkill(i)])
    if len(trend) > 0:
      trendColour = "#0000FF" if trend[0][1] < trend[size - 1][1] else "#FF0000";
    else:
      trendColour = "#000000"
    return {'trend':trend, 'colour':trendColour}
%>

<%def name="ladderEntry(player, rank, totalActivePlayers)">
    <%
    trend = getTrend(player)

    theDate = datetime.now() if ladder._ladderTime['now'] else datetime.fromtimestamp(ladder._ladderTime['range'][1])
    daysAgo = (theDate - player.games[-1].timeAsDatetime()).days
    daysToGo = TableFootballLadder.DAYS_INACTIVE - daysAgo
    nearlyInactive = daysToGo <= 14 and rank != -1
    ladderRowCSS = "inactive" if rank == -1 else "nearly-inactive" if nearlyInactive else "" if rank <= 5 else ""
    ladderRowTitle = ("Player will become inactive in %s day%s" % (daysToGo, "s" if daysToGo > 0 else "")) if nearlyInactive else ""
    ladderPositionCSS = utils.getRankCSS(rank, totalActivePlayers)

    draws = len(player.games) - player.wins - player.losses
    goalRatio = (float(player.goalsFor) / player.goalsAgainst) if player.goalsAgainst > 0 else 0
    %>
  <tr class="${ladderRowCSS}" title="${ladderRowTitle}">
    <td class="${ladderPositionCSS}">${rank if rank != -1 else "-"}</td>
    <td class="ladder-name"><a href="${base}player/${player.name | u}/">${player.name}</a></td>
    <td class="ladder-stat">${"{:d}".format(len(player.games))}</td>
    <td class="ladder-stat">${"{:d}".format(player.wins)}</td>
    <td class="ladder-stat">${"{:d}".format(draws)}</td>
    <td class="ladder-stat">${"{:d}".format(player.losses)}</td>
    <td class="ladder-stat">${"{:d}".format(player.goalsFor)}</td>
    <td class="ladder-stat">${"{:d}".format(player.goalsAgainst)}</td>
    <td class="ladder-stat">${"{:.3f}".format(goalRatio)}</td>
    <td class="ladder-stat">${"{:.3f}".format(player.overrated())}</td>
    <td class="ladder-stat ladder-skill">${"{:.3f}".format(player.elo)}</td>
    <td class="ladder-stat ladder-trend">
      <div id="${player.name | idsafe}_trend" class="ladder-trend"></div>
      <script type="text/javascript">
        plotPlayerSkillTrend("#${player.name | idsafe}_trend", [${trend['trend']}], ['${trend["colour"]}']);
      </script>
    </td>
  </tr>
</%def>

<%
ranked = rankPlayers(ladder)
totalActivePlayers = len([p for p in ladder.players.values() if ladder.isPlayerActive(p)])
%>
<%namespace name="blocks" file="blocks.mako" />
  <table class="table table-hover ladder" id="ladder">
    <thead>
      <tr>
        <th>Pos</th>
        <th>Player</th>
        <th>Games</th>
        <th>Wins</th>
        <th>Draws</th>
        <th>Losses</th>
        <th>For</th>
        <th>Against</th>
        <th>Goal ratio</th>
        <th>Overrated</th>
        <th>Skill</th>
        <th>Trend</th>
      </tr>
    </thead>
    <tbody>
% for player in ranked:
    ${ladderEntry(player[1], player[0], totalActivePlayers)}
% endfor
    </tbody>
  </table>
  