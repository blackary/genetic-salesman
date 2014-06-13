from genetics2 import *
import pygame
import sys
import city_generator

numberOfCities = 30
populationCount = 50

#tourmanager = city_generator.random(numberOfCities)
#tourmanager = city_generator.twenty_fixed()
#tourmanager = city_generator.clickForCities()
tourmanager = city_generator.fetch_fifty_files('fifty.txt')

#Creates a "population" of candidates for best-tour (shortest path)
pop = Population(tourmanager, populationCount, True)


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

