from enum import Enum

class Level:
    def __init__(self, attrList):
        if(len(attrList) < 45):
            print("Incorrect attr Len")
        self.rectSpawn = (attrList[1],attrList[2])
        self.circleSpawn = (attrList[3],attrList[4])
        self.platforms = []
        for i in range(5,45,5):
            if(attrList[i] % 2 == 1):
                posx = attrList[i+1]
                posy = (int) (attrList[i+2] * 720 / 1280)
                #posy = attrList[i+2]
                width = attrList[i+3]
                height = (int) (attrList[i+4] * 720 / 1240)
                #height = attrList[i+4]
                self.platforms += [(posx,posy,width,height)]
        self.cellGrid = []
        self.grid = []

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
    def __init__(self, specs):
        self.specifications = specs #tuple or matrix of SpecialAreas


    def CalculateFitness(self, level):
        lvl = Level(level)
        initCellGrid(lvl, self)
        InitFits(self)
        RectangleReachability(lvl,self)
        CircleReachability(lvl,self)
        ResetJumpStrength(self)
        CoopReachability(lvl,self)
        CellGridToBlockGrid(self)
        fit = fitness(lvl, self)
        return fit

def fitness(lvl, h):
    specs = h.specifications
    if(not len(specs) > 0):
        print("No Specified Area")
        return 1
    
    grid = h.grid
    fullAreaPercent = 0
    minArea = 2
    for area in specs:
        areaPercent = 0
        areaPosX = (int) ((area.x - 40) / blockSize) + 2 
        areaPosY = (int) ((area.y - 40) / blockSize) + 2 
        areaWidth = (int) ((area.width - 40) / blockSize) + 2 
        areaHeight = (int) ((area.height - 40) / blockSize) + 2 
        areaType = area.type
        for i in range(areaPosX, areaPosX + areaWidth):
            for j in range(areaPosY, areaPosY + areaHeight):
                if i > xGridLen or j > yGridLen or i < 0 or j < 0:
                    continue
                #Common
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
        areaPercent = areaPercent / (areaWidth * areaHeight)
        fullAreaPercent += areaPercent
        minArea = min(areaPercent, minArea)
    return (fullAreaPercent / len(specs),)
    if minArea > 0:
        return (minArea,)
    return (0.0000001,)
    #return (fullAreaPercent / len(specs),)
    #return (minArea * 0.8 + fullAreaPercent * 0.2,)


def initCellGrid(lvl, h):
    h.cellGrid = [[Cell() for i in range(yGridLen)] for i in range(xGridLen)]

    for i in range(0,xGridLen):
        for j in range(0,yGridLen):
            if(i  == 0 or i == xGridLen - 1 or i == 1 or i == xGridLen - 2):
                h.cellGrid[i][j].platType = PlatformType.Common
            if(j  == 0 or j == yGridLen - 1 or j == 1 or j == yGridLen - 2):
                h.cellGrid[i][j].platType = PlatformType.Common
    for plat in lvl.platforms:
        platPosX = (int) ((plat[0] - 40) / blockSize) + 2
        platPosY = (int) ((plat[1] - 40) / blockSize) + 2
        platWidth = (int) ((plat[2] - 40) / blockSize) + 2
        platHeight = (int) ((plat[3] - 40) / blockSize) + 2
        
        if(platPosX > xGridLen or platPosY > yGridLen):
            print("Bad platform positioning (" +platPosX + " , " + platPosY + ")")
        for i in range(platPosX,platPosX + platWidth):
            for j in range(platPosY,platPosY + platHeight):
                if(i < xGridLen and j < yGridLen):
                    h.cellGrid[i][j].platType = PlatformType.Common


def InitFits(h):
    for x in range(2,xGridLen-2):
        for y in range(2,yGridLen-2):
            stillFitRectangle = True
            stillFitCircle = True
            
            #Check in 3x3 around cell to see it rectangle fits in that particular cell
            i = -1
            while(i <= 1 and stillFitRectangle):
                j = -1
                while(j <= 1 and stillFitRectangle):
                    if h.cellGrid[x + i][y + j].Platform != PlatformType.NotPlatform:
                        stillFitRectangle = False
                        stillFitCircle = False
                    j = j + 1
                i = i + 1

            #Check in 5x5 around cell to see it circle fits in that particular cell
            i = -2
            while(i <= 2 and stillFitCircle):
                j = -2
                while(j <= 2 and stillFitCircle):
                    if h.cellGrid[x+i][y+j].Platform != PlatformType.NotPlatform:
                        stillFitCircle = False
                    j = j + 1
                i = i + 1

            h.cellGrid[x][y].fitsRectangle = stillFitRectangle
            h.cellGrid[x][y].fitsCircle = stillFitCircle


