# 1 | x | y | x | y |
# 1 | x | y | x | y | 1 | x | y | x | y | 1 | x | y | x | y | 1 | x | y | x | y | 1 | x | y | x | y |
# 1 | x | y | x | y | 1 | x | y | x | y | 1 | x | y | x | y 
#INT_MIN, XINT_MAX, YINT_MAX = 0, 1280 , 760

import random
import evaluateFuncs as ef
import instrumentation
import time as tim
import Functions as fs


from deap import base
from deap import creator
from deap import tools
from evaluateFuncs import Level
import PILViewer as viewer

INT_MIN, XINT_MAX, YINT_MAX = 3, 76, 47

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

lvlSixSpecs = [ef.SpecialArea(1100,600,140,140, ef.AreaType.RectangleOnly), 
ef.SpecialArea(90,440,300,140, ef.AreaType.CircleOnly), 
ef.SpecialArea(500,80,300,140, ef.AreaType.Cooperative), 
ef.SpecialArea(500,600,200,100, ef.AreaType.Common)]

hZero = ef.AreaHeuristic(lvlZeroSpecs, smaller = True)
hOne = ef.AreaHeuristic(lvlOneSpecs, smaller = True)
hTwo = ef.AreaHeuristic(lvlTwoSpecs, smaller = True)
hThree = ef.AreaHeuristic(lvlThreeSpecs, smaller = True)
hFour = ef.AreaHeuristic(lvlFourSpecs, smaller = True)
hFive = ef.AreaHeuristic(lvlFiveSpecs, smaller = True)
hSix = ef.AreaHeuristic(lvlSixSpecs, smaller = True)

multiplier = 15

lvlRNDSpecs1Each = [ef.SpecialArea(random.randint(INT_MIN,XINT_MAX) * multiplier,random.randint(INT_MIN,YINT_MAX) * multiplier,
random.randint(INT_MIN,XINT_MAX) * multiplier,random.randint(INT_MIN,YINT_MAX) * multiplier, ef.AreaType.RectangleOnly), 
ef.SpecialArea(random.randint(INT_MIN,XINT_MAX) * multiplier,random.randint(INT_MIN,YINT_MAX) * multiplier,
random.randint(INT_MIN,XINT_MAX) * multiplier,random.randint(INT_MIN,YINT_MAX) * multiplier, ef.AreaType.CircleOnly), 
ef.SpecialArea(random.randint(INT_MIN,XINT_MAX) * multiplier,random.randint(INT_MIN,YINT_MAX) * multiplier,
random.randint(INT_MIN,XINT_MAX) * multiplier,random.randint(INT_MIN,YINT_MAX) * multiplier, ef.AreaType.Cooperative)]

lvlRNDSpecsRec = [ef.SpecialArea(random.randint(INT_MIN,XINT_MAX) * multiplier,random.randint(INT_MIN,YINT_MAX) * multiplier,
random.randint(INT_MIN,XINT_MAX) * multiplier,random.randint(INT_MIN,YINT_MAX) * multiplier, ef.AreaType.RectangleOnly)]

lvlRNDSpecsCircle = [ef.SpecialArea(random.randint(INT_MIN,XINT_MAX) * multiplier,random.randint(INT_MIN,YINT_MAX) * multiplier,
random.randint(INT_MIN,XINT_MAX) * multiplier,random.randint(INT_MIN,YINT_MAX) * multiplier, ef.AreaType.CircleOnly)]

lvlRNDSpecsCoop = [ef.SpecialArea(random.randint(INT_MIN,XINT_MAX) * multiplier,random.randint(INT_MIN,YINT_MAX) * multiplier,
random.randint(INT_MIN,XINT_MAX) * multiplier,random.randint(INT_MIN,YINT_MAX) * multiplier, ef.AreaType.Cooperative)]

lvlRNDSpecsCirRec = [ef.SpecialArea(random.randint(INT_MIN,XINT_MAX) * multiplier,random.randint(INT_MIN,YINT_MAX) * multiplier,
random.randint(INT_MIN,XINT_MAX) * multiplier,random.randint(INT_MIN,YINT_MAX) * multiplier, ef.AreaType.RectangleOnly), 
ef.SpecialArea(random.randint(INT_MIN,XINT_MAX) * multiplier,random.randint(INT_MIN,YINT_MAX) * multiplier,
random.randint(INT_MIN,XINT_MAX) * multiplier,random.randint(INT_MIN,YINT_MAX) * multiplier, ef.AreaType.CircleOnly)]


