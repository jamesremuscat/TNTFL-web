<%!
    title = ""
    base = "../"
%>
<%!
from datetime import date
%>
<%inherit file="html.mako" />

<%def name="monthlyRanking(monthStart, monthEnd)">
    <%
    epoch = date.fromtimestamp(0)
    start = (monthStart - epoch).total_seconds()
    end = (monthEnd - epoch).total_seconds()
    %>
  <div>
    <a href="#" onClick='updateLadderTo([${start}, ${end}], "${base}")'>
      ${monthStart.strftime('%B')}
    </a>
  </div>
</%def>

<%def name="monthlyRankings(year)">
  <div class="col-sm-3">
    <div class="panel panel-default">
      <div class="panel-heading">
        <h2>${year}</h2>
      </div>
      <div class="panel-body ">
        %for i in reversed(range(1, 13)):
          %if (year > 2016 or i >= 5) and (year < date.today().year or i <= date.today().month):
            ${monthlyRanking(date(year, i, 1), date(year, i + 1, 1) if i < 12 else date(year+1, 1, 1))}
          %endif
        %endfor
      </div>
    </div>
  </div>
</%def>

<div class="container-fluid">
  <div id="rangeSlider"></div>
  <div class="row">
    <div class="col-md-8">
      <div class="panel panel-default">
        <div class="panel-body" id="ladderHolder"></div>
      </div>
    </div>
    <div class="col-md-4">
      <div class="panel panel-default">
        <div class="panel-heading">
          <h2 class="panel-title">Monthly Rankings</h2>
        </div>
        <div class="panel-body">
          <div class="row">
            % for year in reversed(range(2016, date.today().year + 1)):
              % if loop.index % 4 == 0:
                </div><div class="row">
              % endif
              ${monthlyRankings(year)}
            % endfor
          </div>
        </div>
      </div>
    </div>
  </div>
  <script type="text/javascript">
    initHistorySlider(
      "#rangeSlider",
      ${timeRange[0]},
      ${timeRange[1]},
      "${base}"
    );

    var dates = "${'?gamesFrom=%d&gamesTo=%d' % (timeRange[0], timeRange[1])}";
    reloadLadder(dates, "${base}");
  </script>
</div>
