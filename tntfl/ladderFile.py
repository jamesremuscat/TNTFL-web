class LadderFile(object):

    _ladderfilePath = ""

    def __init__(self, ladderFilePath):
        self._ladderFilePath = ladderFilePath

    def getLines(self):
        lines = None
        with open(self._ladderFilePath, 'r') as ladder:
            lines = ladder.readlines()
        return lines

    def appendGame(self, game):
        with open(self._ladderFilePath, 'a') as ladder:
            self._writeGame(ladder, game)

    def rewriteGames(self, games):
        with open(self._ladderFilePath, 'w') as ladder:
            for game in games:
                self._writeGame(ladder, game)

    def _writeGame(self, ladder, game):
        toWrite = "\n%s %s %s %s %.0f" % (game.redPlayer, game.redScore, game.bluePlayer, game.blueScore, game.time)
        if game.isDeleted():
            toWrite += " %s %.0f" % (game.deletedBy, game.deletedAt)
        ladder.write(toWrite)
