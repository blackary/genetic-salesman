import genetics2
import random
import math

def distance(city1,city2):
    x1 = city1.getX()
    y1 = city1.getY()
    x2 = city2.getX()
    y2 = city2.getY()

    return math.sqrt((y2-y1)*(y2-y1) + (x2-x1)*(x2-x1))

def totalLength(tourmanager):
    length = 0
    for i in range(tourmanager.numberOfCities()):
        if i < tourmanager.numberOfCities()-1:
            length += distance(tourmanager.getCity(i),tourmanager.getCity(i+1))
        else:
            length += distance(tourmanager.getCity(i),tourmanager.getCity(0))
    return length

def greedy_TSP(tourmanager):
    "At each step, visit the nearest neighbor that is still unvisited."
    cities = tourmanager.destinationCities[:]
    start = first(cities)
    tour = [start]
    for x in [start]:
        cities.remove(x)

    unvisited = cities

    while unvisited:
        C = nearest_neighbor(tour[-1], unvisited)
        tour.append(C)
        unvisited.remove(C)
    return tour

def nearest_neighbor(A, cities):
    "Find the city in cities that is nearest to city A."
    return min(cities, key=lambda x: distance(x, A))

def first(collection):
    "Start iterating over collection, and return the first element."
    for x in collection: return x