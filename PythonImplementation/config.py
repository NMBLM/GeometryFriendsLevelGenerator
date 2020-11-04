

toolbox = ""
class Config:
    def __init__(self,h = "", mate = "", mutate = "", select = "",popSize = "", genNumber = ""):
        print(h)
        self.h = h
        self.mate = mate
        self.mutate = mutate
        self.select = select
        self.popSize = popSize
        self.genNumber = genNumber
        self.toolbox = toolbox
    
    def setup(self):
        if(self.h != ""):
            self.toolbox.register("evaluate", self.h.CalculateFitness)
        if(self.mate != ""):
            self.toolbox.register("mate", self.mate)
        if(self.mutate != ""):
            self.toolbox.register("mutate", self.mutate)
        if(self.select != ""):
            self.toolbox.register("select", self.select)
        
    def description(self):
        txt = ""
        if(self.h != ""):
            txt += "Heuristic: " + str(self.h) + "\n"
        if(self.mate != ""):
            txt += "Crossover: " + str(self.mate) + "\n"
        if(self.mutate != ""):
            txt += "Mutate: " + str(self.mutate) + "\n"
        if(self.select != ""):
            txt += "Selection: " + str(self.select) + "\n"
        if(self.popSize != ""):
            txt += "Population: " + str(self.popSize) + "\n"
        if(self.genNumber != ""):
            txt += "Number of Total Generation: " + str(self.genNumber) + "\n"
        return txt