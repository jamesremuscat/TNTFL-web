{
% if game.isDeleted():
  "deleted" : {
    "at" : ${game.deletedAt},
    "by" : ${game.deletedBy}
  },
% endif
  "red" : {
    "name" : "${game.redPlayer}",
    "href" : "${base}player/${game.redPlayer | u}/json",
    "score" : ${game.redScore},
    "skillChange" : ${-game.skillChangeToBlue},
    "rankChange" : ${game.redPosChange},
    "newRank" : ${game.redPosAfter}
  },
  "blue" : {
    "name" : "${game.bluePlayer}",
    "href" : "${base}player/${game.bluePlayer | u}/json",
    "score" : ${game.blueScore},
    "skillChange" : ${game.skillChangeToBlue},
    "rankChange" : ${game.bluePosChange},
    "newRank" : ${game.bluePosAfter}
  },
  "positionSwap" : ${"true" if game.positionSwap else "false"},
  "date" : ${game.time}
}