<%page args="ladder, monthStart, monthEnd"/>
<%!
from datetime import date
from tntfl.ladder import TableFootballLadder
%>
<%
epoch = date.fromtimestamp(0)
start = (monthStart - epoch).total_seconds()
end = (monthEnd - epoch).total_seconds()
l = TableFootballLadder("ladder.txt", timeRange=(start, end))
players = [p for p in l.getPlayers() if l.isPlayerActive(p)]
%>

<div>
  <a href="#" onClick='updateLadderTo([${(monthStart - epoch).total_seconds()}, ${(monthEnd - epoch).total_seconds()}])'>
    ${monthStart.month}${players[0].name}
  </a>
</div>
