
class CircularBuffer(object):
    def __init__(self, size):
        self.list = []
        self.maxSize = size
        self.isFull = False

    def put(self, val):
        if len(self.list) == (self.maxSize - 1):
            self.isFull = True

        self.list.append(val)
        if len(self.list) > self.maxSize:
            self.list = self.list[1:]

    def size(self):
        return len(self.list)


class CircularSkillBuffer(CircularBuffer):
    def sum(self):
        total = 0
        for val in self.list:
            total += val
        return total

    def avg(self):
        return self.sum() / len(self.list)

    def lastSkill(self):
        "The player's Skill after they have played their last game"
        return self.getSkill(len(self.list) - 1)

    def getSkill(self, index):
        if len(self.list) == 0:
            return 0
        return self.list[index]
