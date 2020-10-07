import os

import PILViewer as viewer

class InstrumentationManager:

    def __init__(self,on = True, popWrite = True):
        self.on = on
        self.popWrite = popWrite
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


    def WritePop(self,genNumber,pop):
        if(not self.popWrite):
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


    def WriteGenData(self, genNumber, pop):
        if(not self.on):
            return
        text = "Gen " + str(genNumber) + "\n"
        #Best
        text += str(pop[0].fitness.values[0]) + "\n"
        average = 0
        bp = len(pop) / 4
        fq = 0
        sq = 0
        tq = 0
        lq = 0
        for i in range(0,len(pop)):
            if (i < bp):
                fq += pop[i].fitness.values[0]
            elif (i < 2 * bp):
                sq += pop[i].fitness.values[0]
            elif (i < 3 * bp):
                tq += pop[i].fitness.values[0]
            else:
                lq += pop[i].fitness.values[0]
            average += pop[i].fitness.values[0]
        #Average
        text += str(average/bp) + "\n"
        #Average First Quartil
        text += str(fq / bp) + "\n"
        
        #Average Second Quartil
        text += str(sq / bp) + "\n"

        #Average Third Quartil
        text += str(tq / bp) + "\n"

        #Average Fourth Quartil
        text += str(lq / bp) + "\n"

        f = open('GenData\Run_' + str(self.runNumber) + '\data.txt','a')
        f.write(text)
        f.close()