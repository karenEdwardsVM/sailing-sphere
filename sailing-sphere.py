#!/usr/bin/env python3
import pygame
import sys
import random
import math
import tkinter
from tkinter import messagebox

class Background:
    mountains = []

    def __init__(self, colour, movement, maxPeak, points = None):
        self.colour = colour
        self.points = points
        self.movement = movement
        self.maxPeak = maxPeak
        Background.mountains.append(self)

    @staticmethod
    def draw():
        for obj in Background.mountains:
            pygame.draw.polygon(window, obj.colour, obj.points, 0)

    @staticmethod
    def move():
        for obj in Background.mountains:
            #obj.moveEach(window_width, window_height)
            #maxPeak = 400
            for element in obj.points:
                element[0] -= obj.movement
            if obj.points[1][0] < 0:
                obj.points.pop(0)
            obj.points = obj.points[0:-2]
            x = window_width + 50
            if obj.points[-1][0] <= window_width + obj.movement * 2:
                obj.points.append([x, random.randint(obj.maxPeak, 750)])
            obj.points.append([x, window_height])
            obj.points.append([0, window_height])

    @staticmethod
    def generatePoints():
        for obj in Background.mountains:
            #obj.generatePoints(window_width, window_height)
            maxPeak = 400
            numPoints = random.randint(8, 15)
            obj.points = []
            for i in range(numPoints):
                x = 0 if i == 0 else min((obj.points[-1][0] + random.randint(100, 400)), window_width)
                y = random.randint(maxPeak, 750)
                obj.points.append([x, y])
                if x == window_width: 
                    break
            # finish the points for the polygon
            obj.points.append([window_width, random.randint(maxPeak, 750)])
            obj.points.append([window_width, window_height])
            obj.points.append([0, window_height])

#class Pattern:
#    def __init__(self, name, x, y):
#       self.name = name
#       self.x = x
#       self.y = y

