<%! title = "" %>
<%!
import tntfl.templateUtils as utils
from datetime import date, datetime, timedelta
import time
%>
<%
    start = datetime.fromtimestamp(0)
    end = datetime.fromtimestamp(time.time())
    if not ladder._ladderTime['now']:
        start = datetime.fromtimestamp(float(ladder._ladderTime['range'][0]))
        end = datetime.fromtimestamp(float(ladder._ladderTime['range'][1]))
    startStr = start.strftime("%Y-%m-%d")
    endStr = end.strftime("%Y-%m-%d")
%>
<%inherit file="html.mako" />
<div class="container-fluid">

% if not ladder._ladderTime['now']:
  <p>Using games between <input type="text" class="picker" id="startPicker"> and <input type="text" class="picker" id="endPicker"></p>
  <script>
  function changeDate() {
    var startDate = $("#startPicker").datepicker("getDate").getTime() / 1000;
    var endDate = $("#endPicker").datepicker("getDate").getTime() / 1000;
    window.location.href = ".?from=" + startDate + "&to=" + endDate;
  }

  $(function() {
    $("#startPicker").datepicker({
      dateFormat:"yy-mm-dd",
      onSelect:function(dateText) {
        changeDate();
      }
    });
    $("#endPicker").datepicker({
      dateFormat:"yy-mm-dd",
      onSelect:function(dateText) {
        changeDate();
      }
    });
    $("#startPicker").datepicker("setDate", "${startStr}");
    $("#endPicker").datepicker("setDate", "${endStr}");
  });
  </script>
% endif

  <div class="row">
    <div class="col-md-8">
      <div class="panel panel-default">
        <div class="panel-body" id="ladderHolder">
          ${self.blocks.render("ladder", base=self.attr.base)}
        </div>
        <script type="text/javascript">
          setInterval(
            function() {
            	sortOpts = getSortOptions("#ladder th");
            	if ($("tr.inactive")[0].style.display == "table-row") {
            		showInactive = 1
            	}
            	else {
            		showInactive = 0
            	}
            	$("#ladderHolder").load("ladder.cgi?sortCol=" + sortOpts[0][0] + "&sortOrder="+sortOpts[0][1] + "&showInactive=" + showInactive)
          	},
            600000
          );
        </script>
      </div>
    </div>
    <div class="col-md-4">
      <div class="panel panel-default">
        <div class="panel-heading">
          <h2 class="panel-title">Recent Games</h2>
        </div>
        <div class="panel-body" id="recentHolder">
          ${self.blocks.render("recent", base=self.attr.base, games=ladder.games)}
        </div>
        <script type="text/javascript">
          setInterval(function() {$("#recentHolder").load("recent.cgi")}, 600000);
        </script>
      </div>
    </div>
  </div>
</div>
