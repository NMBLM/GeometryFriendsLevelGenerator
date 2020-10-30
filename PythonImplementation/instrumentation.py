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
        os.mkdir('GenData\Run_' + str(self.runNumber))
        self.tmpauxi = 0
        self.fileName = 'GenData\Run_' + str(self.runNumber) + '\data.txt'
        f = open('GenData\RunNumber.txt','w')
        f.write(str(self.runNumber + 1))
        f.close()
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
            if isinstance(lvl, list):
                aux = 1
                for l in lvl:
                    viewer.drawLevel(l,".\\GenData\\Run_"+ str(self.runNumber)+"\\S"+ str(aux) + "level"+ str(auxI)+ ".png")
                    aux+=1
                print(".\\GenData\\Run_"+ str(self.runNumber)+"\\level"+ str(auxI) + ".png")
            else:
                viewer.drawLevel(lvl,".\\GenData\\Run_"+ str(self.runNumber)+"\\level"+ str(auxI)+ ".png")
                print(".\\GenData\\Run_"+ str(self.runNumber)+"\\level"+ str(auxI) + ".png :", lvl.fit )
            auxI += 1

    def DrawBestPop(self,pop,h):
        auxI = 1
        for person in pop:
            lvl = h.TestLevel(person)
            if isinstance(lvl, list):
                aux = 1
                for l in lvl:
                    viewer.drawLevel(l,".\\GenData\\Run_"+ str(self.runNumber)+"\\S"+ str(aux) + "Bestlevel"+ str(auxI)+ ".png")
                    aux+=1
                print(".\\GenData\\Run_"+ str(self.runNumber)+"\\Bestlevel"+ str(auxI) + ".png" )

            else:
                viewer.drawLevel(lvl,".\\GenData\\Run_"+ str(self.runNumber)+"\\Bestlevel"+ str(auxI)+ ".png")
                print(".\\GenData\\Run_"+ str(self.runNumber)+"\\Bestlevel"+ str(auxI) + ".png :", lvl.fit )
            auxI += 1

    def DrawLevel(self,lvl,h):
        eLvl = h.TestLevel(lvl)
        if isinstance(eLvl, list):
            aux = 1
            for l in lvl:
                viewer.drawLevel(l,"S"+ str(aux) + "indlevel.png")
                aux+=1

        else:
            viewer.drawLevel(eLvl,"indLevel.png")
        print("indLevel.png", eLvl.fit )


    def DrawSpecs(self,h):
        self.tmpauxi += 1
        viewer.drawSpecs(h,".\\GenData\\Run_"+ str(self.runNumber)+"\\HeuristicSpec"+str(self.tmpauxi) +".png")
        print(".\\GenData\\Run_"+ str(self.runNumber)+"\\HeuristicSpec" + str(self.tmpauxi) + ".png : " , len(h.specifications))

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
        text += str(average/len(pop)) + "\n"
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


    def DrawGenericPop(self,pop,h,beforeLevel,afterlevel):
        if not os.path.isdir(".\\GenData\\Run_"+ str(self.runNumber)+ beforeLevel):
            os.mkdir(".\\GenData\\Run_"+ str(self.runNumber)+ beforeLevel)
        auxI = 1
        for person in pop:
            lvl = h.TestLevel(person)
            viewer.drawLevel(lvl,".\\GenData\\Run_"+ str(self.runNumber) + beforeLevel +"\\level"+ str(auxI) + afterlevel +".png")
            print(".\\GenData\\Run_"+ str(self.runNumber) + beforeLevel +"\\level"+ str(auxI) + afterlevel +".png :", lvl.fit )
            auxI += 1


    def WriteToRND(self,txt):
        f = open('GenData\Run_' + str(self.runNumber) + '\Info.txt','a')
        f.write(txt)
        f.close()