import random
import evaluateFuncs as ef
import instrumentation
import time as tim
import Functions as fs
import numpy as np

from deap import base
from deap import creator
from deap import tools
from evaluateFuncs import Level

specs = []
hUsed = ef.AreaHeuristic(specs,smaller=True)
IM = []

creator.create("FitnessMax", base.Fitness, weights=(1.0, 1.0))
creator.create("Individual", list, fitness=creator.FitnessMax)

toolbox = base.Toolbox()

INT_MIN, XINT_MAX, YINT_MAX = 3, 76, 47

N_CYCLES = 9

toolbox.register("attr_bool", random.randint, 0, 1)
toolbox.register("attr_xInt", random.randint, INT_MIN, XINT_MAX)
toolbox.register("attr_yInt", random.randint, INT_MIN, YINT_MAX)
toolbox.register("individual", tools.initCycle, creator.Individual,
(toolbox.attr_bool, toolbox.attr_xInt , toolbox.attr_yInt, toolbox.attr_xInt, toolbox.attr_yInt), n=N_CYCLES)


toolbox.register("population", tools.initRepeat, list, toolbox.individual)
toolbox.register("evaluate", hUsed.CalculateFitness)

toolbox.register("mate", fs.levelCrossPlat)

#toolbox.register("mutate", fs.mutateLevel)
#toolbox.register("mutate", fs.levelChangeOneValue)
toolbox.register("mutate", fs.levelUniformChangeValue)


toolbox.register("select", tools.selBest)
#toolbox.register("select", tools.selTournament, tournsize=3)
#toolbox.register("select", tools.selStochasticUniversalSampling)


def getFit(ind):
    return ind.fitness.values[0]

def addSpec(x,y,width,height,t):
    global specs
    if t == "AreaType.Cooperative":
        t = ef.AreaType.Cooperative
    if t == "AreaType.Common":
        t = ef.AreaType.Common
    if t == "AreaType.RectangleOnly":
        t = ef.AreaType.RectangleOnly
    if t == "AreaType.CircleOnly":
        t = ef.AreaType.CircleOnly
    spec = ef.SpecialArea(x,y,width,height,t)
    specs += [spec]

#should be in the heuristic class
def replaceHSpecs(h,specs):
    h.specifications = specs

popSize = 50
elitism = 1
def GAD():
    if not isinstance(hUsed,ef.AreaPercentangeHeuristic) and not isinstance(hUsed,ef.AreaPercentangeTwoHeuristic):
        IM.DrawSpecs(hUsed)
    bestPop = []
    bestFit = 0
    bestFits =[]

    pop = toolbox.population(n=popSize)
    CXPB, MUTPB, NGEN = 0.9 , 0.8, 500

    # Evaluate the entire population
    fitnesses = map(toolbox.evaluate, pop)
    for ind, fit in zip(pop, fitnesses):
        ind.fitness.values = fit
        

    pop.sort(reverse = True, key = getFit)
    bestfit = toolbox.clone(pop[0])

    IM.WritePop(0,pop)
    IM.WriteGenData(0,pop)
    for g in range(1,NGEN):
        startTime = tim.time()

       
        
        if(pop[0].fitness.values[0] > bestFit):
            bestFit = pop[0].fitness.values[0]
            bestPop = [toolbox.clone(pop[0])] + bestPop
            bestFits = [bestFit] + bestFits
        #MUTPB = 1 - bestFit * 2
        
        # Select the next generation individuals
        offspring = toolbox.select(pop, len(pop)-elitism)
        toAdd = list(map(toolbox.clone, pop[0:elitism]))
        # Clone the selected individuals
        #offspring = list(map(toolbox.clone, offspring))
        
        # Guarantee diversity and min popsize

        #offspring = fs.diversityExactEqual(offspring)
        #offspring = fs.diversityEqual(offspring)
        offspring = fs.diversityEqualPlatform(offspring)

        offspringLen = len(offspring)
        extraOffspring = []
        while (offspringLen + len(extraOffspring) < (popSize - elitism)):
            parentOne = random.randint(0,offspringLen-1)
            parentTwo = random.randint(0,offspringLen-1)
            while parentOne == parentTwo:
                parentTwo = random.randint(0,offspringLen-1)
            childOne = toolbox.clone(offspring[parentOne])
            childTwo = toolbox.clone(offspring[parentTwo])
            toolbox.mate(childOne, childTwo)
            del childOne.fitness.values
            del childTwo.fitness.values
            extraOffspring += [childOne,childTwo]
        
        # Apply crossover and mutation on the offspring
        offspring.sort(reverse = True, key = getFit)
        childOffSpring = []
        offspringLen = len(offspring)

        i = 0
        j = i + 1
        while len(childOffSpring) < offspringLen:
            child = fs.levelCrossOneChild(toolbox.clone(offspring[i]), toolbox.clone(offspring[j]))
            del child.fitness.values
            childOffSpring += [child]
            j += 1
            if j > int(offspringLen * 0.3) :
                i += 1
                j = i + 1
                if i == offspringLen:
                    print("PROBLEM")
                    break
        offspring = childOffSpring

        offspring += extraOffspring
        for mutant in offspring:
            if random.random() < 0.7:
                toolbox.mutate(mutant)
                del mutant.fitness.values
        
        offspring = offspring + list(map(toolbox.clone, toAdd))
        
        # Evaluate the individuals with an invalid fitness
        invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
        fitnesses = map(toolbox.evaluate, invalid_ind)
        for ind, fit in zip(invalid_ind, fitnesses):
            ind.fitness.values = fit
        
        # The population is entirely replaced by the offspring
        pop = list(offspring)
        pop.sort(reverse = True, key = getFit)
        bestfit = toolbox.clone(pop[0])
        print("generation: ", g,"  Time: ", tim.time() - startTime,"bestFit: ", getFit(pop[0]), " popsize: ", len(pop))
        IM.WritePop(g,pop)
        IM.WriteGenData(g,pop)
        if getFit(pop[0]) >= 0.95:
            if(pop[0].fitness.values[0] > bestFit):
                bestFit = pop[0].fitness.values[0]
                bestPop = [toolbox.clone(pop[0])] + bestPop
                bestFits = [bestFit] + bestFits
            return (pop, bestPop,bestFit,bestFits)
    return (pop, bestPop,bestFit,bestFits)


def main():
    global specs
    global hUsed
    global IM
    while(True):
        print("Input number of save file")
        try:
            inputText = input()
            saveNumber = int(inputText)
        except:
            print("No number input")
            return
        filename = "TestSpecs\\SpecSave" + str(saveNumber).zfill(2) + ".txt"
        try:
            f = open(filename,'r')
            textSpecs = f.readlines()
            f.close()
        except:
            print("file does not exist")
        try:
            for spec in textSpecs:
                x,y,width,height,t = spec[:-1].split(':')
                addSpec(int(x),int(y),int(width),int(height),t)
            replaceHSpecs(hUsed,specs)
        except:
            print("Save is improperly formated")

        IM = instrumentation.InstrumentationManager(on = True)
        IM.WriteToRND(str(textSpecs))

        ppl,bestPop,bestFit,bestFits  = GAD()
        ppl.sort(reverse = True, key = getFit)

        IM.DrawPop(ppl,hUsed)
        IM.DrawBestPop(bestPop,hUsed)

main()
