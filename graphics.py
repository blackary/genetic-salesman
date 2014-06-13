from genetics3 import *
import pygame
import sys
import city_generator

numberOfCities = 30
populationCount = 50

#tourmanager = city_generator.random(numberOfCities)
#tourmanager = city_generator.twenty_fixed()
tourmanager = city_generator.clickForCities()

#Creates a "population" of candidates for best-tour (shortest path)
pop = Population(tourmanager, populationCount, True)

pop.drawFittestTour((255,0,0),1)
text = "After 0 generations, distance = "
text += str(int(pop.getFittest().getDistance()))
writeText(text,(255,0,0), 0)
ga = GA(tourmanager)

printLocation = 20
generationCount = 0
interval = 10

while(True):
        ev = pygame.event.get()
        # proceed events
        for event in ev:
        # handle MOUSEBUTTONDOWN
            if event.type == pygame.MOUSEBUTTONDOWN:
                for i in range(interval):
                    pop = ga.evolvePopulation(pop)
                    generationCount += 1
                text = "After "
                text += str(generationCount)
                text += " generations, distance = "
                text += str(int(pop.getFittest().getDistance()))
                writeText(text,(generationCount*3,generationCount*3,generationCount*3), printLocation)
                printLocation+=20
            if event.type == pygame.KEYDOWN:
                pop.drawFittestTour((generationCount*3,generationCount*3,generationCount*3),1)
            if event.type == pygame.QUIT:
                sys.exit(0)
pop.drawFittestTour((255,0,0),1)
text = "After 0 generations, distance = "
text += str(int(pop.getFittest().getDistance()))
writeText(text,(255,0,0), 0)

# Evolve population for 20 generations
ga = GA(tourmanager)
pop = ga.evolvePopulation(pop)
for i in range(0, 20):
    pop = ga.evolvePopulation(pop)

pop.drawFittestTour((0,255,0),2)
text = "After 20 generations, distance = "
text += str(int(pop.getFittest().getDistance()))

writeText(text,(0,255,0), 30)

# Evolve population for 180 generations
ga = GA(tourmanager)
pop = ga.evolvePopulation(pop)
for i in range(0, 180):
    pop = ga.evolvePopulation(pop)

pop.drawFittestTour((0,0,255),3)
text = "After 200 generations, distance = "
text += str(int(pop.getFittest().getDistance()))

writeText(text,(0,0,255), 60)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit(0)
            #else:
            #print(event)"""

