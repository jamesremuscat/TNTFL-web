from tntfl.game import Game
import tntfl.templateUtils as utils

class FactChecker(object):
    _reportCount = 10    #eg report the 10 most significant games

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

class HighestSkill(FactChecker):
    def getFact(self, player, game, opponent):
        skill = 0
        highestSkill = {"time": 0, "skill": 0}
        for g in [g for g in player.games if g.time <= game.time]:
            skill += g.skillChangeToBlue if g.bluePlayer == player.name else -g.skillChangeToBlue
            if skill > highestSkill['skill']:
                highestSkill['skill'] = skill
                highestSkill['time'] = g.time
        return ('That game puts %s on their highest ever skill.' % (player.name)) if highestSkill['time'] == game.time else None

class SignificantGames(FactChecker):
    def getSignificanceIndex(self, player, game):
        for i, g in enumerate(sorted([g for g in player.games if g.time <= game.time], key=lambda g:abs(g.skillChangeToBlue), reverse=True)):
            if g.time == game.time:
                return i
    def getFact(self, player, game, opponent):
        index = self.getSignificanceIndex(player, game)
        if index < self._reportCount:
            if index == 0:
                return "That was %s's most significant game." % (player.name)
            return "That was %s's %s most significant game." % (player.name, self.ordinal(index + 1))
        return None

class Games(FactChecker):
    def getFact(self, player, game, opponent):
        numGames = len([g for g in player.games if g.time <= game.time])
        if numGames >= 10 and self.isRoundNumber(numGames):
            return "That was %s's %s game." % (player.name, self.ordinal(numGames))
        return None

#TODO run once per pair
class GamesAgainst(FactChecker):
    def getFact(self, player, game, opponent):
        sharedGames = utils.getSharedGames(player, opponent)
        numGames = len([g for g in sharedGames if g.time <= game.time])
        if numGames >= 10 and self.isRoundNumber(numGames):
            return "That was %s and %s's %s encounter." % (player.name, opponent.name, self.ordinal(numGames))
        return None

class Goals(FactChecker):
    def getFact(self, player, game, opponent):
        totalGoals = sum([g.blueScore if g.bluePlayer == player.name else g.redScore for g in player.games if g.time <= game.time])
        goalsInGame = (game.blueScore if game.bluePlayer == player.name else game.redScore)
        if goalsInGame > 0:
            prevGoalTotal = totalGoals - goalsInGame
            for i in xrange(prevGoalTotal + 1, totalGoals + 1):
                if i >= 10 and self.isRoundNumber(i):
                    return "That game featured %s's %s goal." % (player.name, self.ordinal(i))
        return None

class GoalsAgainst(FactChecker):
    def getFact(self, player, game, opponent):
        sharedGames = utils.getSharedGames(player, opponent)
        totalGoals = sum([g.blueScore if g.bluePlayer == player.name else g.redScore for g in sharedGames if g.time <= game.time])
        goalsInGame = (game.blueScore if game.bluePlayer == player.name else game.redScore)
        if goalsInGame > 0:
            prevGoalTotal = totalGoals - goalsInGame
            for i in xrange(prevGoalTotal + 1, totalGoals + 1):
                if i >= 10 and self.isRoundNumber(i):
                    return "That game featured %s's %s goal against %s." % (player.name, self.ordinal(i), opponent.name)
        return None

class Wins(FactChecker):
    def getFact(self, player, game, opponent):
        numWins = len([g for g in player.games if g.time <= game.time and player.wonGame(g)])
        if numWins >= 10 and self.isRoundNumber(numWins) and player.wonGame(game):
            return "That was %s's %s win." % (player.name, self.ordinal(numWins))
        return None

class WinsAgainst(FactChecker):
    def getFact(self, player, game, opponent):
        sharedGames = utils.getSharedGames(player, opponent)
        numWins = len([g for g in sharedGames if g.time <= game.time and player.wonGame(g)])
        if numWins >= 10 and self.isRoundNumber(numWins) and player.wonGame(game):
            return "That was %s's %s win against %s." % (player.name, self.ordinal(numWins), opponent.name)
        return None

class Streaks(FactChecker):
    def _streakSignificance(self, player, streaks, game):
        if streaks['current'].count >= 3:
            curStreakType = 'winning' if streaks['current'].win else 'losing'
            prevStreaks = [s for s in streaks['past'] if s.win == streaks['current'].win]
            if len(prevStreaks) > 0:
                #find the current streak's significance
                sortedStreaks = sorted(prevStreaks, key=lambda s:s.count, reverse=True)
                for i, s in enumerate(sortedStreaks):
                    if i == 0 and s.count < streaks['current'].count:
                        return "After that game %s was on their longest %s streak." % (player.name, curStreakType)
                    elif s.count < streaks['current'].count:
                        return "After that game %s was on their %s longest %s streak." % (player.name, self.ordinal(i + 1), curStreakType)
                    elif i > self._reportCount:
                        return None
                #not found, "least significant"
                return "After that game %s was on their %s longest %s streak." % (player.name, self.ordinal(len(prevStreaks) + 1), curStreakType)
            else:
                return "After that game %s was on their longest %s streak." % (player.name, curStreakType)
        return None

    def _brokenStreak(self, player, streaks, game):
        if streaks['current'].count < 2 and len(streaks['past']) > 0:
            prevStreak = streaks['past'][-1]
            prevGame = None
            for i, g in enumerate(player.games):
                if g.time == game.time:
                    prevGame = player.games[i - 1]
                    break
            if prevStreak.toDate == prevGame.time:
                return "%s broke their %s streak of %d games." % (player.name, 'winning' if prevStreak.win else 'losing', prevStreak.count)
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
