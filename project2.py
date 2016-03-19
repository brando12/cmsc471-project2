#!/usr/bin/python
import math
import random
import matplotlib.pyplot as plt

def main():

    #Config variables
    step =  .1
    xmin = -2.5
    xmax =  2.5
    ymin = -2.5
    ymax =  2.5
    num_restarts = 10
    max_temp = 1000

    r = lambda x,y: math.sqrt(x**2 + y**2)
    z = lambda x,y: (
                     ( (math.sin(x**2+3*y**2))/(0.1+r(x,y)**2) ) +
                     (x**2 + 5*y**2) *
                     ( (math.exp(1-r(x,y)**2))/(2) )
                    )

    #will save the path of each local search method
    path = {}

    #path["hc"]   = hill_climb(z,step,xmin,xmax,ymin,ymax)


    #path["hcrr"] = hill_climb_random_restart(z,step,num_restarts,xmin,xmax,ymin,ymax)

    path["sa"]   = simulated_annealing(z,step,max_temp,xmin,xmax,ymin,ymax)

    print (path["sa"])

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
        print ("z=" + str(current) + " x=" + str(x) + " y=" + str(y) + "\n")

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

    print (path[-1])
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

    i = 0.1
    posy = 0
    posx = 0
    x = []
    y = []
    z = []

    while (posx < xmax):
        x.append(posx)
        posx += i

        while (posy < ymax):
            y.append(posx)
            z.append(f(posx,posy))
            posy += i

    plt.plot(x, y, z)
    plt.show()


main()
