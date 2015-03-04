<%inherit file="json.mako" />{
  "red" : {
    "name" : "${game.redPlayer}",
    "score" : ${game.redScore},
    "skillChange" : ${-game.skillChangeToBlue}
  },
  "blue" : {
    "name" : "${game.bluePlayer}",
    "score" : ${game.blueScore},
    "skillChange" : ${game.skillChangeToBlue}
  },
  "date" : ${game.time}
}