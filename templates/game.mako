<%page args="game, base, punditryAvailable=False, speculative=False"/>
<%!
import tntfl.templateUtils as utils
%>
<%
redsStripe = game.redScore == 10 and game.blueScore == 0
bluesStripe = game.blueScore == 10 and game.redScore == 0
%>

<%def name="cups(achs)">
  <div style="display:table;margin-left: auto;margin-right: auto;">
    %for ach in achs:
      <div style="display:table-cell;"><img src="${base}img/trophy5_24.png" alt="Achievement unlocked!" title="Achievement unlocked!" style="width:100%;"/></div>
    %endfor
  </div>
</%def>

<div class="recent-game container-fluid">
  % if game.isDeleted():
    <p class="bg-danger">This game was deleted by ${game.deletedBy} at ${utils.formatTime(game.deletedAt)}</p>
  % endif
  <div class="row recent-game-result">
    <div class="col-md-4 red-player ${"yellow-stripe" if redsStripe else ""}">
      <a href="${base}player/${game.redPlayer}/">${game.redPlayer}</a>
    </div>
    <div class="col-md-1 ${"yellow-stripe" if redsStripe else ""}" style="padding:0px;">
      ${cups(game.redAchievements)}
    </div>
    <div class="col-md-2 ${"yellow-stripe" if redsStripe or bluesStripe else ""}">${game.redScore} - ${game.blueScore}</div>
    <div class="col-md-1 ${"yellow-stripe" if bluesStripe else ""}" style="padding:0px;">
      ${cups(game.blueAchievements)}
    </div>
    <div class="col-md-4 blue-player ${"yellow-stripe" if bluesStripe else ""}">
      <a href="${base}player/${game.bluePlayer}/">${game.bluePlayer}</a>
    </div>
  </div>
  <div class="row">
    <div class="col-md-2">
      ${"<span class='skill-change skill-change-red' title='Ladder rank change'>{:+}</span>".format(game.redPosChange) if game.redPosChange != 0 else ""}
    </div>
    <div class="col-md-2">
      ${"<span class='skill-change skill-change-red' title='Skill change'>{:+.3f}</span>".format(-game.skillChangeToBlue) if game.skillChangeToBlue <= 0 else ""}
    </div>
    <div class="col-md-4">
      %if not speculative:
        <a href="${base}game/${game.time}/">${utils.formatTime(game.time)}</a>
        % if punditryAvailable:
          <img src="${base}img/headset16.png"/>
        % endif
      %endif
    </div>
    <div class="col-md-2">
      ${"<span class='skill-change skill-change-blue' title='Skill change'>{:+.3f}</span>".format(game.skillChangeToBlue) if game.skillChangeToBlue > 0 else ""}
    </div>
    <div class="col-md-2">
      ${"<span class='skill-change skill-change-blue' title='Ladder rank change'>{:+}</span>".format(game.bluePosChange) if game.bluePosChange != 0 else ""}
    </div>
  </div>
</div>
