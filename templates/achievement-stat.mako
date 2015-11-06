<%page args="ach, games"/>
<div class="col-sm-3">
  <div class="panel panel-default panel-statbox panel-achievement" title="${ach.description}">
    <div class="panel-heading">
      <h3 class="statbox">${ach.name}</h3>
    </div>
    <div class="panel-body achievement-${ach.__name__}"">
      ${len(games)}
      <div class="achievement-games">
      <ul class="list-unstyled ">
%for game in games:
        <li>
            <a href="../../game/${game.time}">${game.formatTime(game.time)}</a>
        </li>
%endfor
      </ul>
      </div>
    </div>
  </div>
</div>
