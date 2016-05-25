import unittest
import os
from tntfl.ladder import TableFootballLadder
from tntfl.player import Player
from tntfl.game import Game
from tntfl.pundit import *

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

def bulkAppend(player, playerScore, opponent, opponentScore, startTime, count):
    for i in range(startTime, startTime + count):
        game = Game(player.name, playerScore, opponent.name, opponentScore, i)
        player.games.append(game)
        opponent.games.append(game)

class Unit(unittest.TestCase):
    def testHighestSkill(self):
        player = self._create()
        sut = HighestSkill()
        result = sut.getFact(player, player.games[0], None)
        self.assertIsNone(result)
        result = sut.getFact(player, player.games[1], None)
        self.assertEqual(result, 'That game puts foo on their highest ever skill.')
        result = sut.getFact(player, player.games[2], None)
        self.assertIsNone(result)
        result = sut.getFact(player, player.games[3], None)
        self.assertIsNone(result)

    def testSignificantGames(self):
        player = self._create()
        sut = SignificantGames()
        result = sut.getFact(player, player.games[0], None)
        self.assertEqual(result, "That was foo's 3rd most significant game.")
        result = sut.getFact(player, player.games[1], None)
        self.assertEqual(result, "That was foo's 2nd most significant game.")
        result = sut.getFact(player, player.games[2], None)
        self.assertEqual(result, "That was foo's most significant game.")
        result = sut.getFact(player, player.games[3], None)
        self.assertEqual(result, "That was foo's 4th most significant game.")

    def testGames(self):
        player = Player("foo")
        opponent = Player("bar")
        bulkAppend(player, 6, opponent, 4, 0, 1002)

        sut = Games()
        result = sut.getFact(player, player.games[0], None)
        self.assertIsNone(result)
        result = sut.getFact(player, player.games[1], None)
        self.assertIsNone(result)
        result = sut.getFact(player, player.games[10 -1], None)
        self.assertEqual(result, "That was foo's 10th game.")
        result = sut.getFact(player, player.games[12], None)
        self.assertIsNone(result)
        result = sut.getFact(player, player.games[100 -1], None)
        self.assertEqual(result, "That was foo's 100th game.")
        result = sut.getFact(player, player.games[110 -1], None)
        self.assertIsNone(result)
        result = sut.getFact(player, player.games[700 -1], None)
        self.assertEqual(result, "That was foo's 700th game.")
        result = sut.getFact(player, player.games[770 -1], None)
        self.assertIsNone(result)
        result = sut.getFact(player, player.games[1000 -1], None)
        self.assertEqual(result, "That was foo's 1000th game.")
        result = sut.getFact(player, player.games[1001], None)
        self.assertIsNone(result)

    def testGamesAgainst(self):
        player = self._create()
        opponent = Player("baz")
        bulkAppend(player, 6, opponent, 4, 5, 1002)

        sut = GamesAgainst()
        result = sut.getFact(player, player.games[0], opponent)
        self.assertIsNone(result)
        result = sut.getFact(player, player.games[1], opponent)
        self.assertIsNone(result)
        result = sut.getFact(player, player.games[10 +4-1], opponent)
        self.assertEqual(result, "That was foo and baz's 10th encounter.")
        result = sut.getFact(player, player.games[12], opponent)
        self.assertIsNone(result)
        result = sut.getFact(player, player.games[100 +4-1], opponent)
        self.assertEqual(result, "That was foo and baz's 100th encounter.")
        result = sut.getFact(player, player.games[110 +4-1], opponent)
        self.assertIsNone(result)
        result = sut.getFact(player, player.games[700 +4-1], opponent)
        self.assertEqual(result, "That was foo and baz's 700th encounter.")
        result = sut.getFact(player, player.games[770 +4-1], opponent)
        self.assertIsNone(result)
        result = sut.getFact(player, player.games[1000 +4-1], opponent)
        self.assertEqual(result, "That was foo and baz's 1000th encounter.")
        result = sut.getFact(player, player.games[1001], opponent)
        self.assertIsNone(result)

    def testGamesAgainstSingleReport(self):
        player = Player("foo")
        opponent = Player("baz")
        bulkAppend(player, 6, opponent, 4, 0, 1002)

        sut = GamesAgainst()
        result = sut.getFact(player, player.games[10 -1], opponent)
        self.assertEqual(result, "That was foo and baz's 10th encounter.")
        result = sut.getFact(opponent, player.games[10 -1], player)
        self.assertIsNone(result)
        result = sut.getFact(opponent, player.games[700 -1], player)
        self.assertEqual(result, "That was baz and foo's 700th encounter.")
        result = sut.getFact(player, player.games[700 -1], opponent)
        self.assertIsNone(result)

    def testGoals(self):
        player = Player("foo")
        opponent = Player("bar")
        bulkAppend(player, 5, opponent, 5, 0, 1002)
        sut = Goals()
        result = sut.getFact(player, player.games[0], None)
        self.assertIsNone(result)
        result = sut.getFact(player, player.games[1], None)
        self.assertEqual(result, "That game featured foo's 10th goal.")
        result = sut.getFact(player, player.games[10 -1], None)
        self.assertEqual(result, "That game featured foo's 50th goal.")
        result = sut.getFact(player, player.games[12], None)
        self.assertIsNone(result)
        result = sut.getFact(player, player.games[100 -1], None)
        self.assertEqual(result, "That game featured foo's 500th goal.")
        result = sut.getFact(player, player.games[110 -1], None)
        self.assertIsNone(result)
        result = sut.getFact(player, player.games[700 -1], None)
        self.assertIsNone(result)
        result = sut.getFact(player, player.games[770 -1], None)
        self.assertIsNone(result)
        result = sut.getFact(player, player.games[1000 -1], None)
        self.assertEqual(result, "That game featured foo's 5000th goal.")
        result = sut.getFact(player, player.games[1001], None)
        self.assertIsNone(result)

    def testGoalsFirst10(self):
        player = Player("foo")
        opponent = Player("bar")
        bulkAppend(player, 1, opponent, 9, 0, 11)

        sut = Goals()
        result = sut.getFact(player, player.games[8], None)
        self.assertIsNone(result)
        result = sut.getFact(player, player.games[9], None)
        self.assertEqual(result, "That game featured foo's 10th goal.")
        result = sut.getFact(player, player.games[10], None)
        self.assertIsNone(result)

    def testGoalsThenNone(self):
        player = Player("foo")
        opponent = Player("bar")
        bulkAppend(player, 5, opponent, 5, 0, 10)
        player.games.append(Game(player.name, 0, opponent.name, 10, 10))

        sut = Goals()
        result = sut.getFact(player, player.games[9], None)
        self.assertEqual(result, "That game featured foo's 50th goal.")
        result = sut.getFact(player, player.games[10], None)
        self.assertIsNone(result)

    def testGoalsAgainst(self):
        player = self._create()
        opponent = Player("baz")
        bulkAppend(player, 5, opponent, 5, 5, 1002)

        sut = GoalsAgainst()
        result = sut.getFact(player, player.games[0], opponent)
        self.assertIsNone(result)
        result = sut.getFact(player, player.games[1 +4], opponent)
        self.assertEqual(result, "That game featured foo's 10th goal against baz.")
        result = sut.getFact(player, player.games[10 +4-1], opponent)
        self.assertEqual(result, "That game featured foo's 50th goal against baz.")
        result = sut.getFact(player, player.games[12], opponent)
        self.assertIsNone(result)
        result = sut.getFact(player, player.games[100 +4-1], opponent)
        self.assertEqual(result, "That game featured foo's 500th goal against baz.")
        result = sut.getFact(player, player.games[110 +4-1], opponent)
        self.assertIsNone(result)
        result = sut.getFact(player, player.games[700 +4-1], opponent)
        self.assertIsNone(result)
        result = sut.getFact(player, player.games[770 +4-1], opponent)
        self.assertIsNone(result)
        result = sut.getFact(player, player.games[1000 +4-1], opponent)
        self.assertEqual(result, "That game featured foo's 5000th goal against baz.")
        result = sut.getFact(player, player.games[1001], opponent)
        self.assertIsNone(result)

    def testGoalsAgainstThenNone(self):
        player = Player("foo")
        opponent = Player("bar")
        bulkAppend(player, 5, opponent, 5, 0, 10)
        game = Game(player.name, 0, opponent.name, 10, 10)
        player.games.append(game)
        opponent.games.append(game)

        sut = GoalsAgainst()
        result = sut.getFact(player, player.games[9], opponent)
        self.assertEqual(result, "That game featured foo's 50th goal against bar.")
        result = sut.getFact(player, player.games[10], opponent)
        self.assertIsNone(result)

    def testWins(self):
        player = Player("foo")
        opponent = Player("bar")
        bulkAppend(player, 6, opponent, 4, 0, 1002)

        sut = Wins()
        result = sut.getFact(player, player.games[0], None)
        self.assertIsNone(result)
        result = sut.getFact(player, player.games[1], None)
        self.assertIsNone(result)
        result = sut.getFact(player, player.games[10 -1], None)
        self.assertEqual(result, "That was foo's 10th win.")
        result = sut.getFact(player, player.games[12], None)
        self.assertIsNone(result)
        result = sut.getFact(player, player.games[100 -1], None)
        self.assertEqual(result, "That was foo's 100th win.")
        result = sut.getFact(player, player.games[110 -1], None)
        self.assertIsNone(result)
        result = sut.getFact(player, player.games[700 -1], None)
        self.assertEqual(result, "That was foo's 700th win.")
        result = sut.getFact(player, player.games[770 -1], None)
        self.assertIsNone(result)
        result = sut.getFact(player, player.games[1000 -1], None)
        self.assertEqual(result, "That was foo's 1000th win.")
        result = sut.getFact(player, player.games[1001], None)
        self.assertIsNone(result)

    def testWinsThenDraw(self):
        player = Player("foo")
        opponent = Player("bar")
        bulkAppend(player, 6, opponent, 4, 0, 10)
        player.games.append(Game(player.name, 5, opponent.name, 5, 10))

        sut = Wins()
        result = sut.getFact(player, player.games[9], None)
        self.assertEqual(result, "That was foo's 10th win.")
        result = sut.getFact(player, player.games[10], None)
        self.assertIsNone(result)

    def testWinsAgainst(self):
        player = self._create()
        opponent = Player("baz")
        bulkAppend(player, 6, opponent, 4, 5, 1002)

        sut = WinsAgainst()
        result = sut.getFact(player, player.games[0], opponent)
        self.assertIsNone(result)
        result = sut.getFact(player, player.games[1], opponent)
        self.assertIsNone(result)
        result = sut.getFact(player, player.games[10 +4-1], opponent)
        self.assertEqual(result, "That was foo's 10th win against baz.")
        result = sut.getFact(player, player.games[12], opponent)
        self.assertIsNone(result)
        result = sut.getFact(player, player.games[100 +4-1], opponent)
        self.assertEqual(result, "That was foo's 100th win against baz.")
        result = sut.getFact(player, player.games[110 +4-1], opponent)
        self.assertIsNone(result)
        result = sut.getFact(player, player.games[700 +4-1], opponent)
        self.assertEqual(result, "That was foo's 700th win against baz.")
        result = sut.getFact(player, player.games[770 +4-1], opponent)
        self.assertIsNone(result)
        result = sut.getFact(player, player.games[1000 +4-1], opponent)
        self.assertEqual(result, "That was foo's 1000th win against baz.")
        result = sut.getFact(player, player.games[1001], opponent)
        self.assertIsNone(result)

    def testWinsAgainstThenDraw(self):
        player = Player("foo")
        opponent = Player("bar")
        bulkAppend(player, 6, opponent, 4, 0, 10)
        game = Game(player.name, 5, opponent.name, 5, 10)
        player.games.append(game)
        opponent.games.append(game)

        sut = WinsAgainst()
        result = sut.getFact(player, player.games[9], opponent)
        self.assertEqual(result, "That was foo's 10th win against bar.")
        result = sut.getFact(player, player.games[10], opponent)
        self.assertIsNone(result)

    def testFirstGameSince(self):
        player = Player("foo")
        opponent = Player("bar")
        game = Game(player.name, 5, opponent.name, 5, 10)
        player.games.append(game)
        opponent.games.append(game)
        opponent.games.append(Game(opponent.name, 5, "baz", 5, 11))
        retireTime = (60 * 60 * 24 * TableFootballLadder.DAYS_INACTIVE)
        game = Game(player.name, 5, opponent.name, 5, 11 + retireTime)
        player.games.append(game)
        opponent.games.append(game)

        sut = FirstGameSince()
        result = sut.getFact(player, player.games[-1], None)
        self.assertEqual(result, "That was foo's first game since retiring on 1970-03-02.")
        result = sut.getFact(opponent, opponent.games[-1], None)
        self.assertIsNone(result)

    def _create(self):
        player = Player("foo")
        game0 = Game(player.name, 10, "bar", 0, 1)
        game0.skillChangeToBlue = 2
        player.games.append(game0)
        game1 = Game(player.name, 10, "bar", 0, 2)
        game1.skillChangeToBlue = -3
        player.games.append(game1)
        game2 = Game(player.name, 10, "bar", 0, 3)
        game2.skillChangeToBlue = 4
        player.games.append(game2)
        game3 = Game(player.name, 10, "bar", 0, 4)
        game3.skillChangeToBlue = -1
        player.games.append(game3)
        return player

