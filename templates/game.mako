        <div class="recent-game container-fluid">
% if game.isDeleted():
<p class="bg-danger">This game was deleted by ${game.deletedBy} at ${game.formatTime(game.deletedAt)}</p>
% endif
          <div class="row recent-game-result">
            <div class="col-md-4 red-player ${"yellow-stripe" if game.redScore == 10 and game.blueScore == 0 else ""}">
            <a href="${base}player/${game.redPlayer}/">${game.redPlayer}</a>
            </div>
            <div class="col-md-1 ${"yellow-stripe" if game.redScore == 10 else ""}">
              % if len(game.redAchievements) > 0:
                <img src="${base}img/trophy5_24.png" alt="Achievement unlocked!" title="Achievement unlocked!" />
              % endif
            </div>
            <div class="col-md-2 ${"yellow-stripe" if game.blueScore == 10 or game.redScore == 10 else ""}">${game.redScore} - ${game.blueScore}</div>
            <div class="col-md-1 ${"yellow-stripe" if game.blueScore == 10 else ""}">
              % if len(game.blueAchievements) > 0:
                <img src="${base}img/trophy5_24.png" alt="Achievement unlocked!" title="Achievement unlocked!" />
              % endif
            </div>
            <div class="col-md-4 blue-player ${"yellow-stripe" if game.blueScore == 10 and game.redScore == 0 else ""}">
            <a href="${base}player/${game.bluePlayer}/">${game.bluePlayer}</a>
            </div>
          </div>
          <div class="row">
            <div class="col-md-2">${"<span class=\"skill-change skill-change-red\" title=\"Ladder rank change\">{:+}</span>".format(game.redPosChange) if game.redPosChange != 0 else ""}</div>
            <div class="col-md-2">${"<span class=\"skill-change skill-change-red\" title=\"Skill change\">{:+.3f}</span>".format(-game.skillChangeToBlue) if game.skillChangeToBlue <= 0 else ""}</div>
            <div class="col-md-4"><a href="${base}game/${game.time}/">${game.formatTime(game.time)}</a></div>
            <div class="col-md-2">${"<span class=\"skill-change skill-change-blue\" title=\"Skill change\">{:+.3f}</span>".format(game.skillChangeToBlue) if game.skillChangeToBlue > 0 else ""}</div>
            <div class="col-md-2">${"<span class=\"skill-change skill-change-blue\" title=\"Ladder rank change\">{:+}</span>".format(game.bluePosChange) if game.bluePosChange != 0 else ""}</div>
          </div>
        </div>
