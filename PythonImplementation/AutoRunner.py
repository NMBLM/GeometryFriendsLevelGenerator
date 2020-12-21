
import random
import evaluateFuncs as ef
import instrumentation
import time as tim
import Functions as fs
import config as cfg
from guppy import hpy

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

lvlSixSpecs = [ef.SpecialArea(480,608,224,176, ef.AreaType.RectangleOnly), 
ef.SpecialArea(976,240,288,288, ef.AreaType.CircleOnly), 
ef.SpecialArea(48,48,1216,128, ef.AreaType.Cooperative), 
ef.SpecialArea(48,480,320,160, ef.AreaType.Common)]

hZero = ef.AreaHeuristic(lvlZeroSpecs, smaller = True)
hOne = ef.AreaHeuristic(lvlOneSpecs, smaller = True)
hTwo = ef.AreaHeuristic(lvlTwoSpecs, smaller = True)
hThree = ef.AreaHeuristic(lvlThreeSpecs, smaller = True)
hFour = ef.AreaHeuristic(lvlFourSpecs, smaller = True)
hFive = ef.AreaHeuristic(lvlFiveSpecs, smaller = True)
hSix = ef.AreaHeuristic(lvlSixSpecs, smaller = True)


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

cfg10 = cfg.Config(h = hPerOne, mate = fs.levelCrossPlat, mutate= fs.mutateLevel, select= tools.selBest, popSize= popSize, genNumber= NGEN)
cfg11 = cfg.Config(h = hPerTwo, mate = fs.levelCrossPlat, mutate= fs.mutateLevel, select= tools.selBest, popSize= popSize, genNumber= NGEN)
cfg12 = cfg.Config(h = hPerThree, mate = fs.levelCrossPlat, mutate= fs.mutateLevel, select= tools.selBest, popSize= popSize, genNumber= NGEN)
cfg13 = cfg.Config(h = hPerFour, mate = fs.levelCrossPlat, mutate= fs.mutateLevel, select= tools.selBest, popSize= popSize, genNumber= NGEN)

cfg14 = cfg.Config(h = hPer2One, mate = fs.levelCrossPlat, mutate= fs.mutateLevel, select= tools.selBest, popSize= popSize, genNumber= NGEN)
cfg15 = cfg.Config(h = hPer2Two, mate = fs.levelCrossPlat, mutate= fs.mutateLevel, select= tools.selBest, popSize= popSize, genNumber= NGEN)
cfg16 = cfg.Config(h = hPer2Three, mate = fs.levelCrossPlat, mutate= fs.mutateLevel, select= tools.selBest, popSize= popSize, genNumber= NGEN)
cfg17 = cfg.Config(h = hPer2Four, mate = fs.levelCrossPlat, mutate= fs.mutateLevel, select= tools.selBest, popSize= popSize, genNumber= NGEN)


ConfigList = [cfg01,cfg02,cfg03,cfg04,cfg05,cfg06,cfg07,cfg08,cfg09,cfg10,cfg11,cfg12,cfg13,cfg14,cfg15,cfg16,cfg17]

cfgCross1 = cfg.Config(h = hTwo, mate = fs.levelCrossBothPlat, mutate= fs.mutateLevel, select= tools.selBest, popSize= popSize, genNumber= NGEN)
cfgCross2 = cfg.Config(h = hTwo, mate = fs.levelCrossOnePlat, mutate= fs.mutateLevel, select= tools.selBest, popSize= popSize, genNumber= NGEN)
cfgCross3 = cfg.Config(h = hTwo, mate = fs.levelCrossPlat, mutate= fs.mutateLevel, select= tools.selBest, popSize= popSize, genNumber= NGEN)
cfgCross4 = cfg.Config(h = hTwo, mate = fs.levelCrossOneChild, mutate= fs.mutateLevel, select= tools.selBest, popSize= popSize, genNumber= NGEN, sm = True)

ConfigListCross = [cfgCross1,cfgCross2,cfgCross3,cfgCross4]


