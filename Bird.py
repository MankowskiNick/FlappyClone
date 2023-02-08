import math
class Bird:
    def __init__(self, WIDTH, HEIGHT, xPos):
        self.x = xPos
        self.currentHeight = HEIGHT / 2
        self.acceleration = 0
        self.yVelocity = 0
        self.isWaiting = True
        self.alive = True
        self.score = 0
        self.inPipe = False
        self.direction = [1,0]
        self.cooldownCounter = 0
    def Update(self, xVelocity, frameCounter, testPos):
        if self.isWaiting:
            self.yVelocity = 0.3*math.cos(frameCounter * math.pi / 45)
        else:
            if self.x <= testPos:
                self.x += 1
            self.direction = [-xVelocity, self.yVelocity]
        
        self.yVelocity += self.acceleration
        self.currentHeight -= self.yVelocity
    def Start(self):
        self.isWaiting = False
        self.acceleration = -0.2
    def Die(self):
        self.alive = False
    def Jump(self):
        if self.alive:
            self.yVelocity = 5
    def collisionDetect(self, pipe, velocity, floorHeight, birdRadius):
        if self.isWaiting: return False
        for i in range(0,16):
            currentAngle = i * 16 * math.pi / 180
            xCollision = self.x + birdRadius*math.cos(currentAngle) >= pipe.x and self.x + birdRadius*math.cos(currentAngle) <= pipe.x + 52
            yCollision = self.currentHeight + birdRadius*math.sin(currentAngle) <= pipe.topHeight or self.currentHeight + birdRadius*math.sin(currentAngle) >= pipe.bottomHeight
            print(self.cooldownCounter)
            if ((xCollision and yCollision and self.alive) or (self.currentHeight >= floorHeight and self.alive) or (self.currentHeight <= 0 and self.alive)):
                self.Die()
                self.yVelocity = 4
        xCollision = self.x >= pipe.x and self.x <= pipe.x + 52
        yCollision = self.currentHeight <= pipe.topHeight or self.currentHeight >= pipe.bottomHeight
        if xCollision and (not yCollision):
            if (not self.inPipe) and self.alive:
                self.score += 1
                self.inPipe = True
                return True
            elif (self.inPipe):
                self.cooldownCounter += 1
        if self.cooldownCounter == int(-52 / velocity):
            self.inPipe = False
            self.cooldownCounter = 0
        
        return False