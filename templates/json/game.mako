<%!
def isPositionSwap(game):
    bluePosBefore = game.bluePosAfter + game.bluePosChange
    redPosBefore = game.redPosAfter + game.redPosChange
    positionSwap = False
    if bluePosBefore > 0 and redPosBefore > 0:
        if bluePosBefore == game.redPosAfter or redPosBefore == game.bluePosAfter:
            positionSwap = True
    return positionSwap
%>
{
% if game.isDeleted():
  "deleted" : {
    "at" : ${game.deletedAt},
    "by" : "${game.deletedBy}"
  },
% endif
  "red" : {
    "name" : "${game.redPlayer}",
    "href" : "${base}player/${game.redPlayer | u}/json",
    "score" : ${game.redScore},
    "skillChange" : ${-game.skillChangeToBlue},
    "rankChange" : ${game.redPosChange},
    "newRank" : ${game.redPosAfter},
    "achievements" : [
    % for achievement in game.redAchievements:
      { "name" : "${achievement.name}",
       "description" : "${achievement.description}"
       }${"," if loop.index < len(game.redAchievements) - 1 else ""}
    % endfor
    ]
  },
  "blue" : {
    "name" : "${game.bluePlayer}",
    "href" : "${base}player/${game.bluePlayer | u}/json",
    "score" : ${game.blueScore},
    "skillChange" : ${game.skillChangeToBlue},
    "rankChange" : ${game.bluePosChange},
    "newRank" : ${game.bluePosAfter},
    "achievements" : [
    % for achievement in game.blueAchievements:
      { "name" : "${achievement.name}",
       "description" : "${achievement.description}"
       }${"," if loop.index < len(game.blueAchievements) - 1 else ""}
    % endfor
    ]
  },
  "positionSwap" : ${"true" if isPositionSwap(game) else "false"},
  "date" : ${game.time}
}
