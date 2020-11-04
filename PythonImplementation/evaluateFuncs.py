from enum import Enum

class Level:
    def __init__(self, attrList, rectSpawn = [], circlespawn= [],smaller = False):
        if(len(attrList) < 45):
            print("Incorrect attr Len")
        self.smallerNums = smaller
        self.rectSpawn = (attrList[1],attrList[2])
        self.circleSpawn = (attrList[3],attrList[4])
        self.platforms = []
        startRange = 5
        if(len(rectSpawn) > 1):
            startRange = 0
            self.rectSpawn = rectSpawn
            self.circleSpawn = circlespawn
        for i in range(startRange,45,5):
            if(attrList[i] % 2 == 1):
                posx = attrList[i+1]
                posy = attrList[i+2]
                #posy = attrList[i+2]
                width = attrList[i+3]
                height = attrList[i+4]
                #height = attrList[i+4]
                self.platforms += [(posx,posy,width,height)]
        self.cellGrid = []
        self.grid = []
        self.fit = -1

    def description(self):
        text = "RectangleSpawn " + str(self.rectSpawn) + "\n"
        text += "CircleSpawn " + str(self.circleSpawn) + "\n"
        for plat in self.platforms:
            text += "Platform: " + str(plat) + "\n"
        return text



class PlatformType(Enum):
    Common = 0
    CirclePlatform = 1    #Is a platform that only blocks the Circle
    RectanglePlatform = 2  #Is a platform that only blocks the Rectangle
    CooperativeArea = 3
    CircleOnlyArea = 4
    RectangleOnlyArea = 5
    NotPlatform = 6

class BlockType(Enum):
    Unreachable = 0
    Platform = 1
    CirclePlatform = 2     #Is a platform that only blocks the Circle
    RectanglePlatform = 3  #Is a platform that only blocks the Rectangle
    RectangleCanReach = 4
    CircleCanReach = 5
    BothCanReach = 6
    CooperativeCanReach = 7
    RectangleCanReachCirclePlatform = 8         #Is a Circle Platform that the Rectangle can Reach
    CircleCanReachRectanglePlatform = 9         #Is a Rectangle Platform that the Circle can Reach
    CooperativeCanReachRectanglePlatform = 10   #Is a Rectangle Platform that the Circle can Reach when using cooperation to jump

class AreaType(Enum):
    Cooperative = 0
    Common = 1
    CircleOnly = 2
    RectangleOnly = 3

class Cell:
    def __init__(self):
        self.Platform = PlatformType.NotPlatform
        self.fitsRectangle = False
        self.fitsCircle = False
        self.reachesRectangle = False
        self.traversedRectangleLeft = False
        self.traversedRectangleRight = False
        self.reachesCircle = False
        self.reachesCoop = False
        self.jumpStrength = -1
        self.notCoopJump = False

class SpecialArea:
    def __init__(self, x, y, width, height, type):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.type = type

blockSize = 16
#xGridLen = (int) ((1240 - 40) / blockSize + 0.5) + 4
#yGridLen = (int) ((760 - 40) / blockSize + 0.5) + 4
xGridLen = 79
yGridLen = 49
#rectangleMaxLen = (int) (200 / blockSize + 0.5)
rectangleMaxLen = 13

level = [1, 1038, 506, 895, 581, 0, 288, 398, 6, 326, 0, 290, 365, 865, 598, 1, 1244, 542, 753, 119, 1, 357, 39, 271, 442, 1, 803, 678, 683, 120, 0, 838, 544, 590, 398, 0, 819, 439, 833, 240, 1, 1074, 254, 221, 540]
class AreaHeuristic:
    def __init__(self, specs,smaller = False):
        self.specifications = specs #tuple or matrix of SpecialAreas
        self.smallerLevels = smaller


    def CalculateFitness(self, level):
        lvl = Level(level,smaller = self.smallerLevels)
        initCellGrid(lvl)
        InitFits(lvl)
        RectangleReachability(lvl)
        CircleReachability(lvl)
        ResetJumpStrength(lvl)
        CoopReachability(lvl)
        CellGridToBlockGrid(lvl)
        fit = fitness(lvl,self)
        del lvl
        return fit
    
    def TestLevel(self,level):
        lvl = Level(level,smaller = self.smallerLevels)
        initCellGrid(lvl)
        InitFits(lvl)
        RectangleReachability(lvl)
        CircleReachability(lvl)
        ResetJumpStrength(lvl)
        CoopReachability(lvl)
        CellGridToBlockGrid(lvl)
        fit = fitness(lvl,self)
        lvl.fit = fit
        return lvl

        
