import os.path
import cPickle as pickle
from time import time
from tntfl.achievements import Achievements
from tntfl.player import Player, Streak
from tntfl.gameStore import GameStore
from tntfl.game import Game

class TableFootballLadder(object):

    games = []
    players = {}
    _gameStore = None
    _cacheFilePath = "cache"
    _usingCache = True
    achievements = None

    def __init__(self, ladderFilePath, useCache = True):
        self.games = []
        self.players = {}
        self._gameStore = GameStore(ladderFilePath)
        self._usingCache = useCache

        self.achievements = Achievements()

        self._loadFromCache()
        numCachedGames = len(self.games)

        if numCachedGames == 0:
            self._loadFromStore()
            self._writeToCache()

    def _loadFromCache(self):
        if os.path.exists(self._cacheFilePath) and self._usingCache:
            self.games = pickle.load(open(self._cacheFilePath, 'rb'))
            for game in self.games:
                if not game.isDeleted():
                    red = self.getPlayer(game.redPlayer)
                    blue = self.getPlayer(game.bluePlayer)
                    red.game(game)
                    blue.game(game)
                    red.achieve(game.redAchievements, game)
                    blue.achieve(game.blueAchievements, game)

    def _writeToCache(self):
        if self._usingCache:
            pickle.dump(self.games, open(self._cacheFilePath, 'wb'), pickle.HIGHEST_PROTOCOL)

    def _deleteCache(self):
        if os.path.exists(self._cacheFilePath) and self._usingCache:
            os.remove(self._cacheFilePath)

    def _loadFromStore(self):
        loadedGames = self._gameStore.getGames()
        for loadedGame in loadedGames:
            self.addGame(loadedGame)

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

        game.redAchievements = self.achievements.getAllForGame(red, game, blue, self)
        game.blueAchievements = self.achievements.getAllForGame(blue, game, red, self)
        red.achieve(game.redAchievements, game)
        blue.achieve(game.blueAchievements, game)

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

    def getStreaks(self):
        winning = {'player': None, 'streak': Streak()}
        losing = {'player': None, 'streak': Streak()}
        for player in self.players.values():
            streaks = player.getStreaks()
            if streaks['win'].count > winning['streak'].count:
                winning['player'] = player
                winning['streak'] = streaks['win']
            if streaks['lose'].count > losing['streak'].count:
                losing['player'] = player
                losing['streak'] = streaks['lose']
        return {'win': winning, 'lose': losing}

    def addAndWriteGame(self, redPlayer, redScore, bluePlayer, blueScore):
        game = None
        redScore = int(redScore)
        blueScore = int(blueScore)
        if redScore >= 0 and blueScore >= 0 and (redScore + blueScore) > 0:
            self._deleteCache()
            game = Game(redPlayer, redScore, bluePlayer, blueScore, int(time()))
            self.addGame(game)
            self._gameStore.appendGame(game)
        return game

    def deleteGame(self, gameTime, deletedBy):
        self._deleteCache()
        return self._gameStore.deleteGame(gameTime, deletedBy)

    def getPlayers(self):
        return sorted([p for p in self.players.values()], key=lambda x: x.elo, reverse=True)

    def getPlayerRank(self, playerName):
        ranked = [p.name for p in self.getPlayers() if p.isActive()]
        if playerName in ranked:
            return ranked.index(playerName) + 1
        return -1

    def getAchievements(self):
        achievements = {}
        for ach in self.achievements.achievements:
            achievements[ach.__class__] = 0

        for player in self.players.values():
            for name, games in player.achievements.iteritems():
                achievements[name] += len(games)
        return achievements
