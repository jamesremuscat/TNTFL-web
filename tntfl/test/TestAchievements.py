import os
import unittest
from tntfl.player import Player
from tntfl.game import Game
from tntfl.ladder import TableFootballLadder
from tntfl.achievements import *

class Unit(unittest.TestCase):
    def testAgainstTheOdds_Under50(self):
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

    def testAgainstTheOdds_Under50_2(self):
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

    def testAgainstTheOdds_Over50Lose(self):
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

    def testAgainstTheOdds_Over50(self):
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

    def testAgainstTheOdds_Over50_2(self):
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

    def testUnstable(self):
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

    def testComrades(self):
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

    def testTheDominator(self):
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

    def testTheDominatorSwapSides(self):
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

    def testTheDominatorInterupted(self):
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

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
class Functional(unittest.TestCase):
    def testEarlyBird(self):
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

    def testEarlyBirdFirstGame(self):
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
