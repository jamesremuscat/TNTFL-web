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

class GamesAgainst(FactChecker):
    _pairs = [] # run once per pair
    def getFact(self, player, game, opponent):
        sharedGames = utils.getSharedGames(player, opponent)
        numGames = len([g for g in sharedGames if g.time <= game.time])
        pairing = {player.name, opponent.name}
        if numGames >= 10 and self.isRoundNumber(numGames) and pairing not in self._pairs:
            self._pairs.append(pairing)
            return "That was the %s and %s's %s encounter." % (player.name, opponent.name, self.ordinal(numGames))
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
    def s(self, player, streaks, streakType, currentStreakType, winningLosing):
        if streaks['currentType'] == currentStreakType:
            sortedStreaks = sorted(streaks[streakType], key=lambda s:s.count, reverse=True)
            for i, s in enumerate(sortedStreaks):
                if s.count < streaks['current'].count:
                    if i == 0:
                        return "After that game %s was on their longest %s streak." % (player.name, winningLosing)
                    if i < self._reportCount:
                        return "After that game %s was on their %s longest %s streak." % (player.name, self.ordinal(i + 1), winningLosing)
                        #return "Longest %s streak since %s" (winningLosing, Game.formatTime(winStreaks[i + 1].toDate))
        if len(player.games) >= 2 and len(streaks[streakType]) > 0 and player.games[-2].time == streaks[streakType][-1].toDate and streaks[streakType][-1].count >= 3:
            return "%s broke their %s streak of %d games." % (player.name, winningLosing, streaks[streakType][-1].count)
        return None

    def getFact(self, player, game, opponent):
        streaks = player.getAllStreaks(player.games, game.time)
        winFact = self.s(player, streaks, 'win', 'wins', 'winning')
        loseFact = self.s(player, streaks, 'lose', 'losses', 'losing')
        return winFact if winFact != None else loseFact

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
