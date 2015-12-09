<%page args="year"/>
<%!
from datetime import date
%>
<%namespace name="blocks" file="blocks.mako" />

<div class="col-sm-3">
  <div class="panel panel-default">
    <div class="panel-heading">
      <h2>${year}</h2>
    </div>
    <div class="panel-body ">
      %for i in reversed(range(1, 13)):
        %if (year > 2005 or i >= 7) and (date.today().year < year or i <= date.today().month):
          ${blocks.render("monthlyRanking", monthStart=date(year, i, 1), monthEnd=date(year, i + 1, 1) if i < 12 else date(year+1, 1, 1))}
        %endif
      %endfor
    </div>
  </div>
</div>
