<%page args="game, base, totalActivePlayers, punditryAvailable=False, speculative=False"/>
<%!
import tntfl.templateUtils as utils
%>
<%namespace name="blocks" file="blocks.mako"/>
<%
redsStripe = "yellow-stripe" if game.redScore == 10 and game.blueScore == 0 else ""
bluesStripe = "yellow-stripe" if game.blueScore == 10 and game.redScore == 0 else ""
%>

<%def name="playerName(name)">
  <a href="${base}player/${name}/">${name}</a>
</%def>

<%def name="cups(achs)">
  <div style="display:table;margin-left: auto;margin-right: auto;">
    %for ach in achs:
      <div style="display:table-cell;">
        <img src="${base}img/trophy5_24.png" alt="Achievement unlocked!" title="Achievement unlocked!" style="width:100%;"/>
      </div>
    %endfor
  </div>
</%def>

<%def name="rankChange(colour, change)">
  <span class='skill-change skill-change-${colour}' title='Ladder rank change'>
    ${"{:+}".format(change)}
  </span>
</%def>

<%def name="skillChange(colour, change)">
  <span class='skill-change skill-change-${colour}' title='Skill change'>
    ${"{:+.3f}".format(change)}
  </span>
</%def>

<div class="recent-game container-fluid">
  % if game.isDeleted():
    <p class="bg-danger">This game was deleted by ${game.deletedBy} at ${utils.formatTime(game.deletedAt)}</p>
  % endif
  <div class="row recent-game-result">
    <div class="col-md-1 ${utils.getRankCSS(game.redPosAfter + game.redPosChange, totalActivePlayers)} unpad">
      ${game.redPosAfter + game.redPosChange}
    </div>
    <div class="col-md-3 red-player ${redsStripe}">
      ${playerName(game.redPlayer)}
    </div>
    <div class="col-md-1 ${redsStripe}" style="padding:0px;">
      ${cups(game.redAchievements)}
    </div>
    <div class="col-md-2 ${redsStripe} ${bluesStripe}">${game.redScore} - ${game.blueScore}</div>
    <div class="col-md-1 ${bluesStripe}" style="padding:0px;">
      ${cups(game.blueAchievements)}
    </div>
    <div class="col-md-1 ${utils.getRankCSS(game.bluePosAfter + game.bluePosChange, totalActivePlayers)} unpad">
      ${game.bluePosAfter + game.bluePosChange}
    </div>
    <div class="col-md-3 blue-player ${bluesStripe}">
      ${playerName(game.bluePlayer)}
    </div>
  </div>
  <div class="row">
    <div class="col-md-1 unpad">
      ${rankChange("red", game.redPosChange) if game.redPosChange != 0 else ""}
    </div>
    <div class="col-md-3">
      ${skillChange("red", -game.skillChangeToBlue) if game.skillChangeToBlue <= 0 else ""}
    </div>
    <div class="col-md-4">
      %if not speculative:
        ${blocks.render("gameLink", time=game.time, base=base)}
        % if punditryAvailable:
          <img src="${base}img/headset16.png"/>
        % endif
      %endif
    </div>
    <div class="col-md-1 unpad">
      ${rankChange("blue", game.bluePosChange) if game.bluePosChange != 0 else ""}
    </div>
    <div class="col-md-3">
      ${skillChange("blue", game.skillChangeToBlue) if game.skillChangeToBlue > 0 else ""}
    </div>
  </div>
</div>
