import os.path
import cPickle as pickle
from tntfl.achievements import Achievement
from tntfl.player import Player
from tntfl.gameStore import GameStore
from tntfl.game import Game

class TableFootballLadder(object):

    games = []
    players = {}
    gameStore = None

    def __init__(self, ladderFilePath):
        self.games = []
        self.players = {}
        self.gameStore = GameStore(ladderFilePath)

        cacheFile = "cache"
        if os.path.exists(cacheFile):
            self.loadFromCache(cacheFile)

        cachedGames = len(self.games)
        self.update()

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

    def update(self):
        mostRecent = 0
        numGames = len(self.games)
        if numGames > 0:
            mostRecent = self.games[numGames - 1].time
        loadedGames = self.gameStore.getGames()
        for loadedGame in loadedGames:
            if loadedGame.time > mostRecent:
                self.addGame(loadedGame)
            elif loadedGame.isDeleted():
                for game in self.games:
                    if game.time == loadedGame.time:
                        game.deletedBy = loadedGame.deletedBy
                        game.deletedAt = loadedGame.deletedAt
                        break

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
            if bluePosBefore == redPosAfter or redPosBefore == bluePosAfter:
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
        self.gameStore.appendGame(game)

    def writeLadder(self):
        self.gameStore.rewriteGames(self.games)

    def getPlayers(self):
        return sorted([p for p in self.players.values()], key=lambda x: x.elo, reverse=True)

    def getPlayerRank(self, playerName):
        ranked = [p.name for p in self.getPlayers() if p.isActive()]
        if playerName in ranked:
            return ranked.index(playerName) + 1
        return -1