hRNDSpecs1Each  = ef.AreaHeuristic(lvlRNDSpecs1Each, smaller = True)
hRNDSpecsRec  = ef.AreaHeuristic(lvlRNDSpecsRec, smaller = True)
hRNDSpecsCircle  = ef.AreaHeuristic(lvlRNDSpecsCircle, smaller = True)
hRNDSpecsCoop  = ef.AreaHeuristic(lvlRNDSpecsCoop, smaller = True)
hRNDSpecsCirRec  = ef.AreaHeuristic(lvlRNDSpecsCirRec, smaller = True)


hFixedtwo = ef.FixedSpawnAreaHeuristic(lvlTwoSpecs, smaller = True)

#rec circle coop common
hPerOne = ef.AreaPercentangeHeuristic(0.3,0.2,0.3,0, smaller = True)
hPerTwo = ef.AreaPercentangeHeuristic(0,0.3,0.3,0.1, smaller = True)
hPerThree = ef.AreaPercentangeHeuristic(0.5,0.1,0.1,0, smaller = True)

hPer2One = ef.AreaPercentangeTwoHeuristic(0.3,0.2,0.3,0.2, smaller = True)
hPer2Two = ef.AreaPercentangeTwoHeuristic(0.4,0.6,0,0, smaller = True)

hUsed = hThree

IM = []


def getFit(ind):
    return ind.fitness.values[0]

creator.create("FitnessMax", base.Fitness, weights=(1.0, 1.0))
creator.create("Individual", list, fitness=creator.FitnessMax)

toolbox = base.Toolbox()

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
toolbox.register("evaluate", hUsed.CalculateFitness)


#toolbox.register("mate", tools.cxTwoPoint)
toolbox.register("mate", fs.levelCrossPlat)


#toolbox.register("mutate", tools.mutUniformInt,low = INT_MIN, up = YINT_MAX, indpb=0.2)
toolbox.register("mutate", fs.mutateLevel)
#toolbox.register("mutate", fs.levelChangeOneValue)
#toolbox.register("mutate", tools.mutFlipBit, indpb=0.2)


toolbox.register("select", tools.selBest)
#toolbox.register("select", tools.selTournament, tournsize=3)
#toolbox.register("select", tools.selStochasticUniversalSampling)

INT_MIN, XINT_MAX
 

popSize = 50
def GA():
    global IM
    IM = instrumentation.InstrumentationManager(on = True)
    if not isinstance(hUsed,ef.AreaPercentangeHeuristic) or not isinstance(hUsed,ef.AreaPercentangeTwoHeuristic):
        IM.DrawSpecs(hUsed)
    bestPop = []
    bestFit = 0
    bestFits =[]
    pop = toolbox.population(n=popSize)
    CXPB, MUTPB, NGEN = 0.9 , 0.8, 100

    # Evaluate the entire population
    fitnesses = map(toolbox.evaluate, pop)
    for ind, fit in zip(pop, fitnesses):
        ind.fitness.values = fit
        

    
    for g in range(NGEN):
        startTime = tim.time()

        pop.sort(reverse = True, key = getFit)
       
        IM.WritePop(g,pop)
        IM.WriteGenData(g,pop)
        if(pop[0].fitness.values[0] > bestFit):
            bestFit = pop[0].fitness.values[0]
            bestPop = [toolbox.clone(pop[0])] + bestPop
            bestFits = [bestFit] + bestFits
        #MUTPB = 1 - bestFit * 2
        
        # Select the next generation individuals
        offspring = toolbox.select(pop, len(pop))
        toAdd = pop[0:2]
        # Clone the selected individuals
        offspring = list(map(toolbox.clone, offspring))
        
        # Apply crossover and mutation on the offspring
        random.shuffle(offspring)
        for child1, child2 in zip(offspring[::2], offspring[1::2]):
            if random.random() < CXPB:
                toolbox.mate(child1, child2)
                del child1.fitness.values
                del child2.fitness.values
        #offspring = offspring + list(map(toolbox.clone, toAdd))
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

