import numpy as np
import matplotlib.pyplot as plt
import os  

dn = "Run_0"

def runAnalysis(dirName):

    f = open(dirName + "\\data.txt","r")

    GenNumber = 0
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

    #X = np.arange(GenNumber)

    #print(bestFitness)
    #print(average)
    #print(fqaverage)
    #print(sqaverage)
    #print(tqaverage)
    #print(lqaverage)

    print(dirName)
    dpii = 500.0
    plt.plot(bestFitness  ,color ="blue")
    plt.ylabel('BestFitness')
    plt.savefig(dirName+'\\BestFitness.png',dpi = dpii)
    plt.clf()

    plt.plot(average  ,color ="orange")
    plt.ylabel('Average Fitness')
    plt.savefig(dirName+'\\Average.png',dpi = dpii)
    plt.clf()

    plt.plot(fqaverage ,color ="green")
    plt.ylabel('Average First Quartile')
    plt.savefig(dirName+'\\AverageFirstQuartile.png',dpi = dpii)
    plt.clf()

    plt.plot(sqaverage ,color ="red")
    plt.ylabel('Average Second Quartile')
    plt.savefig(dirName+'\\AverageSecondQuartile.png',dpi = dpii)
    plt.clf()

    plt.plot(tqaverage ,color ="purple")
    plt.ylabel('Average Third Quartile')
    plt.savefig(dirName+'\\AverageThirdQuartile.png',dpi = dpii)
    plt.clf()

    plt.plot(lqaverage ,color ="brown")
    plt.ylabel('Average Fourth Quartile')
    plt.savefig(dirName+'\\AverageFourthQuartile.png',dpi = dpii)
    plt.clf()

    plt.plot(bestFitness ,label = "Best" ,color ="blue")

    plt.plot(average ,label = "Average" ,color ="orange")

    plt.plot(fqaverage,label = "First Quartile" ,color ="green")

    plt.plot(sqaverage,label = "Second Quartile" ,color ="red")

    plt.plot(tqaverage,label = "Third Quartile" ,color ="purple")

    plt.plot(lqaverage,label = "Fourth Quartile" ,color ="brown")
    plt.ylabel('FitnessValue')
    plt.legend()
    plt.savefig(dirName+'\\All.png',dpi = dpii)
    plt.clf()

    plt.plot(bestFitness ,label = "Best" ,color ="blue")

    plt.plot(average ,label = "Average" ,color ="orange")

    plt.ylabel('FitnessValue')
    plt.legend()
    plt.savefig(dirName+'\\BestVsAverage.png',dpi = dpii)
    plt.clf()


    plt.plot(fqaverage,label = "First Quartile" ,color ="green")

    plt.plot(sqaverage,label = "Second Quartile" ,color ="red")

    plt.plot(tqaverage,label = "Third Quartile" ,color ="purple")

    plt.plot(lqaverage,label = "Fourth Quartile" ,color ="brown")
    plt.ylabel('FitnessValue')
    plt.legend()
    plt.savefig(dirName+'\\Quartiles.png',dpi = dpii)
    plt.clf()

currentR = 0
dn = "GenData/Run_" + str(currentR)
while(os.path.isdir(dn)):
    runAnalysis(dn)
    currentR += 1
    dn = "GenData/Run_" + str(currentR)
