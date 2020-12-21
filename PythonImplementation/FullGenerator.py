
import random
import evaluateFuncs as ef
import instrumentation
import time as tim
import Functions as fs
import config as cfg
import ApplyCollectibles as ac

from deap import base
from deap import creator
from deap import tools
from evaluateFuncs import Level
import PILViewer as viewer

INT_MIN, XINT_MAX, YINT_MAX = 3, 76, 47


ConfigList = []

popSize = 50
CXPB, MUTPB, NGEN = 0.9 , 0.8, 500

IM = ""

toolbox = base.Toolbox()
cfg.toolbox = toolbox

creator.create("FitnessMax", base.Fitness, weights=(1.0, 1.0))
creator.create("Individual", list, fitness=creator.FitnessMax)

N_CYCLES = 9

toolbox.register("attr_bool", random.randint, 0, 1)
toolbox.register("attr_xInt", random.randint, INT_MIN, XINT_MAX)
toolbox.register("attr_yInt", random.randint, INT_MIN, YINT_MAX)
toolbox.register("individual", tools.initCycle, creator.Individual,
(toolbox.attr_bool, toolbox.attr_xInt , toolbox.attr_yInt, toolbox.attr_xInt, toolbox.attr_yInt), n=N_CYCLES)

toolbox.register("population", tools.initRepeat, list, toolbox.individual)

def getFit(ind):
    return ind.fitness.values[0]

elitism = 1
treshold = 0.92
tresholdMax = 80
def GALoop(hUsed,popSize,NGEN,config):

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
        elif True:
            childOffSpring = []
            offspringLen = len(offspring)
            for parent1, parent2 in zip(offspring[::2], offspring[1::2]):
                child1 = fs.levelCrossOneChild(toolbox.clone(parent1), toolbox.clone(parent2))
                child2 = fs.levelCrossOneChild(toolbox.clone(parent2), toolbox.clone(parent1))
                del child1.fitness.values
                del child2.fitness.values
                childOffSpring += [child1,child2]
            offspring = childOffSpring
        else:
            random.shuffle(offspring)
            for child1, child2 in zip(offspring[::2], offspring[1::2]):
                if random.random() < CXPB:
                    toolbox.mate(child1, child2)
                    del child1.fitness.values
                    del child2.fitness.values
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

    return (pop, bestPop,bestFit,bestFits)

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
        return ef.SpecialArea(x,y,width,height,t)

def main():
    global IM
    specs = []
    print("Input number of save file")
    hUsed = ""
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
            specs += [addSpec(int(x),int(y),int(width),int(height),t)]
        hUsed = ef.AreaHeuristic(specs,smaller=True)
    except:
        print("Save is improperly formated")
    if hUsed == "":
        print("Exit")
        return
    cfg50 = cfg.Config(h = hUsed, mate = fs.levelCrossOneChild, mutate= fs.mutateLevel, select= tools.selBest, popSize= 50+1, genNumber= 500, sm = True)
    #cfg25 = cfg.Config(h = hUsed, mate = fs.levelCrossOneChild, mutate= fs.mutateLevel, select= tools.selBest, popSize= 25+1, genNumber= 500, sm = True)
    #ConfigListSelection = [cfg50,cfg25]
    ConfigListSelection = [cfg50]
    for c in ConfigListSelection:
        IM = instrumentation.InstrumentationManager()
        IM.WriteToRND(c.description())
        if c.select == tools.selTournament:
            toolbox.register("select",c.select, tournsize = c.tournsize)
            c.select = ""
        c.setup()

        ppl,bestPop,bestFit,bestFits  = GALoop(c.h,c.popSize, c.genNumber,c)
        ppl.sort(reverse = True, key = getFit)
        IM.DrawPop(ppl,c.h)
        IM.DrawBestPop(bestPop,c.h)


        world = []
        print(bestPop[0])
        for i in range(10):
            lvl = hUsed.TestLevel(bestPop[0])
            lvl = ac.PlaceCollectibles(hUsed,lvl)
            world += [lvl]
            IM.DrawLevelLevel(lvl,name= "\\col" + str(i+1),col= True)

        IM.GenerateWorld(world,name = "LevelGen"+str(saveNumber)+".xml")

main()