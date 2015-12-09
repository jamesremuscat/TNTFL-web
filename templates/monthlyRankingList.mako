<%!
from datetime import date
from tntfl.ladder import TableFootballLadder
%>
<%namespace name="blocks" file="blocks.mako" />

<div class="container-fluid">
  %for i in range(1, 13):
    ${blocks.render("monthlyRanking", monthStart=date(2015, i, 1), monthEnd=date(2015, i + 1, 1) if i < 12 else date(2016, 1, 1))}
  %endfor
</div>
