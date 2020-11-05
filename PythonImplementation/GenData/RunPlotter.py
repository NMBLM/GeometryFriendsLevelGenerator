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


currentR = 0
dn = "Gendata/Run_" + str(currentR)
while(os.path.isdir(dn)):
    DirectPlot(dn)
    SmoothPlot(dn)
    currentR += 1
    dn = "Gendata/Run_" + str(currentR)


