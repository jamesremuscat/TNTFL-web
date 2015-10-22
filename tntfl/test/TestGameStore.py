import unittest
import os
from tntfl.gameStore import GameStore
from tntfl.game import Game

class TestGameStore(unittest.TestCase):
    def testRead(self):
        try:
            game1 = ("tlr", 0, "cjm", 10, 1445443858)
            filePath = "temp.txt"
            with open(filePath, 'w') as temp:
                temp.write("\n%s %s %s %s %.0f" % game1)

            store = GameStore(filePath)
            games = store.getGames()
            self.assertEqual(len(games), 1)
            self._assertGame(games[0], game1)
        finally:
            os.remove(filePath)

    def testReadDeleted(self):
        try:
            game1 = ("tlr", 0, "cjm", 10, 1445443858, "cjm", 1445443859)
            filePath = "temp.txt"
            with open(filePath, 'w') as temp:
                temp.write("\n%s %s %s %s %.0f %s %.0f" % game1)

            store = GameStore(filePath)
            games = store.getGames()
            self.assertEqual(len(games), 1)
            self._assertGame(games[0], game1)
        finally:
            os.remove(filePath)

    def testAppend(self):
        try:
            game1 = ("tlr", 0, "cjm", 10, 1445443858)
            game2 = ("jma", 5, "tmm", 5, 1445443859)
            filePath = "temp.txt"
            with open(filePath, 'w') as temp:
                temp.write("\n%s %s %s %s %.0f" % game1)

            store = GameStore(filePath)
            store.appendGame(self._createGame(game2))
            games = store.getGames()
            self.assertEqual(len(games), 2)
            self._assertGame(games[0], game1)
            self._assertGame(games[1], game2)
        finally:
            os.remove(filePath)

    def testDelete(self):
        try:
            game1 = ("tlr", 0, "cjm", 10, 1445443858)
            filePath = "temp.txt"
            with open(filePath, 'w') as temp:
                temp.write("\n%s %s %s %s %.0f" % game1)

            store = GameStore(filePath)
            games = store.getGames()
            games[0].deletedBy = "foo"
            games[0].deletedAt = 1445443861
            store.rewriteGames(games)

            games = store.getGames()
            self.assertEqual(len(games), 1)
            self._assertGame(games[0], game1 + ("foo", 1445443861))
        finally:
            os.remove(filePath)

    def testGetAppendDelete(self):
        try:
            game1 = ("tlr", 0, "cjm", 10, 1445443858)
            game2 = ("foo", 2, "bar", 8, 1445443859)
            filePath = "temp.txt"
            with open(filePath, 'w') as temp:
                temp.write("\n%s %s %s %s %.0f" % game1)
                temp.write("\n%s %s %s %s %.0f" % game2)

            store = GameStore(filePath)
            games = store.getGames()
            self.assertEqual(len(games), 2)
            self._assertGame(games[0], game1)
            self._assertGame(games[1], game2)

            game3 = ("bar", 8, "baz", 2, 1445443860)
            game4 = ("bim", 8, "bob", 2, 1445443861)
            store.appendGame(self._createGame(game3))
            store.appendGame(self._createGame(game4))
            games = store.getGames()
            self.assertEqual(len(games), 4)
            self._assertGame(games[0], game1)
            self._assertGame(games[1], game2)
            self._assertGame(games[2], game3)
            self._assertGame(games[3], game4)

            games[2].deletedBy = "baz"
            games[2].deletedAt = 1445443862
            store.rewriteGames(games)
            games = store.getGames()
            self.assertEqual(len(games), 4)
            self._assertGame(games[0], game1)
            self._assertGame(games[1], game2)
            self._assertGame(games[2], game3 + ("baz", 1445443862))
            self._assertGame(games[3], game4)
        finally:
            os.remove(filePath)

    def _createGame(self, args):
        game = None
        if len(args) == 5 or len(args) == 7:
            game = Game(args[0], args[1], args[2], args[3], args[4])
            if len(args) == 7:
                game.deletedBy = args[5]
                game.deletedAt = args[6]
        return game

    def _assertGame(self, resultGame, expectedTuple):
        self.assertEqual(resultGame.redPlayer, expectedTuple[0])
        self.assertEqual(resultGame.redScore, expectedTuple[1])
        self.assertEqual(resultGame.bluePlayer, expectedTuple[2])
        self.assertEqual(resultGame.blueScore, expectedTuple[3])
        self.assertEqual(resultGame.time, expectedTuple[4])
        if len(expectedTuple) == 5:
            expectedTuple += (None, 0)
        self.assertEqual(resultGame.deletedBy, expectedTuple[5])
        self.assertEqual(resultGame.deletedAt, expectedTuple[6])
