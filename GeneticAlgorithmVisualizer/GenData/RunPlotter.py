import numpy as np
import matplotlib.pyplot as plt

dirName = "Run_5"
f = open(dirName + "\\data.txt","r")

GenNumber = 0
bestFitness = []
average = []
averagefq = []
averagesq = []
averagetq = []
averagelq = []

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
        averagefq += [float(l[:-1])]
        l = f.readline()
        l = l.replace(",",".")
        averagesq += [float(l[:-1])]
        l = f.readline()
        l = l.replace(",",".")
        averagetq += [float(l[:-1])]
        l = f.readline()
        l = l.replace(",",".")
        averagelq += [float(l[:-1])]

#X = np.arange(GenNumber)

print(bestFitness)
print(average)
print(averagefq)
print(averagesq)
print(averagetq)
print(averagelq)

dpii = 500.0
plt.plot(bestFitness)
plt.ylabel('BestFitness')
plt.savefig(dirName+'\\BestFitness.png',dpi = dpii)
plt.clf()

plt.plot(average)
plt.ylabel('Average Fitness')
plt.savefig(dirName+'\\Average.png',dpi = dpii)
plt.clf()

plt.plot(averagefq)
plt.ylabel('Average First Quartile')
plt.savefig(dirName+'\\AverageFirstQuartile.png',dpi = dpii)
plt.clf()

plt.plot(averagesq)
plt.ylabel('Average Second Quartile')
plt.savefig(dirName+'\\AverageSecondQuartile.png',dpi = dpii)
plt.clf()

plt.plot(averagetq)
plt.ylabel('Average Third Quartile')
plt.savefig(dirName+'\\AverageThirdQuartile.png',dpi = dpii)
plt.clf()

plt.plot(averagelq)
plt.ylabel('Average Fourth Quartile')
plt.savefig(dirName+'\\AverageFourthQuartile.png',dpi = dpii)
plt.clf()

plt.plot(bestFitness,label = "Best")

plt.plot(average,label = "Average")

plt.plot(averagefq,label = "First Quartile")

plt.plot(averagesq,label = "Second Quartile")

plt.plot(averagetq,label = "Third Quartile")

plt.plot(averagelq,label = "Fourth Quartile")
plt.ylabel('FitnessValue')
plt.legend()
plt.savefig(dirName+'\\All.png',dpi = dpii)
plt.clf()

plt.plot(bestFitness,label = "Best")

plt.plot(average,label = "Average")

plt.ylabel('FitnessValue')
plt.legend()
plt.savefig(dirName+'\\BestVsAverage.png',dpi = dpii)
plt.clf()


plt.plot(averagefq,label = "First Quartile")

plt.plot(averagesq,label = "Second Quartile")

plt.plot(averagetq,label = "Third Quartile")

plt.plot(averagelq,label = "Fourth Quartile")
plt.ylabel('FitnessValue')
plt.legend()
plt.savefig(dirName+'\\Quartiles.png',dpi = dpii)
plt.clf()