def ResetJumpStrength(h):
    for x in range(0,xGridLen):
        for y in range(0,yGridLen):
            h.cellGrid[x][y].jumpStrength = -1


def RectangleReachability(lvl,h):
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
        if(h.cellGrid[x][y].reachesRectangle):
            if direction == -1: #left
                if not h.cellGrid[x][y].traversedRectangleLeft:
                    h.cellGrid[x][y].traversedRectangleLeft = True
                else:
                    continue
            elif  direction == 1: #right
                if not h.cellGrid[x][y].traversedRectangleRight:
                    h.cellGrid[x][y].traversedRectangleRight = True
                else:
                    continue
            else:
                continue
        if h.cellGrid[x][y].fitsRectangle:
            h.cellGrid[x][y].reachesRectangle = True
            if direction == -1:
                h.cellGrid[x][y].traversedRectangleLeft = True
            elif  direction == 1:
                h.cellGrid[x][y].traversedRectangleRight = True
            #Check if Falling
            if h.cellGrid[x][y+1].fitsRectangle:
                lst += [((x, y+1), direction)]
                if direction == -1:
                    lst += [((x + direction, y+1), direction)]
                    h.cellGrid[x][y].traversedRectangleLeft = True
                elif  direction == 1:
                    lst += [((x + direction, y+1), direction)]
                    h.cellGrid[x][y].traversedRectangleRight = True
                continue

            #Check for going left
            if h.cellGrid[x - 1][ y].fitsRectangle:
                lst += [((x-1, y), -1)]
                #check extending
                for i in range(0,rectangleMaxLen): 
                    lst += [((x-1, y-i), 0)]
            else:
                #check for climbing obstacle left
                for i in range(0,3):
                    lst += [((x-1, y-i), -1)]
            #Check for going right
            if h.cellGrid[x + 1][ y].fitsRectangle:
                lst += [((x+1, y), +1)]
                #check extending
                for i in range(0,rectangleMaxLen): 
                    lst += [((x+1, y-i), 0)]
            else:
                #check for climbing obstacle right
                for i in range(0,3):
                    lst += [((x+1, y-i), 1)]


def CircleReachability(lvl, h):
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
        if h.cellGrid[x][y].jumpStrength == 24:
            continue
        if h.cellGrid[x][y].fitsCircle:
            h.cellGrid[x][ y].reachesCircle = True
            #check if on ground
            if not h.cellGrid[x][ y + 1].fitsCircle:
                h.cellGrid[x][ y].jumpStrength = 24

                if h.cellGrid[x - 1][ y].jumpStrength < 24:
                    lst += [((x - 1, y), -1)]
                    for i in range(0,3):
                        lst += [((x-1, y-i), -1)]
                if h.cellGrid[x + 1][ y].jumpStrength < 24:
                    lst += [((x + 1, y), 1)]
                    for i in range(0,3):
                        lst += [((x + 1, y-i), 1)]
                
                for i in range(-1,2):
                    if h.cellGrid[x + i][ y - 1].jumpStrength < 23:
                        h.cellGrid[x + i][ y - 1].jumpStrength = 23
                        lst += [((x + i, y-1), i)]
            else: # mid air
                #if mid jump
                if h.cellGrid[x][ y].jumpStrength > 0 and h.cellGrid[x][ y].jumpStrength < 24:
                    for j in range(-1,2):
                        if h.cellGrid[x + j][ y - 1].jumpStrength < h.cellGrid[x][ y].jumpStrength - 1:
                            h.cellGrid[x + j][ y - 1].jumpStrength = h.cellGrid[x][ y].jumpStrength - 1
                            lst += [((x + j, y - 1), j)]
                    if (h.cellGrid[x][ y].jumpStrength - 1 == 0  or (not h.cellGrid[x][ y-1].fitsCircle))and h.cellGrid[x + direction][ y].jumpStrength < 1:
                        lst += [((x + direction, y), direction)]
                else: #freefalling
                    freefalling += 1
                    lst += [((x , y + 1), 0)]
                    if direction != 0:
                        if h.cellGrid[x + direction][ y + 1].fitsCircle:
                            lst += [((x + direction, y + 1), direction)]     
                        else:
                            lst += [((x - direction, y + 1), -direction)]
    #print( len(lst) + " | " + cellsChecked + " | " + freefalling)


