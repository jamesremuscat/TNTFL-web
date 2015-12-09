<%!
from datetime import date
from tntfl.ladder import TableFootballLadder
%>
<%namespace name="blocks" file="blocks.mako" />

<div class="container-fluid">
  <h2>2015</h2>
  %for i in reversed(range(1, 13)):
    ${blocks.render("monthlyRanking", monthStart=date(2015, i, 1), monthEnd=date(2015, i + 1, 1) if i < 12 else date(2016, 1, 1))}
  %endfor
</div>