cfgSel1 = cfg.Config(h = hTwo, mate = fs.levelCrossOneChild, mutate= fs.mutateLevel, select= tools.selBest, popSize= popSize, genNumber= NGEN)
cfgSel2 = cfg.Config(h = hTwo, mate = fs.levelCrossOneChild, mutate= fs.mutateLevel, select= tools.selTournament, popSize= popSize, genNumber= NGEN, tournsize = 4)
cfgSel22 = cfg.Config(h = hTwo, mate = fs.levelCrossOneChild, mutate= fs.mutateLevel, select= tools.selTournament, popSize= popSize, genNumber= NGEN, tournsize = 6)
cfgSel222 = cfg.Config(h = hTwo, mate = fs.levelCrossOneChild, mutate= fs.mutateLevel, select= tools.selTournament, popSize= popSize, genNumber= NGEN, tournsize = 8)
cfgSel2222 = cfg.Config(h = hTwo, mate = fs.levelCrossOneChild, mutate= fs.mutateLevel, select= tools.selTournament, popSize= popSize, genNumber= NGEN, tournsize = 16)
cfgSel3 = cfg.Config(h = hTwo, mate = fs.levelCrossOneChild, mutate= fs.mutateLevel, select= tools.selStochasticUniversalSampling, popSize= popSize, genNumber= NGEN)
cfgSel4 = cfg.Config(h = hTwo, mate = fs.levelCrossOneChild, mutate= fs.mutateLevel, select= tools.selBest, popSize= popSize, genNumber= NGEN, sm = True)

ConfigListSelection = [cfgSel1,cfgSel2,cfgSel22,cfgSel222,cfgSel2222,cfgSel3,cfgSel4]


cfg18 = cfg.Config(h = hPer2One, mate = fs.levelCrossOneChild, mutate= fs.mutateLevel, select= tools.selBest, popSize= popSize, genNumber= NGEN, sm = True)
cfg19 = cfg.Config(h = hPer2Two, mate = fs.levelCrossOneChild, mutate= fs.mutateLevel, select= tools.selBest, popSize= popSize, genNumber= NGEN, sm = True)
cfg20 = cfg.Config(h = hPer2Three, mate = fs.levelCrossOneChild, mutate= fs.mutateLevel, select= tools.selBest, popSize= popSize, genNumber= NGEN, sm = True)
cfg21 = cfg.Config(h = hPer2Four, mate = fs.levelCrossOneChild, mutate= fs.mutateLevel, select= tools.selBest, popSize= popSize, genNumber= NGEN, sm = True)

cfg22 = cfg.Config(h = hPerOne, mate = fs.levelCrossOneChild, mutate= fs.mutateLevel, select= tools.selBest, popSize= popSize, genNumber= NGEN, sm = True)
cfg23 = cfg.Config(h = hPerTwo, mate = fs.levelCrossOneChild, mutate= fs.mutateLevel, select= tools.selBest, popSize= popSize, genNumber= NGEN, sm = True)
cfg24 = cfg.Config(h = hPerThree, mate = fs.levelCrossOneChild, mutate= fs.mutateLevel, select= tools.selBest, popSize= popSize, genNumber= NGEN, sm = True)
cfg25 = cfg.Config(h = hPerFour, mate = fs.levelCrossOneChild, mutate= fs.mutateLevel, select= tools.selBest, popSize= popSize, genNumber= NGEN, sm = True)

ConfigListTwo = [cfg18,cfg19,cfg20,cfg21,cfg22,cfg23,cfg24,cfg25]


