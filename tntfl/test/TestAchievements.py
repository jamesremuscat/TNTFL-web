import os
import unittest
from tntfl.player import Player
from tntfl.game import Game
from tntfl.ladder import TableFootballLadder
from tntfl.achievements import *

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

class TestAgainstTheOdds(unittest.TestCase):
    def testUnder50(self):
        ach = AgainstTheOdds()
        player = Player("foo")
        player.elo = 0
        opponent = Player("bar")
        opponent.elo = 49
        game = Game(player.name, 10, opponent.name, 0, 0)
        game.skillChangeToBlue = -50
        player.game(game)
        opponent.game(game)
        result = ach.applies(player, game, opponent, None)
        self.assertFalse(result)

    def testUnder50_2(self):
        ach = AgainstTheOdds()
        player = Player("foo")
        player.elo = 0
        opponent = Player("bar")
        opponent.elo = 49
        game = Game(opponent.name, 0, player.name, 10, 0)
        game.skillChangeToBlue = 10
        player.game(game)
        opponent.game(game)
        result = ach.applies(player, game, opponent, None)
        self.assertFalse(result)

    def testOver50Lose(self):
        ach = AgainstTheOdds()
        player = Player("foo")
        player.elo = 0
        opponent = Player("bar")
        opponent.elo = 50
        game = Game(player.name, 0, opponent.name, 10, 0)
        game.skillChangeToBlue = 50
        player.game(game)
        opponent.game(game)
        result = ach.applies(player, game, opponent, None)
        self.assertFalse(result)

    def testOver50(self):
        ach = AgainstTheOdds()
        player = Player("foo")
        player.elo = 0
        opponent = Player("baz")
        opponent.elo = 50
        game = Game(player.name, 10, opponent.name, 0, 0)
        game.skillChangeToBlue = -50
        player.game(game)
        opponent.game(game)
        result = ach.applies(player, game, opponent, None)
        self.assertTrue(result)

    def testOver50_2(self):
        ach = AgainstTheOdds()
        player = Player("foo")
        player.elo = 0
        opponent = Player("baz")
        opponent.elo = 50
        game = Game(opponent.name, 0, player.name, 10, 0)
        game.skillChangeToBlue = 10
        player.game(game)
        opponent.game(game)
        result = ach.applies(player, game, opponent, None)
        self.assertTrue(result)

class TestAgainstAllOdds(unittest.TestCase):
    def testUnder100(self):
        ach = AgainstAllOdds()
        player = Player("foo")
        player.elo = 0
        opponent = Player("bar")
        opponent.elo = 99
        game = Game(player.name, 10, opponent.name, 0, 0)
        game.skillChangeToBlue = -50
        player.game(game)
        opponent.game(game)
        result = ach.applies(player, game, opponent, None)
        self.assertFalse(result)

    def testOver100(self):
        ach = AgainstAllOdds()
        player = Player("foo")
        player.elo = 0
        opponent = Player("bar")
        opponent.elo = 100
        game = Game(player.name, 10, opponent.name, 0, 0)
        game.skillChangeToBlue = -1
        player.game(game)
        opponent.game(game)
        result = ach.applies(player, game, opponent, None)
        self.assertTrue(result)

class TestUnstable(unittest.TestCase):
    def test(self):
        sut = Unstable()
        player = Player("foo")
        opponent = Player("bar")

        game = Game(player.name, 5, opponent.name, 5, 0)
        game.skillChangeToBlue = -5
        player.game(game)
        opponent.game(game)
        result = sut.applies(player, game, opponent, None)
        self.assertFalse(result)
        result = sut.applies(opponent, game, player, None)
        self.assertFalse(result)

        game = Game(player.name, 10, opponent.name, 0, 0)
        game.skillChangeToBlue = -5
        player.game(game)
        opponent.game(game)
        result = sut.applies(player, game, opponent, None)
        self.assertFalse(result)
        result = sut.applies(opponent, game, player, None)
        self.assertFalse(result)

        game = Game(player.name, 0, "bar", 10, 1)
        game.skillChangeToBlue = 5
        player.game(game)
        opponent.game(game)
        result = sut.applies(player, game, opponent, None)
        self.assertTrue(result)
        result = sut.applies(opponent, game, player, None)
        self.assertTrue(result)

        game = Game(player.name, 0, "bar", 10, 1)
        game.skillChangeToBlue = 5
        player.game(game)
        opponent.game(game)
        result = sut.applies(player, game, opponent, None)
        self.assertFalse(result)
        result = sut.applies(opponent, game, player, None)
        self.assertFalse(result)


