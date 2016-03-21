#!/usr/bin/python
import time
import math
import random
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

def main():

    #Config variables
    step =  .05
    xmin = -2.5
    xmax =  2.5
    ymin = -2.5
    ymax =  2.5
    num_restarts = 1000
    max_temp = 1000

    r = lambda x,y: np.sqrt(x**2 + y**2)
    z = lambda x,y: (
                     ( (np.sin(x**2+3*y**2))/(0.1+r(x,y)**2) ) +
                     (x**2 + 5*y**2) *
                     ( (np.exp(1-r(x,y)**2))/(2) )
                    )

    #will save the path of each local search method
    path = {}
    runtime = {}

    #Hill Climbing
    start_time = time.time()
    path["hc"]   = hill_climb(z,step,xmin,xmax,ymin,ymax)
    runtime["hc"] = time.time() - start_time
    print ("Hill Cimbing:        min = " + str(path["hc"][-1]) + " runtime = " + str(runtime["hc"]) + " seconds")

    #Hill Climbing w/ RR
    start_time = time.time()
    path["hcrr"] = hill_climb_random_restart(z,step,num_restarts,xmin,xmax,ymin,ymax)
    runtime["hcrr"] = time.time() - start_time
    print ("Hill Cimbing w/ RR:  min = " + str(path["hcrr"][-1])+ " runtime = " + str(runtime["hcrr"]) + " seconds")

    #Simmulated Annealing
    start_time = time.time()
    path["sa"]   = simulated_annealing(z,step,max_temp,xmin,xmax,ymin,ymax)
    runtime["sa"] = time.time() - start_time
    print ("Simulated Annealing: min = " + str(path["sa"])+ " runtime = " + str(runtime["sa"]) + " seconds")



    print ("Generating graph...")

    graph(z,step,xmin,xmax,ymin,ymax)



def hill_climb(f, step, xmin, xmax, ymin, ymax):

    #stores the path taken
    path = []

    #start from the center
    x = round(random.uniform(xmin, xmax), 5)
    y = round(random.uniform(xmin, xmax), 5)

    #climb down the hills until a minima is found
    minimized = False
    while(minimized is False):

        current = f(x,y)
        path.append(current)
        #print ("z=" + str(current) + " x=" + str(x) + " y=" + str(y) + "\n")

        #check 4 directions (+x,y) (x,+y) (-x,y) (x,-y)
        if   f(x+step,y) < current: x = x + step
        elif f(x-step,y) < current: x = x - step
        elif f(x,y+step) < current: y = y + step
        elif f(x,y-step) < current: y = y - step
        else: minimized = True

    return path



def hill_climb_random_restart(f, step, num_restarts, xmin, xmax, ymin,
ymax):

    path = hill_climb(f,step,xmin,xmax,ymin,ymax)
    minima = path[-1]

    for i in range(1,num_restarts):

        new_path = hill_climb(f,step,xmin,xmax,ymin,ymax)
        new_minima = new_path[-1]

        if new_minima < minima:
            minima = new_minima
            path = new_path

    #print (path[-1])
    return path


def simulated_annealing(f, step, max_temp, xmin, xmax, ymin, ymax):

    prob = lambda old,new,T: math.exp((old-new)/T)

    path = [] #store the path

    T = max_temp
    min_temp = 0.00001
    alpha = 0.9

    x = round(random.uniform(xmin, xmax), 5)
    y = round(random.uniform(xmin, xmax), 5)

    solution = f(x,y)

    while T > min_temp:
        i = 1
        while i <= 100:
            new_x = round(random.uniform(xmin, xmax), 5)
            new_y = round(random.uniform(xmin, xmax), 5)
            new_solution = f(new_x,new_y)
            ap = prob(solution,new_solution,T)

            if ap > random.random():
                solution = new_solution

            i += 1
        T = T*alpha

    return solution


def graph(f, step, xmin, xmax, ymin, ymax):


    X = np.arange(xmin, xmax, step)
    Y = np.arange(ymin, ymax, step)
    xc, yc = np.meshgrid(X, Y)

    Z = f(xc,yc)
    fig = plt.figure(1)
    ax = fig.add_subplot(111,projection="3d")
    ax.plot_surface(xc,yc,Z)
    plt.show()


main()
