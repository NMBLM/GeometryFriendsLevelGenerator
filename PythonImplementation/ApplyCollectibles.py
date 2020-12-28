import evaluateFuncs as ef
import random

# 1280*740 = 947200 | 1280/16*740/16 = 3700
# 79*49 = 3871  | (1100/16)*(240/16) = 1031 if it has this much or more should have 3 collectibles
# # a level should at most have 9 collectibles


xGridLen = ef.xGridLen
yGridLen = ef.yGridLen

smallerAreaLimits = [0,300,750,1000,2000]
areaLimits = [lim * 16 * 16 for lim in smallerAreaLimits]
minRangeBetweenCollectibles = 3
maxAttempts = 10000

def PlaceCollectibles(h,level,maxCollectibles = -1):
    numberOfCollectiblesPlaced = 0
    collectiblesPlaced = []
    for area in h.specifications:
        areaPosX = (int) ((area.x - 40) / ef.blockSize) + 2 
        areaPosY = (int) ((area.y - 40) / ef.blockSize) + 2 
        areaWidth = (int) ((area.width - 40) / ef.blockSize) + 2 
        areaHeight = (int) ((area.height - 40) / ef.blockSize) + 2
        areaType = area.type
        areaArea = areaWidth*areaHeight
        numberOfCollectibles = next(i for i,v in enumerate(smallerAreaLimits) if v > areaArea)
        attempts = 0
        for i in range(numberOfCollectibles):
            colX = random.randint(areaPosX,areaPosX+areaWidth)
            colY = random.randint(areaPosY,areaPosY+areaHeight)
            collectible = [colX,colY]
            nearCollectible = True
            while(nearCollectible and attempts < maxAttempts):
                nearCollectible = False
                for col in collectiblesPlaced:
                    while colX >= 79 or colY >= 49 :
                        colX = random.randint(areaPosX,areaPosX+areaWidth)
                        colY = random.randint(areaPosY,areaPosY+areaHeight)
                        collectible = [colX,colY]
                        nearCollectible = True
                    if isClose(collectible,col,minRangeBetweenCollectibles): #if it is close to another generate new collectible
                        colX = random.randint(areaPosX,areaPosX+areaWidth)
                        colY = random.randint(areaPosY,areaPosY+areaHeight)
                        collectible = [colX,colY]
                        nearCollectible = True
                        attempts += 1
                        break
                if nearCollectible: #if the collectible is new, then compare again with others
                    continue
                else:#check if it will be placed in an cell where it and its surrounding cells match the area type otherwise repeat
                    collectibleSize = 1
                    i = -collectibleSize
                    while(i <= collectibleSize and not nearCollectible):
                        j = -collectibleSize
                        while(j <= collectibleSize and not nearCollectible):
                            if colX+i >=  79 or colY+j >= 49 :
                                j = j + 1
                                continue
                            if not areaTypeMatchCell(areaType, level.grid[colX+i][colY+j]): 
                                nearCollectible = True 
                            j = j + 1
                        i = i + 1
                if nearCollectible: #if it has to repeat then choose new position
                    colX = random.randint(areaPosX,areaPosX+areaWidth)
                    colY = random.randint(areaPosY,areaPosY+areaHeight)
                    collectible = [colX,colY]
                    attempts += 1
            #upon exiting add to collectibles placed if it found one that worked otherwise do not place bad collectible
            #if (attempts < maxAttempts):
            if colX >=  79 or colY >= 49:
                continue
            if not level.grid[colX][colY] == ef.BlockType.Platform:
                numberOfCollectiblesPlaced += 1
                collectiblesPlaced += [collectible]
        level.collectibles = collectiblesPlaced     
    return level

def isClose(posA,posB,maxDistance):
    return ((posA[0] - posB[0])^2 +  (posA[1] - posB[1])^2) < maxDistance*maxDistance


def areaTypeMatchCell(areaType,block):
    if areaType == ef.AreaType.Common:
        if block == ef.BlockType.BothCanReach:
            return True
    elif areaType == ef.AreaType.Cooperative:
        if block == ef.BlockType.CooperativeCanReach:
            return True
        elif block == ef.BlockType.CooperativeCanReachRectanglePlatform:
            return True
    elif areaType == ef.AreaType.CircleOnly:
        if block == ef.BlockType.CircleCanReach:
            return True
        elif block == ef.BlockType.CircleCanReachRectanglePlatform:
            return True
    elif areaType == ef.AreaType.RectangleOnly:
        if block == ef.BlockType.RectangleCanReach:
            return True
        elif block == ef.BlockType.RectangleCanReachCirclePlatform:
            return True
    return False