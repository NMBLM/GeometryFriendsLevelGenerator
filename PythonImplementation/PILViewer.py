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
        return (255,0,0)
    if blockType == ef.BlockType.CircleCanReachRectanglePlatform:
        return (255,0,0)
    if blockType == ef.BlockType.CooperativeCanReachRectanglePlatform:
        return (255,0,0)
    if blockType == ef.BlockType.CirclePlatform:
        return (255,255,0)
    if blockType == ef.BlockType.RectanglePlatform:
        return (0,255,0)   

def getColorSpec(specType):
    if specType == ef.AreaType.Common:
        print("Common")
        return (125,125,125)
    if specType == ef.AreaType.Cooperative:
        print("Cooperative")
        return (0,0,255)
    if specType == ef.AreaType.CircleOnly:
        print("CircleOnly")
        return (255,255,0)
    if specType == ef.AreaType.RectangleOnly:
        print("RectangleOnly")
        return (0,255,0)



def drawLevel (level,name):
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
    
        draw.rectangle([(level.rectSpawn[0]-16 ,level.rectSpawn[1] - 16), (level.rectSpawn[0]+16 ,level.rectSpawn[1] + 16)],fill = squareColor,outline= 0 )
        draw.arc([level.circleSpawn, (level.circleSpawn[0]+36 ,level.circleSpawn[1] + 36)],start = 0, end = 360,fill = circleColor ,width= 3 )
        
        im.save(name, "PNG")


def drawSpecs (h,name):
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
            print(area.x,area.y,area.width,area.height," -> ",areaPosX,areaPosY,areaWidth,areaHeight)
            xy = (squareSide*areaPosX , squareSide*areaPosY)
            wl = (squareSide*(areaPosX + areaWidth) , squareSide*(areaPosY+areaHeight))
            draw.rectangle([xy, wl],fill = color)

        #draw.rectangle([(level.rectSpawn[0]-16 ,level.rectSpawn[1] - 16), (level.rectSpawn[0]+16 ,level.rectSpawn[1] + 16)],fill = squareColor,outline= 0 )
        #draw.arc([level.circleSpawn, (level.circleSpawn[0]+36 ,level.circleSpawn[1] + 36)],start = 0, end = 360,fill = circleColor ,width= 3 )
        im.save(name, "PNG")