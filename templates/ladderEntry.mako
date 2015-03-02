      <tr>
      <td class="ladder-position ${"ladder-first" if index is 0 else "" }">${index + 1}</td>
      <td class="ladder-name">${player.name}</td>
      <td class="ladder-stat">${"{:d}".format(player.goalsFor)}</td>
      <td class="ladder-stat">${"{:d}".format(player.goalsAgainst)}</td>
      <td class="ladder-stat">${"{:d}".format(player.games)}</td>
      <td class="ladder-stat">${"{:.3f}".format(float(player.goalsFor) / player.goalsAgainst)}</td>
      <td class="ladder-stat">${"{:.3f}".format(player.overrated())}</td>
      <td class="ladder-stat ladder-skill">${"{:.3f}".format(player.elo)}</td>
      </tr>