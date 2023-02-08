import random
class Pipe:
    def __init__(self, WIDTH, HEIGHT):

        self.topHeight = random.randint(0,HEIGHT - 350)
        self.bottomHeight = self.topHeight + 200

        self.x = WIDTH

    def Update(self, velocity):
        self.x += velocity
        if self.x <= -26:
            return True
        else:
            return False

class Base:
    def __init__(self, WIDTH, HEIGHT, x):
        self.x = x
    def Update(self, WIDTH, velocity):
        self.x += velocity
        if self.x <= -WIDTH:return True
        else:return False