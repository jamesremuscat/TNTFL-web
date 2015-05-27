<%! base = "../" %>
<%inherit file="json.mako" />{
  "name" : "${player.name}",
  "rank" : ${ladder.getPlayerRank(player.name)},
  "active" : ${"true" if player.isActive() else "false"},
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
