<%page args="year"/>
<%!
from datetime import date
%>
<%namespace name="blocks" file="blocks.mako" />

<%def name="monthlyRanking(monthStart, monthEnd)">
    <%
    epoch = date.fromtimestamp(0)
    start = (monthStart - epoch).total_seconds()
    end = (monthEnd - epoch).total_seconds()
    %>
  <div>
    <a href="#" onClick='updateLadderTo([${start}, ${end}])'>
      ${monthStart.strftime('%B')}
    </a>
  </div>
</%def>

<div class="col-sm-3">
  <div class="panel panel-default">
    <div class="panel-heading">
      <h2>${year}</h2>
    </div>
    <div class="panel-body ">
      %for i in reversed(range(1, 13)):
        %if (year > 2005 or i >= 7) and (year < date.today().year or i <= date.today().month):
          ${monthlyRanking(date(year, i, 1), date(year, i + 1, 1) if i < 12 else date(year+1, 1, 1))}
        %endif
      %endfor
    </div>
  </div>
</div>
