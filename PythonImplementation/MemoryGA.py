# 1 | x | y | x | y |
# 1 | x | y | x | y | 1 | x | y | x | y | 1 | x | y | x | y | 1 | x | y | x | y | 1 | x | y | x | y |
# 1 | x | y | x | y | 1 | x | y | x | y | 1 | x | y | x | y 
#INT_MIN, XINT_MAX, YINT_MAX = 0, 1280 , 760 or 80, 47.5

import random
import evaluateFuncs as ef
import instrumentation
import time as tim
import Functions as fs
import numpy as np
import config as cfg
from guppy import hpy
from deap import base
from deap import creator
from deap import tools
from evaluateFuncs import Level

INT_MIN, XINT_MAX, YINT_MAX = 3, 76, 47
CXPB, MUTPB, NGEN = 0.9 , 0.8, 500

toolbox = base.Toolbox()
cfg.toolbox = toolbox

lvlTwoSpecs = [ef.SpecialArea(100,80,1100,240, ef.AreaType.Cooperative), ef.SpecialArea(430,560,340,180,ef.AreaType.RectangleOnly)]

lvlThreeSpecs = [ef.SpecialArea(90,600,140,140, ef.AreaType.RectangleOnly), 
ef.SpecialArea(1100,600,140,140, ef.AreaType.RectangleOnly), 
ef.SpecialArea(1100,80,140,140, ef.AreaType.Cooperative)]


hTwo = ef.AreaHeuristic(lvlTwoSpecs, smaller = True)
hThree = ef.AreaHeuristic(lvlThreeSpecs, smaller = True)

#rec circle coop common
hPerOne = ef.AreaPercentangeHeuristic(0.25,0.2,0.25,0.1, smaller = True)

hPer2One = ef.AreaPercentangeTwoHeuristic(0.3,0.2,0.3,0.2, smaller = True)

cfg1 = cfg.Config(h = hTwo, mate = fs.levelCrossOneChild, mutate= fs.mutateLevel, select= tools.selBest, popSize= 50, genNumber= 100, sm = True)
cfg2 = cfg.Config(h = hThree, mate = fs.levelCrossOneChild, mutate= fs.mutateLevel, select= tools.selBest, popSize= 50, genNumber= 100, sm = True)
cfg11 = cfg.Config(h = hTwo, mate = fs.levelCrossOneChild, mutate= fs.mutateLevel, select= tools.selBest, popSize= 10, genNumber= 100, sm = True)
cfg22 = cfg.Config(h = hThree, mate = fs.levelCrossOneChild, mutate= fs.mutateLevel, select= tools.selBest, popSize= 10, genNumber= 100, sm = True)
cfg3 = cfg.Config(h = hPerOne, mate = fs.levelCrossOneChild, mutate= fs.mutateLevel, select= tools.selBest, popSize= 50, genNumber= 100, sm = True)
cfg4 = cfg.Config(h = hPer2One, mate = fs.levelCrossOneChild, mutate= fs.mutateLevel, select= tools.selBest, popSize= 50, genNumber= 100, sm = True)

ConfigMetric = [cfg1,cfg11,cfg2,cfg22,cfg3,cfg4]

IM = []


def getFit(ind):
    return ind.fitness.values[0]

creator.create("FitnessMax", base.Fitness, weights=(1.0, 1.0))
creator.create("Individual", list, fitness=creator.FitnessMax)


N_CYCLES = 9

toolbox.register("attr_bool", random.randint, 0, 1)
#toolbox.register("attr_posXInt", random.randint, INT_MIN, XINT_MAX)
#toolbox.register("attr_posYInt", random.randint, INT_MIN, YINT_MAX)
toolbox.register("attr_xInt", random.randint, INT_MIN, XINT_MAX)
toolbox.register("attr_yInt", random.randint, INT_MIN, YINT_MAX)
toolbox.register("individual", tools.initCycle, creator.Individual,
(toolbox.attr_bool, toolbox.attr_xInt , toolbox.attr_yInt, toolbox.attr_xInt, toolbox.attr_yInt), n=N_CYCLES)

#example  [0, 1159, 195, 74, 205, 0, 475, 499, 308, 246, 1, 696, 372, 266, 206, 0, 156, 82, 1261, 744, 1, 247, 187, 182, 196, 0, 927, 573, 630, 310, 1, 1027, 99, 164, 34, 1, 265, 345, 734, 657, 0, 1175, 661, 642, 738]


toolbox.register("population", tools.initRepeat, list, toolbox.individual)


#toolbox.register("mate", tools.cxTwoPoint)
toolbox.register("mate", fs.levelCrossPlat)


