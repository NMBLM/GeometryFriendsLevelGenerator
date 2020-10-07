# 1 | x | y | x | y |
# 1 | x | y | x | y | 1 | x | y | x | y | 1 | x | y | x | y | 1 | x | y | x | y | 1 | x | y | x | y |
# 1 | x | y | x | y | 1 | x | y | x | y | 1 | x | y | x | y 

import random
import evaluateFuncs as ef
import instrumentation
import time as tim

from deap import base
from deap import creator
from deap import tools
from evaluateFuncs import Level
import PILViewer as viewer

lvlOneSpecs = [ef.SpecialArea(740,360,500,360, ef.AreaType.CircleOnly), ef.SpecialArea(80,540,500,180,ef.AreaType.RectangleOnly)]

lvlTwoSepcs = [ef.SpecialArea(100,80,1100,240, ef.AreaType.Cooperative), ef.SpecialArea(430,560,340,180,ef.AreaType.RectangleOnly)]

hOne = ef.AreaHeuristic(lvlOneSpecs)
hTwo = ef.AreaHeuristic(lvlTwoSepcs)

hUsed = hTwo

IM = instrumentation.InstrumentationManager(on = True)

def getFit(ind):
    return ind.fitness.values[0]

def getFirst(a):
    return a[0]


def mutateLevel(ind):
    if random.random() < 0.2:
        for i in range(5,45,5):
            if(ind[i] % 2 == 1):
                if random.random() < 0.8: #remove plat that exists
                    ind[i] = 0
            else:
                if random.random() < 0.8: #add platform
                    ind[i] = 1
    else:
        for i in range(5,45,5):
            if(ind[i] % 2 == 1):
                if random.random() < 0.5: #change plat width height
                    ind[i+3] = random.randint(INT_MIN,XINT_MAX)
                    ind[i+4] = random.randint(INT_MIN,YINT_MAX)
                else: #change plat x and y
                    ind[i+1] = random.randint(INT_MIN,XINT_MAX)
                    ind[i+2] = random.randint(INT_MIN,YINT_MAX)
                    
                    
def levelCrossBothPlat(pOne, pTwo):
    for i in range(5,45,5):
        if(pOne[i] % 2 == 0) and (pTwo[i] % 2 == 0):
            continue
        if(pOne[i] % 2 == 1) and (pTwo[i] % 2 == 1): #both have platform
            for j in range(i+1,i+4):
                aux = pOne[j]
                pOne[j] = pTwo[j]
                pTwo[j] = aux

def levelCrossOnePlat(pOne, pTwo):
    for i in range(5,45,5):
        if(pOne[i] % 2 == 0) and (pTwo[i] % 2 == 0): #no platform in that place
            continue
        if (pOne[i] % 2 == 0 and pTwo[i] % 2 == 1) or (pOne[i] % 2 == 1 and pTwo[i] % 2 == 0): #one has platform other doesn't
            for j in range(i,i+5):
                aux = pOne[j]
                pOne[j] = pTwo[j]
                pTwo[j] = aux

        




creator.create("FitnessMax", base.Fitness, weights=(1.0, 1.0))
creator.create("Individual", list, fitness=creator.FitnessMax)

toolbox = base.Toolbox()

INT_MIN, XINT_MAX, YINT_MAX = 0, 1280 , 760
N_CYCLES = 9

toolbox.register("attr_bool", random.randint, 0, 1)
toolbox.register("attr_xInt", random.randint, INT_MIN, XINT_MAX)
toolbox.register("attr_yInt", random.randint, INT_MIN, YINT_MAX)
toolbox.register("individual", tools.initCycle, creator.Individual,
(toolbox.attr_bool, toolbox.attr_xInt , toolbox.attr_yInt, toolbox.attr_xInt, toolbox.attr_yInt), n=N_CYCLES)

#example  [0, 1159, 195, 74, 205, 0, 475, 499, 308, 246, 1, 696, 372, 266, 206, 0, 156, 82, 1261, 744, 1, 247, 187, 182, 196, 0, 927, 573, 630, 310, 1, 1027, 99, 164, 34, 1, 265, 345, 734, 657, 0, 1175, 661, 642, 738]


toolbox.register("population", tools.initRepeat, list, toolbox.individual)
toolbox.register("evaluate", hUsed.CalculateFitness)

#toolbox.register("mate", tools.cxTwoPoint)
toolbox.register("mate", levelCrossOnePlat)
#toolbox.register("mate", levelCrossBothPlat)

#toolbox.register("mutate", tools.mutUniformInt,low = INT_MIN, up = XINT_MAX, indpb=0.2)
toolbox.register("mutate", mutateLevel)
#toolbox.register("mutate", tools.mutFlipBit, indpb=0.2)


toolbox.register("select", tools.selBest)
#toolbox.register("select", tools.selTournament, tournsize=3)
INT_MIN, XINT_MAX
 
def main():
    pop = toolbox.population(n=10)
    print(pop[0])
    lvl = hUsed.TestLevel(pop[0])
    viewer.drawLevel(lvl,"Test.png")
    
#main()
popSize = 50



def GA():
    bestPop = []
    bestFit = 0
    bestFits =[]

    pop = toolbox.population(n=popSize)
    CXPB, MUTPB, NGEN = 0.5, 0.2, 50

    # Evaluate the entire population
    fitnesses = map(toolbox.evaluate, pop)
    for ind, fit in zip(pop, fitnesses):
        ind.fitness.values = fit
        

    
    for g in range(NGEN):
        startTime = tim.time()

        pop.sort(reverse = True, key = getFit)
        IM.writePop(g,pop)

        if(pop[0].fitness.values[0] > bestFit):
            bestFit = pop[0].fitness.values[0]
            bestPop = [pop[0]] + bestPop
            bestFits = [bestFit] + bestFits

        # Select the next generation individuals
        offspring = toolbox.select(pop, len(pop))
        # Clone the selected individuals
        offspring = list(map(toolbox.clone, offspring))
        
        # Apply crossover and mutation on the offspring
        for child1, child2 in zip(offspring[::2], offspring[1::2]):
            if random.random() < CXPB:
                toolbox.mate(child1, child2)
                del child1.fitness.values
                del child2.fitness.values

        for mutant in offspring:
            if random.random() < MUTPB:
                toolbox.mutate(mutant)
                del mutant.fitness.values

        # Evaluate the individuals with an invalid fitness
        invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
        fitnesses = map(toolbox.evaluate, invalid_ind)
        for ind, fit in zip(invalid_ind, fitnesses):
            ind.fitness.values = fit
        bestfit = max(offspring, key=getFit)
        # The population is entirely replaced by the offspring
        pop = list(offspring)
        print("generation: ", g,"  Time: ", tim.time() - startTime,"bestFit: ", getFit(bestfit), " popsize: ", len(pop))

    return (pop, bestPop,bestFit,bestFits)


ppl,bestPop,bestFit,bestFits  = GA()
ppl.sort(reverse = True, key = getFit)

IM.DrawPop(ppl,hUsed)

IM.DrawBestPop(bestPop,hUsed)



