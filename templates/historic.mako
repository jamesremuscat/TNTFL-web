<%! title = "" %>
<%inherit file="html.mako" />
<div class="container-fluid">
  <div id="rangeSlider"></div>
  <script>
    initHistorySlider(
      "#rangeSlider",
      ${timeRange[0]},
      ${timeRange[1]}
    );
  </script>
  <div class="row">
    <div class="col-md-8">
      <div class="panel panel-default">
        <div class="panel-body" id="ladderHolder">
        </div>
      </div>
    </div>
    <div class="col-md-4">
      <div class="panel panel-default">
        <div class="panel-heading">
          <h2 class="panel-title">Recent Games</h2>
        </div>
        <div class="panel-body" id="recentHolder">
        </div>
        <script type="text/javascript">
          var dates = "${'?gamesFrom=%d&gamesTo=%d' % (timeRange[0], timeRange[1]) if timeRange is not None else ''}";
          reloadLadder(dates);

          var spinner2 = new Spinner().spin();
          $("#recentHolder").append(spinner2.el);
          $("#recentHolder").load("recent.cgi");

          setInterval(function() {reloadLadder("");}, 600000);
          setInterval(function() {$("#recentHolder").load("recent.cgi")}, 600000);
        </script>
      </div>
    </div>
  </div>
</div>