#toolbox.register("mutate", tools.mutUniformInt,low = INT_MIN, up = YINT_MAX, indpb=0.2)
#toolbox.register("mutate", fs.mutateLevel)
#toolbox.register("mutate", fs.levelChangeOneValue)
toolbox.register("mutate", fs.levelUniformChangeValue)
#toolbox.register("mutate", tools.mutFlipBit, indpb=0.2)


toolbox.register("select", tools.selBest)
#toolbox.register("select", tools.selTournament, tournsize=3)
#toolbox.register("select", tools.selStochasticUniversalSampling)

treshold = 0.92
tresholdMax = 80
elitism = 1
hhpy = hpy()
print(hhpy.heap())
def GALoop(hUsed,popSize,NGEN,config):
    global hhpy
    #global IM
    #IM = instrumentation.InstrumentationManager(on = True)
    curTresh = 0
    if not isinstance(hUsed,ef.AreaPercentangeHeuristic) and not isinstance(hUsed,ef.AreaPercentangeTwoHeuristic):
        IM.DrawSpecs(hUsed)
    else:
        IM.DrawPerSpec(hUsed)

    bestPop = []
    bestFit = 0
    bestFits =[]
    pop = toolbox.population(n=popSize)

    # Evaluate the entire population
    fitnesses = map(toolbox.evaluate, pop)
    for ind, fit in zip(pop, fitnesses):
        ind.fitness.values = fit
        

    pop.sort(reverse = True, key = getFit)
    print(hhpy.heap())
    for g in range(NGEN):
        startTime = tim.time()
        IM.WritePop(g,pop)
        IM.WriteGenData(g,pop)
        if(pop[0].fitness.values[0] > bestFit):
            bestFit = pop[0].fitness.values[0]
            bestPop = [toolbox.clone(pop[0])] + bestPop
            bestFits = [bestFit] + bestFits

        if bestFit > treshold:
            curTresh += 1
            if curTresh > tresholdMax:
                return (pop, bestPop, bestFit, bestFits)
        
        # Select the next generation individuals
        offspring = toolbox.select(pop, len(pop)-elitism)
        toAdd = list(map(toolbox.clone, pop[0:elitism]))
        # Clone the selected individuals
        #offspring = list(map(toolbox.clone, offspring))
        
        # Guarantee no copies of levels and min popsize
        #offspring = list(map(toolbox.clone, fs.diversityExactEqual(offspring)))
        #offspring = list(map(toolbox.clone, fs.diversityEqual(offspring)))
        offspring = list(map(toolbox.clone, fs.diversityEqualPlatform(offspring)))

        offspringLen = len(offspring)
        newOffspring = []
        while (offspringLen + len(newOffspring) < (popSize - elitism) ):
            newOffspring = toolbox.population(n=(popSize - elitism) - (offspringLen)) #generate random offspring
            '''
            parentOne = random.randint(0,offspringLen-1)
            parentTwo = random.randint(0,offspringLen-1)
            while parentOne == parentTwo:
                parentTwo = random.randint(0,offspringLen-1)
            childOne = toolbox.clone(offspring[parentOne])
            childTwo = toolbox.clone(offspring[parentTwo])
            toolbox.mate(childOne, childTwo)
            del childOne.fitness.values
            del childTwo.fitness.values
            newOffspring += [childOne,childTwo]
            '''
        crossoverTime = tim.time()
        # Apply crossover and mutation on the offspring
        if config.specialMate:
            offspring.sort(reverse = True, key = getFit)
            childOffSpring = []
            offspringLen = len(offspring)
            
            i = 0
            j = 1  #so that it mates with itself and stays in the pool
            while len(childOffSpring) < offspringLen - len(toAdd) :
                child = fs.levelCrossOneChild(toolbox.clone(offspring[i]), toolbox.clone(offspring[j]))
                del child.fitness.values
                childOffSpring += [child]
                j += 1
                if j > int(offspringLen * 0.3) :
                    i += 1
                    j = i + 1
                    if i == offspringLen:
                        i = 0
                        j = i + 1
                    
            offspring = childOffSpring
        else:
            childOffSpring = []
            offspringLen = len(offspring)
            for parent1, parent2 in zip(offspring[::2], offspring[1::2]):
                child1 = fs.levelCrossOneChild(toolbox.clone(parent1), toolbox.clone(parent2))
                child2 = fs.levelCrossOneChild(toolbox.clone(parent2), toolbox.clone(parent1))
                del child1.fitness.values
                del child2.fitness.values
                childOffSpring += [child1,child2]
            offspring = childOffSpring
        crossoverEndTime = tim.time() - crossoverTime

        offspring += newOffspring
        mutationTime = tim.time()
        for mutant in offspring:
            if random.random() < MUTPB:
                toolbox.mutate(mutant)
                del mutant.fitness.values
        mutationEndTime = tim.time() - mutationTime
        offspring = offspring + list(map(toolbox.clone, toAdd))
        
        # Evaluate the individuals with an invalid fitness
        evalTime = tim.time()
        invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
        fitnesses = map(toolbox.evaluate, invalid_ind)
        for ind, fit in zip(invalid_ind, fitnesses):
            ind.fitness.values = fit
        evalEndTime = tim.time() - evalTime
        # The population is entirely replaced by the offspring
        pop = list(offspring)
        pop.sort(reverse = True, key = getFit)
        timetaken = tim.time() - startTime
        print("generation: ", g,"  Time: ", timetaken,"bestFit: ", getFit(pop[0]), " popsize: ", len(pop))
        IM.WriteToRND(str(g) + ':' + str(timetaken)+':'+str(crossoverEndTime)+':'+str(mutationEndTime)+':'+str(evalEndTime) + '\n' ,name = "\\time")
        IM.WriteToRND("gen "+ str(g) + "\n" + str(hhpy.heap()) + "\n",name = "\\heap")
    return (pop, bestPop,bestFit,bestFits)



