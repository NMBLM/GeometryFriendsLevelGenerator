#import GAMain as gm
import random
import evaluateFuncs as ef
import instrumentation
import Functions as fs
import numpy as np

from deap import base
from deap import creator
from deap import tools
from evaluateFuncs import Level
import PILViewer as viewer
'''
ga.mutateLevel(ind)

ga.levelChangeOneValue(ind)


ga.levelCrossBothPlat(pOne, pTwo)


ga.levelCrossOnePlat(pOne, pTwo)


ga.levelCrossPlat(pOne, pTwo)
'''


INT_MIN, XINT_MAX, YINT_MAX = 3, 76, 47

lvlZeroSpecs = []

hZero = ef.AreaHeuristic(lvlZeroSpecs, smaller = True)



IM = instrumentation.InstrumentationManager(on = True)


def getFit(ind):
    return ind.fitness.values[0]

creator.create("FitnessMax", base.Fitness, weights=(1.0, 1.0))
creator.create("Individual", list, fitness=creator.FitnessMax)

toolbox = base.Toolbox()

N_CYCLES = 9

toolbox.register("attr_bool", random.randint, 0, 1)
toolbox.register("attr_xInt", random.randint, INT_MIN, XINT_MAX)
toolbox.register("attr_yInt", random.randint, INT_MIN, YINT_MAX)
toolbox.register("individual", tools.initCycle, creator.Individual,
(toolbox.attr_bool, toolbox.attr_xInt , toolbox.attr_yInt, toolbox.attr_xInt, toolbox.attr_yInt), n=N_CYCLES)

toolbox.register("population", tools.initRepeat, list, toolbox.individual)
toolbox.register("evaluate", hZero.CalculateFitness)


#toolbox.register("mate", tools.cxTwoPoint)
#toolbox.register("mate", fs.levelCrossPlat)


#toolbox.register("mutate", tools.mutUniformInt,low = INT_MIN, up = YINT_MAX, indpb=0.2)
#toolbox.register("mutate", fs.mutateLevel)
#toolbox.register("mutate", fs.levelChangeOneValue)
#toolbox.register("mutate", tools.mutFlipBit, indpb=0.2)

testPopSize = 10
#See The effects of the different mutations used
pop = toolbox.population(n=testPopSize)
def TestMutations():
    global pop
    
    h = hZero
    IM.DrawGenericPop(pop,h,"\\BeforeMutation", "")

    mutsOne = list(map(toolbox.clone, pop))
    mutsTwo = list(map(toolbox.clone, pop))
    mutsThree = list(map(toolbox.clone, pop))
    mutsFour = list(map(toolbox.clone, pop))

    #Generic Mutation
    toolbox.register("mutate", tools.mutUniformInt,low = INT_MIN, up = YINT_MAX, indpb=0.2)
    for mutant in mutsOne:
        toolbox.mutate(mutant)
        del mutant.fitness.values
    IM.DrawGenericPop(mutsOne,h,"\\AfterMutation","GC")

    #One Significant Change
    toolbox.register("mutate", fs.levelChangeOneValue)
    for mutant in mutsTwo:
        toolbox.mutate(mutant)
        del mutant.fitness.values
    IM.DrawGenericPop(mutsTwo,h,"\\AfterMutation","OC")

    #Several Random Significant Changes
    toolbox.register("mutate", fs.mutateLevel)
    for mutant in mutsThree:
        toolbox.mutate(mutant)
        del mutant.fitness.values

    IM.DrawGenericPop(mutsThree,h,"\\AfterMutation","SC")

    #Relevant Uniform Changes
    toolbox.register("mutate", fs.levelUniformChangeValue)
    for mutant in mutsFour:
        toolbox.mutate(mutant)
        del mutant.fitness.values

    IM.DrawGenericPop(mutsFour,h,"\\AfterMutation","UC")


TestMutations()


def TestCrossover():
    global pop

    h = hZero
    IM.DrawGenericPop(pop,h,"\\BeforeCrossover", "")

    crossOne = list(map(toolbox.clone, pop))
    crossTwo = list(map(toolbox.clone, pop))
    crossThree = list(map(toolbox.clone, pop))

    #Generic crossover
    toolbox.register("mate", tools.cxTwoPoint)
    for child1, child2 in zip(crossOne[::2], crossOne[1::2]):
        toolbox.mate(child1, child2)
        del child1.fitness.values
        del child2.fitness.values
    IM.DrawGenericPop(crossOne,h,"\\AfterCrossover","Generic")

    #CrossOver specific to chromosome
    toolbox.register("mate", fs.levelCrossPlat)
    for child1, child2 in zip(crossTwo[::2], crossTwo[1::2]):
        toolbox.mate(child1, child2)
        del child1.fitness.values
        del child2.fitness.values
    IM.DrawGenericPop(crossTwo,h,"\\AfterCrossover","Spec")

    #Crossover that generates one child
    newOffSpring = []
    parentSet = set()
    parentIndex = list(np.arange(testPopSize))
    while len(newOffSpring) < testPopSize * 2:
        parents = tuple(random.sample(parentIndex,2))
        while parents in parentSet:
            parents = tuple(random.sample(parentIndex,2))
        parentSet.add(parents)
        child = fs.levelCrossOneChild(toolbox.clone(crossThree[parents[0]]), toolbox.clone(crossThree[parents[1]]))
        newOffSpring += [child]
        IM.DrawLevel(child,h,"\\AfterCrossover\\" + str(parents[0]+1) + "_" + str(parents[1]+1)+ "level")
    #IM.DrawGenericPop(newOffSpring,h,"\\AfterCrossover","SC")
    print(parentSet)

    #Crossover that generates one child
    newOffSpring = []
    parentSet = set()
    parentIndex = list(np.arange(testPopSize))
    while len(newOffSpring) < testPopSize * 2:
        parents = tuple(random.sample(parentIndex,2))
        while parents in parentSet:
            parents = tuple(random.sample(parentIndex,2))
        parentSet.add(parents)
        child = fs.levelCrossOneChildEveryValue(toolbox.clone(crossThree[parents[0]]), toolbox.clone(crossThree[parents[1]]))
        newOffSpring += [child]
        IM.DrawLevel(child,h,"\\AfterCrossover\\E" + str(parents[0]+1) + "_" + str(parents[1]+1)+ "level")
    #IM.DrawGenericPop(newOffSpring,h,"\\AfterCrossover","SC")
    print(parentSet)

TestCrossover()