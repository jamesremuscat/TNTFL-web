class TableFootballLadder(object):

    games = []
    players = {}

    def __init__(self, ladderFile):
        ladder = open(ladderFile, 'r')
        for line in ladder.readlines():
            gameLine = line.split()
            if len(gameLine) == 5:
                # Red player, red score, blue player, blue score, time
                game = Game(gameLine[0], gameLine[1], gameLine[2], gameLine[3], gameLine[4])
                self.addGame(game)

    def addGame(self, game):
        if game.redPlayer not in self.players:
            self.players[game.redPlayer] = Player(game.redPlayer)
        red = self.players[game.redPlayer]
        red.goalsFor = red.goalsFor + game.redScore
        red.goalsAgainst = red.goalsAgainst + game.blueScore

        if game.bluePlayer not in self.players:
            self.players[game.bluePlayer] = Player(game.bluePlayer)
        blue = self.players[game.bluePlayer]
        blue.goalsFor = blue.goalsFor + game.blueScore
        blue.goalsAgainst = blue.goalsAgainst + game.redScore

        predict = 1 / (1 + 10 ** ((red.elo - blue.elo) / 180))
        result = float(game.blueScore) / (game.blueScore + game.redScore)
        delta = 25 * (result - predict)

        blue.game(delta, game.time)
        red.game(-delta, game.time)
        self.games.append(game)


class Game(object):
    def __init__(self, redPlayer, redScore, bluePlayer, blueScore, time):
        self.redPlayer = redPlayer.lower()
        self.redScore = int(redScore)
        self.bluePlayer = bluePlayer.lower()
        self.blueScore = int(blueScore)
        self.time = time

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return "{redPlayer} {redScore}-{blueScore} {bluePlayer}".format(redPlayer=self.redPlayer, bluePlayer=self.bluePlayer, redScore=self.redScore, blueScore=self.blueScore)


class Player(object):

    def __init__(self, name):
        self.name = name
        self.elo = 0.0
        self.games = 0
        self.goalsFor = 0
        self.goalsAgainst = 0

    def game(self, delta, time):
        self.elo += delta
        self.games += 1

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return self.name + ":" + str(self.elo)
