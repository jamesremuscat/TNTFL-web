<%page args="ach, games, base"/>
<%!
import tntfl.templateUtils as utils
%>
<div class="col-sm-3">
  <div class="panel panel-default panel-statbox panel-achievement" title="${ach.description}">
    <div class="panel-heading">
      <h3 class="statbox">${ach.name}</h3>
    </div>
    <div class="panel-body achievement-${ach.__name__}">
      ${len(games)}
      <img src="${base}img/arrow-down.png"
           id="achievement-${ach.__name__}-arrow"
           onclick="togglecollapse('achievement-${ach.__name__}', '${base}')"
       />
      <ul class="list-unstyled achievement-games" id="achievement-${ach.__name__}-collapse">
%for game in games:
        <li>
            <a href="${base}game/${game.time}">${utils.formatTime(game.time)}</a>
        </li>
%endfor
      </ul>
      </div>

  </div>
</div>