def getV(v):
    return v[0]

class FixedSpawnAreaHeuristic:
    def __init__(self,specs, spawns = [],smaller = False):
        self.smallerLevels = smaller
        self.specifications = specs
        if len(spawns) >0:
            self.spawns = spawns
        else:
            self.spawns = [((980,690),(88,640)),((232,328),(104,328)),((104,136),(1192,152)),((1080,344),(1192,344))]

    def CalculateFitness(self, level):
        fit = []
        for s in self.spawns:
            lvl = Level(level,s[0],s[1],smaller = self.smallerLevels)
            initCellGrid(lvl)
            InitFits(lvl)
            RectangleReachability(lvl)
            CircleReachability(lvl)
            ResetJumpStrength(lvl)
            CoopReachability(lvl)
            CellGridToBlockGrid(lvl)
            fit += [fitness(lvl,self)]
            del lvl
        fit = max(fit,key=getV)
        return fit
    
    def TestLevel(self,level):
        levels = []
        for s in self.spawns:
            lvl = Level(level,s[0],s[1],smaller = self.smallerLevels)
            initCellGrid(lvl)
            InitFits(lvl)
            RectangleReachability(lvl)
            CircleReachability(lvl)
            ResetJumpStrength(lvl)
            CoopReachability(lvl)
            CellGridToBlockGrid(lvl)
            fit = fitness(lvl,self)
            lvl.fit = fit
            levels += [lvl]
        return levels


class AreaPercentangeHeuristic:
    def __init__(self,recPer = 0,circlePer = 0,coopPer = 0,commonPer = 0,smaller = False):
        self.rectanglePercentage = recPer
        self.circlePercentage = circlePer
        self.coopPercentage = coopPer
        self.commonPercentage = commonPer
        self.smallerLevels = smaller
        
    def CalculateFitness(self, level):
        fit = []            
        lvl = Level(level,smaller = self.smallerLevels)
        initCellGrid(lvl)
        InitFits(lvl)
        RectangleReachability(lvl)
        CircleReachability(lvl)
        ResetJumpStrength(lvl)
        CoopReachability(lvl)
        CellGridToBlockGrid(lvl)
        fit = percentageFitness(lvl,self)
        del lvl
        return fit
    
    def TestLevel(self,level):
        lvl = Level(level,smaller = self.smallerLevels)
        initCellGrid(lvl)
        InitFits(lvl)
        RectangleReachability(lvl)
        CircleReachability(lvl)
        ResetJumpStrength(lvl)
        CoopReachability(lvl)
        CellGridToBlockGrid(lvl)
        fit = percentageFitness(lvl,self)
        lvl.fit = fit
        return lvl

class AreaPercentangeTwoHeuristic:
    def __init__(self,recPer = 0,circlePer = 0,coopPer = 0,commonPer = 0,smaller = False):
        self.rectanglePercentage = recPer
        self.circlePercentage = circlePer
        self.coopPercentage = coopPer
        self.commonPercentage = commonPer
        
    def CalculateFitness(self, level):
        lvl = Level(level,smaller = self.smallerLevels)
        initCellGrid(lvl)
        InitFits(lvl)
        RectangleReachability(lvl)
        CircleReachability(lvl)
        ResetJumpStrength(lvl)
        CoopReachability(lvl)
        CellGridToBlockGrid(lvl)
        fit = percentageFitnessTwo(lvl,self)
        del lvl
        return fit
    
    def TestLevel(self,level):
        lvl = Level(level,smaller = self.smallerLevels)
        initCellGrid(lvl)
        InitFits(lvl)
        RectangleReachability(lvl)
        CircleReachability(lvl)
        ResetJumpStrength(lvl)
        CoopReachability(lvl)
        CellGridToBlockGrid(lvl)
        fit = percentageFitnessTwo(lvl,self)
        lvl.fit = fit
             
        return lvl

