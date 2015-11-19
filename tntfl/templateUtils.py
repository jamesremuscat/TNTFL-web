
def getNumYellowStripes(player, games):
    return len([g for g in games if (g.redPlayer == player.name and g.redScore == 10 and g.blueScore == 0) or (g.bluePlayer == player.name and g.blueScore == 10 and g.redScore == 0)])

def getSharedGames(player1, player2):
    return sorted([g for g in player1.games if g.redPlayer == player2.name or g.bluePlayer == player2.name], key=lambda g:g.time, reverse=True)
