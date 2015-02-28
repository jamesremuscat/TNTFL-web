<%inherit file="html.mako" />
Ladder has ${len(ladder.games)} games<br />
${sorted([p for p in ladder.players.values()], key=lambda x: x.elo, reverse=True)}<br />
