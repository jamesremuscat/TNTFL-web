from tntfl.game import Game
from tntfl.player import Streak
import tntfl.templateUtils as utils

class FactChecker(object):
    _reportCount = 10    #eg report the 10 most significant games

    def __init__(self):
        self._sharedGames = {}

    def ordinal(self, n):
        return "%d%s" % (n,"tsnrhtdd"[(n/10%10!=1)*(n%10<4)*n%10::4])

    def isRoundNumber(self, n):
        digits = len(str(n))
        order = 1
        for i in range(0, digits - 1):
            order *= 10
        if n % order == 0:
            return True
        return False

    def getSharedGames(self, player1, player2):
        if (player1, player2) in self._sharedGames:
            return self._sharedGames[(player1, player2)]
        elif (player2, player1) in self._sharedGames:
            return self._sharedGames[(player2, player1)]
        else:
            self._sharedGames[(player1, player2)] = utils.getSharedGames(player1, player2)
            return self._sharedGames[(player1, player2)]

class HighestSkill(FactChecker):
    _description = 'That game puts %s on their highest ever skill.'

    def __init__(self):
        FactChecker.__init__(self)
        self._skillHistories = {}

    def _getPlayerHistory(self, player):
        if player.name not in self._skillHistories:
            skill = 0
            highestSkill = {"time": 0, "skill": 0}
            history = [0]
            for g in player.games:
                skill += g.skillChangeToBlue if g.bluePlayer == player.name else -g.skillChangeToBlue
                if skill > highestSkill['skill']:
                    highestSkill['skill'] = skill
                    highestSkill['time'] = g.time
                    history.append(g.time)
            self._skillHistories[player.name] = history
        return self._skillHistories[player.name]

    def getFact(self, player, game, opponent):
        curHistory = self._getPlayerHistory(player)
        for time in curHistory:
            if time == game.time:
                return self._description % (player.name)
        return None

class SignificantGames(FactChecker):
    _description = "That was %s's %smost significant game."

    def __init__(self):
        FactChecker.__init__(self)
        self._significances = {}

    def getSignificanceIndex(self, player, game):
        if player.name not in self._significances:
            self._significances[player.name] = [g.time for g in sorted([g for g in player.games], key=lambda g:abs(g.skillChangeToBlue), reverse=True)]
        significances = self._significances[player.name]
        return significances.index(game.time)

    def getFact(self, player, game, opponent):
        index = self.getSignificanceIndex(player, game)
        if index < self._reportCount:
            ordinal = ""
            if index > 0:
                ordinal = "%s " % self.ordinal(index + 1)
            return self._description % (player.name, ordinal)
        return None

class Games(FactChecker):
    _description = "That was %s's %s game."

    def getFact(self, player, game, opponent):
        numGames = len([g for g in player.games if g.time <= game.time])
        if numGames >= 10 and self.isRoundNumber(numGames):
            return self._description % (player.name, self.ordinal(numGames))
        return None

class GamesAgainst(FactChecker):
    _description = "That was %s and %s's %s encounter."

    def __init__(self):
        FactChecker.__init__(self)
        self._pairings = {} #to avoid repeating this fact in a game

    def getFact(self, player, game, opponent):
        key = None
        if (player, opponent) in self._pairings:
            key = (player, opponent)
        elif (opponent, player) in self._pairings:
            key = (opponent, player)
        else:
            key = (player, opponent)
            self._pairings[key] = []
        sharedGames = self.getSharedGames(player, opponent)
        numGames = len([g for g in sharedGames if g.time <= game.time])
        if numGames >= 10 and self.isRoundNumber(numGames) and numGames not in self._pairings[key]:
            self._pairings[key].append(numGames)
            return self._description % (player.name, opponent.name, self.ordinal(numGames))
        return None

class Goals(FactChecker):
    _description = "That game featured %s's %s goal."

    def __init__(self):
        FactChecker.__init__(self)

    def getFact(self, player, game, opponent):
        ordinal = self._getGoalsOrdinal(player, game, opponent, player.games)
        return self._description % (player.name, ordinal) if ordinal is not None else None

    def _getGoalsOrdinal(self, player, game, opponent, games):
        prevGoalTotal = sum([g.blueScore if g.bluePlayer == player.name else g.redScore for g in games if g.time < game.time])
        goalsInGame = game.blueScore if game.bluePlayer == player.name else game.redScore
        for i in xrange(prevGoalTotal + 1, prevGoalTotal + goalsInGame + 1):
            if i >= 10 and self.isRoundNumber(i):
                return self.ordinal(i)
        return None

class GoalsAgainst(Goals):
    _description = "That game featured %s's %s goal against %s."

    def __init__(self):
        Goals.__init__(self)

    def getFact(self, player, game, opponent):
        if (game.redPlayer == player.name or game.redPlayer == opponent.name) and (game.bluePlayer == player.name or game.bluePlayer == opponent.name):
            sharedGames = self.getSharedGames(player, opponent)
            ordinal = self._getGoalsOrdinal(player, game, opponent, sharedGames)
            return self._description % (player.name, ordinal, opponent.name) if ordinal is not None else None
        return None

