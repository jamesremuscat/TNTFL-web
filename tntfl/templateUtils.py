from datetime import date, datetime, timedelta

def getNumYellowStripes(player, games):
    return len([g for g in games if (g.redPlayer == player.name and g.redScore == 10 and g.blueScore == 0) or (g.bluePlayer == player.name and g.blueScore == 10 and g.redScore == 0)])

def getSharedGames(player1, player2):
    return [g for g in player1.games if g.redPlayer == player2.name or g.bluePlayer == player2.name]

def punditryAvailable(pundit, game, ladder):
    red = ladder.getPlayer(game.redPlayer)
    blue = ladder.getPlayer(game.bluePlayer)
    return pundit.anyComment(red, game, blue)

def formatTime(inTime):
    time = datetime.fromtimestamp(float(inTime))
    dateStr = time.strftime("%Y-%m-%d %H:%M")
    if date.fromtimestamp(float(inTime)) == date.today():
        dateStr = "%02d:%02d" % (time.hour, time.minute)
    elif date.fromtimestamp(float(inTime)) > (date.today() - timedelta(7)):
        dateStr = "%s %02d:%02d" % (("Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun")[time.weekday()], time.hour, time.minute)
    return dateStr

def getRankCSS(rank, totalActivePlayers, redScore=0, blueScore=0):
    ladderPositionCSS = "ladder-position"
    if rank == -1:
        ladderPositionCSS = ladderPositionCSS + " inactive"
    # if redScore == 10 and blueScore == 0:
    #     ladderPositionCSS += " yellow-stripe"
    # elif blueScore == 10 and redScore == 0:
    #     ladderPositionCSS += " yellow-stripe"
    elif rank == 1:
        ladderPositionCSS = ladderPositionCSS + " ladder-first"
    elif rank <= totalActivePlayers * 0.1:
        ladderPositionCSS = ladderPositionCSS + " ladder-silver"
    elif rank <= totalActivePlayers * 0.3:
        ladderPositionCSS = ladderPositionCSS + " ladder-bronze"
    return ladderPositionCSS
