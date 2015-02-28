class TableFootballLadder(object):

    games = []

    def __init__(self, ladderFile):
        ladder = open(ladderFile, 'r')
        for line in ladder.readlines():
            gameLine = line.split()
            if len(gameLine) == 5:
                # Red player, red score, blue player, blue score, time
                game = Game(gameLine[0], gameLine[1], gameLine[2], gameLine[3], gameLine[4])
                self.addGame(game)

    def addGame(self, game):
        self.games.append(game)


class Game(object):
    def __init__(self, redPlayer, redScore, bluePlayer, blueScore, time):
        self.redPlayer = redPlayer
        self.redScore = int(redScore)
        self.bluePlayer = bluePlayer
        self.blueScore = int(blueScore)
        self.time = time
