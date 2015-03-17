<tr>
<td class="ladder-name"><a href="${base}player/${stat.opponent}">${stat.opponent}</a></td>
<td><a href="${base}headtohead/${player.name}/${stat.opponent}/" title="Head to Head"><span class="glyphicon glyphicon-transfer"></span></a></td>
<td class="ladder-stat">${stat.games}</td>
<td class="ladder-stat">${stat.wins}</td>
<td class="ladder-stat">${stat.draws}</td>
<td class="ladder-stat">${stat.losses}</td>
<td class="ladder-stat">${stat.goalsFor}</td>
<td class="ladder-stat">${stat.goalsAgainst}</td>
<td class="ladder-stat">${stat.goalsFor - stat.goalsAgainst}</td>
<td class="ladder-stat ladder-skill">${"{:+.3f}".format(stat.skillChange)}</td>
</tr>