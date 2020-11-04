
import random
import evaluateFuncs as ef
import instrumentation
import time as tim
import Functions as fs
import config as cfg

from deap import base
from deap import creator
from deap import tools
from evaluateFuncs import Level
import PILViewer as viewer

INT_MIN, XINT_MAX, YINT_MAX = 3, 76, 47
toolbox = base.Toolbox()
cfg.toolbox = toolbox

lvlZeroSpecs = []

lvlOneSpecs = [ ef.SpecialArea(80,540,500,180,ef.AreaType.RectangleOnly),ef.SpecialArea(740,360,500,360, ef.AreaType.CircleOnly)]

lvlTwoSpecs = [ef.SpecialArea(100,80,1100,240, ef.AreaType.Cooperative), ef.SpecialArea(430,560,340,180,ef.AreaType.RectangleOnly)]

lvlThreeSpecs = [ef.SpecialArea(90,600,140,140, ef.AreaType.RectangleOnly), 
ef.SpecialArea(1100,600,140,140, ef.AreaType.RectangleOnly), 
ef.SpecialArea(1100,80,140,140, ef.AreaType.Cooperative)]

lvlFourSpecs = [ef.SpecialArea(440,700,200,60, ef.AreaType.RectangleOnly), 
ef.SpecialArea(90,440,300,300, ef.AreaType.CircleOnly), 
ef.SpecialArea(900,80,300,140, ef.AreaType.Cooperative)]

lvlFiveSpecs = [ef.SpecialArea(1100,600,140,140, ef.AreaType.RectangleOnly), 
ef.SpecialArea(90,440,300,140, ef.AreaType.CircleOnly), 
ef.SpecialArea(900,80,300,140, ef.AreaType.Cooperative)]

multiplier = 15
lvlRNDSpecs = [ef.SpecialArea(random.randint(INT_MIN,XINT_MAX) * multiplier,random.randint(INT_MIN,YINT_MAX) * multiplier,
random.randint(INT_MIN,XINT_MAX) * multiplier,random.randint(INT_MIN,YINT_MAX) * multiplier, ef.AreaType.RectangleOnly), 
ef.SpecialArea(random.randint(INT_MIN,XINT_MAX) * multiplier,random.randint(INT_MIN,YINT_MAX) * multiplier,
random.randint(INT_MIN,XINT_MAX) * multiplier,random.randint(INT_MIN,YINT_MAX) * multiplier, ef.AreaType.CircleOnly), 
ef.SpecialArea(random.randint(INT_MIN,XINT_MAX) * multiplier,random.randint(INT_MIN,YINT_MAX) * multiplier,
random.randint(INT_MIN,XINT_MAX) * multiplier,random.randint(INT_MIN,YINT_MAX) * multiplier, ef.AreaType.Cooperative)]


hZero = ef.AreaHeuristic(lvlZeroSpecs, smaller = True)
hOne = ef.AreaHeuristic(lvlOneSpecs, smaller = True)
hTwo = ef.AreaHeuristic(lvlTwoSpecs, smaller = True)
hThree = ef.AreaHeuristic(lvlThreeSpecs, smaller = True)
hFour = ef.AreaHeuristic(lvlFourSpecs, smaller = True)
hFive = ef.AreaHeuristic(lvlFiveSpecs, smaller = True)

hRNDSpecs  = ef.AreaHeuristic(lvlRNDSpecs, smaller = True)

hFixedtwo = ef.FixedSpawnAreaHeuristic(lvlTwoSpecs, smaller = True)

#rec circle coop common
hPerOne = ef.AreaPercentangeHeuristic(0.3,0.2,0.3,0, smaller = True)
hPerTwo = ef.AreaPercentangeHeuristic(0,0.3,0.3,0.1, smaller = True)
hPerThree = ef.AreaPercentangeHeuristic(0.5,0.1,0.1,0, smaller = True)
hPerFour = ef.AreaPercentangeHeuristic(0.15,0.20,0.2,0.3, smaller = True)