class TestComrades(unittest.TestCase):
    def test(self):
        sut = Comrades()
        player = Player("foo")
        opponent = Player("bar")
        for i in range(0, 99):
            game = Game(player.name, 5, opponent.name, 5, 0)
            player.game(game)
            opponent.game(game)
            result = sut.applies(player, game, opponent, None)
            self.assertFalse(result)
            result = sut.applies(opponent, game, player, None)
            self.assertFalse(result)

        game = Game(player.name, 5, opponent.name, 5, 0)
        player.game(game)
        opponent.game(game)
        result = sut.applies(player, game, opponent, None)
        self.assertTrue(result)
        result = sut.applies(opponent, game, player, None)
        self.assertTrue(result)

        game = Game(player.name, 5, opponent.name, 5, 0)
        player.game(game)
        opponent.game(game)
        result = sut.applies(player, game, opponent, None)
        self.assertFalse(result)
        result = sut.applies(opponent, game, player, None)
        self.assertFalse(result)


class TestDedication(unittest.TestCase):
    def test(self):
        sut = Dedication()
        player = Player("foo")
        opponent = Player("bar")
        timeBetweenGames = 60*60*24* 59
        for i in range(0, 7):
            game = Game(player.name, 5, opponent.name, 5, i * timeBetweenGames)
            player.game(game)
            opponent.game(game)
            result = sut.applies(player, game, opponent, None)
            self.assertFalse(result)
        game = Game(player.name, 5, opponent.name, 5, 7 * timeBetweenGames)
        player.game(game)
        opponent.game(game)
        result = sut.applies(player, game, opponent, None)
        self.assertTrue(result)


class TestPokeMaster(unittest.TestCase):
    def test(self):
        sut = PokeMaster()
        player = Player("foo")
        opponent = Player("bar")
        game = Game(player.name, 0, opponent.name, 10, 0)
        player.game(game)
        opponent.game(game)
        for i in range(0, 10):
            game = Game(player.name, i, opponent.name, 10 - i, i)
            player.game(game)
            opponent.game(game)
            result = sut.applies(player, game, opponent, None)
            self.assertFalse(result)
        game = Game(player.name, 10, opponent.name, 0, 10)
        player.game(game)
        opponent.game(game)
        result = sut.applies(player, game, opponent, None)
        self.assertTrue(result)


class TestTheDominator(unittest.TestCase):
    def test(self):
        sut = TheDominator()
        player = Player("foo")
        opponent = Player("bar")
        for i in range(0, 9):
            game = Game(player.name, 10, opponent.name, 0, i)
            game.skillChangeToBlue = -1
            player.game(game)
            opponent.game(game)
            result = sut.applies(player, game, opponent, None)
            self.assertFalse(result)

        baz = Player("baz")
        game = Game(player.name, 10, baz.name, 0, 9)
        game.skillChangeToBlue = -1
        player.game(game)
        result = sut.applies(player, game, baz, None)
        self.assertFalse(result)

        game = Game(player.name, 10, opponent.name, 0, 10)
        game.skillChangeToBlue = -1
        player.game(game)
        opponent.game(game)
        result = sut.applies(player, game, opponent, None)
        self.assertTrue(result)
        result = sut.applies(opponent, game, player, None)
        self.assertFalse(result)

    def testSwapSides(self):
        sut = TheDominator()
        player = Player("foo")
        opponent = Player("bar")
        for i in range(0, 9):
            game = Game(player.name, 10, opponent.name, 0, i)
            game.skillChangeToBlue = -1
            player.game(game)
            opponent.game(game)
            result = sut.applies(player, game, opponent, None)
            self.assertFalse(result)

        baz = Player("baz")
        game = Game(player.name, 10, baz.name, 0, 9)
        game.skillChangeToBlue = -1
        player.game(game)
        result = sut.applies(player, game, baz, None)
        self.assertFalse(result)

        game = Game(opponent.name, 0, player.name, 10, 10)
        game.skillChangeToBlue = 1
        player.game(game)
        opponent.game(game)
        result = sut.applies(player, game, opponent, None)
        self.assertTrue(result)
        result = sut.applies(opponent, game, player, None)
        self.assertFalse(result)

    def testInterrupted(self):
        sut = TheDominator()
        player = Player("foo")
        opponent = Player("bar")
        for i in range(0, 9):
            game = Game(player.name, 10, opponent.name, 0, i)
            game.skillChangeToBlue = -1
            player.game(game)
            opponent.game(game)
            result = sut.applies(player, game, opponent, None)
            self.assertFalse(result)

        baz = Player("baz")
        game = Game(player.name, 10, baz.name, 0, 9)
        game.skillChangeToBlue = -1
        player.game(game)
        result = sut.applies(player, game, baz, None)
        self.assertFalse(result)

        game = Game(player.name, 0, opponent.name, 10, 10)
        game.skillChangeToBlue = -1
        player.game(game)
        opponent.game(game)
        result = sut.applies(player, game, opponent, None)
        self.assertFalse(result)
        result = sut.applies(opponent, game, player, None)
        self.assertFalse(result)


