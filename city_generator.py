from genetics2 import *
import sys
import pickle
from random import randrange

def random(numberOfCities,display=True):
    tm = TourManager()
    for i in range(numberOfCities):
        tm.addCity(City(),display)
    return tm

def clickForCities():
    tm = TourManager()
    keepGoing = True
    while(keepGoing):
        ev = pygame.event.get()
        # proceed events
        for event in ev:
        # handle MOUSEBUTTONDOWN
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                print("Clicked!",pos)
                x,y = int(pos[0]/3),int((700 - pos[1]+2)/3)
                print(x,y)
                tm.addCity(City(x,y))
            if event.type == pygame.KEYDOWN:
                keepGoing = False
            if event.type == pygame.QUIT:
                sys.exit(0)
    return tm

def generate_fifty_files(filename):
    cityList = []
    for i in range(50):
        x = randrange(200)
        y = randrange(200)
        cityList.append((x,y))
    with open(filename, 'wb') as f:
        pickle.dump(cityList,f)

def fetch_fifty_files(filename,display=True):
    tm = TourManager()
    with open(filename, 'rb') as f:
        cityList = pickle.load(f)
    for i in range(50):
        x = cityList[i][0]
        y = cityList[i][1]
        tm.addCity(City(x,y),display)
    return tm

def twenty_fixed():
   tm = TourManager()
   city = City(60, 200)
   tm.addCity(city)
   city2 = City(180, 200)
   tm.addCity(city2)
   city3 = City(80, 180)
   tm.addCity(city3)
   city4 = City(140, 180)
   tm.addCity(city4)
   city5 = City(20, 160)
   tm.addCity(city5)
   city6 = City(100, 160)
   tm.addCity(city6)
   city7 = City(200, 160)
   tm.addCity(city7)
   city8 = City(140, 140)
   tm.addCity(city8)
   city9 = City(40, 120)
   tm.addCity(city9)
   city10 = City(100, 120)
   tm.addCity(city10)
   city11 = City(180, 100)
   tm.addCity(city11)
   city12 = City(60, 80)
   tm.addCity(city12)
   city13 = City(120, 80)
   tm.addCity(city13)
   city14 = City(180, 60)
   tm.addCity(city14)
   city15 = City(20, 40)
   tm.addCity(city15)
   city16 = City(100, 40)
   tm.addCity(city16)
   city17 = City(200, 40)
   tm.addCity(city17)
   city18 = City(20, 20)
   tm.addCity(city18)
   city19 = City(60, 20)
   tm.addCity(city19)
   city20 = City(160, 20)
   tm.addCity(city20)
   return tm

#generate_fifty_files('fifty.pickle')