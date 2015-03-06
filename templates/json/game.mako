<%inherit file="json.mako" />{
  "red" : {
    "name" : "${game.redPlayer}",
    "score" : ${game.redScore},
    "skillChange" : ${-game.skillChangeToBlue},
    "positionChange" : ${game.redPosChange}
  },
  "blue" : {
    "name" : "${game.bluePlayer}",
    "score" : ${game.blueScore},
    "skillChange" : ${game.skillChangeToBlue},
    "positionChange" : ${game.bluePosChange}
  },
  "date" : ${game.time}
}