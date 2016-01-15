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
  % if game.isDeleted():
    <p class="bg-danger">This game was deleted by ${game.deletedBy} at ${utils.formatTime(game.deletedAt)}</p>
  % endif
    <tr class="recent-game">
      <td width="20%" class="player red-player ${redsStripe}">${playerName(game.redPlayer)}</td>
      <td width="10%" class="rank ${utils.getRankCSS(game.redPosAfter + game.redPosChange, totalActivePlayers, game.redScore, game.blueScore)}">${game.redPosAfter + game.redPosChange}</td>
      <td width="10%" class="ach ${redsStripe}">${cups(game.redAchievements)}</td>
      
      <td width="20%" class="score ${redsStripe} ${bluesStripe}">${game.redScore} - ${game.blueScore}</td>
      
      <td width="10%" class="ach ${bluesStripe}">${cups(game.blueAchievements)}</td>
      <td width="10%" class="rank ${utils.getRankCSS(game.bluePosAfter + game.bluePosChange, totalActivePlayers, game.redScore, game.blueScore)}">${game.bluePosAfter + game.bluePosChange}</td>
      <td width="20%" class="player blue-player ${bluesStripe}">${playerName(game.bluePlayer)}</td>
    </tr>
    <tr class="game-changes">
      <td width="20%" class="score-change red">${skillChange("red", -game.skillChangeToBlue) if game.skillChangeToBlue <= 0 else ""}</td>
      <td width="10%" class="rank-change red">${rankChange("red", game.redPosChange) if game.redPosChange != 0 else ""}</td>
      <td class="detail" colspan="3">
        %if not speculative:
        ${blocks.render("gameLink", time=game.time, base=base)}
        % if punditryAvailable:
          <img src="${base}img/headset16.png"/>
        % endif
        %endif
      </td>
      <td width="10%" class="rank-change blue">${rankChange("blue", game.bluePosChange) if game.bluePosChange != 0 else ""}</td>
      <td width="20%" class="score-change blue">${skillChange("blue", game.skillChangeToBlue) if game.skillChangeToBlue > 0 else ""}</td>
    </tr>
