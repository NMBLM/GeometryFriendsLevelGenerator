# 1 | x | y | x | y |
# 1 | x | y | x | y | 1 | x | y | x | y | 1 | x | y | x | y | 1 | x | y | x | y | 1 | x | y | x | y |
# 1 | x | y | x | y | 1 | x | y | x | y | 1 | x | y | x | y 
#INT_MIN, XINT_MAX, YINT_MAX = 0, 1280 , 760

import random
import evaluateFuncs as ef
import instrumentation
import time as tim

from deap import base
from deap import creator
from deap import tools
from evaluateFuncs import Level
import PILViewer as viewer

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

hZero = ef.AreaHeuristic(lvlZeroSpecs)
hOne = ef.AreaHeuristic(lvlOneSpecs)
hTwo = ef.AreaHeuristic(lvlTwoSpecs)
hThree = ef.AreaHeuristic(lvlThreeSpecs)
hFour = ef.AreaHeuristic(lvlFourSpecs)
hFive = ef.AreaHeuristic(lvlFiveSpecs)


hFixedtwo = ef.FixedSpawnAreaHeuristic(lvlTwoSpecs)

#rec circle coop common
hPerOne = ef.AreaPercentangeHeuristic(0.3,0.2,0.3,0)
hPerTwo = ef.AreaPercentangeHeuristic(0,0.3,0.3,0.1)
hPerThree = ef.AreaPercentangeHeuristic(0.5,0.1,0.1,0)

hPer2One = ef.AreaPercentangeTwoHeuristic(0.3,0.2,0.3,0.2)
hPer2Two = ef.AreaPercentangeTwoHeuristic(0.4,0.6,0,0)

hUsed = hPer2One

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
        for i in range(0,45,5):
            if(ind[i] % 2 == 1 or i == 0):
                if random.random() < 0.5: #change plat width height
                    ind[i+3] = random.randint(INT_MIN,XINT_MAX)
                    ind[i+4] = random.randint(INT_MIN,YINT_MAX)
                else: #change plat x and y
                    ind[i+1] = random.randint(INT_MIN,XINT_MAX)
                    ind[i+2] = random.randint(INT_MIN,YINT_MAX)

def levelChangeOneValue(ind):
    sIndex = [0]
    for i in range(5,45,5):
        if ind[i] % 2 == 1:
            sIndex += [i]
    if len(sIndex) == 1: #if it has no platforms add one
        index = random.choice([5,10,15,20,25,30,35,40])
        ind[index] = 1
        ind[index+1] = random.randint(INT_MIN,XINT_MAX)
        ind[index+2] = random.randint(INT_MIN,YINT_MAX)
        ind[index+3] = random.randint(INT_MIN,XINT_MAX)
        ind[index+4] = random.randint(INT_MIN,YINT_MAX)
    elif random.random() < 0.1: #just add a platform
        aIndex = list({5,10,15,20,25,30,35,40}-set(sIndex)) #return the indexes that don't have platforms
        if len(aIndex) == 0: #if already has max platforms change a random value
            index = random.choice(sIndex)
            i = random.randint(1,4)
            intMax = XINT_MAX
            if i % 2 == 0:
                intMax = YINT_MAX
            ind[index + i] = random.randint(INT_MIN,intMax)
        else:
            index = random.choice(aIndex)
            ind[index] = 1
            ind[index+1] = random.randint(INT_MIN,XINT_MAX)
            ind[index+2] = random.randint(INT_MIN,YINT_MAX)
            ind[index+3] = random.randint(INT_MIN,XINT_MAX)
            ind[index+4] = random.randint(INT_MIN,YINT_MAX)
    elif random.random() < 0.2: #just remove a platform
        index = random.choice(sIndex[1:])
        ind[index] = 0
    else: #change a random value
        index = random.choice(sIndex)
        i = random.randint(1,4)
        intMax = XINT_MAX
        if i % 2 == 0:
            intMax = YINT_MAX
        ind[index + i] = random.randint(INT_MIN,intMax)


              
def levelCrossBothPlat(pOne, pTwo):
    for i in range(0,45,5):
        if(pOne[i] % 2 == 0) and (pTwo[i] % 2 == 0): #no platform in that place
            continue
        if(pOne[i] % 2 == 1) and (pTwo[i] % 2 == 1): #both have platform
            for j in range(i+1,i+4):
                aux = pOne[j]
                pOne[j] = pTwo[j]
                pTwo[j] = aux

def levelCrossOnePlat(pOne, pTwo):
    for i in range(0,45,5):
        if(pOne[i] % 2 == 0) and (pTwo[i] % 2 == 0): #no platform in that place
            continue
        if (pOne[i] % 2 == 0 and pTwo[i] % 2 == 1) or (pOne[i] % 2 == 1 and pTwo[i] % 2 == 0): #one has platform other doesn't
            for j in range(i,i+5):
                aux = pOne[j]
                pOne[j] = pTwo[j]
                pTwo[j] = aux

def levelCrossPlat(pOne, pTwo):
    for i in range(0,45,5):
        if(pOne[i] % 2 == 0) and (pTwo[i] % 2 == 0): #no platform in that place
            continue
        if (pOne[i] % 2 == 0 and pTwo[i] % 2 == 1) or (pOne[i] % 2 == 1 and pTwo[i] % 2 == 0) or ((pOne[i] % 2 == 1) and (pTwo[i] % 2 == 1) and random.random() < 0.5):
            #one has platform other doesn't or both have they switch with a 50% chance
            for j in range(i,i+5):
                aux = pOne[j]
                pOne[j] = pTwo[j]
                pTwo[j] = aux

        
def diversityExactEqual(population):
    diverse = []
    for person in population:
        if not person in diverse:
            diverse += [toolbox.clone(person)]
    return diverse



creator.create("FitnessMax", base.Fitness, weights=(1.0, 1.0))
creator.create("Individual", list, fitness=creator.FitnessMax)

toolbox = base.Toolbox()

INT_MIN, XINT_MAX, YINT_MAX = 40, 1160, 680
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
#toolbox.register("mate", levelCrossOnePlat)
toolbox.register("mate", levelCrossPlat)
#toolbox.register("mate", levelCrossBothPlat)

#toolbox.register("mutate", tools.mutUniformInt,low = INT_MIN, up = XINT_MAX, indpb=0.2)
toolbox.register("mutate", mutateLevel)
#toolbox.register("mutate", levelChangeOneValue)
#toolbox.register("mutate", tools.mutFlipBit, indpb=0.2)


toolbox.register("select", tools.selBest)
#toolbox.register("select", tools.selTournament, tournsize=3)
INT_MIN, XINT_MAX
 

popSize = 50
def GA():
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

elitism = 2
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
        offspring = diversityExactEqual(offspring)

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
    #ppl,bestPop,bestFit,bestFits  = GA()
    ppl,bestPop,bestFit,bestFits  = GAD()
    ppl.sort(reverse = True, key = getFit)

    IM.DrawPop(ppl,hUsed)
    IM.DrawBestPop(bestPop,hUsed)

def Test():
    TestLvl = [1, 96, 720, 522, 689, 1, 1160, 587, 764, 63, 0, 338, 512, 395, 239, 0, 575, 330, 585, 549, 0, 84, 230, 256, 427, 1, 79, 695, 277, 556, 0, 800, 462, 381, 40, 1, 483, 348, 1015, 759, 1, 292, 508, 104, 744]
    IM.DrawLevel(TestLvl,hUsed)

main()
#Test()