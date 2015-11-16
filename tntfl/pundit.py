

class FactChecker(object):
    pass

class HighestSkill(FactChecker):
    def applies(self, player, game, opponent, ladder):
        return 'New highest skill' if player.highestSkill['time'] == game.time else None


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