def fitness(lvl, h):
    specs = h.specifications
    if(not len(specs) > 0):
        #print("No Specified Area")
        return 1
    
    grid = lvl.grid
    fullAreaPercent = 0
    minArea = 2
    for area in specs:
        areaPercent = 0
        areaPosX = (int) ((area.x - 40) / blockSize) + 2 
        areaPosY = (int) ((area.y - 40) / blockSize) + 2 
        areaWidth = (int) ((area.width - 40) / blockSize) + 2 
        areaHeight = (int) ((area.height - 40) / blockSize) + 2
        areaAmount = 0
        areaType = area.type
        for i in range(areaPosX, areaPosX + areaWidth):
            for j in range(areaPosY, areaPosY + areaHeight):
                if i >= xGridLen or j >= yGridLen or i < 0 or j < 0:
                    continue
                areaAmount += 1
                if areaType == AreaType.Common:
                    if grid[i][j] == BlockType.BothCanReach:
                        areaPercent += 1
                elif areaType == AreaType.Cooperative:
                    if grid[i][j] == BlockType.CooperativeCanReach:
                        areaPercent += 1
                    elif grid[i][j] == BlockType.CooperativeCanReachRectanglePlatform:
                        areaPercent += 1
                elif areaType == AreaType.CircleOnly:
                    if grid[i][j] == BlockType.CircleCanReach:
                        areaPercent += 1
                    elif grid[i][j] == BlockType.CircleCanReachRectanglePlatform:
                        areaPercent += 1
                elif areaType == AreaType.RectangleOnly:
                    if grid[i][j] == BlockType.RectangleCanReach:
                        areaPercent += 1
                    elif grid[i][j] == BlockType.RectangleCanReachCirclePlatform:
                        areaPercent += 1
        if areaAmount == 0:
            return (0,)
        areaPercent = areaPercent / areaAmount
        fullAreaPercent += areaPercent
        minArea = min(areaPercent, minArea)
    #return (fullAreaPercent / len(specs),)
    if minArea > 0:
        return (minArea,)
    return (0.0000001,)
    #return (fullAreaPercent / len(specs),)
    #return (minArea * 0.8 + fullAreaPercent * 0.2,)

# In this the sum of each percentage being 100% would mean the entire map is reachable which is impossible
# Takes the entire map into consideration
def percentageFitness(lvl, h):
    gridNum = (xGridLen-4) * (yGridLen-4)
    rectangleGridPer = 0
    circleGridPer = 0
    coopGridPer = 0
    commonGridPer = 0
    for x in range(0,xGridLen):
        for y in range(0,yGridLen):
            if lvl.grid[x][y] == BlockType.CooperativeCanReach or lvl.grid[x][y] == BlockType.CooperativeCanReachRectanglePlatform:
                coopGridPer += 1
            elif lvl.grid[x][y] == BlockType.RectangleCanReach or lvl.grid[x][y] == BlockType.RectangleCanReachCirclePlatform:
                rectangleGridPer += 1
            elif lvl.grid[x][y] == BlockType.CircleCanReach or lvl.grid[x][y] == BlockType.CircleCanReachRectanglePlatform:
                circleGridPer += 1
            elif lvl.grid[x][y] == BlockType.BothCanReach:
                commonGridPer += 1
    rectangleGridPer = rectangleGridPer / gridNum
    circleGridPer = circleGridPer / gridNum
    coopGridPer = coopGridPer / gridNum
    commonGridPer = commonGridPer / gridNum
    fit = 1 - abs(h.rectanglePercentage - rectangleGridPer) - abs(h.circlePercentage - circleGridPer) - abs(h.coopPercentage - coopGridPer) - abs(h.commonPercentage - commonGridPer)
    return (fit,)

