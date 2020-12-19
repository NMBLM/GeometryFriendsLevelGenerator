from PIL import Image, ImageDraw
import evaluateFuncs as ef

squareColor = (60,180,60)
circleColor = (216,216,40)

def getColor (blockType):
    if blockType == ef.BlockType.Unreachable:
        return (255,255,255)
    if blockType == ef.BlockType.Platform:
        return (0,0,0)
    if blockType == ef.BlockType.RectangleCanReach:
        return (0,255,0)
    if blockType == ef.BlockType.CircleCanReach:
        return (255,255,0)        
    if blockType == ef.BlockType.BothCanReach:
        return (125,125,125)
    if blockType == ef.BlockType.CooperativeCanReach:
        return (0,0,255)
    if blockType == ef.BlockType.RectangleCanReachCirclePlatform:
        return (125,0,0)
    if blockType == ef.BlockType.CircleCanReachRectanglePlatform:
        return (125,125,0)
    if blockType == ef.BlockType.CooperativeCanReachRectanglePlatform:
        return (125,0,125)
    if blockType == ef.BlockType.CirclePlatform:
        return (200,200,0)
    if blockType == ef.BlockType.RectanglePlatform:
        return (0,200,0)   

def getColorSpec(specType):
    if specType == ef.AreaType.Common:
        #print("Common")
        return (125,125,125)
    if specType == ef.AreaType.Cooperative:
        #print("Cooperative")
        return (0,0,255)
    if specType == ef.AreaType.CircleOnly:
        #print("CircleOnly")
        return (255,255,0)
    if specType == ef.AreaType.RectangleOnly:
        #print("RectangleOnly")
        return (0,255,0)

def getColorPer(specType):
    if specType == 3:
        #print("Common")
        return (125,125,125)
    if specType == 2:
        #print("Cooperative")
        return (0,0,255)
    if specType == 1:
        #print("CircleOnly")
        return (255,255,0)
    if specType == 0:
        #print("RectangleOnly")
        return (0,255,0)


def drawLevel (level,name,collectibles = False):
    xGridLen = 79
    yGridLen = 49
    squareSide = 16
    with Image.new("RGB",(xGridLen * squareSide ,yGridLen * squareSide),(254,254,254)) as im:

        draw = ImageDraw.Draw(im)
        for i in range(79):
            for j in range(49):
                color = getColor(level.grid[i][j])
                xy = (squareSide*i , squareSide*j)
                wl = (squareSide*(i+1) , squareSide*(j+1))
                draw.rectangle([xy, wl],fill = color)
        if level.smallerNums:
            recS = (level.rectSpawn[0] * squareSide - squareSide, level.rectSpawn[1] * squareSide - squareSide)
            recST = (level.rectSpawn[0] * squareSide + squareSide, level.rectSpawn[1] * squareSide + squareSide)
            cirS = (level.circleSpawn[0] * squareSide, level.circleSpawn[1] * squareSide)
            cirsT = (level.circleSpawn[0] * squareSide + 2 * squareSide, level.circleSpawn[1] * squareSide + 2*squareSide)
        else:
            recS = (level.rectSpawn[0] - squareSide, level.rectSpawn[1] - squareSide)
            recST = (level.rectSpawn[0] + squareSide, level.rectSpawn[1] + squareSide)
            cirS = level.circleSpawn 
            cirsT = (level.circleSpawn[0] + 2 * squareSide, level.circleSpawn[1] + 2 * squareSide)
        draw.rectangle([recS,recST] ,fill = squareColor,outline= 0 )
        draw.arc([cirS, cirsT],start = 0, end = 360,fill = circleColor ,width= 3 )
        
        if collectibles:
            for col in level.collectibles:
                colS = (col[0] * squareSide - squareSide, col[1] * squareSide - squareSide)
                colST= (col[0] * squareSide + squareSide, col[1] * squareSide + squareSide)
                draw.rectangle([colS,colST], fill=(128,0,128), outline=0)
        im.save(name, "PNG")


def drawSpecs (h,name,resize = False):
    xGridLen = 79
    yGridLen = 49
    squareSide = 16
    level = ef.blankLevel
    with Image.new("RGB",(xGridLen * squareSide ,yGridLen * squareSide),(254,254,254)) as im:

        draw = ImageDraw.Draw(im)
        for i in range(79):
            for j in range(49):
                color = getColor(level.grid[i][j])
                xy = (squareSide*i , squareSide*j)
                wl = (squareSide*(i+1) , squareSide*(j+1))
                draw.rectangle([xy, wl],fill = color)
    
        for area in h.specifications:
            areaPosX = (int) ((area.x - 40) / ef.blockSize) + 2 
            areaPosY = (int) ((area.y - 40) / ef.blockSize) + 2 
            areaWidth = (int) ((area.width - 40) / ef.blockSize) + 2 
            areaHeight = (int) ((area.height - 40) / ef.blockSize) + 2
            color = getColorSpec(area.type)
            xy = (squareSide*areaPosX , squareSide*areaPosY)
            wl = (squareSide*(areaPosX + areaWidth) , squareSide*(areaPosY+areaHeight))
            draw.rectangle([xy, wl],fill = color)

        #draw.rectangle([(level.rectSpawn[0]-16 ,level.rectSpawn[1] - 16), (level.rectSpawn[0]+16 ,level.rectSpawn[1] + 16)],fill = squareColor,outline= 0 )
        #draw.arc([level.circleSpawn, (level.circleSpawn[0]+36 ,level.circleSpawn[1] + 36)],start = 0, end = 360,fill = circleColor ,width= 3 )
        if resize:
            im.save(name + ".png", "PNG")
            im = Image.open(name + ".png")
            im.thumbnail((1120,630))
            im.save(name + "Thumbnail.png", "PNG")
        else:
            im.save(name, "PNG")

def drawCoveragePercentage(name, recPer = 0,circlePer = 0,coopPer = 0,commonPer = 0,resize = False):
    xGridLen = 79
    yGridLen = 49
    squareSide = 16
    level = ef.blankLevel
    totalBlockNumber = 79*49
    recBlockNumber = int(totalBlockNumber * recPer)
    circleBlockNumber = int(totalBlockNumber * circlePer)
    cooperativeBlockNumber = int(totalBlockNumber * coopPer)
    commonBlockNumber = int(totalBlockNumber * commonPer)
    x = 0
    y = 0
    blockMax = [recBlockNumber,circleBlockNumber,cooperativeBlockNumber,commonBlockNumber]
    with Image.new("RGB",(xGridLen * squareSide ,yGridLen * squareSide),(254,254,254)) as im:
        draw = ImageDraw.Draw(im)
        for i in range(len(blockMax)):
            if x == xGridLen:
                break
            currentBlockNumber = 0
            while(currentBlockNumber <blockMax[i]):
                color = getColorPer(i)
                currentBlockNumber += 1
                xy = (squareSide*x , squareSide*y)
                wl = (squareSide*(x+1) , squareSide*(y+1))
                draw.rectangle([xy, wl],fill = color)
                y+=1
                if y == yGridLen:
                    x+=1
                    y = 0
                    if x == xGridLen:
                        break
        if resize:
            im.save(name + ".png", "PNG")
            im = Image.open(name + ".png")
            im.thumbnail((1120,630))
            im.save(name + "Thumbnail.png", "PNG")
        else:
            im.save(name, "PNG")