class Wins(FactChecker):
    _description = "That was %s's %s win."

    def __init__(self):
        FactChecker.__init__(self)
        self._wins = {}

    def _getWinsOrdinal(self, player, game, games):
        numWins = len([g for g in games if g.time <= game.time ])
        if numWins >= 10 and self.isRoundNumber(numWins) and player.wonGame(game):
            return self.ordinal(numWins)

    def getFact(self, player, game, opponent):
        if player.name not in self._wins:
            self._wins[player.name] = [g for g in player.games if player.wonGame(g)]
        ordinal = self._getWinsOrdinal(player, game, self._wins[player.name])
        return self._description % (player.name, ordinal) if ordinal is not None else None

class WinsAgainst(Wins):
    _description = "That was %s's %s win against %s."

    def __init__(self):
        FactChecker.__init__(self)
        self._winsAgainst = {}

    def getFact(self, player, game, opponent):
        sharedGames = self.getSharedGames(player, opponent)
        if player.name not in self._winsAgainst:
            self._winsAgainst[player.name] = {}
        playerWins = self._winsAgainst[player.name]
        if opponent.name not in playerWins:
            self._winsAgainst[player.name][opponent.name] = [g for g in sharedGames if player.wonGame(g)]
            playerWins = self._winsAgainst[player.name]
        ordinal = self._getWinsOrdinal(player, game, playerWins[opponent.name])
        return self._description % (player.name, ordinal, opponent.name) if ordinal is not None else None

class Streaks(FactChecker):
    _description = "After that game %s was on their %slongest %s streak."
    _descriptionBroken = "%s broke their %s streak of %d games."

    def __init__(self):
        FactChecker.__init__(self)
        self._streaks = {}

    def _getStreakTypeText(self, winning):
        return 'winning' if winning else 'losing'

    def _splitStreak(self, streak, time):
        split = Streak()
        split.gameTimes = [g for g in streak.gameTimes if g <= time]
        split.win = streak.win
        return split

    def _rewind(self, streaks, time):
        rewound = {'past': [], 'current':Streak()}
        for streak in streaks['past']:
            if streak.toDate < time:
                rewound['past'].append(streak)
            elif streak.fromDate < time:
                rewound['current'] = self._splitStreak(streak, time)
            else:
                return rewound
        if streaks['current'].count > 0 and streaks['current'].fromDate < time:
            rewound['current'] = self._splitStreak(streaks['current'], time)
        return rewound

    #returns 1-indexed significance, 0 = insignificant
    def _getStreakSignificance(self, player, streaks):
        if streaks['current'].count >= 3:
            prevStreaks = [s for s in streaks['past'] if s.win == streaks['current'].win]
            if len(prevStreaks) > 0:
                #find the current streak's significance
                sortedStreaks = sorted(prevStreaks, key=lambda s:s.count, reverse=True)
                for i, s in enumerate(sortedStreaks):
                    if s.count < streaks['current'].count:
                        return i + 1
                    elif i >= self._reportCount:
                        return 0
                #not found, is "least significant"
                return len(prevStreaks) + 1
            else:
                return 1
        return 0

    def _getBrokenStreak(self, player, streaks, game):
        if streaks['current'].count < 2 and len(streaks['past']) > 0 and streaks['past'][-1].count >= 3:
            prevStreak = streaks['past'][-1]
            for i, g in enumerate(player.games):
                if g.time == game.time and prevStreak.toDate == player.games[i - 1].time:
                    return prevStreak
        return None

    def getFact(self, player, game, opponent):
        if player.name not in self._streaks:
            self._streaks[player.name] = player.getAllStreaks(player.games)
        streaks = self._rewind(self._streaks[player.name], game.time)
        significance = self._getStreakSignificance(player, streaks)
        if significance > 0:
            return self._description % (player.name, "%s " % self.ordinal(significance) if significance > 1 else "", self._getStreakTypeText(streaks['current'].win))
        else:
            broken = self._getBrokenStreak(player, streaks, game)
            return self._descriptionBroken % (player.name, self._getStreakTypeText(broken.win), broken.count) if broken is not None else None

class Pundit(object):
    _factCheckers = []

    def _addSubClasses(self, clz):
        for sclz in clz.__subclasses__():
            self._factCheckers.append(sclz())
            self._addSubClasses(sclz)

    def __init__(self):
        self._addSubClasses(FactChecker)

    def getAllForGame(self, player, game, opponent):
        facts = []
        for clz in self._factCheckers:
            fact = clz.getFact(player, game, opponent)
            if fact != None:
                facts.append(fact)
        return facts

    def anyComment(self, player, game, opponent):
        for clz in self._factCheckers:
            fact = clz.getFact(player, game, opponent)
            if fact != None:
                return True
            fact = clz.getFact(opponent, game, player)
            if fact != None:
                return True
        return False
