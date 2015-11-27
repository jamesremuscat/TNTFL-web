<%page args="player, rank, base"/>
<%!
import re
from datetime import datetime
from tntfl.player import Player

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
<%
trend = getTrend(player)

daysAgo = (datetime.now() - player.games[-1].timeAsDatetime()).days
daysToGo = Player.DAYS_INACTIVE - daysAgo
nearlyInactive = daysToGo <= 14 and rank != -1
ladderRowCSS = "inactive" if rank == -1 else "nearly-inactive" if nearlyInactive else ""
ladderRowTitle = ("Player will become inactive in %s day%s" % (daysToGo, "s" if daysToGo > 0 else "")) if nearlyInactive else ""
ladderPositionCSS = "ladder-position" + (" inactive" if rank == -1 else " ladder-first" if rank == 1 else "")

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
      <td class="ladder-stat ladder-trend"><div id="${player.name | idsafe}_trend" class="ladder-trend">&nbsp;</div></td>
      <script type="text/javascript">
        plotPlayerSkillTrend("#${player.name | idsafe}_trend", [${trend['trend']}], ['${trend["colour"]}']);
      </script>
    </tr>
