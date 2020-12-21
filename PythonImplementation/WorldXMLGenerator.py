import evaluateFuncs as ef
import xml.etree.ElementTree as ET
import xml.dom.minidom as MD
 
 
 
 
def prettify(elem):
    rough_string = ET.tostring(elem, 'utf-8')
    reparsed = MD.parseString(rough_string)
    return reparsed.toprettyxml(indent="\t")

def WriteWorld(population,name="test.xml"):
    world = ET.Element('Levels')
    num = 1
    for individual in population:
        individual.increaseSize()
        AddLevel(individual,world,num)
        num+=1
    # create a new XML file with the results
    #print(mydata)
    mData = prettify(world)
    myfile = open(name, "w")
    myfile.write(str(mData)) #to remove b' at beginning and ' at the end
    myfile.close()



def AddLevel(individual,world,num):
    level = ET.SubElement(world,'Level'+ str(num))

    rectangleSpawn = ET.SubElement(level,'SquareStartingPosition')
    rectangleSpawn.set('X',str(individual.rectSpawn[0]))
    rectangleSpawn.set('Y',str(individual.rectSpawn[1]))

    circleSpawn = ET.SubElement(level,'BallStartingPosition')
    circleSpawn.set('X',str(individual.circleSpawn[0]))
    circleSpawn.set('Y',str(individual.circleSpawn[1]))

    collectibles = ET.SubElement(level,'Collectibles')
    for col in individual.collectibles:
        collectible = ET.SubElement(collectibles,'Collectible')
        collectible.set('X',str(col[0]))
        collectible.set('Y',str(col[1]))

    platforms = ET.SubElement(level,'BlackObstacles')
    for plat in individual.platforms:
        platform = ET.SubElement(platforms,'Obstacle')
        platform.set('X',str(plat[0]))
        platform.set('Y',str(plat[1]))
        platform.set('width',str(plat[2]))
        platform.set('height',str(plat[3]))
        platform.set('centered',"False")
    
    #empty elements
    ET.SubElement(level,'Description')
    ET.SubElement(level,'Tips')
    ET.SubElement(level,'GreenObstacles')
    ET.SubElement(level,'YellowObstacles')
    ET.SubElement(level,'GreenElevators')
    ET.SubElement(level,'OrangeElevators')
    return level
