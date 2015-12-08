
function plotPlayerSkillTrend(id, skill, colours) {
  $.plot(
    id,
    skill,
    {
      'legend' : {show: false},
      'xaxis': {show: false},
      'yaxis': {show: false},
      'grid': {'show': false},
      'series': {'shadowSize': 0},
      'colors': colours
    }
  );
}

function togglecollapse(name){
  var element = document.getElementById(name + '-collapse');
  var image = document.getElementById(name + '-arrow');
  if (element.style.display == "block"){
      element.style.display = "none";
      image.src = "../../img/arrow-down.png";
  }
  else{
      element.style.display = "block";
      image.src = "../../img/arrow-up.png";
  }
}

function plotPlayerSkill(id, skill){
  $.plot(id, skill, {'legend' : {show: false}, 'xaxis': {mode: 'time'}, grid: {hoverable: true}, colors: ['#0000FF']});

  $("<div id='tooltip'></div>").css({
    position: "absolute",
    display: "none",
    border: "1px solid #fdd",
    padding: "2px",
    "background-color": "#fee",
    opacity: 0.80
  }).appendTo("body");

  $(id).bind("plothover", function (event, pos, item) {
    if (item) {
      var x = item.datapoint[0].toFixed(2);
      var y = item.datapoint[1].toFixed(2);
      $("#tooltip").html(y)
        .css({top: item.pageY+5, left: item.pageX+5})
        .fadeIn(200);
    } else {
      $("#tooltip").hide();
    }
  });
}

function plotHeadToHeadGoals(id, histograms){
  $.plot(
    id,
    histograms,
    {
      'legend': {show: false},
      'xaxis': {'ticks': 10},
      grid: {hoverable: true},
      colors: ['#FF0000', '#0000FF'],
      'series': {
        'bars': {
          'show': true,
          'align': 'center'
        }
      }
    }
  );
}

function plotGamesPerDay(id, data){
  $.plot(
    id,
    data,
    {
      'legend' : {show: false},
      'xaxis': {mode: 'time'},
      grid: {hoverable: true},
      colors: ['#0000FF']
    }
  );
}

function getSortOptions(tableQuery) {
  //returns an array of a tablesorter sort order
  var hdrorder = null;
  $(tableQuery).each(function(index) {
    if ($(this).hasClass('headerSortDown')) {
      hdrorder = [index, 0];
    } else if ($(this).hasClass('headerSortUp')) {
      hdrorder = [index, 1];
    }
  });

  if (hdrorder == null && tableQuery != ".floatThead-table th") {
    return getSortOptions(".floatThead-table th")
  }

  return hdrorder;
}

function reloadLadder() {
  var sortOpts = getSortOptions("#ladder th");
  var showInactive = 0;
  if ($("tr.inactive")[0].style.display == "table-row") {
    showInactive = 1;
  }
  $("#ladderHolder").load("ladder.cgi?sortCol=" + sortOpts[0] + "&sortOrder="+sortOpts[1] + "&showInactive=" + showInactive);
}

function initHistorySlider(id, fromTime, toTime, fnOnFinish) {
  $(id).ionRangeSlider({
      type: "double",
      grid: true,
      force_edges: true,
      min: moment(1120176000, 'X').format('X'),
      max: moment().format('X'),
      from: fromTime,
      to: toTime,
      prettify: function (num) {
        return moment(num, 'X').format('LL');
      },
      onFinish: fnOnFinish
  });
}
