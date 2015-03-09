<%! base = "../" %>
<%inherit file="json.mako" />[
<% players = [p for p in ladder.getPlayers() if p.isActive() ]%>
%for player in players:
{
  "name" : "${player.name}",
  "skill" : ${player.elo},
  "href" : "${self.attr.base}player/${player.name}/json"
}${"," if loop.index < len(players) - 1 else ""}
%endfor
]