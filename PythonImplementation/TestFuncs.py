#import GAMain as gm
import random
import evaluateFuncs as ef
import instrumentation
import Functions as fs
import numpy as np
import ApplyCollectibles as ac
import WorldXMLGenerator as wg


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
#INT_MIN, XINT_MAX, YINT_MAX = 40, 1160, 680

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


def Showcrossover():
    TestLvlOne = [1, 320, 678, 120, 678, 1, 460, 400, 75, 300, 1, 735, 400, 75, 300, 1, 535, 400, 250, 75, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    TestLvlTwo =  [0, 37, 40, 6, 25, 0, 31, 24, 4, 18, 1, 11, 17, 19, 26, 0, 67, 34, 67, 19, 1, 33, 45, 48, 14, 1, 43, 47, 33, 44, 1, 69, 9, 38, 16, 0, 43, 17, 42, 10, 1, 22, 18, 49, 16]
    TestLvlThree = [1, 51, 35, 8, 14, 0, 26, 31, 45, 45, 1, 66, 42, 23, 20, 1, 8, 39, 75, 5, 0, 16, 33, 54, 10, 1, 18, 16, 48, 17, 1, 28, 42, 38, 18, 0, 57, 23, 29, 30, 0, 4, 20, 54, 25]
    TestLvlFour =  [0, 4, 43, 21, 31, 1, 26, 19, 12, 22, 0, 33, 29, 60, 27, 0, 15, 21, 37, 13, 1, 62, 14, 62, 47, 1, 44, 15, 55, 19, 1, 60, 25, 7, 22, 0, 76, 7, 17, 17, 0, 30, 4, 24, 6]
    TestLvlFive = [1, 29, 42, 6, 12, 0, 76, 7, 15, 3, 1, 31, 34, 8, 7, 0, 34, 45, 76, 19, 1, 15, 44, 71, 19, 1, 54, 41, 76, 29, 1, 28, 17, 61, 16, 0, 46, 46, 32, 12, 0, 37, 43, 41, 24]
    h = hZero
    hZero.smallerLevels = False
    testPop = [TestLvlOne,TestLvlTwo,TestLvlThree,TestLvlFour,TestLvlFive]
    for l in testPop[1:]:
        for i in range(len(l)):
            if l[i] == 1:
                continue
            l[i] = l[i] * 16
    IM.DrawGenericPop(testPop,h,"\\BeforeCrossover", "")
    crossOne = list(map(toolbox.clone, testPop))
    crossTwo = list(map(toolbox.clone, testPop))
    crossThree = list(map(toolbox.clone, testPop))

    #Generic crossover
    toolbox.register("mate", tools.cxTwoPoint)
    for child1, child2 in zip(crossOne[::2], crossOne[1::2]):
        toolbox.mate(child1, child2)
        
    IM.DrawGenericPop(crossOne,h,"\\AfterCrossover","Generic")

    #CrossOver specific to chromosome
    toolbox.register("mate", fs.levelCrossPlat)
    for child1, child2 in zip(crossTwo[::2], crossTwo[1::2]):
        toolbox.mate(child1, child2)
        
    IM.DrawGenericPop(crossTwo,h,"\\AfterCrossover","Spec")

    #Crossover that generates one child
    newOffSpring = []
    parentSet = set()
    testPopSize = len(testPop)
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

def ShowMutations():
    TestLvlOne = [1, 320, 678, 120, 678, 1, 460, 400, 75, 300, 1, 735, 400, 75, 300, 1, 535, 400, 250, 75, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    TestLvlTwo =  [0, 984, 696, 88, 650, 1, 200, 600, 288, 32, 1, 504, 376, 48, 384, 1, 552, 648, 256, 32, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    TestLvlOneOne = [1, 320, 678, 120, 678,  1, 535, 400, 250, 75, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 460, 400, 75, 300, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 735, 400, 75, 300]
    TestLvlTwoTwo =  [0, 984, 696, 88, 650, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 200, 600, 288, 32, 1, 504, 376, 48, 384,  0, 0, 0, 0, 0, 1, 552, 648, 256, 32,  0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    TestLvlThree = [1, 51, 35, 8, 14, 0, 26, 31, 45, 45, 1, 66, 42, 23, 20, 1, 8, 39, 75, 5, 0, 16, 33, 54, 10, 1, 18, 16, 48, 17, 1, 28, 42, 38, 18, 0, 57, 23, 29, 30, 0, 4, 20, 54, 25]
    TestLvlFour =  [0, 4, 43, 21, 31, 1, 26, 19, 12, 22, 0, 33, 29, 60, 27, 0, 15, 21, 37, 13, 1, 62, 14, 62, 47, 1, 44, 15, 55, 19, 1, 60, 25, 7, 22, 0, 76, 7, 17, 17, 0, 30, 4, 24, 6]
    TestLvlFive = [1, 29, 42, 6, 12, 0, 76, 7, 15, 3, 1, 31, 34, 8, 7, 0, 34, 45, 76, 19, 1, 15, 44, 71, 19, 1, 54, 41, 76, 29, 1, 28, 17, 61, 16, 0, 46, 46, 32, 12, 0, 37, 43, 41, 24]
    TestLvlSix =  [0, 37, 40, 6, 25, 0, 31, 24, 4, 18, 1, 11, 17, 19, 26, 0, 67, 34, 67, 19, 1, 33, 45, 48, 14, 1, 43, 47, 33, 44, 1, 69, 9, 38, 16, 0, 43, 17, 42, 10, 1, 22, 18, 49, 16]
    h = hZero
    hZero.smallerLevels = True
    testPop = [TestLvlOne,TestLvlTwo,TestLvlOneOne,TestLvlTwoTwo,TestLvlThree,TestLvlFour,TestLvlFive,TestLvlSix]
    testPop = [TestLvlOne,TestLvlTwo,TestLvlOneOne,TestLvlTwoTwo]
    for l in testPop[:4]:
        for i in range(len(l)):
            if l[i] == 1:
                continue
            l[i] = int(l[i] / 16)
    h = hZero
    IM.DrawGenericPop(testPop,h,"\\BeforeMutation", "")

    mutsOne = list(map(toolbox.clone, testPop))
    mutsTwo = list(map(toolbox.clone, testPop))
    mutsThree = list(map(toolbox.clone, testPop))
    mutsFour = list(map(toolbox.clone, testPop))

    #Generic Mutation
    toolbox.register("mutate", tools.mutUniformInt,low = INT_MIN, up = YINT_MAX, indpb=0.2)
    for mutant in mutsOne:
        toolbox.mutate(mutant)
    IM.DrawGenericPop(mutsOne,h,"\\AfterMutation","GC")

    #One Significant Change
    toolbox.register("mutate", fs.levelChangeOneValue)
    for mutant in mutsTwo:
        toolbox.mutate(mutant)
    IM.DrawGenericPop(mutsTwo,h,"\\AfterMutation","OC")

    #Several Random Significant Changes
    toolbox.register("mutate", fs.mutateLevel)
    for mutant in mutsThree:
        toolbox.mutate(mutant)

    IM.DrawGenericPop(mutsThree,h,"\\AfterMutation","SC")

    #Relevant Uniform Changes
    toolbox.register("mutate", fs.levelUniformChangeValue)
    for mutant in mutsFour:
        toolbox.mutate(mutant)

    IM.DrawGenericPop(mutsFour,h,"\\AfterMutation","UC")



def ShowcrossoverV2():
    TestLvlOne = [1, 320, 678, 120, 678, 1, 460, 400, 75, 300, 1, 735, 400, 75, 300, 1, 535, 400, 250, 75, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    TestLvlTwo =  [0, 984, 696, 88, 650, 1, 200, 600, 288, 32, 1, 504, 376, 48, 384, 1, 552, 648, 256, 32, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    TestLvlOneOne = [1, 320, 678, 120, 678,  1, 535, 400, 250, 75, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 460, 400, 75, 300, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 735, 400, 75, 300]
    TestLvlTwoTwo =  [0, 984, 696, 88, 650, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 200, 600, 288, 32, 1, 504, 376, 48, 384,  0, 0, 0, 0, 0, 1, 552, 648, 256, 32,  0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    TestLvlThree = [1, 51, 35, 8, 14, 0, 26, 31, 45, 45, 1, 66, 42, 23, 20, 1, 8, 39, 75, 5, 0, 16, 33, 54, 10, 1, 18, 16, 48, 17, 1, 28, 42, 38, 18, 0, 57, 23, 29, 30, 0, 4, 20, 54, 25]
    TestLvlFour =  [0, 4, 43, 21, 31, 1, 26, 19, 12, 22, 0, 33, 29, 60, 27, 0, 15, 21, 37, 13, 1, 62, 14, 62, 47, 1, 44, 15, 55, 19, 1, 60, 25, 7, 22, 0, 76, 7, 17, 17, 0, 30, 4, 24, 6]
    TestLvlFive = [1, 29, 42, 6, 12, 0, 76, 7, 15, 3, 1, 31, 34, 8, 7, 0, 34, 45, 76, 19, 1, 15, 44, 71, 19, 1, 54, 41, 76, 29, 1, 28, 17, 61, 16, 0, 46, 46, 32, 12, 0, 37, 43, 41, 24]
    TestLvlSix =  [0, 37, 40, 6, 25, 0, 31, 24, 4, 18, 1, 11, 17, 19, 26, 0, 67, 34, 67, 19, 1, 33, 45, 48, 14, 1, 43, 47, 33, 44, 1, 69, 9, 38, 16, 0, 43, 17, 42, 10, 1, 22, 18, 49, 16]
    h = hZero
    hZero.smallerLevels = True
    testPop = [TestLvlOne,TestLvlTwo,TestLvlOneOne,TestLvlTwoTwo,TestLvlThree,TestLvlFour,TestLvlFive,TestLvlSix]
    testPop = [TestLvlOne,TestLvlTwo,TestLvlOneOne,TestLvlTwoTwo]
    for l in testPop[:4]:
        for i in range(len(l)):
            if l[i] == 1:
                continue
            l[i] = int(l[i] / 16)
    IM.DrawGenericPop(testPop,h,"\\BeforeCrossover", "")
    crossOne = list(map(toolbox.clone, testPop))
    crossTwo = list(map(toolbox.clone, testPop))
    crossThree = list(map(toolbox.clone, testPop))
    IM.DrawGenericPop([],h,"\\AfterCrossover","Generic")

    #Generic crossover 1
    toolbox.register("mate", tools.cxOnePoint)
    newOffSpring = []
    parentSet = set()
    testPopSize = len(crossTwo)
    parentIndex = list(np.arange(testPopSize))

    while len(newOffSpring) < testPopSize*(testPopSize-1):
        parents = tuple(random.sample(parentIndex,2))
        while parents in parentSet:
        #while parentIndex[0] == parentIndex[1]:
            parents = tuple(random.sample(parentIndex,2))
        parentSet.add(parents)
        child1 = toolbox.clone(crossTwo[parents[0]])
        child2 = toolbox.clone(crossTwo[parents[1]])
        toolbox.mate(child1, child2)
        newOffSpring += [(child1,"GenOne" + str(parents[0]+1) + "_" + str(parents[1]+1)+ "level"),(child2,"GenOne" + str(parents[0]+1) + "_" + str(parents[1]+1)+ "level2")]
        IM.DrawLevel(child1,h,"\\AfterCrossover\\GenOne" + str(parents[0]+1) + "_" + str(parents[1]+1)+ "level")
        IM.DrawLevel(child2,h,"\\AfterCrossover\\GenOne" + str(parents[0]+1) + "_" + str(parents[1]+1)+ "level2")
    IM.WriteGenericPop(newOffSpring,"OnePointCross")

    #Generic crossover
    toolbox.register("mate", tools.cxTwoPoint)
    newOffSpring = []
    parentSet = set()
    testPopSize = len(crossTwo)
    parentIndex = list(np.arange(testPopSize))
    while len(newOffSpring) < testPopSize*(testPopSize-1):
        parents = tuple(random.sample(parentIndex,2))
        while parents in parentSet:
        #while parentIndex[0] == parentIndex[1]:
            parents = tuple(random.sample(parentIndex,2))
        parentSet.add(parents)
        child1 = toolbox.clone(crossTwo[parents[0]])
        child2 = toolbox.clone(crossTwo[parents[1]])
        toolbox.mate(child1, child2)
        newOffSpring += [(child1,"Gen" + str(parents[0]+1) + "_" + str(parents[1]+1)+ "level"),(child2,"Gen" + str(parents[0]+1) + "_" + str(parents[1]+1)+ "level")]
        IM.DrawLevel(child1,h,"\\AfterCrossover\\Gen" + str(parents[0]+1) + "_" + str(parents[1]+1)+ "level")
        IM.DrawLevel(child2,h,"\\AfterCrossover\\Gen" + str(parents[0]+1) + "_" + str(parents[1]+1)+ "level2")
    IM.WriteGenericPop(newOffSpring,"TwoPointCross")

    #CrossOver specific to chromosome
    toolbox.register("mate", fs.levelCrossPlat)
    newOffSpring = []
    parentSet = set()
    testPopSize = len(crossTwo)
    parentIndex = list(np.arange(testPopSize))
    while len(newOffSpring) <  testPopSize*(testPopSize-1):
        parents = tuple(random.sample(parentIndex,2))
        while parents in parentSet:
            parents = tuple(random.sample(parentIndex,2))
        parentSet.add(parents)
        child1 = toolbox.clone(crossTwo[parents[0]])
        child2 = toolbox.clone(crossTwo[parents[1]])
        toolbox.mate(child1, child2)
        newOffSpring += [(child1,"Spec" + str(parents[0]+1) + "_" + str(parents[1]+1)+ "level"),(child2,"Spec" + str(parents[0]+1) + "_" + str(parents[1]+1)+ "level")]
        IM.DrawLevel(child1,h,"\\AfterCrossover\\Spec" + str(parents[0]+1) + "_" + str(parents[1]+1)+ "level")
        IM.DrawLevel(child2,h,"\\AfterCrossover\\Spec" + str(parents[0]+1) + "_" + str(parents[1]+1)+ "level2")
    IM.WriteGenericPop(newOffSpring,"SpecificCrossover")    
    #Crossover that generates one child
    newOffSpring = []
    parentSet = set()
    testPopSize = len(crossThree)
    parentIndex = list(np.arange(testPopSize))
    while len(newOffSpring) <  testPopSize*(testPopSize-1):
        parents = tuple(random.sample(parentIndex,2))
        #while parents in parentSet:
        while parentIndex[0] == parentIndex[1]:
            parents = tuple(random.sample(parentIndex,2))
        parentSet.add(parents)
        child1 = fs.levelCrossOneChild(toolbox.clone(crossThree[parents[0]]), toolbox.clone(crossThree[parents[1]]))
        child2 = fs.levelCrossOneChild(toolbox.clone(crossThree[parents[0]]), toolbox.clone(crossThree[parents[1]]))
        newOffSpring += [(child1,str(parents[0]+1) + "_" + str(parents[1]+1)+ "level"),(child2, str(parents[0]+1) + "_" + str(parents[1]+1)+ "level")]
        IM.DrawLevel(child1,h,"\\AfterCrossover\\" + str(parents[0]+1) + "_" + str(parents[1]+1)+ "level")
        IM.DrawLevel(child2,h,"\\AfterCrossover\\" + str(parents[0]+1) + "_" + str(parents[1]+1)+ "level2")
    IM.WriteGenericPop(newOffSpring,"BestCrossover")
    #IM.DrawGenericPop(newOffSpring,h,"\\AfterCrossover","SC")
    print(parentSet)

    #Crossover that generates one child
    newOffSpring = []
    parentSet = set()
    testPopSize = len(crossThree)
    parentIndex = list(np.arange(testPopSize))
    while len(newOffSpring) <  testPopSize*(testPopSize-1):
        parents = tuple(random.sample(parentIndex,2))
        #while parents in parentSet:
        while parentIndex[0] == parentIndex[1]:
            parents = tuple(random.sample(parentIndex,2))
        parentSet.add(parents)
        child = fs.levelCrossOneChildEveryValue(toolbox.clone(crossThree[parents[0]]), toolbox.clone(crossThree[parents[1]]))
        newOffSpring += [child]
        IM.DrawLevel(child,h,"\\AfterCrossover\\E" + str(parents[0]+1) + "_" + str(parents[1]+1)+ "level")
    #IM.DrawGenericPop(newOffSpring,h,"\\AfterCrossover","SC")
    print(parentSet)


def TestPlaceCollectibles():
    lvlTwoSpecs = [ef.SpecialArea(100,80,1100,240, ef.AreaType.Cooperative), ef.SpecialArea(430,560,340,180,ef.AreaType.RectangleOnly)]
    hTwo = ef.AreaHeuristic(lvlTwoSpecs, smaller = True)
    TestLvlOne = [1, 320, 678, 120, 678, 1, 460, 400, 75, 300, 1, 735, 400, 75, 300, 1, 535, 400, 250, 75, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    TestLvlTwo =  [0, 984, 696, 88, 650, 1, 200, 600, 288, 32, 1, 504, 376, 48, 384, 1, 552, 648, 256, 32, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    TestLvlOneOne = [1, 320, 678, 120, 678,  1, 535, 400, 250, 75, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 460, 400, 75, 300, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 735, 400, 75, 300]
    TestLvlTwoTwo =  [0, 984, 696, 88, 650, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 200, 600, 288, 32, 1, 504, 376, 48, 384,  0, 0, 0, 0, 0, 1, 552, 648, 256, 32,  0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    TestLvlThree = [1, 51, 35, 8, 14, 0, 26, 31, 45, 45, 1, 66, 42, 23, 20, 1, 8, 39, 75, 5, 0, 16, 33, 54, 10, 1, 18, 16, 48, 17, 1, 28, 42, 38, 18, 0, 57, 23, 29, 30, 0, 4, 20, 54, 25]
    TestLvlFour =  [0, 4, 43, 21, 31, 1, 26, 19, 12, 22, 0, 33, 29, 60, 27, 0, 15, 21, 37, 13, 1, 62, 14, 62, 47, 1, 44, 15, 55, 19, 1, 60, 25, 7, 22, 0, 76, 7, 17, 17, 0, 30, 4, 24, 6]
    TestLvlFive = [1, 29, 42, 6, 12, 0, 76, 7, 15, 3, 1, 31, 34, 8, 7, 0, 34, 45, 76, 19, 1, 15, 44, 71, 19, 1, 54, 41, 76, 29, 1, 28, 17, 61, 16, 0, 46, 46, 32, 12, 0, 37, 43, 41, 24]
    TestLvlSix =  [0, 37, 40, 6, 25, 0, 31, 24, 4, 18, 1, 11, 17, 19, 26, 0, 67, 34, 67, 19, 1, 33, 45, 48, 14, 1, 43, 47, 33, 44, 1, 69, 9, 38, 16, 0, 43, 17, 42, 10, 1, 22, 18, 49, 16]
    h = hZero
    TestLvlSeven = [0, 16, 19, 14, 40, 0, 49, 45, 43, 28, 0, 53, 13, 69, 29, 1, 19, 22, 36, 12, 1, 24, 17, 3, 24, 1, 58, 27, 51, 20, 0, 18, 3, 21, 15, 0, 36, 45, 52, 6, 0, 65, 22, 11, 18]
    testPop = [TestLvlOne,TestLvlTwo,TestLvlOneOne,TestLvlTwoTwo,TestLvlThree,TestLvlFour,TestLvlFive,TestLvlSix]
    #testPop = [TestLvlOne,TestLvlOneOne,TestLvlThree,TestLvlFour,TestLvlFive,TestLvlSix]
    #testPop = [TestLvlOne,TestLvlTwo,TestLvlOneOne,TestLvlTwoTwo]
    testPop = [TestLvlSeven]
    counter = 1
    world = []
    for i in range(len(testPop)):
        if(i < 4):
            hTwo.smallerLevels = True
            lvl = hTwo.TestLevel(testPop[i])
        else:
            hTwo.smallerLevels = True
            lvl = hTwo.TestLevel(testPop[i])
        lvl = ac.PlaceCollectibles(hTwo,lvl)
        world += [lvl]
        IM.DrawLevelLevel(lvl,name= "\\col" + str(counter),col= True)
        counter+= 1

    wg.WriteWorld(world,name= "OneLevel.xml")

def WriteWorldNoCollect():
    TestLvlOne = [1, 320, 678, 120, 678, 1, 460, 400, 75, 300, 1, 735, 400, 75, 300, 1, 535, 400, 250, 75, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    TestLvlTwo =  [0, 984, 696, 88, 650, 1, 200, 600, 288, 32, 1, 504, 376, 48, 384, 1, 552, 648, 256, 32, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    #TestLvlOneOne = [1, 320, 678, 120, 678,  1, 535, 400, 250, 75, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 460, 400, 75, 300, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 735, 400, 75, 300]
    #TestLvlTwoTwo =  [0, 984, 696, 88, 650, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 200, 600, 288, 32, 1, 504, 376, 48, 384,  0, 0, 0, 0, 0, 1, 552, 648, 256, 32,  0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    Mutated1 = [1,20, 10, 7, 42, 1, 28, 25, 4, 26, 1, 45, 25, 4, 18, 1, 33, 32, 15, 4, 0, 0, 0, 38, 0, 0, 0, 0, 42, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 11, 0, 0]
    Mutated2 = [1,61, 35, 5, 40, 1, 12, 37, 18, 2, 1, 31, 23, 3, 35, 1, 32, 40, 16, 2, 1, 21, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 47, 1, 0, 0, 9, 0]
    Mutated3 = [1,20, 42, 7, 42, 1, 28, 25, 4, 18, 1, 45, 25, 4, 18, 0, 33, 25, 15, 4, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    Mutated4 = [1,61, 37, 5, 40, 1, 12, 37, 18, 2, 1, 12, 23, 3, 24, 1, 42, 21, 56, 12, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    Mutated5 = [1,20, 42, 7, 4, 1, 28, 25, 4, 18, 1, 45, 25, 4, 18, 1, 33, 25, 15, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    Mutated6 = [1,61, 43, 5, 40, 1, 12, 37, 73, 2, 1, 31, 23, 3, 24, 1, 34, 40, 16, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    Cross11 = [1,20, 42, 7, 42, 1, 28, 25, 4, 18, 1, 31, 23, 3, 24, 1, 33, 25, 15, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    Cross21 = [1,61, 43, 5, 40, 1, 12, 37, 18, 2, 1, 45, 25, 4, 18, 1, 34, 40, 16, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    Cross12 = [1,20, 42, 7, 42, 1, 28, 25, 4, 18, 1, 45, 25, 4, 18, 1, 33, 25, 15, 2, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    Cross22  = [1,61, 43, 5, 40, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 12, 37, 18, 4, 0, 31, 23, 3, 24, 0, 0, 0, 0, 0, 1, 34, 40, 16, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    Cross13 = [1,20, 42, 7, 42, 1, 28, 25, 4, 18, 1, 45, 25, 4, 18, 1, 33, 40, 16, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    Cross23 = [1,61, 43, 5, 40, 1, 12, 37, 18, 2, 1, 31, 23, 3, 24, 1, 34, 25, 15, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    Cross14 = [1,20, 42, 7, 42, 1, 33, 25, 15, 4, 0, 0, 0, 0, 0, 1, 34, 40, 16, 2, 1, 28, 25, 4, 18, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    Cross24 = [1,61, 43, 7, 42, 1, 12, 37, 18, 2, 1, 31, 23, 3, 24, 0, 0, 0, 0, 0, 1, 28, 25, 4, 18, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 45, 25, 4, 18]
    h = hZero
    counter = 1
    testPop = [TestLvlOne,TestLvlTwo,Mutated1,Mutated2,Mutated3,Mutated4,Mutated5,Mutated6,Cross11,Cross21,Cross12,Cross22,Cross13,Cross23,Cross14,Cross24]
    testPop = [Mutated1,Mutated2,Mutated3,Mutated4,Mutated5,Mutated6]
    testPop = [Cross11,Cross21,Cross12,Cross22,Cross13,Cross23,Cross14,Cross24]
    testPop = [TestLvlOne,TestLvlTwo]
    world = []
    for i in range(len(testPop)):
        if(i < 2):
            h.smallerLevels = False
            lvl = h.TestLevel(testPop[i])
        else:
            h.smallerLevels = True
            lvl = h.TestLevel(testPop[i])
        lvl = ac.PlaceCollectibles(hZero,lvl)
        if(i < 2):
            lvl.collectibles = [[1,1]]
        else:
            lvl.collectibles = [[1,1]]
        world += [lvl]
        IM.DrawLevelLevel(lvl,name= "\\col" + str(counter),col= True)
        counter+= 1

    wg.WriteWorld(world,name= "Cross2.xml")
    #wg.WriteWorld(world,name= "Mut2.xml")

#TestMutations()
#TestCrossover()
#Showcrossover()
#ShowMutations()
#ShowcrossoverV2()
#TestPlaceCollectibles()
WriteWorldNoCollect()