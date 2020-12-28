import numpy as np
import matplotlib.pyplot as plt
import os  
from scipy.interpolate import make_interp_spline, BSpline


dn = "Run_0"

def DirectPlot(dirName):

    f = open(dirName + "\\data.txt","r")
    print(dirName)

    GenNumber = 1
    bestFitness = []
    average = []
    fqaverage = []
    sqaverage = []
    tqaverage = []
    lqaverage = []

    while(f.readline()):
        GenNumber = GenNumber + 1
        l = f.readline()
        if(len(l)>1):
            l = l.replace(",",".")
            bestFitness += [float(l[:-1])]
            l = f.readline()
            l = l.replace(",",".")
            average += [float(l[:-1])]
            l = f.readline()
            l = l.replace(",",".")
            fqaverage += [float(l[:-1])]
            l = f.readline()
            l = l.replace(",",".")
            sqaverage += [float(l[:-1])]
            l = f.readline()
            l = l.replace(",",".")
            tqaverage += [float(l[:-1])]
            l = f.readline()
            l = l.replace(",",".")
            lqaverage += [float(l[:-1])]

    #X = np.arange(1,GenNumber)

    #print(bestFitness)
    #print(average)
    #print(fqaverage)
    #print(sqaverage)
    #print(tqaverage)
    #print(lqaverage)


    dpii = 500.0
    plt.plot(bestFitness  ,color ="blue")
    plt.ylabel('BestFitness')
    plt.savefig(dirName+'\\PlotBestFitness.png',dpi = dpii)
    plt.clf()

    plt.plot(average  ,color ="orange")
    plt.ylabel('Average Fitness')
    plt.savefig(dirName+'\\PlotAverage.png',dpi = dpii)
    plt.clf()

    plt.plot(fqaverage ,color ="green")
    plt.ylabel('Average First Quartile')
    plt.savefig(dirName+'\\PlotAverageFirstQuartile.png',dpi = dpii)
    plt.clf()

    plt.plot(sqaverage ,color ="red")
    plt.ylabel('Average Second Quartile')
    plt.savefig(dirName+'\\PlotAverageSecondQuartile.png',dpi = dpii)
    plt.clf()

    plt.plot(tqaverage ,color ="purple")
    plt.ylabel('Average Third Quartile')
    plt.savefig(dirName+'\\PlotAverageThirdQuartile.png',dpi = dpii)
    plt.clf()

    plt.plot(lqaverage ,color ="brown")
    plt.ylabel('Average Fourth Quartile')
    plt.savefig(dirName+'\\PlotAverageFourthQuartile.png',dpi = dpii)
    plt.clf()

    plt.plot(bestFitness ,label = "Best" ,color ="blue")

    plt.plot(average ,label = "Average" ,color ="orange")

    plt.plot(fqaverage,label = "First Quartile" ,color ="green")

    plt.plot(sqaverage,label = "Second Quartile" ,color ="red")

    plt.plot(tqaverage,label = "Third Quartile" ,color ="purple")

    plt.plot(lqaverage,label = "Fourth Quartile" ,color ="brown")
    plt.ylabel('FitnessValue')
    plt.legend()
    plt.savefig(dirName+'\\PlotAll.png',dpi = dpii)
    plt.clf()

    plt.plot(bestFitness ,label = "Best" ,color ="blue")

    plt.plot(average ,label = "Average" ,color ="orange")

    plt.ylabel('FitnessValue')
    plt.legend()
    plt.savefig(dirName+'\\PlotBestVsAverage.png',dpi = dpii)
    plt.clf()


    plt.plot(fqaverage,label = "First Quartile" ,color ="green")

    plt.plot(sqaverage,label = "Second Quartile" ,color ="red")

    plt.plot(tqaverage,label = "Third Quartile" ,color ="purple")

    plt.plot(lqaverage,label = "Fourth Quartile" ,color ="brown")
    plt.ylabel('FitnessValue')
    plt.legend()
    plt.savefig(dirName+'\\PlotQuartiles.png',dpi = dpii)
    plt.clf()




