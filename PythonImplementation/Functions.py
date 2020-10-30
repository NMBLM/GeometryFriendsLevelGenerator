import random

INT_MIN, XINT_MAX, YINT_MAX = 3, 76, 47
#INT_MIN, XINT_MAX, YINT_MAX = 40, 1160, 680


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
    if random.random() < 0.2: # 20% chance to cross positions
        for j in range(0,5):
                aux = pOne[j]
                pOne[j] = pTwo[j]
                pTwo[j] = aux
    for i in range(5,45,5):
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
            diverse += [person]
    return diverse

def diversityEqual(population):
    diverse = []
    diverseHelp = []

    for person in population:
        personLevelRec = (person[1],person[2])
        personLevelCircle = (person[3],person[4])
        personPlat = []
        startRange = 5
        for i in range(startRange,45,5):
            if(person[i] % 2 == 1):
                posx = person[i+1]
                posy = person[i+2]
                #posy = attrList[i+2]
                width = person[i+3]
                height = person[i+4]
                #height = attrList[i+4]
                personPlat += [(posx,posy,width,height)]
        personHelp = [personLevelRec,personLevelCircle,personPlat]
        stillEqual = False
        for dh in diverseHelp:
            stillEqual = True
            if not dh[0] == personHelp[0]:
                stillEqual = False
                continue
            elif not dh[1] == personHelp[1]:
                stillEqual = False
                continue
            else:
                for plat in personHelp[3]:
                    if not plat in dh[3]:
                        stillEqual = False
                        break
            if stillEqual:
                break
        if not stillEqual:
            diverse += [person]
            diverseHelp += [personHelp]
    return diverse

def diversityEqualPlatform(population):
    diverse = []
    diverseHelp = []
    for person in population:
        personHelp = []
        startRange = 5
        for i in range(startRange,45,5):
            if(person[i] % 2 == 1):
                posx = person[i+1]
                posy = person[i+2]
                width = person[i+3]
                height = person[i+4]
                personHelp += [(posx,posy,width,height)]
        stillEqual = False
        for dh in diverseHelp:
            stillEqual = True
            if len(personHelp) == 0:
                if len(dh) == 0:
                    break
                else:
                    stillEqual = False
                    continue
            for plat in personHelp:
                if len(dh) == 0:
                    stillEqual = False
                    break
                if not plat in dh:
                    stillEqual = False
                    break
            if stillEqual:
                break
        if not stillEqual:
            diverse += [person]
            diverseHelp += [personHelp]
    return diverse