class TestConsistency(unittest.TestCase):
    def test(self):
        sut = Consistency()
        player = Player("foo")
        opponent = Player("bar")
        for i in range(0, 4):
            game = Game(player.name, 2, opponent.name, 8, i)
            player.game(game)
            opponent.game(game)
            result = sut.applies(player, game, opponent, None)
            self.assertFalse(result)
        game = Game(player.name, 2, opponent.name, 8, 4)
        player.game(game)
        opponent.game(game)
        result = sut.applies(player, game, opponent, None)
        self.assertTrue(result)

    def testInterrupted(self):
        sut = Consistency()
        player = Player("foo")
        opponent = Player("bar")
        for i in range(0, 4):
            game = Game(player.name, 2, opponent.name, 8, i)
            player.game(game)
            opponent.game(game)
            result = sut.applies(player, game, opponent, None)
            self.assertFalse(result)
        game = Game(player.name, 3, opponent.name, 7, 4)
        player.game(game)
        opponent.game(game)
        result = sut.applies(player, game, opponent, None)
        self.assertFalse(result)
        game = Game(player.name, 2, opponent.name, 8, 5)
        player.game(game)
        opponent.game(game)
        result = sut.applies(player, game, opponent, None)
        self.assertFalse(result)

    def testCont(self):
        sut = Consistency()
        player = Player("foo")
        opponent = Player("bar")
        for i in range(0, 4):
            game = Game(player.name, 2, opponent.name, 8, i)
            player.game(game)
            opponent.game(game)
            result = sut.applies(player, game, opponent, None)
            self.assertFalse(result)
        game = Game(player.name, 2, opponent.name, 8, 4)
        player.game(game)
        opponent.game(game)
        result = sut.applies(player, game, opponent, None)
        self.assertTrue(result)
        game = Game(player.name, 2, opponent.name, 8, 5)
        player.game(game)
        opponent.game(game)
        result = sut.applies(player, game, opponent, None)
        self.assertFalse(result)

    def testTwice(self):
        sut = Consistency()
        player = Player("foo")
        opponent = Player("bar")
        for i in range(0, 4):
            game = Game(player.name, 2, opponent.name, 8, i)
            player.game(game)
            opponent.game(game)
            result = sut.applies(player, game, opponent, None)
            self.assertFalse(result)
        game = Game(player.name, 2, opponent.name, 8, 4)
        player.game(game)
        opponent.game(game)
        result = sut.applies(player, game, opponent, None)
        self.assertTrue(result)

        for i in range(5, 9):
            game = Game(player.name, 2, opponent.name, 8, i)
            player.game(game)
            opponent.game(game)
            result = sut.applies(player, game, opponent, None)
            self.assertFalse(result)
        game = Game(player.name, 2, opponent.name, 8, 9)
        player.game(game)
        opponent.game(game)
        result = sut.applies(player, game, opponent, None)
        self.assertTrue(result)


class TestEarlyBird(unittest.TestCase):
    def test(self):
        ladder = TableFootballLadder(os.path.join(__location__, "testLadder.txt"), False)
        player = Player("foo")
        opponent = Player("baz")
        game = Game(opponent.name, 0, player.name, 10, 6000000003)
        ladder.addGame(game)

        sut = EarlyBird()
        result = sut.applies(player, game, opponent, ladder)
        self.assertTrue(result)
        result = sut.applies(opponent, game, player, ladder)
        self.assertFalse(result)

    def testFirstGame(self):
        ladder = TableFootballLadder(os.path.join(__location__, "emptyLadder.txt"), False)
        player = Player("foo")
        opponent = Player("baz")
        game = Game(opponent.name, 0, player.name, 10, 0)
        ladder.addGame(game)

        sut = EarlyBird()
        result = sut.applies(player, game, opponent, ladder)
        self.assertTrue(result)
        result = sut.applies(opponent, game, player, ladder)
        self.assertFalse(result)