def SmoothPlot(dirName):

    f = open(dirName + "\\data.txt","r")
    print(dirName)

    GenNumber = 1
    bestFitness = []
    average = []
    fqaverage = []
    sqaverage = []
    tqaverage = []
    lqaverage = []

    while(f.readline()):
        GenNumber = GenNumber + 1
        l = f.readline()
        if(len(l)>1):
            l = l.replace(",",".")
            bestFitness += [float(l[:-1])]
            l = f.readline()
            l = l.replace(",",".")
            average += [float(l[:-1])]
            l = f.readline()
            l = l.replace(",",".")
            fqaverage += [float(l[:-1])]
            l = f.readline()
            l = l.replace(",",".")
            sqaverage += [float(l[:-1])]
            l = f.readline()
            l = l.replace(",",".")
            tqaverage += [float(l[:-1])]
            l = f.readline()
            l = l.replace(",",".")
            lqaverage += [float(l[:-1])]

    X = np.arange(1,GenNumber)

    #print(bestFitness)
    #print(average)
    #print(fqaverage)
    #print(sqaverage)
    #print(tqaverage)
    #print(lqaverage)

    xnew = np.linspace(X.min(), X.max(), int(len(X)/20)) 

    spl = make_interp_spline(X, np.array(bestFitness), k=3)
    bestFitness = spl(xnew)
    spl = make_interp_spline(X, np.array(average), k=3)
    average = spl(xnew)
    spl = make_interp_spline(X, np.array(fqaverage), k=3)
    fqaverage = spl(xnew)
    spl = make_interp_spline(X, np.array(sqaverage), k=3)
    sqaverage = spl(xnew)
    spl = make_interp_spline(X, np.array(tqaverage), k=3)
    tqaverage = spl(xnew)
    spl = make_interp_spline(X, np.array(lqaverage), k=3)
    lqaverage = spl(xnew)


    dpii = 500.0
    plt.plot(xnew,bestFitness  ,color ="blue")
    plt.ylabel('BestFitness')
    plt.savefig(dirName+'\\SmoothBestFitness.png',dpi = dpii)
    plt.clf()

    plt.plot(xnew,average  ,color ="orange")
    plt.ylabel('Average Fitness')
    plt.savefig(dirName+'\\SmoothAverage.png',dpi = dpii)
    plt.clf()

    plt.plot(xnew,fqaverage ,color ="green")
    plt.ylabel('Average First Quartile')
    plt.savefig(dirName+'\\SmoothAverageFirstQuartile.png',dpi = dpii)
    plt.clf()

    plt.plot(xnew,sqaverage ,color ="red")
    plt.ylabel('Average Second Quartile')
    plt.savefig(dirName+'\\SmoothAverageSecondQuartile.png',dpi = dpii)
    plt.clf()

    plt.plot(xnew,tqaverage ,color ="purple")
    plt.ylabel('Average Third Quartile')
    plt.savefig(dirName+'\\SmoothAverageThirdQuartile.png',dpi = dpii)
    plt.clf()

    plt.plot(xnew,lqaverage ,color ="brown")
    plt.ylabel('Average Fourth Quartile')
    plt.savefig(dirName+'\\SmoothAverageFourthQuartile.png',dpi = dpii)
    plt.clf()

    plt.plot(xnew,bestFitness ,label = "Best" ,color ="blue")

    plt.plot(xnew,average ,label = "Average" ,color ="orange")

    plt.plot(xnew,fqaverage,label = "First Quartile" ,color ="green")

    plt.plot(xnew,sqaverage,label = "Second Quartile" ,color ="red")

    plt.plot(xnew,tqaverage,label = "Third Quartile" ,color ="purple")

    plt.plot(xnew,lqaverage,label = "Fourth Quartile" ,color ="brown")
    plt.ylabel('FitnessValue')
    plt.legend()
    plt.savefig(dirName+'\\SmoothAll.png',dpi = dpii)
    plt.clf()

    plt.plot(xnew,bestFitness ,label = "Best" ,color ="blue")

    plt.plot(xnew,average ,label = "Average" ,color ="orange")

    plt.ylabel('FitnessValue')
    plt.legend()
    plt.savefig(dirName+'\\SmoothBestVsAverage.png',dpi = dpii)
    plt.clf()


    plt.plot(xnew,fqaverage,label = "First Quartile" ,color ="green")

    plt.plot(xnew,sqaverage,label = "Second Quartile" ,color ="red")

    plt.plot(xnew,tqaverage,label = "Third Quartile" ,color ="purple")

    plt.plot(xnew,lqaverage,label = "Fourth Quartile" ,color ="brown")
    plt.ylabel('FitnessValue')
    plt.legend()
    plt.savefig(dirName+'\\SmoothQuartiles.png',dpi = dpii)
    plt.clf()

def BestChangeGen(dirName):
    f = open(dirName + "\\data.txt","r")
    print(dirName)
    previousBest = 0
    GenNumber = 1
    bestFitness = []
    allBestFit = []
    while(f.readline()):
        GenNumber = GenNumber + 1
        l = f.readline()
        if(len(l)>1):
            l = l.replace(",",".")
            genBestFit = float(l[:-1])
            allBestFit += [genBestFit]
            if(genBestFit > previousBest):
                previousBest = genBestFit
                bestFitness += [(len(allBestFit)-1,genBestFit)]
            l = f.readline()
            l = f.readline()
            l = f.readline()
            l = f.readline()
            l = f.readline()
    print(bestFitness)

