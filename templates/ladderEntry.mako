<%
import re

def idsafe(text):
  return re.sub("[^A-Za-z0-9\-_\:\.]", "_", text)

trend = []
size = player.skillBuffer.size()
for i in range(0, size):
    trend.append([i, player.skillBuffer.getSkill(i)])

trendColour = "#0000FF" if trend[0][1] < trend[size - 1][1] else "#FF0000";
%>
% if index == -1:
<tr class="inactive">
      <td class="ladder-position inactive">-</td>
% else:
<tr>
      <td class="ladder-position ${"ladder-first" if index is 0 else "" }">${index + 1}</td>
% endif
      <td class="ladder-name">${player.name}</td>
      <td class="ladder-stat">${"{:d}".format(player.goalsFor)}</td>
      <td class="ladder-stat">${"{:d}".format(player.goalsAgainst)}</td>
      <td class="ladder-stat">${"{:d}".format(player.games)}</td>
      <td class="ladder-stat">${"{:d}".format(player.wins)}</td>
      <td class="ladder-stat">${"{:d}".format(player.losses)}</td>
      <td class="ladder-stat">${"{:.3f}".format(float(player.goalsFor) / player.goalsAgainst)}</td>
      <td class="ladder-stat">${"{:.3f}".format(player.overrated())}</td>
      <td class="ladder-stat ladder-skill">${"{:.3f}".format(player.elo)}</td>
      <td class="ladder-stat ladder-trend"><div id="${player.name | idsafe}_trend" class="ladder-trend">&nbsp;</div></td>
      <script type="text/javascript">
        $(function() {
          $.plot("#${player.name | idsafe}_trend", [ ${trend} ], {'legend' : {show: false}, 'xaxis': {show: false}, 'yaxis': {show: false}, 'grid': {'show': false}, 'series': {'shadowSize': 0}, 'colors': ['${trendColour}']});
        });

  
      </script>
      </tr>