#best only to get examples of levels generated
hr1_100 = cfg.Config(h = hOne, mate = fs.levelCrossOneChild, mutate= fs.mutateLevel, select= tools.selBest, popSize= 50, genNumber= 100, sm = True)
hr1_500 = cfg.Config(h = hOne, mate = fs.levelCrossOneChild, mutate= fs.mutateLevel, select= tools.selBest, popSize= 50, genNumber= 500, sm = True)
hr1_2000 = cfg.Config(h = hOne, mate = fs.levelCrossOneChild, mutate= fs.mutateLevel, select= tools.selBest, popSize= 50, genNumber= 2000, sm = True)
hr2_100 = cfg.Config(h = hTwo, mate = fs.levelCrossOneChild, mutate= fs.mutateLevel, select= tools.selBest, popSize= 50, genNumber= 100, sm = True)
hr2_500 = cfg.Config(h = hTwo, mate = fs.levelCrossOneChild, mutate= fs.mutateLevel, select= tools.selBest, popSize= 50, genNumber= 500, sm = True)
hr2_2000 = cfg.Config(h = hTwo, mate = fs.levelCrossOneChild, mutate= fs.mutateLevel, select= tools.selBest, popSize= 50, genNumber= 2000, sm = True)
hr3_100 = cfg.Config(h = hThree, mate = fs.levelCrossOneChild, mutate= fs.mutateLevel, select= tools.selBest, popSize= 50, genNumber= 100, sm = True)
hr3_500 = cfg.Config(h = hThree, mate = fs.levelCrossOneChild, mutate= fs.mutateLevel, select= tools.selBest, popSize= 50, genNumber= 500, sm = True)
hr3_2000 = cfg.Config(h = hThree, mate = fs.levelCrossOneChild, mutate= fs.mutateLevel, select= tools.selBest, popSize= 50, genNumber= 2000, sm = True)
hr4_100 = cfg.Config(h = hFour, mate = fs.levelCrossOneChild, mutate= fs.mutateLevel, select= tools.selBest, popSize= 50, genNumber= 100, sm = True)
hr4_500 = cfg.Config(h = hFour, mate = fs.levelCrossOneChild, mutate= fs.mutateLevel, select= tools.selBest, popSize= 50, genNumber= 500, sm = True)
hr4_2000 = cfg.Config(h = hFour, mate = fs.levelCrossOneChild, mutate= fs.mutateLevel, select= tools.selBest, popSize= 50, genNumber= 2000, sm = True)
hr5_100 = cfg.Config(h = hFive, mate = fs.levelCrossOneChild, mutate= fs.mutateLevel, select= tools.selBest, popSize= 50, genNumber= 100, sm = True)
hr5_500 = cfg.Config(h = hFive, mate = fs.levelCrossOneChild, mutate= fs.mutateLevel, select= tools.selBest, popSize= 50, genNumber= 500, sm = True)
hr5_2000 = cfg.Config(h = hFive, mate = fs.levelCrossOneChild, mutate= fs.mutateLevel, select= tools.selBest, popSize= 50, genNumber= 2000, sm = True)
hr6_100 = cfg.Config(h = hSix, mate = fs.levelCrossOneChild, mutate= fs.mutateLevel, select= tools.selBest, popSize= 50, genNumber= 100, sm = True)
hr6_500 = cfg.Config(h = hSix, mate = fs.levelCrossOneChild, mutate= fs.mutateLevel, select= tools.selBest, popSize= 50, genNumber= 500, sm = True)
hr6_2000 = cfg.Config(h = hSix, mate = fs.levelCrossOneChild, mutate= fs.mutateLevel, select= tools.selBest, popSize= 50, genNumber= 2000, sm = True)

