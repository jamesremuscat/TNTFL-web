from tntfl.game import Game

class FactChecker(object):
    reportCount = 10    #eg report the 10 most significant games

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
    def applies(self, player, game, opponent, ladder):
        skill = 0
        highestSkill = {"time": 0, "skill": 0}
        for g in [g for g in player.games if g.time <= game.time]:
            skill += g.skillChangeToBlue if g.bluePlayer == player.name else -g.skillChangeToBlue
            if skill > highestSkill['skill']:
                highestSkill['skill'] = skill
                highestSkill['time'] = g.time
        return 'New highest skill.' if highestSkill['time'] == game.time else None

class Significance(FactChecker):
    def getSignificanceIndex(self, player, game):
        for i, g in enumerate(sorted([g for g in player.games if g.time <= game.time], key=lambda g:abs(g.skillChangeToBlue), reverse=True)):
            if g.time == game.time:
                return i
    def applies(self, player, game, opponent, ladder):
        index = self.getSignificanceIndex(player, game)
        if index < self.reportCount:
            if index == 0:
                return "Most significant game."
            return "%s most significant game." % self.ordinal(index + 1)
        return None

class GameNumber(FactChecker):
    def applies(self, player, game, opponent, ladder):
        numGames = len([g for g in player.games if g.time <= game.time])
        if numGames >= 10 and self.isRoundNumber(numGames):
            return "%s game." % self.ordinal(numGames)
        return None

class GoalNumber(FactChecker):
    def applies(self, player, game, opponent, ladder):
        maxGoals = sum([g.blueScore if g.bluePlayer == player.name else g.redScore for g in player.games if g.time <= game.time])
        minGoals = maxGoals - (game.blueScore if game.bluePlayer == player.name else game.redScore)
        for i in xrange(minGoals, maxGoals):
            if i >= 10 and self.isRoundNumber(i):
                return "%s goal." % self.ordinal(i)
        return None

class Streaks(FactChecker):
    def s(self, player, streaks, streakType, currentStreakType, winningLosing):
        if streaks['currentType'] == currentStreakType:
            sortedStreaks = sorted(streaks[streakType], key=lambda s:s.count, reverse=True)
            for i, s in enumerate(sortedStreaks):
                if s.count < streaks['current'].count:
                    if i == 0:
                        return "Longest %s streak." % winningLosing
                    if i < self.reportCount:
                        return "%s longest %s streak." % (self.ordinal(i + 1), winningLosing)
                        #return "Longest %s streak since %s" (winningLosing, Game.formatTime(winStreaks[i + 1].toDate))
            return "Broke %s streak of %d games." % (winningLosing, streaks[streakType][-1].count)
        if len(player.games) >= 2 and len(streaks[streakType]) > 0 and player.games[-2].time == streaks[streakType][-1].toDate and streaks[streakType][-1].count >= 3:
        return None

    def applies(self, player, game, opponent, ladder):
        streaks = player.getAllStreaks(game.time)
        winFact = self.s(player, streaks, 'win', 'wins', 'winning')
        loseFact = self.s(player, streaks, 'lose', 'losses', 'losing')
        return winFact if winFact != None else loseFact

class Pundit(object):
    factCheckers = []

    def __init__(self):
        for clz in FactChecker.__subclasses__():
            self.factCheckers.append(clz())

    def getAllForGame(self, player, game, opponent, ladder):
        facts = []
        for clz in self.factCheckers:
            fact = clz.applies(player, game, opponent, ladder)
            if fact != None:
                facts.append(fact)
        return facts
