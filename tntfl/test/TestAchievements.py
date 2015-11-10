import unittest
from tntfl.player import Player
from tntfl.game import Game
from tntfl.achievements import *

class TestAchievements(unittest.TestCase):
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
