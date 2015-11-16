from tntfl.game import Game

class FactChecker(object):
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
        if index < 10:
            if index == 0:
                return "Most significant game."
            return self.ordinal(index + 1) + " most significant game."
        return None

class GameNumber(FactChecker):
    def applies(self, player, game, opponent, ladder):
        numGames = len([g for g in player.games if g.time <= game.time])
        if numGames >= 10 and self.isRoundNumber(numGames):
            return self.ordinal(numGames) + " game."
        return None

class GoalNumber(FactChecker):
    def applies(self, player, game, opponent, ladder):
        maxGoals = sum([g.blueScore if g.bluePlayer == player.name else g.redScore for g in player.games if g.time <= game.time])
        minGoals = maxGoals - (game.blueScore if game.bluePlayer == player.name else game.redScore)
        for i in xrange(minGoals, maxGoals):
            if i >= 10 and self.isRoundNumber(i):
                return self.ordinal(i) + " goal."
        return None

class Streaks(FactChecker):
    def applies(self, player, game, opponent, ladder):
        streaks = player.getAllStreaks(game.time)
        if streaks['currentType'] == 'wins':
            winStreaks = sorted(streaks['win'], key=lambda s:s.count, reverse=True)
            for i, s in enumerate(winStreaks):
                if s.count < streaks['current'].count:
                    if i == 0:
                        return "Longest winning streak."
                    if i < len(winStreaks) / 10:
                        return self.ordinal(i + 1) + " longest winning streak."
                        #return "Longest winning streak since " + Game.formatTime(winStreaks[i + 1].toDate)
                    return None
        elif streaks['currentType'] == 'losses':
            loseStreaks = sorted(streaks['lose'], key=lambda s:s.count, reverse=True)
            for i, s in enumerate(loseStreaks):
                if s.count < streaks['current'].count:
                    if i == 0:
                        return "Longest losing streak."
                    if i < len(loseStreaks) / 10:
                        return self.ordinal(i + 1) + " longest losing streak."
                        #return "Longest losing streak since " + Game.formatTime(loseStreaks[i + 1].toDate)
                    return None
        return None

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