def CoopReachability(lvl, h):
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
        if h.cellGrid[x][y].jumpStrength == 30:
            continue
        if h.cellGrid[x][y].fitsCircle:
            if not h.cellGrid[x][ y].reachesCircle:
                h.cellGrid[x][ y].reachesCoop = True
            
            #check if on ground
            if not h.cellGrid[x][ y + 1].fitsCircle:
                #Check if can doo coop jump
                if h.cellGrid[x][y].reachesRectangle:
                    h.cellGrid[x][ y].jumpStrength = 30
                    if h.cellGrid[x - 1][ y].jumpStrength < 30:
                        lst += [((x - 1, y), -1)]
                        for i in range(0,3):
                            lst += [((x-1, y-i), -1)]
                    if h.cellGrid[x + 1][ y].jumpStrength < 30:
                        lst += [((x + 1, y), 1)]
                        for i in range(0,3):
                            lst += [((x + 1, y-i), 1)]
                    
                    for i in range(-1,2):
                        if h.cellGrid[x + i][ y - 1].jumpStrength < 29:
                            h.cellGrid[x + i][ y - 1].jumpStrength = 29
                            lst += [((x + i, y-1), i)]
                else: #no coop jump
                    h.cellGrid[x][ y].jumpStrength = 24
                    if h.cellGrid[x - 1][ y].jumpStrength < 24:
                        lst += [((x - 1, y), -1)]
                        for i in range(0,3):
                            lst += [((x-1, y-i), -1)]
                    if h.cellGrid[x + 1][ y].jumpStrength < 24:
                        lst += [((x + 1, y), 1)]
                        for i in range(0,3):
                            lst += [((x + 1, y-i), 1)]
                    
                    for i in range(-1,2):
                        if h.cellGrid[x + i][ y - 1].jumpStrength < 23:
                            h.cellGrid[x + i][ y - 1].jumpStrength = 23
                            lst += [((x + i, y-1), i)]
            else: # mid air
                #if mid jump
                if h.cellGrid[x][ y].jumpStrength > 0 and h.cellGrid[x][ y].jumpStrength < 30:
                    for j in range(-1,2):
                        if h.cellGrid[x + j][ y - 1].jumpStrength < h.cellGrid[x][ y].jumpStrength - 1:
                            h.cellGrid[x + j][ y - 1].jumpStrength = h.cellGrid[x][ y].jumpStrength - 1
                            lst += [((x + j, y - 1), j)]
                    if (h.cellGrid[x][ y].jumpStrength - 1 == 0  or (not h.cellGrid[x][ y-1].fitsCircle))and h.cellGrid[x + direction][ y].jumpStrength < 1:
                        lst += [((x + direction, y), direction)]
                else: #freefalling
                    freefalling += 1
                    lst += [((x , y + 1), 0)]
                    if direction != 0:
                        if h.cellGrid[x + direction][ y + 1].fitsCircle:
                            lst += [((x + direction, y + 1), direction)]     
                        else:
                            lst += [((x - direction, y + 1), -direction)]
    #print( len(lst) + " | " + cellsChecked + " | " + freefalling)


def CellGridToBlockGrid(h):
    h.grid = [[BlockType.Unreachable for i in range(yGridLen)] for i in range(xGridLen)]
    for x in range(0,xGridLen):
        for y in range(0,yGridLen):
            if h.cellGrid[x][ y].Platform == PlatformType.Common:
                h.grid[x][ y] = BlockType.Platform
                continue
            if h.cellGrid[x][ y].Platform != PlatformType.NotPlatform:
                h.grid[x][ y] = BlockType.Platform
                continue
            if h.cellGrid[x][ y].reachesCoop:
                h.grid[x][ y] = BlockType.CooperativeCanReach
                continue
            if h.cellGrid[x][ y].reachesCircle:
                h.grid[x][ y] = BlockType.CircleCanReach
                if h.cellGrid[x][ y].reachesRectangle:
                    h.grid[x][ y] = BlockType.BothCanReach
                continue
            if h.cellGrid[x][ y].reachesRectangle:
                h.grid[x][ y] = BlockType.RectangleCanReach
                if h.cellGrid[x][y].reachesCircle:
                    h.grid[x][ y] = BlockType.BothCanReach
                continue
            h.grid[x][ y] = BlockType.Unreachable

