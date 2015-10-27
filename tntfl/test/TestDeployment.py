import urllib2
import unittest
import urlparse
import json

class TestDeployment(unittest.TestCase):
    urlBase = 'http://www/~tlr/tntfl-test/'

    def _page(self, page):
        return urlparse.urljoin(self.urlBase, page)

class TestPages(TestDeployment):
    def testIndexReachable(self):
        self._testPage('')

    def testAchievementsReachable(self):
        self._testPage('achievements.cgi')

    def testApiReachable(self):
        self._testPage('api/')

    def testGameReachable(self):
        self._testPage('game/1223308996/')

    def testDeleteReachable(self):
        try:
            self._testPage('game/1223308996/delete')
        except urllib2.HTTPError as e:
            self.assertEqual(e.code, 401)

    def testHeadToHeadReachable(self):
        self._testPage('headtohead/jrem/sam/')

    def testPlayerReachable(self):
        self._testPage('player/jrem/')

    def testPlayerGamesReachable(self):
        self._testPage('player/jrem/games/')

    def testSpeculateReachable(self):
        self._testPage('speculate/')

    def testStatsReachable(self):
        self._testPage('stats/')

    def _testPage(self, page):
        response = urllib2.urlopen(self._page(page))
        self.assertTrue("<!DOCTYPE html>" in response.read())

class TestApi(TestDeployment):
    def testGame(self):
        response = self._getJsonFrom('game/1223308996/json')
        
        self.assertEqual(response['red']['name'], 'jrem')
        self.assertEqual(response['red']['href'], '../../player/jrem/json')
        self.assertEqual(response['red']['score'], 10)
        self.assertEqual(response['red']['skillChange'], 14.8698309141)
        self.assertEqual(response['red']['rankChange'], 0)
        self.assertEqual(response['red']['newRank'], 15)
        redAchievements = response['red']['achievements']
        self.assertEqual(len(redAchievements), 3)
        self.assertEqual(redAchievements[0]['name'], "Flawless Victory")
        self.assertEqual(redAchievements[0]['description'], "Beat an opponent 10-0")
        self.assertEqual(redAchievements[1]['name'], "Early Bird")
        self.assertEqual(redAchievements[1]['description'], "Play and win the first game of the day")
        self.assertEqual(redAchievements[2]['name'], "Pok&#233;Master")
        self.assertEqual(redAchievements[2]['description'], "Collect all the scores")

        self.assertEqual(response['blue']['name'], 'kjb')
        self.assertEqual(response['blue']['href'], '../../player/kjb/json')
        self.assertEqual(response['blue']['score'], 0)
        self.assertEqual(response['blue']['skillChange'], -14.8698309141)
        self.assertEqual(response['blue']['rankChange'], 0)
        self.assertEqual(response['blue']['newRank'], 14)
        self.assertEqual(response['blue']['achievements'], [])

    def testPlayerApiReachable(self):
        response = self._getJsonFrom('player/jrem/json')

    def testPlayerGamesApiReachable(self):
        response = self._getJsonFrom('player/jrem/games/json')

    def testLadderApiReachable(self):
        response = self._getJsonFrom('ladder/json')

    def testRecentApiReachable(self):
        response = self._getJsonFrom('recent/json')

    def testLadderReachable(self):
        response = urllib2.urlopen(self._page('ladder.cgi'))

    def testRecentReachable(self):
        response = urllib2.urlopen(self._page('recent.cgi'))

    def _getJsonFrom(self, page):
        response = urllib2.urlopen(self._page(page))
        return json.load(response)
