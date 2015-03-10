from datetime import date, datetime, timedelta
from tntfl.aks import CircularSkillBuffer


class ExclusionsFile(object):

    def __init__(self, fileName):
        self.exclusions = []
        f = open(fileName, 'r')
        for line in f.readlines():
            self.exclusions.append(line.strip().lower())

    def contains(self, name):
        return (name in self.exclusions)


exclusions = ExclusionsFile("ladderExclude")


class TableFootballLadder(object):

    games = []
    players = {}

    def __init__(self, ladderFile):
        self.ladderFile = ladderFile
        ladder = open(ladderFile, 'r')
        for line in ladder.readlines():
            gameLine = line.split()
            if len(gameLine) == 5:
                # Red player, red score, blue player, blue score, time
                game = Game(gameLine[0], gameLine[1], gameLine[2], gameLine[3], int(gameLine[4]))
                self.addGame(game)
        ladder.close()

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

        game.skillChangeToBlue = delta

        bluePosBefore = -1
        redPosBefore = -1

        for index, player in enumerate(sorted([p for p in self.players.values() if p.isActive()], key=lambda x: x.elo, reverse=True)):
            if player.name == game.bluePlayer:
                bluePosBefore = index
            elif player.name == game.redPlayer:
                redPosBefore = index

        blue.game(game)
        red.game(game)
        self.games.append(game)

        for index, player in enumerate(sorted([p for p in self.players.values() if p.isActive()], key=lambda x: x.elo, reverse=True)):
            if player.name == game.bluePlayer:
                bluePosAfter = index
            elif player.name == game.redPlayer:
                redPosAfter = index
        if bluePosBefore > 0:
            game.bluePosChange = bluePosBefore - bluePosAfter  # It's this way around because a rise in position is to a lower numbered rank.
        if redPosBefore > 0:
            game.redPosChange = redPosBefore - redPosAfter

    def addAndWriteGame(self, game):
        self.addGame(game)
        ladder = open(self.ladderFile, 'a')
        ladder.write("\n%s %s %s %s %.0f" % (game.redPlayer, game.redScore, game.bluePlayer, game.blueScore, game.time))
        ladder.close()

    def getPlayers(self):
        return sorted([p for p in self.players.values()], key=lambda x: x.elo, reverse=True)

    def getPlayerRank(self, playerName):
        ranked = [p.name for p in self.getPlayers() if p.isActive()]
        if playerName in ranked:
            return ranked.index(playerName) + 1
        return -1


class Game(object):
    skillChangeToBlue = None

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

    @staticmethod
    def formatTime(inTime):
        time = datetime.fromtimestamp(float(inTime))
        dateStr = time

        if date.fromtimestamp(float(inTime)) == date.today():
            dateStr = "%02d:%02d" % (time.hour, time.minute)
        elif date.fromtimestamp(float(inTime)) > (date.today() - timedelta(7)):
            dateStr = "%s %02d:%02d" % (("Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun")[time.weekday()], time.hour, time.minute)

        return dateStr


class Player(object):

    def __init__(self, name):
        self.name = name
        self.elo = 0.0
        self.games = []
        self.wins = 0
        self.losses = 0
        self.goalsFor = 0
        self.goalsAgainst = 0
        self.skillBuffer = CircularSkillBuffer(10)
        self.gamesAsRed = 0
        self.highestSkill = {"time": 0, "skill": 0}
        self.lowestSkill = {"time": 0, "skill": 0}
        self.mostSignificantGame = None

    def game(self, game):
        if self.name == game.redPlayer:
            delta = -game.skillChangeToBlue
            opponent = game.bluePlayer
            self.gamesAsRed += 1
            if game.redScore > game.blueScore:
                self.wins += 1
            elif game.redScore < game.blueScore:
                self.losses += 1
        elif self.name == game.bluePlayer:
            delta = game.skillChangeToBlue
            opponent = game.redPlayer
            if game.redScore < game.blueScore:
                self.wins += 1
            elif game.redScore > game.blueScore:
                self.losses += 1
        else:
            return
        self.skillBuffer.put({'oldskill': self.elo, 'skill': self.elo + delta, 'played': opponent})
        self.elo += delta

        if (self.elo > self.highestSkill["skill"]):
            self.highestSkill = {"time": game.time, "skill": self.elo}

        if (self.elo < self.lowestSkill["skill"]):
            self.lowestSkill = {"time": game.time, "skill": self.elo}

        if self.mostSignificantGame is None or abs(delta) > abs(self.mostSignificantGame.skillChangeToBlue):
            self.mostSignificantGame = game

        self.games.append(game)

    def isActive(self):
        return (not exclusions.contains(self.name))

    def overrated(self):
        lastSkill = self.skillBuffer.lastSkill()
        if self.skillBuffer.isFull:
            return lastSkill - self.skillBuffer.avg()
        return 0

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return self.name + ":" + str(self.elo)


class PerPlayerStat(object):
    games = 0
    goalsFor = 0
    goalsAgainst = 0
    skillChange = 0
    wins = 0
    losses = 0
    draws = 0

    def __init__(self, opponent):
        self.opponent = opponent

    def append(self, goalsFor, goalsAgainst, skillChange):
        self.games += 1
        self.goalsFor += goalsFor
        self.goalsAgainst += goalsAgainst
        self.skillChange += skillChange
        if goalsFor > goalsAgainst:
            self.wins += 1
        elif goalsFor < goalsAgainst:
            self.losses += 1
        else:
            self.draws += 1
