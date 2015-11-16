import time
from datetime import date
from tntfl.aks import CircularSkillBuffer


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
        self.withinActive = 0
        self.wins = 0
        self.losses = 0
        self.goalsFor = 0
        self.goalsAgainst = 0
        self.skillBuffer = CircularSkillBuffer(10)
        self.gamesAsRed = 0
        self.highestSkill = {"time": 0, "skill": 0}
        self.lowestSkill = {"time": 0, "skill": 0}
        self.achievements = {}

    def game(self, game):
        if self.name == game.redPlayer:
            delta = -game.skillChangeToBlue
            self.gamesAsRed += 1
            if game.redScore > game.blueScore:
                self.wins += 1
            elif game.redScore < game.blueScore:
                self.losses += 1
            self.goalsFor += game.redScore
            self.goalsAgainst += game.blueScore
        elif self.name == game.bluePlayer:
            delta = game.skillChangeToBlue
            if game.redScore < game.blueScore:
                self.wins += 1
            elif game.redScore > game.blueScore:
                self.losses += 1
            self.goalsFor += game.blueScore
            self.goalsAgainst += game.redScore
        else:
            return
        self.elo += delta
        self.skillBuffer.put(self.elo)

        if (self.elo > self.highestSkill["skill"]):
            self.highestSkill = {"time": game.time, "skill": self.elo}

        if (self.elo < self.lowestSkill["skill"]):
            self.lowestSkill = {"time": game.time, "skill": self.elo}

        self.games.append(game)
        self.withinActive = game.time + (60 * 60 * 24 * self.DAYS_INACTIVE)

    def getSkillBounds(self):
        return {"highest": self.highestSkill, "lowest": self.lowestSkill}

    def mostSignificantGame(self):
        mostSignificantGame = None
        for game in self.games:
            if self.name == game.redPlayer:
                delta = -game.skillChangeToBlue
            else:
                delta = game.skillChangeToBlue
            if mostSignificantGame is None or abs(delta) > abs(mostSignificantGame.skillChangeToBlue):
                mostSignificantGame = game
        return mostSignificantGame

    @property
    def gamesToday(self):
        today = date.today()
        return self.gamesOn(today)

    def gamesOn(self, date):
        return len([g for g in self.games if g.timeAsDatetime().date() == date])

    def skillChangeToday(self):
        today = date.today()
        skillChange = 0
        for game in [g for g in self.games if g.timeAsDatetime().date() == today]:
            skillChange += game.skillChangeToBlue if game.bluePlayer == self.name else -game.skillChangeToBlue
        return skillChange

    def rankChangeToday(self):
        today = date.today()
        change = 0
        for game in [g for g in self.games if g.timeAsDatetime().date() == today]:
            change += game.bluePosChange if game.bluePlayer == self.name else game.redPosChange
        return change

    def achieve(self, achievements, game):
        for achievement in achievements:
            if achievement in self.achievements.keys():
                self.achievements[achievement].append(game)
            else:
                self.achievements[achievement] = [game]

    def isActive(self, atTime=time.time()):
        #  Using date.* classes is too slow here
        return self.withinActive > atTime

    def overrated(self):
        if self.skillBuffer.isFull:
            lastSkill = self.skillBuffer.lastSkill()
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

    def getAllStreaks(self):
        winStreaks = []
        loseStreaks = []
        currentStreak = Streak()
        wonPrev = False
        lostPrev = False

        for game in self.games:
            wonGame = self.wonGame(game)
            lostGame = self.lostGame(game)
            if (wonGame and wonPrev) or (lostGame and lostPrev):
                currentStreak.toDate = game.time
                currentStreak.count += 1
            else:
                # end of streak
                if wonPrev:
                    winStreaks.append(currentStreak)
                if lostPrev:
                    loseStreaks.append(currentStreak)
                currentStreak = Streak()
                currentStreak.fromDate = game.time
                currentStreak.toDate = game.time if (wonGame or lostGame) else 0
                currentStreak.count = 1 if (wonGame or lostGame) else 0
            wonPrev = wonGame
            lostPrev = lostGame

        currentStreakType = "wins" if wonPrev else "losses" if lostPrev else "(last game was a draw)"
        return {'win': winStreaks, 'lose': loseStreaks, 'current': currentStreak, 'currentType': currentStreakType}

    def getStreaks(self):
        streaks = self.getAllStreaks()
        winStreaks = sorted(streaks['win'], key=lambda s:s.count, reverse=True)
        loseStreaks = sorted(streaks['lose'], key=lambda s:s.count, reverse=True)
        return {
            'win': winStreaks[0] if len(winStreaks) > 0 else Streak(),
            'lose': loseStreaks[0] if len(winStreaks) > 0 else Streak(),
            'current': streaks['current'],
            'currentType': streaks['currentType']
        }

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