hPer2One = ef.AreaPercentangeTwoHeuristic(0.3,0.2,0.3,0.2, smaller = True)
hPer2Two = ef.AreaPercentangeTwoHeuristic(0.4,0.6,0,0, smaller = True)
hPer2Three = ef.AreaPercentangeTwoHeuristic(0.1,0.1,0.4,0.4, smaller = True)
hPer2Four = ef.AreaPercentangeTwoHeuristic(0.1,0.05,0.7,0.15, smaller = True)



ConfigList = []

elitism = 1
popSize = 50
CXPB, MUTPB, NGEN = 0.9 , 0.8, 500


cfg01 = cfg.Config(h = hOne, mate = fs.levelCrossPlat, mutate= fs.mutateLevel, select= tools.selBest, popSize= popSize, genNumber= NGEN)
cfg02 = cfg.Config(h = hTwo, mate = fs.levelCrossPlat, mutate= fs.mutateLevel, select= tools.selBest, popSize= popSize, genNumber= NGEN)
cfg03 = cfg.Config(h = hThree, mate = fs.levelCrossPlat, mutate= fs.mutateLevel, select= tools.selBest, popSize= popSize, genNumber= NGEN)
cfg04 = cfg.Config(h = hFour, mate = fs.levelCrossPlat, mutate= fs.mutateLevel, select= tools.selBest, popSize= popSize, genNumber= NGEN)
cfg05= cfg.Config(h = hFive, mate = fs.levelCrossPlat, mutate= fs.mutateLevel, select= tools.selBest, popSize= popSize, genNumber= NGEN)
cfg06 = cfg.Config(h = hTwo, mate = fs.levelCrossPlat, mutate= fs.mutateLevel, select= tools.selBest, popSize= popSize, genNumber= 2000)
cfg07 = cfg.Config(h = hThree, mate = fs.levelCrossPlat, mutate= fs.mutateLevel, select= tools.selBest, popSize= popSize, genNumber= 2000)
cfg08 = cfg.Config(h = hFour, mate = fs.levelCrossPlat, mutate= fs.mutateLevel, select= tools.selBest, popSize= popSize, genNumber= 2000)
cfg09 = cfg.Config(h = hFive, mate = fs.levelCrossPlat, mutate= fs.mutateLevel, select= tools.selBest, popSize= popSize, genNumber= 2000)
cfg10 = cfg.Config(h = lvlRNDSpecs, mate = fs.levelCrossPlat, mutate= fs.mutateLevel, select= tools.selBest, popSize= popSize, genNumber= NGEN)

cfg11 = cfg.Config(h = hPerOne, mate = fs.levelCrossPlat, mutate= fs.mutateLevel, select= tools.selBest, popSize= popSize, genNumber= NGEN)
cfg12 = cfg.Config(h = hPerTwo, mate = fs.levelCrossPlat, mutate= fs.mutateLevel, select= tools.selBest, popSize= popSize, genNumber= NGEN)
cfg13 = cfg.Config(h = hPerThree, mate = fs.levelCrossPlat, mutate= fs.mutateLevel, select= tools.selBest, popSize= popSize, genNumber= NGEN)
cfg14 = cfg.Config(h = hPerFour, mate = fs.levelCrossPlat, mutate= fs.mutateLevel, select= tools.selBest, popSize= popSize, genNumber= NGEN)

cfg15 = cfg.Config(h = hPer2One, mate = fs.levelCrossPlat, mutate= fs.mutateLevel, select= tools.selBest, popSize= popSize, genNumber= NGEN)
cfg16 = cfg.Config(h = hPer2Two, mate = fs.levelCrossPlat, mutate= fs.mutateLevel, select= tools.selBest, popSize= popSize, genNumber= NGEN)
cfg17 = cfg.Config(h = hPer2Three, mate = fs.levelCrossPlat, mutate= fs.mutateLevel, select= tools.selBest, popSize= popSize, genNumber= NGEN)
cfg18 = cfg.Config(h = hPer2Four, mate = fs.levelCrossPlat, mutate= fs.mutateLevel, select= tools.selBest, popSize= popSize, genNumber= NGEN)


