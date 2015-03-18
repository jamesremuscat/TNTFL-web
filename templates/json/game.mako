{
  "red" : {
    "name" : "${game.redPlayer}",
    "href" : "${base}player/${game.redPlayer}/json",
    "score" : ${game.redScore},
    "skillChange" : ${-game.skillChangeToBlue},
    "rankChange" : ${game.redPosChange}
  },
  "blue" : {
    "name" : "${game.bluePlayer}",
    "href" : "${base}player/${game.bluePlayer}/json",
    "score" : ${game.blueScore},
    "skillChange" : ${game.skillChangeToBlue},
    "rankChange" : ${game.bluePosChange}
  },
  "date" : ${game.time}
}