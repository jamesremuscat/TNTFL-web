
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

function togglecollapse(name, base){
  var element = document.getElementById(name + '-collapse');
  var image = document.getElementById(name + '-arrow');
  if (element.style.display == "block"){
      element.style.display = "none";
      image.src = base + "img/arrow-down.png";
  }
  else{
      element.style.display = "block";
      image.src = base + "img/arrow-up.png";
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

  if (hdrorder == null) {
    hdrorder = [10,1];
  }

  return hdrorder;
}

function isShowInactive() {
  return $("#inactiveButton").is(':visible');
}

function ladderTablePostProc(sortOpts, showInactive) {
  $("#ladder").tablesorter({'sortList': [[sortOpts[0], sortOpts[1]]], 'headers': { 11: { 'sorter': false}}});
  $("#ladder").floatThead();
  if (showInactive) {
    $('.inactive').show();
    $('.button_active').hide();
  }
}

function reloadLadder(dates) {
  var sortOpts = getSortOptions("#ladder th");
  var showInactive = isShowInactive();

  $("#ladderHolder").empty();
  var spinner = new Spinner().spin();
  $("#ladderHolder").append(spinner.el);
  $("#ladderHolder").load("ladder.cgi" + dates,
    function() {
      ladderTablePostProc(sortOpts, showInactive);
    }
  );
}

function updateLadderTo(range) {
  var dates = "?gamesFrom=" + range[0] + "&gamesTo=" + range[1];
  window.history.pushState("object or string", "Title", dates);
  reloadLadder(dates);
  $("#rangeSlider").data("ionRangeSlider").update({from: range[0], to: range[1]});
}

function initHistorySlider(id, fromTime, toTime) {
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
      onFinish: function (data) {
        var dates = "?gamesFrom=" + data.from + "&gamesTo=" + data.to;
        window.history.pushState("object or string", "Title", dates);
        //window.location.href = "." + dates;
        reloadLadder(dates);
      }
  });
}

function checkGameSubmitForm() {
  const allInputs = $(".game-entry input").map(function() { return $(this).val() !== ""}).get();
  var allFilled = true;
  for (var i = 0; i < allInputs.length; i++) {
    allFilled = allFilled && allInputs[i];
  }

  const redScore = $('input.red.score').val();
  const blueScore = $('input.blue.score').val();

  const scoreValid = function(score) {
    if (isNaN(score)) {
      return false;
    }
    if (score < 0) {
      return false;
    }
    if (score > 10) {
      return false;
    }
    return true;
  }
  $('#gameFormSubmit').prop("disabled", !allFilled || !scoreValid(redScore) || !scoreValid(blueScore));
}