import random

INT_MIN, XINT_MAX, YINT_MAX = 3, 76, 47
#INT_MIN, XINT_MAX, YINT_MAX = 40, 1160, 680


def mutateLevel(ind):
    if random.random() < 0.2:
        for i in range(5,45,5):
            if(ind[i] % 2 == 1):
                if random.random() < 0.5: #remove plat that exists
                    ind[i] = 0
            else:
                if random.random() < 0.5: #add platform
                    ind[i] = 1
    else:
        for i in range(0,45,5):
            if(ind[i] % 2 == 1 or i == 0):
                for j in range(i+1,i+5,2): # x, width
                    if random.random() < 0.5:
                        ind[j] = random.randint(INT_MIN,XINT_MAX)
                for j in range(i+2,i+5,2):
                    if random.random() < 0.5: # y, height
                        ind[j] = random.randint(INT_MIN,YINT_MAX)




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


def levelUniformChangeValue(ind):
    sIndex = [0]
    rand = random.random()
    for i in range(5,45,5): #find index of active platforms
        if ind[i] % 2 == 1:
            sIndex += [i]
    if len(sIndex) == 1: #if it has no platforms add one
        index = random.choice([5,10,15,20,25,30,35,40])
        ind[index] = 1
        ind[index+1] = random.randint(INT_MIN,XINT_MAX)
        ind[index+2] = random.randint(INT_MIN,YINT_MAX)
        ind[index+3] = random.randint(INT_MIN,XINT_MAX)
        ind[index+4] = random.randint(INT_MIN,YINT_MAX)
    elif rand < 0.1: #just add a platform
        aIndex = list({5,10,15,20,25,30,35,40}-set(sIndex)) #return the indexes that don't have platforms
        if len(aIndex) == 0: #if already has max platforms change a random value
            for i in range(5,45,5):
                for j in range(1,5):
                    if random.random() < 0.4:
                        ind[i+j] = random.randint(INT_MIN,XINT_MAX) if j%2 ==1 else random.randint(INT_MIN,YINT_MAX)
        else: #create a new platform
            index = random.choice(aIndex)
            ind[index] = 1
            ind[index+1] = random.randint(INT_MIN,XINT_MAX)
            ind[index+2] = random.randint(INT_MIN,YINT_MAX)
            ind[index+3] = random.randint(INT_MIN,XINT_MAX)
            ind[index+4] = random.randint(INT_MIN,YINT_MAX)
            sIndex.append(index)
    elif rand < 0.2: #just remove a platform
        index = random.choice(sIndex[1:])
        ind[index] = 0
    #uniform chance to change a value always
    for i in sIndex:
        for j in range(1,5):
            if random.random() < 0.4:
                ind[i+j] = random.randint(INT_MIN,XINT_MAX) if j%2 ==1 else random.randint(INT_MIN,YINT_MAX)


def levelUniformChangeValueLimited(ind):
    sIndex = [0]
    rand = random.random()
    for i in range(5,45,5): #find index of active platforms
        if ind[i] % 2 == 1:
            sIndex += [i]
    if len(sIndex) == 1: #if it has no platforms add one
        index = random.choice([5,10,15,20,25,30,35,40])
        ind[index] = 1
        ind[index+1] = random.randint(INT_MIN,XINT_MAX)
        ind[index+2] = random.randint(INT_MIN,YINT_MAX)
        ind[index+3] = random.randint(INT_MIN,int(XINT_MAX / 2))
        ind[index+4] = random.randint(INT_MIN,int(YINT_MAX / 2))
    elif rand < 0.1: #just add a platform
        aIndex = list({5,10,15,20,25,30,35,40}-set(sIndex)) #return the indexes that don't have platforms
        if len(aIndex) == 0: #if already has max platforms change a random value
            for i in range(5,45,5):
                for j in range(1,5):
                    if random.random() < 0.4:
                        ind[i+j] = random.randint(INT_MIN,XINT_MAX) if j%2 ==1 else random.randint(INT_MIN,YINT_MAX)
        else: #create a new platform
            index = random.choice(aIndex)
            ind[index] = 1
            ind[index+1] = random.randint(INT_MIN,XINT_MAX)
            ind[index+2] = random.randint(INT_MIN,YINT_MAX)
            ind[index+3] = random.randint(INT_MIN,int(XINT_MAX / 2))
            ind[index+4] = random.randint(INT_MIN,int(YINT_MAX / 2))
            sIndex.append(index)
    elif rand < 0.2: #just remove a platform
        index = random.choice(sIndex[1:])
        ind[index] = 0
    #uniform chance to change a value always
    for i in sIndex:
        for j in [1,2]:
            if random.random() < 0.4:
                ind[i+j] = random.randint(INT_MIN,XINT_MAX) if j%2 ==1 else random.randint(INT_MIN,YINT_MAX)
        for j in [3,4]:
            if random.random() < 0.4:
                ind[i+j] = random.randint(INT_MIN,int(XINT_MAX / 2)) if j%2 ==1 else random.randint(INT_MIN,int(YINT_MAX / 2))
              
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

def levelCrossOneChild(pOne, pTwo):
    child = pOne
    if (random.random() < 0.5): 
        for j in range(1,3): #parent One rectangle
            child[j] = pOne[j]
    else:
        for j in range(1,3): #parent Two rectangle
            child[j] = pTwo[j]

    if (random.random() < 0.5):
        for j in range(3,5): #parent One circle
            child[j] = pOne[j]
    else:
        for j in range(3,5): #parent Two circle
            child[j] = pTwo[j]
            
    for i in range(5,45,5):
        if (random.random() < 0.5):
            for j in range(i,i+5): #parent One platform
                child[j] = pOne[j]
            else:
                for j in range(i,i+5): #parent Two platform
                    child[j] = pTwo[j]
    return child

def levelCrossOneChildSimplified(pOne, pTwo):
    child = pOne #clone parent
    if (random.random() < 0.5): 
        for j in range(1,3): #parent Two rectangle
            child[j] = pTwo[j]
    if (random.random() < 0.5):
        for j in range(3,5): #parent Two circle
            child[j] = pTwo[j]
    for i in range(5,45,5):
        if (random.random() < 0.5):
            for j in range(i,i+5): #parent Two platform
                child[j] = pTwo[j]
    return child


def levelCrossOneChildEveryValue(pOne, pTwo):
    child = pOne
    for i in range(1,45): #first value can be skipped because it does not matter ever
        if (random.random() < 0.5): 
            child[i] = pOne[i]
        else:
            child[i] = pTwo[i]
    return child


        
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
        startRange = 5 #platforms only
        personHelp = []
        for i in range(startRange,45,5):
            if(person[i] % 2 == 1): #platform is active
                posx = person[i+1]
                posy = person[i+2]
                width = person[i+3]
                height = person[i+4]
                personHelp += [(posx,posy,width,height)]
        stillEqual = False
        #When it exits this loop if stillEqual is False then no copies where found
        for dh in diverseHelp:
            stillEqual = True
            if len(personHelp) == 0: #if it does not have any platforms
                if len(dh) == 0: #if the other level also does not have platforms then they are equal
                    break
                else:
                    stillEqual = False
                    continue #continue because it already is not equal
            for plat in personHelp:
                if len(dh) == 0:
                    stillEqual = False
                    break #break because it already is not equal
                #if platform in the current level is not in the one we are comparing to then it is different and can move to comparing next one
                if not plat in dh: 
                    stillEqual = False
                    break #break because it already is not equal
            if stillEqual:
                break
        if not stillEqual:
            diverse += [person]
            diverseHelp += [personHelp]
    return diverse