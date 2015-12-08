<%! title = "" %>
<%inherit file="html.mako" />
<div class="container-fluid">

% if timeRange != None:

  <div id="rangeSlider"></div>
  <script>
    initHistorySlider(
      "#rangeSlider",
      ${timeRange[0]},
      ${timeRange[1]},
      function (data) {
        $("#ladderHolder").empty();
        var spinner = new Spinner().spin();
        $("#ladderHolder").append(spinner.el);
        var dates = "?gamesFrom=" + data.from + "&gamesTo=" + data.to;
        window.history.pushState("object or string", "Title", dates);
        //window.location.href = "." + dates;
        $("#ladderHolder").load("ladder.cgi" + dates);
      }
    );
  </script>

% endif

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
          var spinner = new Spinner().spin();
          $("#ladderHolder").append(spinner.el);
          var dates = "";
          %if timeRange != None:
          dates = "?gamesFrom=" + ${timeRange[0]} + "&gamesTo=" + ${timeRange[1]};
          %endif
          $("#ladderHolder").load("ladder.cgi" + dates);
          var spinner2 = new Spinner().spin();
          $("#recentHolder").append(spinner2.el);
          $("#recentHolder").load("recent.cgi");
          setInterval(function() {reloadLadder();}, 600000);
          setInterval(function() {$("#recentHolder").load("recent.cgi")}, 600000);
        </script>
      </div>
    </div>
  </div>
</div>