hr1_100_10 = cfg.Config(h = hOne, mate = fs.levelCrossOneChild, mutate= fs.mutateLevel, select= tools.selBest, popSize= 10, genNumber= 100, sm = True)
hr1_500_10= cfg.Config(h = hOne, mate = fs.levelCrossOneChild, mutate= fs.mutateLevel, select= tools.selBest, popSize= 10, genNumber= 500, sm = True)
hr1_2000_10 = cfg.Config(h = hOne, mate = fs.levelCrossOneChild, mutate= fs.mutateLevel, select= tools.selBest, popSize= 10, genNumber= 2000, sm = True)
hr2_100_10 = cfg.Config(h = hTwo, mate = fs.levelCrossOneChild, mutate= fs.mutateLevel, select= tools.selBest, popSize= 10, genNumber= 100, sm = True)
hr2_500_10 = cfg.Config(h = hTwo, mate = fs.levelCrossOneChild, mutate= fs.mutateLevel, select= tools.selBest, popSize= 10, genNumber= 500, sm = True)
hr2_2000_10 = cfg.Config(h = hTwo, mate = fs.levelCrossOneChild, mutate= fs.mutateLevel, select= tools.selBest, popSize= 10, genNumber= 2000, sm = True)
hr3_100_10 = cfg.Config(h = hThree, mate = fs.levelCrossOneChild, mutate= fs.mutateLevel, select= tools.selBest, popSize= 10, genNumber= 100, sm = True)
hr3_500_10 = cfg.Config(h = hThree, mate = fs.levelCrossOneChild, mutate= fs.mutateLevel, select= tools.selBest, popSize= 10, genNumber= 500, sm = True)
hr3_2000_10 = cfg.Config(h = hThree, mate = fs.levelCrossOneChild, mutate= fs.mutateLevel, select= tools.selBest, popSize= 10, genNumber= 2000, sm = True)
hr4_100_10 = cfg.Config(h = hFour, mate = fs.levelCrossOneChild, mutate= fs.mutateLevel, select= tools.selBest, popSize= 10, genNumber= 100, sm = True)
hr4_500_10 = cfg.Config(h = hFour, mate = fs.levelCrossOneChild, mutate= fs.mutateLevel, select= tools.selBest, popSize= 10, genNumber= 500, sm = True)
hr4_2000_10 = cfg.Config(h = hFour, mate = fs.levelCrossOneChild, mutate= fs.mutateLevel, select= tools.selBest, popSize= 10, genNumber= 2000, sm = True)
hr5_100_10 = cfg.Config(h = hFive, mate = fs.levelCrossOneChild, mutate= fs.mutateLevel, select= tools.selBest, popSize= 10, genNumber= 100, sm = True)
hr5_500_10 = cfg.Config(h = hFive, mate = fs.levelCrossOneChild, mutate= fs.mutateLevel, select= tools.selBest, popSize= 10, genNumber= 500, sm = True)
hr5_2000_10= cfg.Config(h = hFive, mate = fs.levelCrossOneChild, mutate= fs.mutateLevel, select= tools.selBest, popSize= 10, genNumber= 2000, sm = True)
hr6_100_10 = cfg.Config(h = hSix, mate = fs.levelCrossOneChild, mutate= fs.mutateLevel, select= tools.selBest, popSize= 10, genNumber= 100, sm = True)
hr6_500_10 = cfg.Config(h = hSix, mate = fs.levelCrossOneChild, mutate= fs.mutateLevel, select= tools.selBest, popSize= 10, genNumber= 500, sm = True)
hr6_2000_10= cfg.Config(h = hSix, mate = fs.levelCrossOneChild, mutate= fs.mutateLevel, select= tools.selBest, popSize= 10, genNumber= 2000, sm = True)

ConfigHResutls = [hr1_100,hr1_500,hr1_2000,hr2_100,hr2_500,hr2_2000,hr3_100,hr3_500,hr3_2000,hr4_100,
    hr4_500,hr4_2000,hr5_100,hr5_500,hr5_2000,hr6_100,hr6_500,hr6_2000,
    hr1_100_10,hr1_500_10,hr1_2000_10,hr2_100_10,hr2_500_10,hr2_2000_10,hr3_100_10,hr3_500_10,hr3_2000_10,
    hr4_100_10,hr4_500_10,hr4_2000_10,hr5_100_10,hr5_500_10,hr5_2000_10,hr6_100_10,hr6_500_10,hr6_2000_10]

ConfigHResutls += ConfigListTwo

ConfigMetric = [hr3_100,hr3_500,hr3_2000,hr3_100_10,hr3_500_10,hr3_2000_10,cfg19,cfg20,cfg23,cfg24]

hDraw1 = cfg.Config(h = hOne, mate = fs.levelCrossPlat, mutate= fs.mutateLevel, select= tools.selBest, popSize= 10, genNumber= 5, sm = True)
hDraw2 = cfg.Config(h = hTwo, mate = fs.levelCrossPlat, mutate= fs.mutateLevel, select= tools.selBest, popSize= 10, genNumber= 5, sm = True)
hDraw3 = cfg.Config(h = hThree, mate = fs.levelCrossPlat, mutate= fs.mutateLevel, select= tools.selBest, popSize= 10, genNumber= 5, sm = True)
hDraw4 = cfg.Config(h = hFour, mate = fs.levelCrossPlat, mutate= fs.mutateLevel, select= tools.selBest, popSize= 10, genNumber= 5, sm = True)
hDraw5= cfg.Config(h = hFive, mate = fs.levelCrossPlat, mutate= fs.mutateLevel, select= tools.selBest, popSize= 10, genNumber= 5, sm = True)