elitism = 1
def GAD():
    if not isinstance(hUsed,ef.AreaPercentangeHeuristic) and not isinstance(hUsed,ef.AreaPercentangeTwoHeuristic):
        IM.DrawSpecs(hUsed)
    bestPop = []
    bestFit = 0
    bestFits =[]
    pop = toolbox.population(n=popSize)
    CXPB, MUTPB, NGEN = 0.9 , 0.8, 100

    # Evaluate the entire population
    fitnesses = map(toolbox.evaluate, pop)
    for ind, fit in zip(pop, fitnesses):
        ind.fitness.values = fit
        

    pop.sort(reverse = True, key = getFit)
    bestfit = toolbox.clone(pop[0])

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

        offspring = fs.diversityExactEqual(offspring)
        #offspring = fs.diversityEqual(offspring)
        #offspring = fs.diversityEqualPlatform(offspring)

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
            if random.random() < 1:
                toolbox.mate(child1, child2)
                del child1.fitness.values
                del child2.fitness.values

        offspring += newOffspring
        for mutant in offspring:
            if random.random() < 1-getFit(bestfit):
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

    return (pop, bestPop,bestFit,bestFits)



def main():
    global IM
    IM = instrumentation.InstrumentationManager(on = True)
    #ppl,bestPop,bestFit,bestFits  = GA()
    ppl,bestPop,bestFit,bestFits  = GAD()
    ppl.sort(reverse = True, key = getFit)

    IM.DrawPop(ppl,hUsed)
    IM.DrawBestPop(bestPop,hUsed)

def Test():
    TestLvl = [1, 320, 678, 120, 678, 1, 460, 400, 75, 300, 1, 735, 400, 75, 300, 1, 535, 400, 250, 75, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    IM = instrumentation.InstrumentationManager(on = True)
    hUsed.smallerLevels = False
    IM.DrawLevel(TestLvl,hUsed)

def MultipleRuns(runNumber = 1):
    global IM
    global hUsed
    for i in range(0,runNumber):
        #lvlRNDSpecs = [ef.SpecialArea(random.randint(INT_MIN,XINT_MAX) * multiplier,random.randint(INT_MIN,YINT_MAX) * multiplier,
        #random.randint(INT_MIN,XINT_MAX) * multiplier /2,random.randint(INT_MIN,YINT_MAX) * multiplier/2, ef.AreaType.RectangleOnly),
        #ef.SpecialArea(random.randint(INT_MIN,XINT_MAX) * multiplier,random.randint(INT_MIN,YINT_MAX) * multiplier,
        #random.randint(INT_MIN,XINT_MAX) * multiplier/2,random.randint(INT_MIN,YINT_MAX) * multiplier/2, ef.AreaType.CircleOnly), 
        #ef.SpecialArea(random.randint(INT_MIN,XINT_MAX) * multiplier,random.randint(INT_MIN,YINT_MAX) * multiplier,
        #random.randint(INT_MIN,XINT_MAX) * multiplier/2,random.randint(INT_MIN,YINT_MAX) * multiplier/2, ef.AreaType.Cooperative)]
        lvlRNDSpecs = [ef.SpecialArea(random.randint(INT_MIN,XINT_MAX) * multiplier,random.randint(INT_MIN,YINT_MAX) * multiplier,
        random.randint(INT_MIN,XINT_MAX) * multiplier/2,random.randint(INT_MIN,YINT_MAX) * multiplier/2, ef.AreaType.CircleOnly), 
        ef.SpecialArea(random.randint(INT_MIN,XINT_MAX) * multiplier,random.randint(INT_MIN,YINT_MAX) * multiplier,
        random.randint(INT_MIN,XINT_MAX) * multiplier/2,random.randint(INT_MIN,YINT_MAX) * multiplier/2, ef.AreaType.Cooperative)]
        hRNDSpecs  = ef.AreaHeuristic(lvlRNDSpecs, smaller = True)
        hUsed = hRNDSpecs
        print("Start Run ",i + 1)
        IM = instrumentation.InstrumentationManager(on = True)
        ppl,bestPop,bestFit,bestFits = GAD()
        ppl.sort(reverse = True, key = getFit)

        IM.DrawPop(ppl,hUsed)
        IM.DrawBestPop(bestPop,hUsed)


#MultipleRuns(2)
main()
#Test()
