<%!
from datetime import date
from tntfl.ladder import TableFootballLadder
%>
<%
winners = []
epoch = date.fromtimestamp(0)
for i in range(1, 13):
    monthStart = date(2015, i, 1)
    monthEnd = date(2015, i + 1, 1) if i < 12 else date(2016, 1, 1)
    start = (monthStart - epoch).total_seconds()
    end = (monthEnd - epoch).total_seconds()
    l = TableFootballLadder("ladder.txt", timeRange=(start, end))
    players = [p for p in l.getPlayers() if l.isPlayerActive(p)]
    winners.append([[monthStart, monthEnd], players])

%>
<div class="container-fluid">
  %for winner in winners:
    <a href="#" onClick='updateLadderTo([${(winner[0][0] - epoch).total_seconds()}, ${(winner[0][1] - epoch).total_seconds()}])'>
      ${winner[0][0].month}${winner[1][0].name}
    </a>
    <br/>
  %endfor
</div>
