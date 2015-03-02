class CircularSkillBuffer:
  
    def __init__(self, size):
        self.list = []
        self.maxSize = size
        self.isFull = False
    
    def put(self, val):
        if len(self.list) == (self.maxSize - 1):
            self.justFull = True
            self.isFull = True
        else:
            self.justFull = False
          
        self.list.append(val);
        if len(self.list) > self.maxSize:
            self.list = self.list[1:]
    
    def sum(self):
        total = 0
        for val in self.list:
            total += val['skill']
        return total
    
    def avg(self):
        return self.sum() / len(self.list)

    def oldSum(self):
        total = 0
        for val in self.list:
            total += val['oldskill']
        return total
    
    def oldAvg(self):
        return self.oldSum() / len(self.list)
    
    def lastSkill(self):
        "The player's Skill after they have played their last game"
        return self.getSkill(len(self.list) - 1)

    def penultimateSkill(self):
        "The player's skill before they player their last game. They must have played 2 games to call this"
        return self.getSkill(len(self.list) - 2)
        
    def getPlayed(self, index):
        if len(self.list) == 0:
            return 0
        return self.list[index]['played']
    
    def getSkill(self, index):
        if len(self.list) == 0:
            return 0
        return self.list[index]['skill']
    
    def getOldSkill(self, index):
        if len(self.list) == 0:
            return 0
        return self.list[index]['oldskill']
    
    def getStreak(self):
        """The player's skill streak.
           This is:
             0        if they havn't played enough games (0 or 1) or their last game didn't change their skill (unlikely!)
             positive if they have an upwards streak
             negative if they have a downwards streak
        """
        if len(self.list) < 2 or self.lastSkill() == self.penultimateSkill():
            return 0
        
        op = 0
        sign = 0
        if self.penultimateSkill() < self.lastSkill():
            op = lambda x, y: x < y
            sign = +1
        else:
            op = lambda x, y: x > y
            sign = -1
    
        i = 2
        while op(self.getSkill(len(self.list) - (i + 1)), self.getSkill(len(self.list) - i)):
            i += 1
    
        return sign * (i - 1)
    
    def size(self):
        return len(self.list)
