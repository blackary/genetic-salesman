#!/usr/bin/env python

"""
This Python code is based on Java code by Lee Jacobson found in an article
entitled "Applying a genetic algorithm to the travelling salesman problem"
that can be found at: http://goo.gl/cJEY1
"""

import math
import random
import pygame
x = 100
y = 20
import os
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (x,y)

pygame.init()
myfont = pygame.font.SysFont("ariel", 30)

#window = pygame.display.set_mode((700, 700))

def to_pygame(coords, height, obj_height=0):
    """Convert an object's coords into pygame coordinates (lower-left of object => top left in pygame coords)."""
    return (coords[0]*3, (height - coords[1] - obj_height)*3 + 100)

def drawDot(x,y):
    pygame.draw.circle(window, (255,255,255), to_pygame((x,y), 200, 2), 5, 2)

def drawBetween(A,B,color,width):
    x1 = A.getX()
    y1 = A.getY()
    x2 = B.getX()
    y2 = B.getY()

    pygame.draw.line(window, color, to_pygame((x1, y1),200), to_pygame((x2, y2),200),width)

def writeText(text,color,distanceFromTop):
    label = myfont.render(text, 1, color)
    window.blit(label, (20, distanceFromTop))
    pygame.display.flip()

class City:
    def __init__(self, x=None, y=None):
        self.x = None
        self.y = None
        if x is not None:
            self.x = x
        else:
            self.x = int(random.random() * 200)
        if y is not None:
            self.y = y
        else:
            self.y = int(random.random() * 200)

    def getX(self):
        return self.x

    def getY(self):
        return self.y

    def distanceTo(self, city):
        xDistance = abs(self.getX() - city.getX())
        yDistance = abs(self.getY() - city.getY())
        distance = math.sqrt((xDistance * xDistance) + (yDistance * yDistance))
        return distance

    def __repr__(self):
        return str(self.getX()) + ", " + str(self.getY())


class TourManager:
    def __init__(self):
        self.destinationCities = []

    def __repr__(self):
        geneString = "|"
        for city in self.destinationCities:
            geneString += str(city) + "|"
        return geneString

    def addCity(self, city, display=True):
        self.destinationCities.append(city)
        if display:
            drawDot(city.getX(),city.getY())
            pygame.display.flip()

    def getCity(self, index):
        return self.destinationCities[index]

    def numberOfCities(self):
        return len(self.destinationCities)

    def drawCities(self):
        for city in self.destinationCities:
            drawDot(city.getX(),city.getY())
            pygame.display.flip()

    def removeCity(self, index):
        self.destinationCities.pop(index)

    def swapCities(self,index1,index2):
        self.destinationCities[index1],self.destinationCities[index2] = self.destinationCities[index2],self.destinationCities[index1]

    def takeTour(self,color,width):
        for cityIndex in range(len(self.destinationCities)):
            fromCity = self.getCity(cityIndex)
            destinationCity = None
            if cityIndex + 1 < len(self.destinationCities):
                destinationCity = self.getCity(cityIndex + 1)
            else:
                destinationCity = self.getCity(0)

            drawBetween(fromCity,destinationCity,color,width)

        pygame.display.flip()

class Tour:
    def __init__(self, tourmanager, tour=None):
        self.tourmanager = tourmanager
        self.tour = []
        self.fitness = 0.0
        self.distance = 0
        if tour is not None:
            self.tour = tour
        else:
            for i in range(0, self.tourmanager.numberOfCities()):
                self.tour.append(None)

        #self.t = turtle.Turtle()

    def __len__(self):
        return len(self.tour)

    def __getitem__(self, index):
        return self.tour[index]

    def __setitem__(self, key, value):
        self.tour[key] = value

    def __repr__(self):
        geneString = "|"
        for i in range(0, self.tourSize()):
            geneString += str(self.getCity(i)) + "|"
        return geneString

    def generateIndividual(self):
        for cityIndex in range(0, self.tourmanager.numberOfCities()):
            self.setCity(cityIndex, self.tourmanager.getCity(cityIndex))
        random.shuffle(self.tour)

    def getCity(self, tourPosition):
        return self.tour[tourPosition]

    def setCity(self, tourPosition, city):
        self.tour[tourPosition] = city
        self.fitness = 0.0
        self.distance = 0

    def getFitness(self):
        if self.fitness == 0:
            self.fitness = 1 / float(self.getDistance())
        return self.fitness

    def getDistance(self):
        if self.distance == 0:
            tourDistance = 0
            for cityIndex in range(0, self.tourSize()):
                fromCity = self.getCity(cityIndex)
                destinationCity = None
                if cityIndex + 1 < self.tourSize():
                    destinationCity = self.getCity(cityIndex + 1)
                else:
                    destinationCity = self.getCity(0)
                tourDistance += fromCity.distanceTo(destinationCity)
            self.distance = tourDistance
        return self.distance

    def tourSize(self):
        return len(self.tour)

    def containsCity(self, city):
        return city in self.tour


    def takeTour(self,color,width):
        for cityIndex in range(0, self.tourSize()):
            fromCity = self.getCity(cityIndex)
            destinationCity = None
            if cityIndex + 1 < self.tourSize():
                destinationCity = self.getCity(cityIndex + 1)
            else:
                destinationCity = self.getCity(0)

            drawBetween(fromCity,destinationCity,color,width)

            pygame.display.flip()


