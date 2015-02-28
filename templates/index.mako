<%! title = "Table Football Ladder 3.0" %>
<%inherit file="html.mako" />
<p>Ladder has ${len(ladder.games)} games</p>
${sorted([p for p in ladder.players.values()], key=lambda x: x.elo, reverse=True)}<br />