# In this the sum of each percentange adds to 100%
# Only takes into consideration reachable areas
def percentageFitnessTwo(lvl, h):
    gridNum = 0
    rectangleGridPer = 0
    circleGridPer = 0
    coopGridPer = 0
    commonGridPer = 0
    for x in range(0,xGridLen):
        for y in range(0,yGridLen):
            if lvl.grid[x][y] == BlockType.CooperativeCanReach or lvl.grid[x][y] == BlockType.CooperativeCanReachRectanglePlatform:
                coopGridPer += 1
                gridNum += 1
            elif lvl.grid[x][y] == BlockType.RectangleCanReach or lvl.grid[x][y] == BlockType.RectangleCanReachCirclePlatform:
                rectangleGridPer += 1
                gridNum += 1
            elif lvl.grid[x][y] == BlockType.CircleCanReach or lvl.grid[x][y] == BlockType.CircleCanReachRectanglePlatform:
                circleGridPer += 1
                gridNum += 1
            elif lvl.grid[x][y] == BlockType.BothCanReach:
                commonGridPer += 1
                gridNum += 1
    if gridNum == 0:
        return (0,)
    rectangleGridPer = rectangleGridPer / gridNum
    circleGridPer = circleGridPer / gridNum
    coopGridPer = coopGridPer / gridNum
    commonGridPer = commonGridPer / gridNum
    fit = 1 - abs(h.rectanglePercentage - rectangleGridPer) - abs(h.circlePercentage - circleGridPer) - abs(h.coopPercentage - coopGridPer) - abs(h.commonPercentage - commonGridPer)
    return (fit,)


def initCellGrid(lvl):
    lvl.cellGrid = [[Cell() for i in range(yGridLen)] for i in range(xGridLen)]

    for i in range(0,xGridLen):
        for j in range(0,yGridLen):
            if(i  == 0 or i == xGridLen - 1 or i == 1 or i == xGridLen - 2):
                lvl.cellGrid[i][j].Platform = PlatformType.Common
            if(j  == 0 or j == yGridLen - 1 or j == 1 or j == yGridLen - 2):
                lvl.cellGrid[i][j].Platform = PlatformType.Common
    for plat in lvl.platforms:
        if lvl.smallerNums:
            platPosX = plat[0]
            platPosY = plat[1]
            platWidth = plat[2]
            platHeight = plat[3]
        else:
            platPosX = (int) ((plat[0] - 40) / blockSize) + 2
            platPosY = (int) ((plat[1] - 40) / blockSize) + 2
            platWidth = (int) ((plat[2] - 40) / blockSize) + 2
            platHeight = (int) ((plat[3] - 40) / blockSize) + 2
        if(platPosX > xGridLen or platPosY > yGridLen):
            print("Bad platform positioning (" ,platPosX , " , " , platPosY , ")")
        for i in range(platPosX,platPosX + platWidth):
            for j in range(platPosY,platPosY + platHeight):
                if(i < xGridLen and j < yGridLen):
                    lvl.cellGrid[i][j].Platform = PlatformType.Common


def InitFits(lvl):
    for x in range(2,xGridLen-2):
        for y in range(2,yGridLen-2):
            stillFitRectangle = True
            stillFitCircle = True
            
            #Check in 3x3 around cell to see it rectangle fits in that particular cell
            i = -1
            while(i <= 1 and stillFitRectangle):
                j = -1
                while(j <= 1 and stillFitRectangle):
                    if lvl.cellGrid[x + i][y + j].Platform != PlatformType.NotPlatform:
                        stillFitRectangle = False
                        stillFitCircle = False
                    j = j + 1
                i = i + 1

            #Check in 5x5 around cell to see it circle fits in that particular cell
            i = -2
            while(i <= 2 and stillFitCircle):
                j = -2
                while(j <= 2 and stillFitCircle):
                    if lvl.cellGrid[x+i][y+j].Platform != PlatformType.NotPlatform:
                        stillFitCircle = False
                    j = j + 1
                i = i + 1

            lvl.cellGrid[x][y].fitsRectangle = stillFitRectangle
            lvl.cellGrid[x][y].fitsCircle = stillFitCircle


