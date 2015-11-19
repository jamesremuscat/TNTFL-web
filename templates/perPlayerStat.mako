<%page args="base, player, stat"/>
<%
goalRatio = (float(stat.goalsFor)/stat.goalsAgainst) if stat.goalsAgainst > 0 else 0
%>
<tr>
<td class="ladder-name"><a href="${base}player/${stat.opponent}">${stat.opponent}</a></td>
<td><a href="${base}headtohead/${player.name}/${stat.opponent}/" title="Head to Head"><span class="glyphicon glyphicon-transfer"></span></a></td>
<td class="ladder-stat">${stat.games}</td>
<td class="ladder-stat">${stat.wins}</td>
<td class="ladder-stat">${stat.draws}</td>
<td class="ladder-stat">${stat.losses}</td>
<td class="ladder-stat">${stat.goalsFor}</td>
<td class="ladder-stat">${stat.goalsAgainst}</td>
<td class="ladder-stat">${"{:.3f}".format(goalRatio)}</td>
<td class="ladder-stat ladder-skill">${"{:+.3f}".format(stat.skillChange)}</td>
</tr>