class Population:
    def __init__(self, tourmanager, populationSize, initialise):
        self.tours = []
        for i in range(0, populationSize):
            self.tours.append(None)

        if initialise:
            for i in range(0, populationSize):
                newTour = Tour(tourmanager)
                newTour.generateIndividual()
                self.saveTour(i, newTour)

    def __setitem__(self, key, value):
        self.tours[key] = value

    def __getitem__(self, index):
        return self.tours[index]

    def saveTour(self, index, tour):
        self.tours[index] = tour

    def getTour(self, index):
        return self.tours[index]

    def getFittest(self, start=0):
        fittest = self.tours[0]
        for i in range(start, self.populationSize()):
            if fittest.getFitness() <= self.getTour(i).getFitness():
                fittest = self.getTour(i)
        return fittest

    def drawFittestTour(self,color,width):
        fittest = self.getFittest()
        fittest.takeTour(color,width)

    def drawFirstTour(self,color,width):
        first = self.tours[0]
        first.takeTour(color,width)

    def populationSize(self):
        return len(self.tours)


class GA:
    def __init__(self, tourmanager, mutationRate = 0.015, tournamentSize = 5, elitism = 1):
        self.tourmanager = tourmanager
        self.mutationRate = mutationRate
        self.tournamentSize = tournamentSize
        self.elitism = elitism

    def evolvePopulation(self, pop):
        newPopulation = Population(self.tourmanager, pop.populationSize(), False)
        elitismOffset = self.elitism
        for i in range(elitismOffset):
            newPopulation.saveTour(i, pop.getFittest(i))

        for i in range(elitismOffset, newPopulation.populationSize()):
            parent1 = self.tournamentSelection(pop)
            parent2 = self.tournamentSelection(pop)
            child = self.crossover(parent1, parent2)
            newPopulation.saveTour(i, child)

        for i in range(elitismOffset, newPopulation.populationSize()):
            self.mutate(newPopulation.getTour(i))

        return newPopulation

    def crossover(self, parent1, parent2):
        child = Tour(self.tourmanager)

        startPos = int(random.random() * parent1.tourSize())
        endPos = int(random.random() * parent1.tourSize())

        for i in range(0, child.tourSize()):
            if startPos < endPos and i > startPos and i < endPos:
                child.setCity(i, parent1.getCity(i))
            elif startPos > endPos:
                if not (i < startPos and i > endPos):
                    child.setCity(i, parent1.getCity(i))

        for i in range(0, parent2.tourSize()):
            if not child.containsCity(parent2.getCity(i)):
                for ii in range(0, child.tourSize()):
                    if child.getCity(ii) == None:
                        child.setCity(ii, parent2.getCity(i))
                        break

        return child

    def mutate(self, tour):
        for tourPos1 in range(0, tour.tourSize()):
            if random.random() < self.mutationRate:
                tourPos2 = int(tour.tourSize() * random.random())

                city1 = tour.getCity(tourPos1)
                city2 = tour.getCity(tourPos2)

                tour.setCity(tourPos2, city1)
                tour.setCity(tourPos1, city2)

    def tournamentSelection(self, pop):
        tournament = Population(self.tourmanager, self.tournamentSize, False)
        for i in range(0, self.tournamentSize):
            randomId = int(random.random() * pop.populationSize())
            tournament.saveTour(i, pop.getTour(randomId))
        fittest = tournament.getFittest()
        return fittest