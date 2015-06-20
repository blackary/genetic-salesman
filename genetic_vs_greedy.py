from genetics import *
import pygame
import sys
import city_generator
import time
import greedy
import csv

GREEDY_COLOR = (0, 255, 0)
GENETIC_COLOR = (255, 0, 0)
GREEDY_GENETIC_COLOR = (0, 0, 255)
PRINTGAP = 20

numberOfCities = 30
populationCount = 100
generationsBeforeChange = 10
maxMutationRate = 0.15
minTournamentSize = 2
maxTournamentSize = 8
elitismMin = 1
elitismMax = 1
totalIterations = 100  # max iterations
generationCount = 400  # was 400


def runGreedy(tm, display=True):
    cityList = greedy.greedy_TSP(tm)

    tourmanager2 = TourManager()

    for i in range(len(cityList)):
        tourmanager2.addCity(cityList[i], display)

    if display:
        tourmanager2.takeTour((0, 255, 0), 1)
        tourmanager2.drawCities()

        text = "Using greedy algorithm, distance = "
        text += str(int(greedy.totalLength(tourmanager2)))
        writeText(text, (0, 255, 0), 0)

    return int(greedy.totalLength(tourmanager2)), tourmanager2, text


def runGenetic(tm, generations, population=None, totalTime=None, display=True, greedyGenetic=False, text1="",
               greedyTour="", geneticPop="", geneticBest=0):
    # Creates a "population" of candidates for best-tour (shortest path)
    if population == None:
        pop = Population(tm, populationCount, True)
    else:
        pop = population
    if totalTime == None:
        totalTime = 0

    ga = GA(tm, tournamentSize=3)

    currentShortest = int(pop.getFittest().getDistance())

    s = time.time()
    for i in range(generations):
        pop = ga.evolvePopulation(pop)

        if ((i + 1) % generationsBeforeChange == 0):  # Add in manipulations to genetic algorithm variables periodically
            mutation = random.random() * maxMutationRate
            tournament = random.randint(minTournamentSize, maxTournamentSize)
            elitism = random.randint(elitismMin, elitismMax)
            ga = GA(tm, mutation, tournament, elitism)
        e = time.time()
        #For fair comparison, make Greedy Genetic run for same time as Genetic
        if (totalTime != 0) & ((e - s) > totalTime):
            break

        newShortest = int(pop.getFittest().getDistance())

        if display and newShortest != currentShortest:
            window.fill((0, 0, 0))
            if greedyTour != "":
                writeText(text1, GREEDY_COLOR, 0)
                greedyTour.takeTour(GREEDY_COLOR, 5)
            tm.drawCities()
            if greedyGenetic:
                text = "Greedy Genetic: After %d generations, distance = %d. A gain of %d!" % (
                    i + 1, newShortest, currentShortest - newShortest)
            else:
                text = "Pure Genetic: After %d generations, distance = %d. A gain of %d!" % (
                    i + 1, newShortest, currentShortest - newShortest)

            if greedyGenetic:
                geneticText = "Best pure genetic : " + str(geneticBest)
                writeText(geneticText, GENETIC_COLOR, PRINTGAP)
                geneticPop.drawFittestTour(GENETIC_COLOR, 3)
                writeText(text, GREEDY_GENETIC_COLOR, 2 * PRINTGAP)
                pop.drawFittestTour(GREEDY_GENETIC_COLOR, 1)
            else:
                writeText(text, GENETIC_COLOR, PRINTGAP)
                pop.drawFittestTour(GENETIC_COLOR, 1)
            pygame.display.flip()
            currentShortest = newShortest

    return int(pop.getFittest().getDistance()), pop

def tourmanagerToTour(tm):
    tour = Tour(tm, tm.destinationCities)
    return tour

def rotateTour(tm, index):
    tmNew = TourManager()
    for i in range(tm.numberOfCities()):
        tmNew.addCity(tm.getCity((i + index) % tm.numberOfCities()), display=False)
    return tourmanagerToTour(tmNew)


def printText(greedyText, geneticText, greedyGeneticText, menuText):
    window.fill((0, 0, 0))
    writeText(menuText, (255, 255, 255), 3 * PRINTGAP)
    writeText(greedyText, GREEDY_COLOR, 0)
    writeText(geneticText, GENETIC_COLOR, PRINTGAP)
    writeText(greedyGeneticText, GREEDY_GENETIC_COLOR, 2 * PRINTGAP)