def TimePlot(dirName):

    f = open(dirName + "\\time.txt","r")
    print(dirName)

    GenNumber = 1
    totaltime = []
    crossoverTime = []
    mutationTime = []
    evalTime = []
    l = f.readline()
    allValues = []
    while(l):
        GenNumber = GenNumber + 1
        stringValues = l.split(':')
        values = []
        for v in stringValues:
            values += [float(v)]
        totaltime += [values[1]]
        crossoverTime += [values[2]]
        mutationTime += [values[3]]
        evalTime += [values[4]]
        allValues += (values,)
        l = f.readline()

    f.close()
    totalTimeAverage = 0
    crossoverTimeAverage = 0
    mutationTimeAverage = 0
    evalTimeAverage = 0
    for val in allValues:
        totalTimeAverage += val[1]
        crossoverTimeAverage += val[2]
        mutationTimeAverage += val[3]
        evalTimeAverage += val[4]
    
    #better way
    #totalTimeAverage = sum(totaltime) / len(totaltime)
    #crossoverTimeAverage = sum(crossoverTime) / len(crossoverTime)
    #mutationTimeAverage = sum(mutationTime) / len(mutationTime)
    #evalTimeAverage = sum(evalTime) / len(evalTime)

    totalTimeAverage = totalTimeAverage / len(allValues)
    crossoverTimeAverage = crossoverTimeAverage / len(allValues)
    mutationTimeAverage = mutationTimeAverage / len(allValues)
    evalTimeAverage = evalTimeAverage / len(allValues)


    print("TotalAverage: ", totalTimeAverage)
    print("CrossoverAverage: ", crossoverTimeAverage)
    print("MutationAverage: ", mutationTimeAverage)
    print("EvaluationAverage: ", evalTimeAverage)

    f = open(dirName + "\\info.txt","a")
    f.write("TotalAverage: " + str(totalTimeAverage))
    f.write(" CrossoverAverage: "+ str(crossoverTimeAverage))
    f.write(" MutationAverage: "+ str(mutationTimeAverage))
    f.write(" EvaluationAverage: "+ str(evalTimeAverage))
    f.write("\n")
    f.close()

    dpii = 500.0
    plt.plot(totaltime  ,color ="blue")
    plt.ylabel('Total Time Taken')
    plt.savefig(dirName+'\\TotalTime.png',dpi = dpii)
    plt.clf()

    plt.plot(crossoverTime  ,color ="orange")
    plt.ylabel('Crossover Time')
    plt.savefig(dirName+'\\CrossoverTime.png',dpi = dpii)
    plt.clf()

    plt.plot(mutationTime ,color ="green")
    plt.ylabel('Mutation Time')
    plt.savefig(dirName+'\\MutationTime.png',dpi = dpii)
    plt.clf()

    plt.plot(evalTime ,color ="red")
    plt.ylabel('Evaluation Time')
    plt.savefig(dirName+'\\EvaluationTime.png',dpi = dpii)
    plt.clf()

    plt.plot(totaltime ,label = 'Total Time Taken' ,color ="blue")

    plt.plot(crossoverTime ,label = 'Crossover Time' ,color ="orange")

    plt.plot(mutationTime,label = 'Mutation Time' ,color ="green")

    plt.plot(evalTime,label = 'Evaluation Time' ,color ="red")

    plt.ylabel('Time')
    plt.legend()
    plt.savefig(dirName+'\\TimePlotAll.png',dpi = dpii)
    plt.clf()

    plt.plot(totaltime ,label = 'Total Time Taken' ,color ="blue")
    plt.plot(evalTime,label = 'Evaluation Time' ,color ="red")

    plt.ylabel('Time')
    plt.legend()
    plt.savefig(dirName+'\\TimeEvalPlotAll.png',dpi = dpii)
    plt.clf()

def EvalOnceTimePlot(dirName):

    f = open(dirName + "CalcFit.txt","r")
    print(dirName)

    GenNumber = 1
    evalTime = []
    l = f.readline()
    while(l):
        evalTime += [float(l)]
        l = f.readline()

    f.close()
    evalTimeAverage = sum(evalTime) / len(evalTime)

    print("EvalTimeAverage: ", evalTimeAverage)

    X = np.arange(1,len(evalTime)+1)

    xnew = np.linspace(X.min(), X.max(), int(len(X)/10)) 

    spl = make_interp_spline(X, np.array(evalTime), k=3)
    evalTimeS = spl(xnew)
    
    dpii = 500.0
    plt.plot(evalTime  ,color ="blue")
    plt.ylabel('Time Per Evaluation')
    plt.savefig(dirName+'EvalTime.png',dpi = dpii)
    plt.clf()

    plt.plot(xnew,evalTimeS  ,color ="blue")
    plt.ylabel('Time Per Evaluation')
    plt.savefig(dirName+'EvalTimeS.png',dpi = dpii)
    plt.clf()


def main():
    currentR = 5312
    dn = "Gendata/Run_" + str(currentR)
    while(os.path.isdir(dn)):
        DirectPlot(dn)
        SmoothPlot(dn)
        #BestChangeGen(dn)
        #TimePlot(dn)
        currentR += 1
        dn = "Gendata/Run_" + str(currentR)



def time():
    dn = ""
    EvalOnceTimePlot(dn)

main()
#time()