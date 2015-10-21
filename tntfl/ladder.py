import os.path
import cPickle as pickle
from datetime import date, datetime, timedelta
from tntfl.achievements import Achievement
from tntfl.player import Player

class TableFootballLadder(object):

    games = []
    players = {}

    def __init__(self, ladderFile):
        ladderFile = "/home/local/jrem/public_html/tntfl/ladder.txt"
        self.games = []
        self.players = {}
        self.ladderFile = ladderFile

        cacheFile = "cache"
        if (os.path.exists(cacheFile)):
            self.loadFromCache(cacheFile)

        cachedGames = len(self.games)
        self.update(ladderFile)

        if cachedGames < len(self.games):
            pickle.dump(self.games, open(cacheFile, 'wb'), pickle.HIGHEST_PROTOCOL)

    def loadFromCache(self, cacheFile):
        self.games = pickle.load(open(cacheFile, 'rb'))
        for game in self.games:
            if not game.isDeleted():
                red = self.getPlayer(game.redPlayer)
                blue = self.getPlayer(game.bluePlayer)
                red.game(game)
                blue.game(game)
                red.achieve(game.redAchievements)
                blue.achieve(game.blueAchievements)

    def update(self, ladderFile):
        mostRecent = 0
        numGames = len(self.games)
        if (numGames > 0):
            mostRecent = self.games[numGames - 1].time
        ladder = open(ladderFile, 'r')
        for line in ladder.readlines():
            gameLine = line.split()
            if len(gameLine) == 5 and int(gameLine[4]) > mostRecent:
                # Red player, red score, blue player, blue score, time
                game = Game(gameLine[0], gameLine[1], gameLine[2], gameLine[3], int(gameLine[4]))
                self.addGame(game)
            elif len(gameLine) == 7:
                red = gameLine[0]
                redScore = gameLine[1]
                blue = gameLine[2]
                blueScore = gameLine[3]
                time = int(gameLine[4])
                deletedBy = gameLine[5]
                deletedAt = int(gameLine[6])
                if time > mostRecent:
                    game = Game(red, redScore, blue, blueScore, time)
                    game.deletedBy = deletedBy
                    game.deletedAt = deletedAt
                    self.addGame(game)
                else:
                    for game in self.games:
                        if game.time == time:
                            game.deletedBy = deletedBy
                            game.deletedAt = deletedAt
                            break
        ladder.close()

    def getPlayer(self, name):
        if name not in self.players:
            self.players[name] = Player(name)
        return self.players[name]

    def addGame(self, game):
        self.games.append(game)

        if game.isDeleted():
            return

        red = self.getPlayer(game.redPlayer)
        blue = self.getPlayer(game.bluePlayer)

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

        game.redAchievements = Achievement.getAllForGame(red, game, blue, self)
        game.blueAchievements = Achievement.getAllForGame(blue, game, red, self)
        red.achieve(game.redAchievements)
        blue.achieve(game.blueAchievements)

    def getSkillBounds(self):
        highSkill = {'player': None, 'skill': 0, 'time': 0}
        lowSkill = {'player': None, 'skill': 0, 'time': 0}
        for player in self.players.values():
            skill = player.getSkillBounds()
            if skill['highest']['skill'] > highSkill['skill']:
                highSkill['player'] = player
                highSkill['skill'] = skill['highest']['skill']
                highSkill['time'] = skill['highest']['time']
            if skill['lowest']['skill'] < lowSkill['skill']:
                lowSkill['player'] = player
                lowSkill['skill'] = skill['lowest']['skill']
                lowSkill['time'] = skill['lowest']['time']
        return {'highest': highSkill, 'lowest': lowSkill}

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
        self.redAchievements = []
        self.blueAchievements = []

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return "{redPlayer} {redScore}-{blueScore} {bluePlayer}".format(redPlayer=self.redPlayer, bluePlayer=self.bluePlayer, redScore=self.redScore, blueScore=self.blueScore)

    def isDeleted(self):
        return self.deletedAt > 0

    def timeAsDatetime(self):
        return datetime.fromtimestamp(self.time)

    @staticmethod
    def formatTime(inTime):
        time = datetime.fromtimestamp(float(inTime))
        dateStr = time.strftime("%Y-%m-%d %H:%M")

        if date.fromtimestamp(float(inTime)) == date.today():
            dateStr = "%02d:%02d" % (time.hour, time.minute)
        elif date.fromtimestamp(float(inTime)) > (date.today() - timedelta(7)):
            dateStr = "%s %02d:%02d" % (("Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun")[time.weekday()], time.hour, time.minute)

        return dateStr