ConfigList = [cfg01,cfg02,cfg03,cfg04,cfg05,cfg06,cfg07,cfg08,cfg09,cfg10,cfg11,cfg12,cfg13,cfg14,cfg15,cfg16,cfg17,cfg18]


IM = ""

creator.create("FitnessMax", base.Fitness, weights=(1.0, 1.0))
creator.create("Individual", list, fitness=creator.FitnessMax)


N_CYCLES = 9

toolbox.register("attr_bool", random.randint, 0, 1)
toolbox.register("attr_xInt", random.randint, INT_MIN, XINT_MAX)
toolbox.register("attr_yInt", random.randint, INT_MIN, YINT_MAX)
toolbox.register("individual", tools.initCycle, creator.Individual,
(toolbox.attr_bool, toolbox.attr_xInt , toolbox.attr_yInt, toolbox.attr_xInt, toolbox.attr_yInt), n=N_CYCLES)
#example  [0, 1159, 195, 74, 205, 0, 475, 499, 308, 246, 1, 696, 372, 266, 206, 0, 156, 82, 1261, 744, 1, 247, 187, 182, 196, 0, 927, 573, 630, 310, 1, 1027, 99, 164, 34, 1, 265, 345, 734, 657, 0, 1175, 661, 642, 738]

toolbox.register("population", tools.initRepeat, list, toolbox.individual)



def getFit(ind):
    return ind.fitness.values[0]



def GALoop(hUsed):
    #global IM
    #IM = instrumentation.InstrumentationManager(on = True)
    if not isinstance(hUsed,ef.AreaPercentangeHeuristic) and not isinstance(hUsed,ef.AreaPercentangeTwoHeuristic):
        IM.DrawSpecs(hUsed)
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
        #MUTPB = 1 - bestFit * 2
        
        # Select the next generation individuals
        offspring = toolbox.select(pop, len(pop)-elitism)
        toAdd = list(map(toolbox.clone, pop[0:elitism]))
        # Clone the selected individuals
        #offspring = list(map(toolbox.clone, offspring))
        
        # Guarantee diversity and min popsize

        #offspring = list(map(toolbox.clone, fs.diversityExactEqual(offspring)))
        #offspring = list(map(toolbox.clone, fs.diversityEqual(offspring)))
        offspring = list(map(toolbox.clone, fs.diversityEqualPlatform(offspring)))

        offspringLen = len(offspring)
        newOffspring = []
        while (offspringLen + len(newOffspring) < (popSize - elitism)):
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
        
        # Apply crossover and mutation on the offspring
        random.shuffle(offspring)
        for child1, child2 in zip(offspring[::2], offspring[1::2]):
            if random.random() < CXPB:
                toolbox.mate(child1, child2)
                del child1.fitness.values
                del child2.fitness.values

        offspring += newOffspring
        for mutant in offspring:
            if random.random() < MUTPB:
                toolbox.mutate(mutant)
                del mutant.fitness.values
        
        offspring = offspring + list(map(toolbox.clone, toAdd))
        
        # Evaluate the individuals with an invalid fitness
        invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
        fitnesses = map(toolbox.evaluate, invalid_ind)
        for ind, fit in zip(invalid_ind, fitnesses):
            ind.fitness.values = fit
        bestfit = max(offspring, key=getFit)
        # The population is entirely replaced by the offspring
        pop = list(offspring)
        pop.sort(reverse = True, key = getFit)

        print("generation: ", g,"  Time: ", tim.time() - startTime,"bestFit: ", getFit(pop[0]), " popsize: ", len(pop))

    return (pop, bestPop,bestFit,bestFits)


def main():
    global IM
    for c in ConfigList:
        c.setup()
        IM = instrumentation.InstrumentationManager()
        IM.WriteToRND(c.description())

        
        ppl,bestPop,bestFit,bestFits  = GALoop(c.h)
        ppl.sort(reverse = True, key = getFit)

        IM.DrawPop(ppl,c.h)
        IM.DrawBestPop(bestPop,c.h)

main()