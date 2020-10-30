
toolbox = ""
class Config:
    def __init__(self,h = "", mate = "", mutate = "", select = "",):
        print(h)
        self.h = h
        self.mate = mate
        self.mutate = mutate
        self.select = select
    
    def setup(self):
        if(self.h != ""):
            toolbox.register("evaluate", self.h.CalculateFitness)
        if(self.mate != ""):
            toolbox.register("mate", self.mate)
        if(self.mutate != ""):
            toolbox.register("mutate", self.mutate)
        if(self.select != ""):
            toolbox.register("select", self.select)
        
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
        return txt