<%page args="sortCol=10, sortOrder=1, showInactive=0"/>
<%!
from datetime import datetime

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
%>
<%
ranked = rankPlayers(ladder)
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
${blocks.render("ladderEntry", player=player[1], rank=player[0], base=base)}
% endfor
    </tbody>
  </table>
  