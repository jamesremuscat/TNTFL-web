{
  "red" : {
    "name" : "${game.redPlayer}",
    "href" : "${base}player/${game.redPlayer}/json",
    "score" : ${game.redScore},
    "skillChange" : ${-game.skillChangeToBlue},
    "rankChange" : ${game.redPosChange},
    "newRank" : ${game.redPosAfter}
  },
  "blue" : {
    "name" : "${game.bluePlayer}",
    "href" : "${base}player/${game.bluePlayer}/json",
    "score" : ${game.blueScore},
    "skillChange" : ${game.skillChangeToBlue},
    "rankChange" : ${game.bluePosChange},
    "newRank" : ${game.bluePosAfter}
  },
  "positionSwap" : ${"true" if game.positionSwap else "false"},
  "date" : ${game.time}
}