class Functional(unittest.TestCase):
    def testStreaks(self):
        l = TableFootballLadder(os.path.join(__location__, "testStreak.txt"), False)
        streaky = l.players['streak']

        sut = Streaks()
        result = sut.getFact(streaky, streaky.games[2], None)
        self.assertEqual(result, "At 3 games, streak was on their longest winning streak.")
        result = sut.getFact(streaky, streaky.games[3], None)
        self.assertEqual(result, "At 4 games, streak was on their longest winning streak.")
        result = sut.getFact(streaky, streaky.games[4], None)
        self.assertEqual(result, "streak broke their winning streak of 4 games.")
        result = sut.getFact(streaky, streaky.games[5], None)
        self.assertIsNone(result)

    def testStreaks2nd(self):
        l = TableFootballLadder(os.path.join(__location__, "testStreak.txt"), False)
        streaky = l.players['streak']
        bulkAppend(streaky, 6, Player('baz'), 4, 5000000012, 3)

        sut = Streaks()
        result = sut.getFact(streaky, streaky.games[-2], None)
        self.assertIsNone(result)
        result = sut.getFact(streaky, streaky.games[-1], None)
        self.assertEqual(result, "At 3 games, streak was on their 2nd longest winning streak.")

    def testStreaksAgainst(self):
        l = TableFootballLadder(os.path.join(__location__, "testStreak.txt"), False)
        streaky = l.players['streak']
        test = l.players['test']

        sut = StreaksAgainst()
        result = sut.getFact(streaky, streaky.games[3], test)
        self.assertEqual(result, "That was streak's 4th consecutive win against test.")
        result = sut.getFact(streaky, streaky.games[4], test)
        self.assertIsNone(result)
        result = sut.getFact(test, streaky.games[4], streaky)
        self.assertEqual(result, "test avoided losing to streak for the first time in 4 games.")
