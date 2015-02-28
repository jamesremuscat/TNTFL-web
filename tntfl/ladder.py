class TableFootballLadder(object):

    games = []

    def __init__(self, ladderFile):
        ladder = open(ladderFile, 'r')
        for line in ladder.readlines():
            gameLine = line.split()
            if len(gameLine) == 5:
                game = Game(gameLine[0], gameLine[2], gameLine[1], gameLine[3], gameLine[4])
                self.addGame(game)

    def addGame(self, game):
        self.games.append(game)


class Game(object):
    def __init__(self, r, b, rs, bs, time):
        self.red = r
        self.blue = b
        self.redScore = int(rs)
        self.blueScore = int(bs)
        self.time = time
        self.vars = {r: {}, b: {}}
        self.speculative = False
