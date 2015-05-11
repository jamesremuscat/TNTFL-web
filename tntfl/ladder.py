import os.path
import time
from datetime import date, datetime, timedelta
from tntfl.aks import CircularSkillBuffer


class ExclusionsFile(object):

    def __init__(self, fileName):
        self.exclusions = []
        if os.path.exists(fileName):
            f = open(fileName, 'r')
            for line in f.readlines():
                self.exclusions.append(line.strip().lower())

    def contains(self, name):
        return (name in self.exclusions)


exclusions = ExclusionsFile("ladderExclude")


class TableFootballLadder(object):

    games = []
    players = {}

    highSkill = {'player': None, 'skill': 0, time: 0}
    lowSkill = {'player': None, 'skill': 0, time: 0}

    def __init__(self, ladderFile):
        self.games = []
        self.players = {}
        self.ladderFile = ladderFile
        ladder = open(ladderFile, 'r')
        for line in ladder.readlines():
            gameLine = line.split()
            if len(gameLine) == 5:
                # Red player, red score, blue player, blue score, time
                game = Game(gameLine[0], gameLine[1], gameLine[2], gameLine[3], int(gameLine[4]))
                self.addGame(game)
            elif len(gameLine) == 7:
                game = Game(gameLine[0], gameLine[1], gameLine[2], gameLine[3], int(gameLine[4]))
                game.deletedBy = gameLine[5]
                game.deletedAt = gameLine[6]
                self.addGame(game)
        ladder.close()

    def addGame(self, game):
        self.games.append(game)

        if game.isDeleted():
            return

        if game.redPlayer not in self.players:
            self.players[game.redPlayer] = Player(game.redPlayer)
        red = self.players[game.redPlayer]

        if game.bluePlayer not in self.players:
            self.players[game.bluePlayer] = Player(game.bluePlayer)
        blue = self.players[game.bluePlayer]

        predict = 1 / (1 + 10 ** ((red.elo - blue.elo) / 180))
        result = float(game.blueScore) / (game.blueScore + game.redScore)
        delta = 25 * (result - predict)

        game.skillChangeToBlue = delta

        bluePosBefore = -1
        redPosBefore = -1

        for index, player in enumerate(sorted([p for p in self.players.values() if p.isActive(game.time - 1)], key=lambda x: x.elo, reverse=True)):
            if player.name == game.bluePlayer:
                bluePosBefore = index
            elif player.name == game.redPlayer:
                redPosBefore = index

        blue.game(game)
        red.game(game)

        bluePosAfter, redPosAfter = -1, -1

        for index, player in enumerate(sorted([p for p in self.players.values() if p.isActive(game.time)], key=lambda x: x.elo, reverse=True)):
            if player.name == game.bluePlayer:
                bluePosAfter = index
                game.bluePosAfter = bluePosAfter + 1  # because it's zero-indexed here
            elif player.name == game.redPlayer:
                redPosAfter = index
                game.redPosAfter = redPosAfter + 1
        if bluePosBefore > 0:
            game.bluePosChange = bluePosBefore - bluePosAfter  # It's this way around because a rise in position is to a lower numbered rank.
        if redPosBefore > 0:
            game.redPosChange = redPosBefore - redPosAfter
        if bluePosBefore > 0 and redPosBefore > 0:
            if (bluePosBefore == redPosAfter or redPosBefore == bluePosAfter):
                game.positionSwap = True

        if blue.elo > self.highSkill['skill']:
            self.highSkill['skill'] = blue.elo
            self.highSkill['player'] = blue
            self.highSkill['time'] = game.time
        if red.elo > self.highSkill['skill']:
            self.highSkill['skill'] = red.elo
            self.highSkill['player'] = red
            self.highSkill['time'] = game.time
        if blue.elo < self.lowSkill['skill']:
            self.lowSkill['skill'] = blue.elo
            self.lowSkill['player'] = blue
            self.lowSkill['time'] = game.time
        if red.elo < self.lowSkill['skill']:
            self.lowSkill['skill'] = red.elo
            self.lowSkill['player'] = red
            self.lowSkill['time'] = game.time

    def addAndWriteGame(self, game):
        self.addGame(game)
        ladder = open(self.ladderFile, 'a')
        ladder.write("\n%s %s %s %s %.0f" % (game.redPlayer, game.redScore, game.bluePlayer, game.blueScore, game.time))
        ladder.close()

    def writeLadder(self, ladderFile):
        ladder = open(ladderFile, 'w')
        for game in self.games:
            if game.isDeleted():
                ladder.write("\n%s %s %s %s %.0f %s %.0f" % (game.redPlayer, game.redScore, game.bluePlayer, game.blueScore, game.time, game.deletedBy, game.deletedAt))
            else:
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
    skillChangeToBlue = 0
    positionSwap = False
    deletedBy = None
    deletedAt = 0

    def __init__(self, redPlayer, redScore, bluePlayer, blueScore, time):
        self.redPlayer = redPlayer.lower()
        self.redScore = int(redScore)
        self.redPosChange = 0
        self.redPosAfter = -1
        self.bluePlayer = bluePlayer.lower()
        self.blueScore = int(blueScore)
        self.bluePosChange = 0
        self.bluePosAfter = -1
        self.time = time

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return "{redPlayer} {redScore}-{blueScore} {bluePlayer}".format(redPlayer=self.redPlayer, bluePlayer=self.bluePlayer, redScore=self.redScore, blueScore=self.blueScore)

    def isDeleted(self):
        return self.deletedAt > 0

    @staticmethod
    def formatTime(inTime):
        time = datetime.fromtimestamp(float(inTime))
        dateStr = time.strftime("%Y-%m-%d %H:%M")

        if date.fromtimestamp(float(inTime)) == date.today():
            dateStr = "%02d:%02d" % (time.hour, time.minute)
        elif date.fromtimestamp(float(inTime)) > (date.today() - timedelta(7)):
            dateStr = "%s %02d:%02d" % (("Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun")[time.weekday()], time.hour, time.minute)

        return dateStr


