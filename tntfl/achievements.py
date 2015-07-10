from collections import Counter


class Achievement(object):
    pass

    @staticmethod
    def getAllForGame(player, game, opponent, ladder):
        '''
        Identifies all achievements unlocked by player in game against opponent.
        This method should be called AFTER Player.game() has been called with game for BOTH players.
        '''
        achievements = []
        if player.games[-1] == game:
            for clz in Achievement.__subclasses__():
                if clz.applies(player, game, opponent, ladder):
                    achievements.append(clz)
                    player.achieve(clz)
        return achievements


class FirstGame(Achievement):
    name = "First Game"
    description = "Enter your first game into the ladder"

    @staticmethod
    def applies(player, game, opponent, ladder):
        return len(player.games) == 1 and player.games[0] == game


class BeatANewbie(Achievement):
    name = "Fresh Blood"
    description = "Claim points from a new player on their first game"

    @staticmethod
    def applies(player, game, opponent, ladder):
        if game.redPlayer == player.name:
            return game.skillChangeToBlue < 0 and len(opponent.games) == 1
        else:
            return game.skillChangeToBlue > 0 and len(opponent.games) == 1


class YellowStripe(Achievement):
    name = "Flawless Victory"
    description = "Beat an opponent 10-0"

    @staticmethod
    def applies(player, game, opponent, ladder):
        if game.redPlayer == player.name:
            return game.redScore == 10 and game.blueScore == 0
        else:
            return game.redScore == 0 and game.blueScore == 10


class MostlyHarmless(Achievement):
    name = "Mostly Harmless"
    description = "Play 100 games"

    @staticmethod
    def applies(player, game, opponent, ladder):
        return len(player.games) == 100


class Dangerous(Achievement):
    name = "Dangerous"
    description = "Play 1,000 games"

    @staticmethod
    def applies(player, game, opponent, ladder):
        return len(player.games) == 1000


class Elite(Achievement):
    name = "Elite"
    description = "Play 10,000 games"

    @staticmethod
    def applies(player, game, opponent, ladder):
        return len(player.games) == 10000


class AgainstTheOdds(Achievement):
    name = "Against the Odds"
    description = "Beat a player 50 or more skillpoints higher than you"

    @staticmethod
    def applies(player, game, opponent, ladder):
        if game.redPlayer == player.name:
            return (game.redScore > game.blueScore) and (player.elo - game.skillChangeToBlue) + 50 <= (opponent.elo + game.skillChangeToBlue)
        else:
            return (game.blueScore > game.redScore) and (player.elo + game.skillChangeToBlue) + 50 <= (opponent.elo - game.skillChangeToBlue)


class TheBest(Achievement):
    name = "The Best"
    description = "Move into first place"

    @staticmethod
    def applies(player, game, opponent, ladder):
        # It would be better if we could query a rankings table or obtain this information from the player
        rank = game.bluePosAfter if player.name == game.bluePlayer else game.redPosAfter
        delta = game.bluePosChange if player.name == game.bluePlayer else game.redPosChange
        return rank == 1 and delta != 0


class TheWorst(Achievement):
    name = "The Worst"
    description = "Be in last place"

    @staticmethod
    def applies(player, game, opponent, ladder):
        # It would be better if we could query a rankings table or obtain this information from the player
        rank = game.bluePosAfter if player.name == game.bluePlayer else game.redPosAfter
        # Can't do this, need access to rankings table
        return rank == -1


class Improver(Achievement):
    name = "Improver"
    description = "Gain 100 skill points from your lowest point"

    @staticmethod
    def applies(player, game, opponent, ladder):
        threshold = player.lowestSkill["skill"] + 100
        delta = game.skillChangeToBlue if player.name == game.bluePlayer else -game.skillChangeToBlue
        return player.elo >= threshold and player.elo - delta < threshold


class Unstable(Achievement):
    name = "Unstable"
    description = "See-saw 10 skill points in consecutive games"
    previousDeltas = {}

    @staticmethod
    def applies(player, game, opponent, ladder):
        delta = game.bluePosChange if player.name == game.bluePlayer else game.bluePosChange
        if player.name in Unstable.previousDeltas:
            previousDelta = Unstable.previousDeltas[player.name]
            if (previousDelta <= -10 and delta >= 10) or (previousDelta >= 10 and delta <= -10):
                # Don't care about previousDeltas any more
                return True
        Unstable.previousDeltas[player.name] = delta
        return False


class Comrades(Achievement):
    name = "Comrades"
    description = "Play 100 games against the same opponent"
    pairCounts = Counter()

    @staticmethod
    def applies(player, game, opponent, ladder):
        pair = frozenset([player.name, opponent.name])
        Comrades.pairCounts[pair] += 1
        # Each game is counted twice with player/opponent switched, hence need to trigger on 199 and 200
        return 199 <= Comrades.pairCounts[pair] <= 200
