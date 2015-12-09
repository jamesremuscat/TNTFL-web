<%page args="year"/>
<%!
from datetime import date
from tntfl.ladder import TableFootballLadder
%>
<%namespace name="blocks" file="blocks.mako" />

<div class="col-sm-3">
  <div class="panel panel-default">
    <div class="panel-heading">
        <h2>${year}</h2>
    </div>
    <div class="panel-body ">
      %for i in reversed(range(1, 13 if date.today().year < year else (date.today().month + 1))):
        ${blocks.render("monthlyRanking", monthStart=date(year, i, 1), monthEnd=date(year, i + 1, 1) if i < 12 else date(year+1, 1, 1))}
      %endfor
    </div>
  </div>
</div>
