

class FactChecker(object):
    pass

class HighestSkill(FactChecker):
    def applies(self, player, game, opponent, ladder):
        return 'New highest skill' if player.highestSkill['time'] == game.time else None

class Significance(FactChecker):
    def getSignificanceIndex(self, player, game):
        for i, g in enumerate(sorted([g for g in player.games], key=lambda g:abs(g.skillChangeToBlue), reverse=True)):
            if g.time == game.time:
                return i
    def applies(self, player, game, opponent, ladder):
        index = self.getSignificanceIndex(player, game)
        if index < 10:
            if index == 0:
                return "Most significant game."
            ordinal = lambda n: "%d%s" % (n,"tsnrhtdd"[(n/10%10!=1)*(n%10<4)*n%10::4])
            return ordinal(index + 1) + " most significant game."
        return None

class GameNumber(FactChecker):
    def applies(self, player, game, opponent, ladder):
        numGames = len([g for g in player.games if g.time <= game.time])
        digits = len(str(numGames))
        order = 1
        for i in range(0, digits - 1):
            order *= 10
        if numGames % order == 0:
            ordinal = lambda n: "%d%s" % (n,"tsnrhtdd"[(n/10%10!=1)*(n%10<4)*n%10::4])
            return ordinal(numGames) + " game."
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
