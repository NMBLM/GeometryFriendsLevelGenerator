#import GAMain as gm
import random

'''
ga.mutateLevel(ind)

ga.levelChangeOneValue(ind)


ga.levelCrossBothPlat(pOne, pTwo)


ga.levelCrossOnePlat(pOne, pTwo)


ga.levelCrossPlat(pOne, pTwo)


#toolbox.register("mate", tools.cxTwoPoint)
#toolbox.register("mate", levelCrossOnePlat)
toolbox.register("mate", levelCrossPlat)
#toolbox.register("mate", levelCrossBothPlat)

#toolbox.register("mutate", tools.mutUniformInt,low = INT_MIN, up = XINT_MAX, indpb=0.2)
toolbox.register("mutate", mutateLevel)
#toolbox.register("mutate", levelChangeOneValue)
#toolbox.register("mutate", tools.mutFlipBit, indpb=0.2)

'''

#See The effects of the different mutations used
def TestMutations():
    
    pop = gm.toolbox.population(n=10)
    h = gm.hZero
    gm.IM.DrawGenericPop(pop,h,"\\BeforeMutation", "")

    mutsOne = list(map(gm.toolbox.clone, pop))
    mutsTwo = list(map(gm.toolbox.clone, pop))
    mutsThree = list(map(gm.toolbox.clone, pop))

    #Generic Mutation
    gm.toolbox.register("mutate", gm.tools.mutUniformInt,low = gm.INT_MIN, up = gm.XINT_MAX, indpb=0.2)
    for mutant in mutsOne:
        gm.toolbox.mutate(mutant)
        del mutant.fitness.values
    gm.IM.DrawGenericPop(mutsOne,h,"\\AfterMutation","GC")

    #One Significant Change
    gm.toolbox.register("mutate", gm.levelChangeOneValue)
    for mutant in mutsTwo:
        gm.toolbox.mutate(mutant)
        del mutant.fitness.values
    gm.IM.DrawGenericPop(mutsTwo,h,"\\AfterMutation","OC")

    #Several Random Significant Changes
    gm.toolbox.register("mutate", gm.mutateLevel)
    for mutant in mutsThree:
        gm.toolbox.mutate(mutant)
        del mutant.fitness.values
    
    gm.IM.DrawGenericPop(mutsThree,h,"\\AfterMutation","SC")


TestMutations()
