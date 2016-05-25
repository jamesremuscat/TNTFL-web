from datetime import datetime

class Game(object):

    def __init__(self, redPlayer, redScore, bluePlayer, blueScore, time):
        self.redPlayer = redPlayer.lower()
        self.redScore = int(redScore)
        self.redPosChange = 0
        self.redPosAfter = -1
        self.bluePlayer = bluePlayer.lower()
        self.blueScore = int(blueScore)
        self.bluePosChange = 0
        self.bluePosAfter = -1
        self.time = int(time)
        self.redAchievements = []
        self.blueAchievements = []
        self.skillChangeToBlue = 0
        self.deletedBy = None
        self.deletedAt = 0

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return "{redPlayer} {redScore}-{blueScore} {bluePlayer}".format(redPlayer=self.redPlayer, bluePlayer=self.bluePlayer, redScore=self.redScore, blueScore=self.blueScore)

    def isDeleted(self):
        return self.deletedAt > 0

    def timeAsDatetime(self):
        return datetime.fromtimestamp(self.time)