def main():
    # window.fill((0,0,0))

    with open("tsp-small.csv", "a", newline='') as ofile:
        writer = csv.writer(ofile, delimiter=',')
        size = os.path.getsize("tsp-small.csv")
        if size == 0:
            line1 = ["GreedyTime", "GreedyLen", "GeneticTime", "GeneticLen", "GeneticPlusTime", "GeneticPlusLen"]
            writer.writerow(line1)

        for i in range(totalIterations):
            menu_text = "Press 1 to choose city locations, 2 to generate %d random cities" % numberOfCities
            window.fill((0, 0, 0))
            writeText(menu_text, (255, 255, 255), 0)
            chosen = False
            while not chosen:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        sys.exit()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_1:
                            tourmanager = city_generator.clickForCities()
                            chosen = True
                        elif event.key == pygame.K_2:
                            tourmanager = city_generator.random(numberOfCities, display=True)
                            chosen = True
            window.fill((0, 0, 0))
            #Other options for city generation
            # tourmanager = city_generator.twenty_fixed()
            #tourmanager = city_generator.fetch_fifty_files('fifty.pickle')

            print("Tourmanager: ", tourmanager)
            print("Running greedy...")
            start = time.time()
            greedyLen, tm2, greedyText = runGreedy(tourmanager, display=True)
            done = time.time()
            greedyTime = done - start

            #print("Tourmanager: ",tourmanager)
            print("Running genetic...")
            start = time.time()
            #Run genetic algorithm for 400 generations
            geneticLen, pop2 = runGenetic(tourmanager, generationCount, display=True, text1=greedyText, greedyTour=tm2)
            done = time.time()
            geneticTime = done - start

            print("Running greedy genetic...")
            start = time.time()
            #Run greedy+genetic algorithm by adding two versions of the greedy algorithm to the initial population
            pop = Population(tourmanager, populationCount, True)
            pop.saveTour(0, tourmanagerToTour(tm2))
            pop.saveTour(1, tourmanagerToTour(tm2))
            geneticPlusLen, pop3 = runGenetic(tm2, generationCount * 10, pop, totalTime=geneticTime, display=True,
                                              greedyGenetic=True, greedyTour=tm2, text1=greedyText, geneticPop=pop2,
                                              geneticBest=geneticLen)
            done = time.time()
            geneticPlusTime = done - start

            print("****************Loop number", i, "*************************")
            print("Greedy time: ", greedyTime)
            print("Greedy length: ", greedyLen)
            print("Genetic time: ", geneticTime)
            print("Genetic length: ", geneticLen)
            print("Genetic+ time: ", geneticPlusTime)
            print("Genetic+ length: ", geneticPlusLen)

            data = [greedyTime, greedyLen, geneticTime, geneticLen, geneticPlusTime, geneticPlusLen]
            writer.writerow(data)

            menu_text = "1: try again, 2: quit, 3: see GREEDY, 4: GENETIC, 5: GREEDY, 6: all 3"
            finalGreedyText = greedyText
            finalGeneticText = "Best pure genetic : %d " % (geneticLen)
            finalGreedyGeneticText = "Best greedy genetic: %d " % (geneticPlusLen)

            printText(finalGreedyText, finalGeneticText, finalGreedyGeneticText, menu_text)
            tm2.takeTour(GREEDY_COLOR, 1)
            pop2.drawFittestTour(GENETIC_COLOR, 1)
            pop3.drawFittestTour(GREEDY_GENETIC_COLOR, 1)

            chosen = False
            while not chosen:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        sys.exit()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_1:
                            chosen = True
                        elif event.key == pygame.K_2:
                            sys.exit(0)
                        elif event.key == pygame.K_3:
                            printText(finalGreedyText, finalGeneticText, finalGreedyGeneticText, menu_text)
                            tm2.takeTour(GREEDY_COLOR, 5)
                        elif event.key == pygame.K_4:
                            printText(finalGreedyText, finalGeneticText, finalGreedyGeneticText, menu_text)
                            pop2.drawFittestTour(GENETIC_COLOR, 5)
                        elif event.key == pygame.K_5:
                            printText(finalGreedyText, finalGeneticText, finalGreedyGeneticText, menu_text)
                            pop3.drawFittestTour(GREEDY_GENETIC_COLOR, 5)
                        elif event.key == pygame.K_6:
                            printText(finalGreedyText, finalGeneticText, finalGreedyGeneticText, menu_text)
                            tm2.takeTour(GREEDY_COLOR, 1)
                            pop2.drawFittestTour(GENETIC_COLOR, 1)
                            pop3.drawFittestTour(GREEDY_GENETIC_COLOR, 1)

    while (True):
        ev = pygame.event.get()
        # proceed events
        for event in ev:
            if event.type == pygame.QUIT:
                sys.exit(0)


if __name__ == '__main__': main()