specDraw = [hDraw1,hDraw2,hDraw3,hDraw4,hDraw5]

IM = ""

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

cfg18 = cfg.Config(h = hPer2One, mate = fs.levelCrossOneChild, mutate= fs.mutateLevel, select= tools.selBest, popSize= popSize, genNumber= NGEN, sm = True)
cfg19 = cfg.Config(h = hPer2Two, mate = fs.levelCrossOneChild, mutate= fs.mutateLevel, select= tools.selBest, popSize= popSize, genNumber= NGEN, sm = True)
cfg20 = cfg.Config(h = hPer2Three, mate = fs.levelCrossOneChild, mutate= fs.mutateLevel, select= tools.selBest, popSize= popSize, genNumber= NGEN, sm = True)
cfg21 = cfg.Config(h = hPer2Four, mate = fs.levelCrossOneChild, mutate= fs.mutateLevel, select= tools.selBest, popSize= popSize, genNumber= NGEN, sm = True)

cfg22 = cfg.Config(h = hPerOne, mate = fs.levelCrossOneChild, mutate= fs.mutateLevel, select= tools.selBest, popSize= popSize, genNumber= NGEN, sm = True)
cfg23 = cfg.Config(h = hPerTwo, mate = fs.levelCrossOneChild, mutate= fs.mutateLevel, select= tools.selBest, popSize= popSize, genNumber= NGEN, sm = True)
cfg24 = cfg.Config(h = hPerThree, mate = fs.levelCrossOneChild, mutate= fs.mutateLevel, select= tools.selBest, popSize= popSize, genNumber= NGEN, sm = True)
cfg25 = cfg.Config(h = hPerFour, mate = fs.levelCrossOneChild, mutate= fs.mutateLevel, select= tools.selBest, popSize= popSize, genNumber= NGEN, sm = True)

def generateRandomPercentageHeuristicConfig(popsize,ngen,OneOrTwo = True):
    recPer = random.random()
    circlePer = random.random()
    coopPer = random.random()
    commonPer = random.random()
    whitePer = random.random()
    
    if OneOrTwo:
        totalPer = recPer + circlePer + coopPer + commonPer + whitePer
        recPer = recPer / totalPer
        circlePer = circlePer / totalPer
        coopPer = coopPer / totalPer
        commonPer = commonPer / totalPer
        h = ef.AreaPercentangeHeuristic(recPer ,circlePer ,coopPer ,commonPer , smaller = True)
    else:
        totalPer = recPer + circlePer + coopPer + commonPer
        recPer = recPer / totalPer
        circlePer = circlePer / totalPer
        coopPer = coopPer / totalPer
        commonPer = commonPer / totalPer
        h = ef.AreaPercentangeTwoHeuristic(recPer ,circlePer ,coopPer ,commonPer , smaller = True)
    conf = cfg.Config(h = h, mate = fs.levelCrossOneChild, mutate= fs.mutateLevel, select= tools.selBest, popSize= popsize, genNumber= NGEN, sm = True)
    return conf

elitism = 1
treshold = 0.92
tresholdMax = 80
def GALoop(hUsed,popSize,NGEN,config):

    h = hpy()
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


def main():
    global IM
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

def mainPer():
    global IM
    configs = []
    for i in range(10):
        configs += [generateRandomPercentageHeuristicConfig(50,500)]
    for i in range(10):
        configs += [generateRandomPercentageHeuristicConfig(10,500)]
    for i in range(10):
        configs += [generateRandomPercentageHeuristicConfig(50,500,False)]
    for i in range(10):
        configs += [generateRandomPercentageHeuristicConfig(10,500,False)]
           
    for c in configs:
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


#main()
#mainPer()


def mainMetric():
    global IM
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


mainMetric()