def ResetJumpStrength(lvl):
    for x in range(0,xGridLen):
        for y in range(0,yGridLen):
            lvl.cellGrid[x][y].jumpStrength = -1


def RectangleReachability(lvl):
    if lvl.smallerNums:
        x = lvl.rectSpawn[0]
        y = lvl.rectSpawn[1]
    else:
        x = (int) ((lvl.rectSpawn[0] - 40) / blockSize) + 3
        y = (int) ((lvl.rectSpawn[1] - 40) / blockSize) + 3
    lst = []
    lst += [((x, y), 0)]
    while len(lst) > 0:
        startPos = lst[0]
        
        x = startPos[0][0]
        y = startPos[0][1]
        direction = startPos[1]
        lst = lst[1:]
        if x >= xGridLen or y >= yGridLen or x < 0 or y < 0:
            continue
        #if already reached once, check for which side it is reaching from
        if(lvl.cellGrid[x][y].reachesRectangle):
            if direction == -1: #left
                if not lvl.cellGrid[x][y].traversedRectangleLeft:
                    lvl.cellGrid[x][y].traversedRectangleLeft = True
                else:
                    continue
            elif  direction == 1: #right
                if not lvl.cellGrid[x][y].traversedRectangleRight:
                    lvl.cellGrid[x][y].traversedRectangleRight = True
                else:
                    continue
            else:
                continue
        if lvl.cellGrid[x][y].fitsRectangle:
            lvl.cellGrid[x][y].reachesRectangle = True
            if direction == -1:
                lvl.cellGrid[x][y].traversedRectangleLeft = True
            elif  direction == 1:
                lvl.cellGrid[x][y].traversedRectangleRight = True
            #Check if Falling
            if lvl.cellGrid[x][y+1].fitsRectangle:
                lst += [((x, y+1), direction)]
                if direction == -1:
                    lst += [((x + direction, y+1), direction)]
                    lvl.cellGrid[x][y].traversedRectangleLeft = True
                elif  direction == 1:
                    lst += [((x + direction, y+1), direction)]
                    lvl.cellGrid[x][y].traversedRectangleRight = True
                continue

            #Check for going left
            if lvl.cellGrid[x - 1][ y].fitsRectangle:
                lst += [((x-1, y), -1)]
                #check extending
                for i in range(0,rectangleMaxLen): 
                    lst += [((x-1, y-i), 0)]
            else:
                #check for climbing obstacle left
                for i in range(0,3):
                    lst += [((x-1, y-i), -1)]
            #Check for going right
            if lvl.cellGrid[x + 1][ y].fitsRectangle:
                lst += [((x+1, y), +1)]
                #check extending
                for i in range(0,rectangleMaxLen): 
                    lst += [((x+1, y-i), 0)]
            else:
                #check for climbing obstacle right
                for i in range(0,3):
                    lst += [((x+1, y-i), 1)]


