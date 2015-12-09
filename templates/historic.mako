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
          <h2 class="panel-title">Months</h2>
        </div>
        <div class="panel-body" id="monthsHolder">
          <a href="#" onClick='what()'>What</a>
        </div>
      </div>
    </div>
  </div>
  <script type="text/javascript">
    function what() {
      var fromDate = 1143754991;
      var toDate = 1356576477;
      var dates = "?gamesFrom=" + fromDate + "&gamesTo=" + toDate;
        window.history.pushState("object or string", "Title", dates);
        reloadLadder(dates);
        $("#rangeSlider").data("ionRangeSlider").update({from: fromDate, to: toDate});
    }

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
