class Achievement(object):
    pass

    @staticmethod
    def getAllForGame(player, game, opponent):
        '''
        Identifies all achievements unlocked by player in game against opponent.
        This method should be called AFTER Player.game() has been called with game for BOTH players.
        '''
        achievements = []
        if player.games[-1] == game:
            for clz in Achievement.__subclasses__():
                if clz.applies(player, game, opponent):
                    achievements.append(clz)
        return achievements


class FirstGame(Achievement):
    name = "First Game"
    description = "Enter your first game into the ladder"

    @staticmethod
    def applies(player, game, opponent):
        return len(player.games) == 1 and player.games[0] == game


class BeatANewbie(Achievement):
    name = "Fresh Blood"
    description = "Claim points from a new player on their first game"

    @staticmethod
    def applies(player, game, opponent):
        if game.redPlayer == player.name:
            return game.skillChangeToBlue < 0 and len(opponent.games) == 1
        else:
            return game.skillChangeToBlue > 0 and len(opponent.games) == 1


class YellowStripe(Achievement):
    name = "Flawless Victory"
    description = "Beat an opponent 10-0"

    @staticmethod
    def applies(player, game, opponent):
        if game.redPlayer == player.name:
            return game.redScore == 10 and game.blueScore == 0
        else:
            return game.redScore == 0 and game.blueScore == 10


class MostlyHarmless(Achievement):
    name = "Mostly Harmless"
    description = "Play 100 games"

    @staticmethod
    def applies(player, game, opponent):
        return len(player.games) == 100


class Dangerous(Achievement):
    name = "Dangerous"
    description = "Play 1,000 games"

    @staticmethod
    def applies(player, game, opponent):
        return len(player.games) == 1000


class Elite(Achievement):
    name = "Elite"
    description = "Play 10,000 games"

    @staticmethod
    def applies(player, game, opponent):
        return len(player.games) == 10000