def main():
    global IM
    global hhpy
    print(hhpy.heap())
    for c in ConfigMetric:
        IM = instrumentation.InstrumentationManager(on = False,popWrite = False)
        IM.WriteToRND(c.description())
        c.setup()
        ppl,bestPop,bestFit,bestFits  = GALoop(c.h,c.popSize, c.genNumber,c)
        ppl.sort(reverse = True, key = getFit)
        IM.popWrite = True
        IM.on = True
        IM.WritePop(1,ppl)
        IM.DrawPop(ppl,c.h)
        IM.DrawBestPop(bestPop,c.h)

def Test():
    TestLvl = [1, 320, 678, 120, 678, 1, 460, 400, 75, 300, 1, 735, 400, 75, 300, 1, 535, 400, 250, 75, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    TestLvl =  [0, 984, 696, 88, 650, 1, 200, 600, 288, 32, 1, 504, 376, 48, 384, 1, 552, 648, 256, 32, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    #TestLvl = [1, 22, 12, 6, 35, 1, 64, 19, 34, 35, 1, 27, 22, 44, 3, 1, 65, 46, 30, 16, 1, 71, 30, 27, 33, 1, 75, 45, 66, 8, 1, 60, 39, 74, 28, 1, 27, 46, 35, 38, 1, 12, 24, 12, 41]
    #TestLvl = [1, 984, 696, 88, 650,  1, 200, 600, 288, 32, 1, 504, 376, 48, 384, 1, 552, 648, 256, 32, 0, 71, 30, 27, 33, 0, 75, 45, 66, 8, 0, 60, 39, 74, 28, 0, 27, 46, 35, 38, 0, 12, 24, 12, 41]
    #TestLvl = [1, 232, 328, 104, 328,  1, 936, 568, 160, 128, 1, 232, 568, 160, 128, 1, 40, 456, 480, 112, 1, 728, 456, 512, 128, 1, 1080, 184, 160, 272, 0, 60, 39, 74, 28, 0, 27, 46, 35, 38, 0, 12, 24, 12, 41]
    #TestLvl = [0, 22, 21, 21, 32, 1, 5, 35, 64, 3, 1, 62, 34, 29, 17, 0, 38, 32, 15, 38, 0, 38, 35, 50, 6, 0, 7, 33, 41, 4, 0, 67, 32, 50, 31, 0, 19, 22, 10, 34, 1, 46, 12, 9, 27]
    #TestLvl = [1, 61, 43, 5, 40, 1, 12, 37, 18, 2, 1, 31, 23, 3, 24, 1, 34, 25, 15, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    #TestLvl = [1, 20, 42, 7, 42, 1, 28, 25, 4, 18, 1, 45, 25, 4, 18, 1, 33, 40, 16, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    #TestLvl = [1,61, 43, 5, 40, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 12, 37, 18, 4, 0, 31, 23, 3, 24, 0, 0, 0, 0, 0, 1, 34, 40, 16, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    TestLvl = [1,20, 42, 7, 42, 1, 28, 25, 4, 18, 1, 45, 25, 4, 18, 1, 33, 25, 15, 2, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    IM = instrumentation.InstrumentationManager(on = True)
    hTwo.smallerLevels = True
    IM.DrawLevel(TestLvl,hTwo)




main()
#Test()