class Streak(object):
    def __init__(self):
        self.count = 0
        self.fromDate = 0
        self.toDate = 0


class Player(object):

    # Number of days inactivity after which players are considered inactive
    DAYS_INACTIVE = 60

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
        self.gamesToday = 0

    def game(self, game):
        if self.name == game.redPlayer:
            delta = -game.skillChangeToBlue
            opponent = game.bluePlayer
            self.gamesAsRed += 1
            if game.redScore > game.blueScore:
                self.wins += 1
            elif game.redScore < game.blueScore:
                self.losses += 1
            self.goalsFor += game.redScore
            self.goalsAgainst += game.blueScore
        elif self.name == game.bluePlayer:
            delta = game.skillChangeToBlue
            opponent = game.redPlayer
            if game.redScore < game.blueScore:
                self.wins += 1
            elif game.redScore > game.blueScore:
                self.losses += 1
            self.goalsFor += game.blueScore
            self.goalsAgainst += game.redScore
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

        if date.fromtimestamp(game.time) == date.today():
            self.gamesToday += 1

        self.games.append(game)

    def isActive(self, atTime=time.time()):
        #  Using date.* classes is too slow here
        return (not exclusions.contains(self.name)) and len(self.games) > 0 and (self.games[-1].time > atTime - (60 * 60 * 24 * self.DAYS_INACTIVE))

    def overrated(self):
        lastSkill = self.skillBuffer.lastSkill()
        if self.skillBuffer.isFull:
            return lastSkill - self.skillBuffer.avg()
        return 0

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return self.name + ":" + str(self.elo)

    def wonGame(self, game):
        return (game.redPlayer == self.name and game.redScore > game.blueScore) or (game.bluePlayer == self.name and game.blueScore > game.redScore)

    def lostGame(self, game):
        return (game.redPlayer == self.name and game.redScore < game.blueScore) or (game.bluePlayer == self.name and game.blueScore < game.redScore)

    def getStreaks(self):
        winStreak = Streak()

        loseStreak = Streak()

        currentStreak = Streak()

        lastWon = False
        lastLost = False

        for game in self.games:
            wonGame = self.wonGame(game)
            lostGame = self.lostGame(game)

            if (wonGame != lastWon) or (lostGame != lastLost):
                # end of streak
                if lastWon:
                    if currentStreak.count > winStreak.count:
                        winStreak = currentStreak
                if lastLost:
                    if currentStreak.count > loseStreak.count:
                        loseStreak = currentStreak
                currentStreak = Streak()
                currentStreak.fromDate = game.time
                currentStreak.toDate = game.time if (wonGame or lostGame) else 0
                currentStreak.count = 1 if (wonGame or lostGame) else 0

            if (wonGame and lastWon) or (lostGame and lastLost):
                currentStreak.toDate = game.time
                currentStreak.count += 1

            lastWon = wonGame
            lastLost = lostGame

        currentStreakType = "wins" if lastWon else "losses" if lastLost else "(last game was a draw)"

        return {'win': winStreak, 'lose': loseStreak, 'current': currentStreak, 'currentType': currentStreakType}


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