class Obstacle:
    obstacles = []

    def __init__(self, x, y, width, height, colour, movement):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.colour = colour
        self.movement = movement
        Obstacle.obstacles.append(self)

    def __str__(self):
        return f"x = {self.x}, y = {self.y}, width = {self.width}, height = {self.height}, colour = {self.colour}, movement = {self.movement}"

    @staticmethod
    def draw(thiccness):
        for obj in Obstacle.obstacles:
            rectangle = pygame.Rect(obj.x, obj.y, obj.width, obj.height)
            pygame.draw.rect(window, obj.colour, rectangle, thiccness)

    @staticmethod
    def move():
        for obj in Obstacle.obstacles:
            obj.x -= obj.movement

    @staticmethod
    def isOffWindow():
        toDelete = []
        generate = False
        for obj in Obstacle.obstacles:
            if obj.x <= 0:
                toDelete.append(obj)
        for obj in toDelete:
            Obstacle.obstacles.remove(obj)
        if len(Obstacle.obstacles) < 1:
            Obstacle.generateNextObstacles()

    @staticmethod
    def checkCollisions(xCirc, yCirc, radius):
        game_running = True
        for obj in Obstacle.obstacles:
            if obj.isCollidingWith(xCirc, yCirc, radius):
                print(f"Hit: {obj}")
                game_running = False
        return game_running
    
    @staticmethod
    def generateNextObstacles():
        width = random.randint(50, 75)
        # speed range
        if (timeChange * 0.15) >= 2:
            lowSpeed = 16 * math.floor(math.log(timeChange * 0.15, 2))
            highSpeed = 25 * math.floor(math.log(timeChange * 0.15, 2))
            speed = random.randint(lowSpeed, highSpeed)
        else:
            speed = random.randint(16, 25)
        x = window_width
        y = random.randint(70, window_height - 70)
        #Obstacle(window_width, y, width, width, (210, 0, 0), speed)
        pattern = random.randint(0, 3)
        randRange = random.randint(6, 12)
        if pattern == 0:
            # L
            for i in range(randRange):
                Obstacle(x + i * (width + 5), y, width, width, (210, 0, 0), speed)
            for i in range(randRange):
                Obstacle(x + randRange * (width + 5), y + i * (width + 5), width, width, (210, 0, 0), speed)
        if pattern == 1:
            # step
            for i in range(randRange):
                Obstacle(x + i * (width + 5), y, width, width, (210, 0, 0), speed)
            for i in range(randRange // 2):
                Obstacle(x, y + i * (width + 5), width, width, (210, 0, 0), speed)
            for i in range(randRange):
                Obstacle(x + i * (width + 5), y, width, width, (210, 0, 0), speed)
        if pattern == 2:
            # upside-down V - ^
            for i in range(randRange // 2):
                Obstacle(x + i * (width + 5), y + i * (width + 5), width, width, (210, 0, 0), speed)
            for i in range(randRange // 2):
                Obstacle(x - i * (width + 5), y + i * (width + 5), width, width, (210, 0, 0), speed)
        if pattern == 3:
            for i in range(randRange):
                if i % 2 == 0:
                    Obstacle(x + i * (width + 5), y + width, width, width, (210, 0, 0), speed)
                else:
                    Obstacle(x + i * (width + 5), y, width, width, (210, 0, 0), speed)
        Obstacle.fitOnScreen()

    #@staticmethod
    #def findVertical():
    #    # count = { (index: , count: ), (index: , count: ) }
    #    vertIndecies = []
    #    for i in range(len(Obstacle.obstacles) - 1):
    #        lastY = Obstacle.obstacles[i]
    #        if lastY != Obstacle.obstacles[i + 1]:
    #            vertIndecies.append(Obstacle.obstacles[i + 1].index())
    #        else: 
    #            break
    #    return vertIndecies

    # problem, if the object goes from too far down to too far up.
    @staticmethod
    def fitOnScreen():
        # change y to fit on screen
        maxYIndex = Obstacle.findMaxY()
        minYIndex = Obstacle.findMinY()
        if Obstacle.obstacles[maxYIndex].y > window_height:
            #print(f"Off bottom of screen y is {Obstacle.obstacles[maxYIndex].y}")
            difference = Obstacle.obstacles[maxYIndex].y - window_height
            #print(f"difference is {difference}")
            #print(f"Before Change:")
            #for obj in Obstacle.obstacles:
            #    print(f"{obj}")
            for obj in Obstacle.obstacles:
                obj.y -= (difference + Obstacle.obstacles[maxYIndex].height + 15)
            #print(f"After change:")
            #for obj in Obstacle.obstacles:
            #    print(f"{obj}")
        if Obstacle.obstacles[minYIndex].y < 0:
            difference = (-1) * Obstacle.obstacles[minYIndex].y
            for obj in Obstacle.obstacles:
                obj.y += (difference + Obstacle.obstacles[maxYIndex].height + 15)
    
    # find max y in the array of obstacles, return index
    @staticmethod
    def findMaxY():
        maxY = Obstacle.obstacles[0].y
        index = 0
        for obj in Obstacle.obstacles:
            if obj.y > maxY:
                maxY = obj.y
                index = Obstacle.obstacles.index(obj)
        return index

    # find min y in the array of obstacles, return index
    @staticmethod
    def findMinY():
        minY = Obstacle.obstacles[0].y
        index = 0
        for obj in Obstacle.obstacles:
            if obj.y < minY:
                minY = obj.y
                index = Obstacle.obstacles.index(obj)
        return index

    def isCollidingWith(self, xCirc, yCirc, radius):
        # center of rect
        xCenterObs = self.x + (0.5 * self.width)
        yCenterObs = self.y + (0.5 * self.height)
        # distance between centers and distance between x's and y's
        distance = math.pow((xCirc - xCenterObs), 2) + math.pow((yCirc - yCenterObs), 2)
        xDist = abs(xCirc - xCenterObs)
        yDist = abs(yCirc - yCenterObs)
        # check for collision on x axis, or y axis
        if xDist > (self.width / 2 + radius): 
            return False
        if yDist > (self.height / 2 + radius): 
            return False
        if xDist <= (self.width / 2): 
            return True
        if yDist <= (self.height / 2):
            return True
        # check on diagonals 
        return (distance <= (math.pow(radius, 2))) 

class Player: 
    def __init__(self, radius, colour, yVelocity):
        self.x = window_width // 3  
        self.y = window_height // 2
        self.radius = radius
        self.colour = colour
        self.yVelocity = yVelocity

    def draw(self):
        pygame.draw.circle(window, self.colour, (int(self.x), int(self.y)), self.radius)

    def move(self, pressed):
        if pressed[pygame.K_SPACE] and self.y > 0:
            self.yVelocity -= 10
        # apply gravity or downward velocity
        self.y += self.yVelocity 
        self.yVelocity += 1
        # keep character from going past top or bottom of screen
        if self.y <= 0:
            self.y = 0
            self.yVelocity = 10
        if self.y > window_height: 
            self.y = window_height
            self.yVelocity = 0


def playingGame():
    global window_width, window_height, window, timeChange
    window_width = 1200
    window_height = 800
    timeChange = 0
    pygame.init()
    # create game window
    window = pygame.display.set_mode((window_width, window_height))
    pygame.display.set_caption("Flappy Dove")
    player = Player(50, (250, 250, 250), 0)
    clock = pygame.time.Clock()
    startTime = pygame.time.get_ticks()
    Obstacle.generateNextObstacles()
    # mountains
    Background((49, 188, 81), 5, 400)
    Background((76, 0, 153), 8, 600)
    Background.generatePoints()
    game_running = True
    
    while game_running:
        clock.tick(40)
        pressed = pygame.key.get_pressed()
        player.move(pressed)

        # content
        window.fill((0, 0, 0))
        Background.move()
        Background.draw()

        player.draw()
        Obstacle.draw(0)
        Obstacle.move()
        timeChange = (pygame.time.get_ticks() - startTime) // 1000
        Obstacle.isOffWindow()
        game_running = Obstacle.checkCollisions(player.x, player.y, player.radius)
        pygame.display.update()
        # event handling
        if player.y >= window_height:
            game_running = False
        for event in pygame.event.get():
            # Close the program if the user presses the 'X' or presses 'Q'
            if event.type == pygame.QUIT:
                game_running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q: 
                    game_running = False
    print("Quitting game")
    pygame.quit()
    sys.exit()

playingGame()