def CircleReachability(lvl):
    if lvl.smallerNums:
        x = lvl.circleSpawn[0]
        y = lvl.circleSpawn[1]
    else:
        x = (int) ((lvl.circleSpawn[0] - 40) / blockSize) + 4
        y = (int) ((lvl.circleSpawn[1] - 40) / blockSize) + 4
    cellsChecked = 0
    freefalling = 0
    lst = []
    lst += [((x, y), 0)]
    while len(lst) > 0 and cellsChecked < 10000:
        cellsChecked += 1
        startPos = lst[0]
        x = startPos[0][0]
        y = startPos[0][1]
        direction = startPos[1]
        lst = lst[1:]
        if x >= xGridLen or y >= yGridLen or x < 0 or y < 0:
            continue
        #already jumped from this one
        if lvl.cellGrid[x][y].jumpStrength == 24:
            continue
        if lvl.cellGrid[x][y].fitsCircle:
            lvl.cellGrid[x][ y].reachesCircle = True
            #check if on ground
            if not lvl.cellGrid[x][ y + 1].fitsCircle:
                lvl.cellGrid[x][ y].jumpStrength = 24

                if lvl.cellGrid[x - 1][ y].jumpStrength < 24:
                    lst += [((x - 1, y), -1)]
                    for i in range(0,3):
                        lst += [((x-1, y-i), -1)]
                if lvl.cellGrid[x + 1][ y].jumpStrength < 24:
                    lst += [((x + 1, y), 1)]
                    for i in range(0,3):
                        lst += [((x + 1, y-i), 1)]
                
                for i in range(-1,2):
                    if lvl.cellGrid[x + i][ y - 1].jumpStrength < 23:
                        lvl.cellGrid[x + i][ y - 1].jumpStrength = 23
                        lst += [((x + i, y-1), i)]
            else: # mid air
                #if mid jump
                if lvl.cellGrid[x][ y].jumpStrength > 0 and lvl.cellGrid[x][ y].jumpStrength < 24:
                    for j in range(-1,2):
                        if lvl.cellGrid[x + j][ y - 1].jumpStrength < lvl.cellGrid[x][ y].jumpStrength - 1:
                            lvl.cellGrid[x + j][ y - 1].jumpStrength = lvl.cellGrid[x][ y].jumpStrength - 1
                            lst += [((x + j, y - 1), j)]
                    if (lvl.cellGrid[x][ y].jumpStrength - 1 == 0  or (not lvl.cellGrid[x][ y-1].fitsCircle))and lvl.cellGrid[x + direction][ y].jumpStrength < 1:
                        lst += [((x + direction, y), direction)]
                else: #freefalling
                    freefalling += 1
                    lst += [((x , y + 1), 0)]
                    if direction != 0:
                        if lvl.cellGrid[x + direction][ y + 1].fitsCircle:
                            lst += [((x + direction, y + 1), direction)]     
                        else:
                            lst += [((x - direction, y + 1), -direction)]
    #print("Circle ", str(len(lst)) , " | " , str(cellsChecked) , " | " , str(freefalling)," \n")


