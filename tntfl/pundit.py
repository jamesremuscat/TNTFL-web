from tntfl.game import Game
import tntfl.templateUtils as utils

class FactChecker(object):
    _reportCount = 10    #eg report the 10 most significant games
    _sharedGames = {}

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
    _skillHistories = {}

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

    def getSignificanceIndex(self, player, game):
        for i, g in enumerate(sorted([g for g in player.games if g.time <= game.time], key=lambda g:abs(g.skillChangeToBlue), reverse=True)):
            if g.time == game.time:
                return i
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

#TODO run once per pair
class GamesAgainst(FactChecker):
    _description = "That was %s and %s's %s encounter."

    def getFact(self, player, game, opponent):
        sharedGames = self.getSharedGames(player, opponent)
        numGames = len([g for g in sharedGames if g.time <= game.time])
        if numGames >= 10 and self.isRoundNumber(numGames):
            return self._description % (player.name, opponent.name, self.ordinal(numGames))
        return None

class Goals(FactChecker):
    _description = "That game featured %s's %s goal."

    def getFact(self, player, game, opponent):
        totalGoals = sum([g.blueScore if g.bluePlayer == player.name else g.redScore for g in player.games if g.time <= game.time])
        goalsInGame = (game.blueScore if game.bluePlayer == player.name else game.redScore)
        if goalsInGame > 0:
            prevGoalTotal = totalGoals - goalsInGame
            for i in xrange(prevGoalTotal + 1, totalGoals + 1):
                if i >= 10 and self.isRoundNumber(i):
                    return self._description % (player.name, self.ordinal(i))
        return None

class GoalsAgainst(FactChecker):
    _description = "That game featured %s's %s goal against %s."

    def getFact(self, player, game, opponent):
        sharedGames = self.getSharedGames(player, opponent)
        totalGoals = sum([g.blueScore if g.bluePlayer == player.name else g.redScore for g in sharedGames if g.time <= game.time])
        goalsInGame = (game.blueScore if game.bluePlayer == player.name else game.redScore)
        if goalsInGame > 0:
            prevGoalTotal = totalGoals - goalsInGame
            for i in xrange(prevGoalTotal + 1, totalGoals + 1):
                if i >= 10 and self.isRoundNumber(i):
                    return self._description % (player.name, self.ordinal(i), opponent.name)
        return None

class Wins(FactChecker):
    _description = "That was %s's %s win."

    def getFact(self, player, game, opponent):
        numWins = len([g for g in player.games if g.time <= game.time and player.wonGame(g)])
        if numWins >= 10 and self.isRoundNumber(numWins) and player.wonGame(game):
            return self._description % (player.name, self.ordinal(numWins))
        return None

class WinsAgainst(FactChecker):
    _description = "That was %s's %s win against %s."

    def getFact(self, player, game, opponent):
        sharedGames = self.getSharedGames(player, opponent)
        numWins = len([g for g in sharedGames if g.time <= game.time and player.wonGame(g)])
        if numWins >= 10 and self.isRoundNumber(numWins) and player.wonGame(game):
            return self._description % (player.name, self.ordinal(numWins), opponent.name)
        return None

class Streaks(FactChecker):
    _description = "After that game %s was on their %slongest %s streak."
    _descriptionBroken = "%s broke their %s streak of %d games."

    def _getStreakTypeText(self, winning):
        return 'winning' if winning else 'losing'

    def _streakSignificance(self, player, streaks, game):
        if streaks['current'].count >= 3:
            curStreakType = self._getStreakTypeText(streaks['current'].win)
            prevStreaks = [s for s in streaks['past'] if s.win == streaks['current'].win]
            if len(prevStreaks) > 0:
                #find the current streak's significance
                sortedStreaks = sorted(prevStreaks, key=lambda s:s.count, reverse=True)
                for i, s in enumerate(sortedStreaks):
                    if i == 0 and s.count < streaks['current'].count:
                        return self._description % (player.name, "", curStreakType)
                    elif s.count < streaks['current'].count:
                        return self._description % (player.name, "%s " % self.ordinal(i + 1), curStreakType)
                    elif i > self._reportCount:
                        return None
                #not found, is "least significant"
                return self._description % (player.name, "%s " % self.ordinal(len(prevStreaks) + 1), curStreakType)
            else:
                return self._description % (player.name, "", curStreakType)
        return None

    def _brokenStreak(self, player, streaks, game):
        if streaks['current'].count < 2 and len(streaks['past']) > 0:
            prevStreak = streaks['past'][-1]
            prevStreakType = self._getStreakTypeText(prevStreak.win)
            prevGame = None
            for i, g in enumerate(player.games):
                if g.time == game.time:
                    prevGame = player.games[i - 1]
                    break
            if prevStreak.toDate == prevGame.time and prevStreak.count >= 3:
                return self._descriptionBroken % (player.name, prevStreakType, prevStreak.count)
        return None

    def getFact(self, player, game, opponent):
        streaks = player.getAllStreaks(player.games, game.time)
        cur = self._streakSignificance(player, streaks, game)
        return cur if cur is not None else self._brokenStreak(player, streaks, game)

class Pundit(object):
    _factCheckers = []

    def __init__(self):
        for clz in FactChecker.__subclasses__():
            self._factCheckers.append(clz())

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
