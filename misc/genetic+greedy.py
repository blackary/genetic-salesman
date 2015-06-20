from genetics2 import *
import pygame
import sys
import city_generator
import time
import greedy
import csv

numberOfCities = 30
populationCount = 100
generationsBeforeChange = 10
maxMutationRate = 0.15
minTournamentSize = 2
maxTournamentSize = 8
elitismMin = 1
elitismMax = 1
totalIterations = 100
generationCount = 400

def runGreedy(tm, display = True):
    cityList = greedy.greedy_TSP(tm)

    tourmanager2 = TourManager()

    for i in range(len(cityList)):
        tourmanager2.addCity(cityList[i],display)

    if display:
        tourmanager2.takeTour((0,255,0),1)
        tourmanager2.drawCities()

        text = "Using greedy algorithm, distance = "
        text += str(int(greedy.totalLength(tourmanager2)))
        writeText(text,(0,255,0), 0)

    return int(greedy.totalLength(tourmanager2)), tourmanager2

def runGenetic(tm,generations, population = None, totalTime = None, display = True):
    #Creates a "population" of candidates for best-tour (shortest path)
    #print("Got here!")
    if population == None:
        pop = Population(tm, populationCount, True)
    else:
        pop = population
    if totalTime == None:
        totalTime = 0
    #print("Got here!")
    #pop.drawFittestTour((255,0,0),1)
    if display:
        text = "After 0 generations, distance = "
        text += str(int(pop.getFittest().getDistance()))
        print("Got here!")
        writeText(text,(255,0,0), 20)
    ga = GA(tm,tournamentSize=3)

    printLocation = 20
    generationCount = 0
    interval = 10
    currentShortest = int(pop.getFittest().getDistance())

    """while(True):
        ev = pygame.event.get()
        # proceed events
        for event in ev:
            if event.type == pygame.QUIT:
                sys.exit(0)
    """
    s = time.time()
    for i in range(generations):
        pop = ga.evolvePopulation(pop)

        if((i+1)%generationsBeforeChange==0):
            #pass
            mutation = random.random()*maxMutationRate
            tournament = random.randint(minTournamentSize,maxTournamentSize)
            elitism = random.randint(elitismMin,elitismMax)
            ga = GA(tm,mutation,tournament,elitism)
        e = time.time()
        if (totalTime!=0) & ((e-s) > totalTime):
            break

    #window.fill((0,0,0))
    if display:
        tm.drawCities()
        text = "After "
        text += str(generations)
        text += " generations, distance = "
        text += str(int(pop.getFittest().getDistance()))
        text += ", "
        text += str(int(currentShortest - pop.getFittest().getDistance()))
        text += " units shorter"
        writeText(text,(255,255,255), printLocation+20)
        pop.drawFittestTour((255,255,255),1)
        pygame.display.flip()

    return int(pop.getFittest().getDistance())

def tourmanagerToTour(tm):
    tour = Tour(tm, tm.destinationCities)

    return tour

def geneticPlus(tm2,popCount):
    pop = Population(tm2, popCount, True)
    """for i in range(popCount):
        print("Tour #", i)
        newTour = rotateTour(tm2,i)
        pop.saveTour(i,newTour)"""
    pop.saveTour(0,tourmanagerToTour(tm2))
    pop.saveTour(1,tourmanagerToTour(tm2))
    geneticPlusLen = runGenetic(tm2,100,pop)
    return geneticPlusLen

def rotateTour(tm, index):
    tmNew = TourManager()
    for i in range(tm.numberOfCities()):
        tmNew.addCity(tm.getCity((i+index)%tm.numberOfCities()),display=False)
    return tourmanagerToTour(tmNew)

def main():
    #window.fill((0,0,0))

    with open("tsp.csv","a",newline='') as ofile:
        writer = csv.writer(ofile, delimiter = ',')
        size = os.path.getsize("tsp.csv")
        if size == 0:
            line1 = ["GreedyTime","GreedyLen","GeneticTime","GeneticLen","GeneticPlusTime","GeneticPlusLen"]
            writer.writerow(line1)

        for i in range(totalIterations):
            tourmanager = city_generator.random(numberOfCities,display=False)
            #tourmanager = city_generator.twenty_fixed()
            #tourmanager = city_generator.clickForCities()
            #tourmanager = city_generator.fetch_fifty_files('fifty.pickle')
            print("Tourmanager: ",tourmanager)
            print("Running greedy...")
            start = time.time()
            greedyLen,tm2 = runGreedy(tourmanager, display=False)
            done = time.time()
            greedyTime = done - start

            #print("Tourmanager: ",tourmanager)
            print("Running genetic...")
            start = time.time()
            #Run genetic algorithm for 400 generations
            geneticLen = runGenetic(tourmanager,generationCount,display=False)
            done = time.time()
            geneticTime = done-start

            print("Running greedy genetic...")
            start = time.time()
            #Run greedy+genetic algorithm
            pop = Population(tourmanager, populationCount, True)
            pop.saveTour(0,tourmanagerToTour(tm2))
            pop.saveTour(1,tourmanagerToTour(tm2))
            geneticPlusLen = runGenetic(tm2,generationCount*10,pop,totalTime=geneticTime, display=False)
            #geneticPlusLen = geneticPlus(tm2,10)
            done = time.time()
            geneticPlusTime = done-start

            print("****************Loop number", i, "*************************")
            print("Greedy time: ", greedyTime)
            print("Greedy length: ", greedyLen)
            print("Genetic time: ", geneticTime)
            print("Genetic length: ", geneticLen)
            print("Genetic+ time: ", geneticPlusTime)
            print("Genetic+ length: ", geneticPlusLen)

            data = [greedyTime,greedyLen,geneticTime,geneticLen,geneticPlusTime,geneticPlusLen]
            writer.writerow(data)

    """while(True):
        ev = pygame.event.get()
        # proceed events
        for event in ev:
            if event.type == pygame.QUIT:
                sys.exit(0)"""

if __name__ == '__main__': main()