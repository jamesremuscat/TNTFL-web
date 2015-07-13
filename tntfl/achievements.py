from collections import Counter
import datetime


def oncePerPlayer(applies):
    '''
    Decorate an Achievement class's applies() function with oncePerPlayer to limit the achievement
    to a maximum of once per player.
    '''
    def actualApplies(self, player, game, opponent, ladder):
        return applies(self, player, game, opponent, ladder)
    return lambda self, p, g, o, l: False if p in self.players else actualApplies(self, p, g, o, l)


class Achievement(object):

    achievements = []

    def __init__(self):
        self.players = []

    @staticmethod
    def getAllForGame(player, game, opponent, ladder):
        '''
        Identifies all achievements unlocked by player in game against opponent.
        This method should be called AFTER Player.game() has been called with game for BOTH players.
        '''
        theseAchievements = []
        if player.games[-1] == game:
            for clz in Achievement.achievements:
                if clz.applies(player, game, opponent, ladder):
                    theseAchievements.append(clz.__class__)
                    player.achieve(clz.__class__)
                    clz.players.append(player)
        return theseAchievements


class FirstGame(Achievement):
    name = "First Game"
    description = "Enter your first game into the ladder"

    def applies(self, player, game, opponent, ladder):
        return len(player.games) == 1 and player.games[0] == game


class BeatANewbie(Achievement):
    name = "Fresh Blood"
    description = "Claim points from a new player on their first game"

    def applies(self, player, game, opponent, ladder):
        if game.redPlayer == player.name:
            return game.skillChangeToBlue < 0 and len(opponent.games) == 1
        else:
            return game.skillChangeToBlue > 0 and len(opponent.games) == 1


class YellowStripe(Achievement):
    name = "Flawless Victory"
    description = "Beat an opponent 10-0"

    def applies(self, player, game, opponent, ladder):
        if game.redPlayer == player.name:
            return game.redScore == 10 and game.blueScore == 0
        else:
            return game.redScore == 0 and game.blueScore == 10


class MostlyHarmless(Achievement):
    name = "Mostly Harmless"
    description = "Play 100 games"

    def applies(self, player, game, opponent, ladder):
        return len(player.games) == 100


class CommittedCoreFiler(Achievement):
    name = "Committed CoreFiler"
    description = "Play 500 games"

    def applies(self, player, game, opponent, ladder):
        return len(player.games) == 500


class Dangerous(Achievement):
    name = "Dangerous"
    description = "Play 1,000 games"

    def applies(self, player, game, opponent, ladder):
        return len(player.games) == 1000


class Resident(Achievement):
    name = "Resident"
    description = "Play 2,000 games"

    def applies(self, player, game, opponent, ladder):
        return len(player.games) == 2000


class Elite(Achievement):
    name = "Elite"
    description = "Play 10,000 games"

    def applies(self, player, game, opponent, ladder):
        return len(player.games) == 10000


class AgainstTheOdds(Achievement):
    name = "Against the Odds"
    description = "Beat a player 50 or more skillpoints higher than you"

    def applies(self, player, game, opponent, ladder):
        if game.redPlayer == player.name:
            return (game.redScore > game.blueScore) and (player.elo - game.skillChangeToBlue) + 50 <= (opponent.elo + game.skillChangeToBlue)
        else:
            return (game.blueScore > game.redScore) and (player.elo + game.skillChangeToBlue) + 50 <= (opponent.elo - game.skillChangeToBlue)


class TheBest(Achievement):
    name = "The Best"
    description = "Move into first place"

    def applies(self, player, game, opponent, ladder):
        # It would be better if we could query a rankings table or obtain this information from the player
        rank = game.bluePosAfter if player.name == game.bluePlayer else game.redPosAfter
        delta = game.bluePosChange if player.name == game.bluePlayer else game.redPosChange
        return rank == 1 and delta != 0


class TheWorst(Achievement):
    name = "The Worst"
    description = "Move into last place"

    def applies(self, player, game, opponent, ladder):
        delta = game.bluePosChange if player.name == game.bluePlayer else game.redPosChange
        players = sorted([p for p in ladder.players.values() if p.isActive(atTime=game.time)], key=lambda x: x.elo, reverse=True)
        return player == players[-1] and delta != 0


class Improver(Achievement):
    name = "Improver"
    description = "Gain 100 skill points from your lowest point"

    @oncePerPlayer
    def applies(self, player, game, opponent, ladder):
        threshold = player.lowestSkill["skill"] + 100
        delta = game.skillChangeToBlue if player.name == game.bluePlayer else -game.skillChangeToBlue
        return player.elo >= threshold and player.elo - delta < threshold


class Unstable(Achievement):
    name = "Unstable"
    description = "See-saw 10 skill points in consecutive games"
    previousDeltas = {}

    def applies(self, player, game, opponent, ladder):
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

    def applies(self, player, game, opponent, ladder):
        pair = frozenset([player.name, opponent.name])
        Comrades.pairCounts[pair] += 1
        # Each game is counted twice with player/opponent switched, hence need to trigger on 199 and 200
        return 199 <= Comrades.pairCounts[pair] <= 200


class Antichrist(Achievement):
    name = "Antichrist"
    description = "Play a game on 25th December"

    def applies(self, player, game, opponent, ladder):
        d = datetime.datetime.fromtimestamp(game.time)
        return d.month == 12 and d.day == 25


class NightOwl(Achievement):
    name = "Night Owl"
    description = "Play a game between 0000 and 0300 hours"

    def applies(self, player, game, opponent, ladder):
        d = datetime.datetime.fromtimestamp(game.time)
        return d.hour < 3 or (d.hour == 3 and d.minutes == 0 and d.seconds == 0 and d.microseconds == 0)


class Deviant(Achievement):
    name = "Deviant"
    description = "Play a game where != 10 goals are scored"

    def applies(self, player, game, opponent, ladder):
        return game.redScore + game.blueScore != 10


class Dedication(Achievement):
    name = "Dedication"
    description = "Play a game at least once every 60 days for a year"
    sixtyDays = 1000 * 60 * 60 * 24 * 60
    oneYear = 1000 * 60 * 60 * 24 * 365
    streaks = {}

    def applies(self, player, game, opponent, ladder):
        if player.name in Dedication.streaks:
            streak = Dedication.streaks[player.name]
            if game.time - streak[1] <= sixtyDays:
                if game.time - streak[0] >= oneYear:
                    # This should be a one-time achievement. Else needs significant rewrite.
                    return True
                else:
                    Dedication.streaks[player.name] = (streak[0], game.time)
                    return False

            Dedication.streaks[player.name] = (game.time, game.time)
            return False


for clz in Achievement.__subclasses__():
    Achievement.achievements.append(clz())