def CoopReachability(lvl):
    if lvl.smallerNums:
        x = lvl.circleSpawn[0]
        y = lvl.circleSpawn[1]
    else:
        x = (int) ((lvl.circleSpawn[0] - 40) / blockSize) + 4
        y = (int) ((lvl.circleSpawn[1] - 40) / blockSize) + 4
    cellsChecked = 0
    freefalling = 0
    lst = []
    lst += [((x, y), 0)]
    while len(lst) > 0 and cellsChecked < 10000 :
        cellsChecked += 1
        startPos = lst[0]
        x = startPos[0][0]
        y = startPos[0][1]
        direction = startPos[1]
        lst = lst[1:]
        if x >= xGridLen or y >= yGridLen or x < 0 or y < 0:
            continue
        #already jumped from this one
        if lvl.cellGrid[x][y].jumpStrength == 30 or  lvl.cellGrid[x][y].notCoopJump:
            continue
        if lvl.cellGrid[x][y].fitsCircle:
            if not lvl.cellGrid[x][ y].reachesCircle:
                lvl.cellGrid[x][ y].reachesCoop = True
            
            #check if on ground
            if not lvl.cellGrid[x][ y + 1].fitsCircle:
                #Check if can do coop jump
                if lvl.cellGrid[x][y].reachesRectangle:
                    lvl.cellGrid[x][ y].jumpStrength = 30
                    if lvl.cellGrid[x - 1][ y].jumpStrength < 30:
                        lst += [((x - 1, y), -1)]
                        for i in range(0,3): #can go up small things
                            lst += [((x-1, y-i), -2)]
                    if lvl.cellGrid[x + 1][ y].jumpStrength < 30:
                        lst += [((x + 1, y), 1)]
                        for i in range(0,3): #can go up small things
                            lst += [((x + 1, y-i), 2)]
                    
                    for i in range(-1,2): #actual jump
                        if lvl.cellGrid[x + i][ y - 1].jumpStrength < 29:
                            lvl.cellGrid[x + i][ y - 1].jumpStrength = 29
                            lst += [((x + i, y-1), i)]
                else: #no coop jump
                    lvl.cellGrid[x][ y].jumpStrength = 24
                    lvl.cellGrid[x][y].notCoopJump = True
                    if lvl.cellGrid[x - 1][ y].jumpStrength < 24:
                        lst += [((x - 1, y), -1)]
                        for i in range(0,3):#can go up small things
                            lst += [((x-1, y-i), -1)]
                    if lvl.cellGrid[x + 1][ y].jumpStrength < 24:
                        lst += [((x + 1, y), 1)]
                        for i in range(0,3):#can go up small things
                            lst += [((x + 1, y-i), 1)]
                    
                    for i in range(-1,2):#actual jump
                        if lvl.cellGrid[x + i][ y - 1].jumpStrength < 23:
                            lvl.cellGrid[x + i][ y - 1].jumpStrength = 23
                            lst += [((x + i, y-1), i)]
            else: # mid air
                #if mid jump
                if lvl.cellGrid[x][ y].jumpStrength > 0 and lvl.cellGrid[x][ y].jumpStrength < 30:
                    for j in range(-1,2):
                        if lvl.cellGrid[x + j][ y - 1].jumpStrength < lvl.cellGrid[x][ y].jumpStrength - 1:
                            lvl.cellGrid[x + j][ y - 1].jumpStrength = lvl.cellGrid[x][ y].jumpStrength - 1
                            lst += [((x + j, y - 1), j)]
                    if (lvl.cellGrid[x][ y].jumpStrength - 1 == 0  or (not lvl.cellGrid[x][ y-1].fitsCircle))and lvl.cellGrid[x + direction][ y].jumpStrength < 1:
                        lst += [((x + direction, y), direction)]
                else: #freefalling
                    freefalling += 1
                    lst += [((x , y + 1), 0)]
                    if direction != 0:
                        if lvl.cellGrid[x + direction][ y + 1].fitsCircle:
                            lst += [((x + direction, y + 1), direction)]     
                        else:
                            lst += [((x - direction, y + 1), -direction)]
    #print("Coop ", str(len(lst)) , " | " , str(cellsChecked) , " | " , str(freefalling)," \n")


def CellGridToBlockGrid(lvl):
    lvl.grid = [[BlockType.Unreachable for i in range(yGridLen)] for i in range(xGridLen)]
    for x in range(0,xGridLen):
        for y in range(0,yGridLen):
            if lvl.cellGrid[x][y].Platform == PlatformType.Common:
                lvl.grid[x][ y] = BlockType.Platform
                continue
            if lvl.cellGrid[x][ y].Platform != PlatformType.NotPlatform:
                lvl.grid[x][ y] = BlockType.Platform
                continue
            if lvl.cellGrid[x][ y].reachesCoop and not lvl.cellGrid[x][ y].reachesRectangle:
                lvl.grid[x][ y] = BlockType.CooperativeCanReach
                continue
            if lvl.cellGrid[x][ y].reachesCircle:
                lvl.grid[x][ y] = BlockType.CircleCanReach
                if lvl.cellGrid[x][ y].reachesRectangle:
                    lvl.grid[x][ y] = BlockType.BothCanReach
                continue
            if lvl.cellGrid[x][ y].reachesRectangle:
                lvl.grid[x][ y] = BlockType.RectangleCanReach
                if lvl.cellGrid[x][y].reachesCircle or lvl.cellGrid[x][ y].reachesCoop :
                    lvl.grid[x][ y] = BlockType.BothCanReach
                continue
            lvl.grid[x][ y] = BlockType.Unreachable

blankLevel = Level(9*[0,0,0,0,0])
initCellGrid(blankLevel)
CellGridToBlockGrid(blankLevel)