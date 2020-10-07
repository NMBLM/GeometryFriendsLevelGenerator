import os

import PILViewer as viewer

class InstrumentationManager:

    def __init__(self,on = True):
        self.on = on
        self.directory = os.getcwd()
        self.genN = 0
        f = open('GenData\RunNumber.txt','r')
        self.runNumber = int(f.readline())
        f.close()
        f = open('GenData\RunNumber.txt','w')
        f.write(str(self.runNumber + 1))
        f.close()
        os.mkdir('GenData\Run_' + str(self.runNumber))
        
        self.fileName = 'GenData\Run_' + str(self.runNumber) + '\data.txt'
        print(self.fileName)


    def writeGenData(self, genNumber, pop):
        pass

    def writePop(self,genNumber,pop):
        if(not self.on):
            return
        f = open('GenData\Run_' + str(self.runNumber) + '\pop.txt','a')
        f.write('Generation '+ str(genNumber) + ':\n')
        for ind in pop:
            f.write("fit: " + str(ind.fitness.values) + " | " + str(ind) + "\n")
        f.close()

    def DrawPop(self,pop,h):
        auxI = 1
        for person in pop:
            lvl = h.TestLevel(person)
            viewer.drawLevel(lvl,".\\GenData\\Run_"+ str(self.runNumber)+"\\level"+ str(auxI)+ ".png")
            print(".\\GenData\\Run_"+ str(self.runNumber)+"\\level"+ str(auxI) + ".png :", lvl.fit )
            auxI += 1

    def DrawBestPop(self,pop,h):
        auxI = 1
        for person in pop:
            lvl = h.TestLevel(person)
            viewer.drawLevel(lvl,".\\GenData\\Run_"+ str(self.runNumber)+"\\Bestlevel"+ str(auxI)+ ".png")
            print(".\\GenData\\Run_"+ str(self.runNumber)+"\\Bestlevel"+ str(auxI) + ".png :", lvl.fit )
            auxI += 1
