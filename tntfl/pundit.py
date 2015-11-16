

class FactChecker(object):
    pass

class HighestSkill(FactChecker):
    description = 'New highest skill'
    def applies(self, player, game, ladder):
        return player.highestSkill['time'] == game.time

class Pundit(object):
    factCheckers = []

    def __init__(self):
        for clz in FactChecker.__subclasses__():
            self.factCheckers.append(clz())

    def getAllForGame(self, player, game, ladder):
        facts = []
        for clz in self.factCheckers:
            if clz.applies(player, game, ladder):
                facts.append(clz.__class__)
        return facts
