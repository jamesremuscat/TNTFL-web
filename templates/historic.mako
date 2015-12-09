<%! title = "" %>
<%inherit file="html.mako" />
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
        <div class="panel-body" id="monthsHolder">
          ${self.blocks.render("monthlyRankingList", year=2015)}
        </div>
      </div>
    </div>
  </div>
  <script type="text/javascript">
    initHistorySlider(
      "#rangeSlider",
      ${timeRange[0]},
      ${timeRange[1]}
    );

    var dates = "${'?gamesFrom=%d&gamesTo=%d' % (timeRange[0], timeRange[1]) if timeRange is not None else ''}";
    reloadLadder(dates);
    setInterval(function() {reloadLadder("");}, 600000);


  </script>
</div>
