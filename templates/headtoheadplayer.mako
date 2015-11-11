<%page args="base, player, colour"/>
<%!
from tntfl.game import Game
%>
<%
skillBounds = player.getSkillBounds()
%>
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
          <td>${"{:.3f}".format(skillBounds['highest']['skill'])}<br />
% if skillBounds['highest']['time'] > 0:
          at <a href="${base}game/${skillBounds['highest']['time']}/">${Game.formatTime(skillBounds['highest']['time'])}</a></td>
% else:
          before first game</td>
% endif
          <th>Lowest ever skill</th>
          <td>${"{:.3f}".format(skillBounds['lowest']['skill'])}<br />
% if skillBounds['lowest']['time'] > 0:
          at <a href="${base}game/${skillBounds['lowest']['time']}/">${Game.formatTime(skillBounds['lowest']['time'])}</a></td>
% else:
          before first game</td>
% endif
          </tr>
                  </table>
                  </div>
              </div>
