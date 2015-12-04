<%! base = "../" %>
<%inherit file="json.mako" />{
  "name" : "${player.name}",
  "rank" : ${ladder.getPlayerRank(player.name)},
  "active" : ${"true" if ladder.isPlayerActive(player) else "false"},
  "skill": ${player.elo},
  "overrated" : ${player.overrated()},
  "total" : {
    "for": ${player.goalsFor},
    "against": ${player.goalsAgainst},
    "games": ${len(player.games)},
    "wins": ${player.wins},
    "losses": ${player.losses},
    "gamesToday" : ${player.gamesToday}
  },
  "games" : { "href" : "games/json" }
}
