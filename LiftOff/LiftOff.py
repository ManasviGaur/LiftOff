import pygame
import sys
import random

from pygame.locals import *

pygame.init()

width = 1250
height = 714
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
fps = 60
randomBg=random.choice([1,2,3,4,5,6,7])
randomRocket=random.choice([1,2,3,4,5])
randomObs = random.choice([1,2])
# images
background = pygame.image.load("images/background"+str(randomBg)+".png").convert_alpha()
rocket = pygame.image.load("images/rocket"+str(randomRocket)+".png").convert_alpha()
obs = str(randomObs)
Obstacle = pygame.image.load("images/obs" + obs + ".png").convert_alpha()
rotatedObstacle = pygame.image.load("images/obs" + obs + ".png").convert_alpha()

# Game Caption
pygame.display.set_caption("LiftOff")
# sounds
point = pygame.mixer.Sound("sounds/sfx_point.wav")
hit = pygame.mixer.Sound("sounds/sfx_hit.wav")
#bgmusic
pygame.mixer.music.load("sounds/bgmusic.mp3") 
pygame.mixer.music.play(-1)

class Game:
    def __init__(self):
        
        self.gameOn = True
        self.rocketX = 100
        self.rocketY = 100
        self.ObstaclesX = [width, width + 200, width + 400, width + 600, width + 800, width + 1000, width + 1200]
        self.lowerObstacleY = [self.randomObstacle(), self.randomObstacle(), self.randomObstacle(), self.randomObstacle(),
                           self.randomObstacle(), self.randomObstacle(), self.randomObstacle()]
        self.upperObstacleY = [self.randomRotatedObstacle(), self.randomRotatedObstacle(), self.randomRotatedObstacle(),
                           self.randomRotatedObstacle(), self.randomRotatedObstacle(), self.randomRotatedObstacle(), self.randomRotatedObstacle()]
        self.gravity = 0
        self.ObstacleVel = 0
        self.flap = 0
        self.score = 0
        self.rotateAngle = 0
        self.isGameOver = False
        self.intro = True
        self.playSound = True
        self.speed_accelerating = 5

        try:
            self.highest_score = int(self.gethighestscore())
        except:
            self.highest_score = 0

    def movingObstacle(self):
        for i in range(0, 7):
            self.ObstaclesX[i] += -self.ObstacleVel

        for i in range(0, 7):
            if (self.ObstaclesX[i] < -50):
                self.ObstaclesX[i] = width + 100
                self.lowerObstacleY[i] = self.randomObstacle()
                self.upperObstacleY[i] = self.randomRotatedObstacle()

    def randomObstacle(self):
        return random.randrange(int(height / 2) + 50, height - 100)

    def randomRotatedObstacle(self):
        return random.randrange(-int(height / 2) + 100, -100)

    def flapping(self):
        self.rocketY += self.gravity
        if (self.isGameOver == False):
            self.flap -= 1
            self.rocketY -= self.flap

    def isCollide(self):
        for i in range(0, 7):
            if (self.rocketX >= self.ObstaclesX[i] and self.rocketX <= (self.ObstaclesX[i] + Obstacle.get_width())
                    and ((self.rocketY + rocket.get_height() - 15) >= self.lowerObstacleY[i] or
                         (self.rocketY) <= self.upperObstacleY[i] + rotatedObstacle.get_height() - 15)):
                return True

            elif (self.rocketX == self.ObstaclesX[i] and (
                    self.rocketY <= self.lowerObstacleY[i] and self.rocketY >= self.upperObstacleY[i])):
                if (self.isGameOver == False):
                    self.score += 1
                    pygame.mixer.Sound.play(point)
                    #accelerating speed of game
                    self.speed_accelerating += 0.001

        if (self.rocketY <= 0):
            return True

        elif (self.rocketY + rocket.get_height() >= height):
            self.gravity = 0
            return True

        return False

    def gethighestscore(self):
        with open("Highest Score.txt", "r") as f:
            return f.read()

    def game_intro(self):
        if self.intro == True:
            randomBg=random.choice([1,2,3,4])
            background = pygame.image.load("images/background"+str(randomBg)+".png").convert_alpha()
            
            while self.intro:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()

                    if event.type == KEYDOWN:
                        if event.key == K_RETURN:
                            self.mainGame()
                screen.blit(background, (0, 0))
                self.screenText("LiftOff", (255, 255, 255), 500, 150, 90, "Fixedsys", bold=True)
                self.screenText("Highest Score : ", (255, 255, 255), 440, 500, 48, "Fixedsys", bold=True)
                self.screenText(str(self.highest_score), (255, 255, 255), 750, 500, 48, "Fixedsys", bold=True)
                self.screenText("Press Enter To Play", (255, 255, 255), 430, 600, 48, "Fixedsys", bold=True)

                pygame.display.update()
                clock.tick(fps)

            
    def gameOver(self):
        if (self.isCollide()):
            self.isGameOver = True
            self.screenText("Game Over!", (255, 255, 255), 450, 300, 84, "Fixedsys", bold=True)
            self.screenText("Press Enter To Play Again", (255, 255, 255), 400, 600, 48, "Fixedsys", bold=True)
            self.screenText("Highest Score : ", (255, 255, 255), 440, 425, 48, "Fixedsys", bold=True)
            self.screenText(str(self.highest_score), (255, 255, 255), 750, 425, 48, "Fixedsys", bold=True)
            self.screenText("Your Score : ", (255, 255, 255), 440, 475, 48, "Fixedsys", bold=True)
            self.screenText(str(self.score), (255, 255, 255), 750, 475, 48, "Fixedsys", bold=True)
            self.ObstacleVel = 0
            self.flap = 0
            self.rotateAngle = -90
            if (self.playSound):
                pygame.mixer.Sound.play(hit)
                self.playSound = False
            

    def screenText(self, text, color, x, y, size, style, bold=False):
        font = pygame.font.SysFont(style, size, bold=bold)
        screen_text = font.render(text, True, color)
        screen.blit(screen_text, (x, y))

    def mainGame(self):
        randomBg=random.choice([1,2,3,4])
        randomBocket=random.choice([1,2,3])
        randomObs = random.choice([1,2])
        background = pygame.image.load("images/background"+str(randomBg)+".png").convert_alpha()
        rocket = pygame.image.load("images/rocket"+str(randomBocket)+".png").convert_alpha()
        obs = str(randomObs)
        Obstacle = pygame.image.load("images/obs" + obs + ".png").convert_alpha()
        rotatedObstacle = pygame.image.load("images/obs" + obs + ".png").convert_alpha()
        while self.gameOn:
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == KEYDOWN:
                    if event.key == K_SPACE:
                        if (self.isGameOver == False):
                            self.ObstacleVel = 5
                            self.gravity = 10
                            self.flap = 20
                            self.rotateAngle = 15

                    if event.key == K_RETURN:
                        newGame = Game()
                        newGame.game_intro()

                if event.type == KEYUP:
                    if event.key == K_SPACE:
                        self.rotateAngle = 0
                        # blitting images
            screen.blit(background, (0, 0))

            for i in range(0, 7):
                # lower  Obstacle
                screen.blit(Obstacle, (self.ObstaclesX[i], self.lowerObstacleY[i]))
                # upper Obstacle
                screen.blit(rotatedObstacle, (self.ObstaclesX[i], self.upperObstacleY[i]))

            screen.blit(pygame.transform.rotozoom(rocket, self.rotateAngle, 1), (self.rocketX, self.rocketY))

            # moving Obstacle
            self.movingObstacle()
            # flapping
            self.flapping()
            # game over
            self.gameOver()
            # displaying score
            self.screenText(str(self.score), (255, 255, 255), 600, 50, 68, "Fixedsys", bold=True)
            #checking highest score
            if self.highest_score < self.score:
                self.highest_score = self.score
            with open("Highest Score.txt", "w") as f:
                f.write(str(self.highest_score))

            pygame.display.update()
            clock.tick(fps)


LiftOff = Game()
LiftOff.game_intro()
# LiftOff.mainGame()