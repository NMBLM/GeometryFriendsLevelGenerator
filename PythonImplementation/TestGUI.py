from tkinter import *
from tkinter import ttk
import os
from PIL import ImageTk, Image
import PILViewer as pv
import evaluateFuncs as ev


root = Tk()
root.title("Specifiy Specs")
root.geometry("1800x750")




specRows = {}
curEntry = 0
lastEntry = 0

specs = []
heuristic = ev.AreaHeuristic(specs)

def saveSpecsToFile():
    f = open('TestSpecs\SaveNumber.txt','r')
    numberOfSaves = int(f.readline())
    f.close() 

    filename = "TestSpecs\\SpecSave" + str(numberOfSaves).zfill(2) + ".txt"
    f = open(filename,'w')
    f.write(heuristic.description())
    f.close()

    f = open('TestSpecs\SaveNumber.txt','w')
    f.write(str(numberOfSaves + 1))
    f.close()

    cleanError()
    printError("Saved on: " + "TestSpecs\\SpecSave" + str(numberOfSaves).zfill(2) + ".txt")
    return




def getEntryValue(entry):
    try:
        val = int(entry.get())
        return val
    except:
        printError("Entry Value not integer\n")
        return -1

def printError(txt):
    if not (txt in errorMessage.get()):
        txt = errorMessage.get() + txt
    errorMessage.set(txt)

def cleanError():
    errorMessage.set("")


def getSpecs():
    global specs
    global heuristic
    specs = []
    cleanError()
    for row in specRows.values():
        intSpecs = row[:-3]
        values = []
        error = False
        for spec in intSpecs:
            val = getEntryValue(spec)
            if val == -1:
                error = True
                break
            if val == 0:
                printError(" Entry Value should not be zero\n")
                error = True
                break
            values.append(val)
        if not error:
            x,y,width,height = values
            t = row[-3].get()
            addSpec(x,y,width,height,t)
    replaceHSpecs(heuristic,specs)
    showHeuristic()


def addSpec(x,y,width,height,t):
    global specs
    if t == "cooperative":
        t = ev.AreaType.Cooperative
    if t == "common":
        t = ev.AreaType.Common
    if t == "rectangle":
        t = ev.AreaType.RectangleOnly
    if t == "circle":
        t = ev.AreaType.CircleOnly
    spec = ev.SpecialArea(x,y,width,height,t)
    specs += [spec]

def replaceHSpecs(h,specs):
    h.specifications = specs



def addAllRows():
    if len(specRows) >= 10:
        printError("Maximum number of specs\n")
        return
    curSpecRow = 1
    cleanError()
    for k in specRows: #add all previous rows
        reAddRow(curSpecRow,specRows[k],k)
        curSpecRow += 1
    addNewRow(curSpecRow)
    
def addNewRow(curI):
    global curEntry
    global lastEntry
    specsEntry = []
    for x in range(4):
        entry = Entry(root)
        entry.grid(row = curI, column= x, pady= 5, padx = 5)
        entry.insert(0,0)
        specsEntry.append(entry)
    typeDropVar = StringVar()
    typeDropVar.set("cooperative")
    typeDrop = OptionMenu(root,typeDropVar,"cooperative","rectangle","circle","common",)
    typeDrop.grid(row = curI, column = x + 1)
    specsEntry.append(typeDropVar)
    specsEntry.append(typeDrop)
    removeSpec = Button(root, text= "-", padx = 10, pady = 5, fg="white", bg ="#0A2858", command = lambda: removeSpecificSpecRow(str(curEntry)))
    removeSpec.grid(row = curI, column = x + 2)
    specsEntry.append(removeSpec)
    specRows[str(curEntry)] = specsEntry
    lastEntry = str(curEntry) #because for the last entry the lambda evaluates for the updated curEntry unlike the others
    curEntry += 1

def reAddRow(curI, row, key):
    specsEntry = []
    for x in range(4):
        entry = Entry(root)
        entry.grid(row = curI, column= x, pady= 5, padx = 5)
        entry.insert(0,row[x].get())
        specsEntry.append(entry)
        row[x].destroy()
    typeDropVar = StringVar()
    typeDropVar.set(row[x+1].get())
    typeDrop = OptionMenu(root,typeDropVar,"cooperative","rectangle","circle","common",)
    typeDrop.grid(row = curI, column = x + 1)
    row[x+2].destroy()
    specsEntry.append(typeDropVar)
    specsEntry.append(typeDrop)
    removeSpec = Button(root, text= "-", padx = 10, pady = 5, fg="white", bg ="#0A2858", command = lambda: removeSpecificSpecRow(key))
    removeSpec.grid(row = curI, column = x + 2)
    row[x+3].destroy()
    specsEntry.append(removeSpec)
    specRows[key] = specsEntry

def removeSpecificSpecRow(key):
    global specRows
    cleanError()
    if len(specRows) == 1:
        printError("Can't have no specifications")
        return
    if key not in specRows:
        key = lastEntry
    for l in specRows[key]:
        try:
            l.destroy()
        except:
            continue
    specRows.pop(key,None)


def showHeuristic():
    #global imgLabel
    pv.drawSpecs(heuristic,"TestSpecs\\PreviewHeuristic",True)
    img = ImageTk.PhotoImage(Image.open("TestSpecs\\PreviewHeuristicThumbnail.png"))
    imgLabel = ttk.Label(image=img)
    #imgLabel.config(image=img)
    imgLabel.image = img
    imgLabel.grid(row = 0, rowspan= 200, column = 10, columnspan = 200)

#top label
xInfoLabel = Label(root, text= "Pos X")
xInfoLabel.grid(row=0,column = 0)
yInfoLabel = Label(root, text= "Pos Y")
yInfoLabel.grid(row=0,column = 1)
wInfoLabel = Label(root, text= "Width")
wInfoLabel.grid(row=0,column = 2)
hInfoLabel = Label(root, text= "Height")
hInfoLabel.grid(row=0,column = 3)
tInfoLabel = Label(root, text= "Area Type")
tInfoLabel.grid(row=0,column = 4)

#error
errorMessage = StringVar()
errorLabel = Label(root, textvariable = errorMessage)
errorLabel.grid(row = 110)

#Buttons
addRow = Button(root, text= "Add Row", padx = 10, pady = 5, fg="white", bg ="#0A2858", command = addAllRows)
addRow.grid(row = 100,column = 0 )

confirmSpec = Button(root, text= "Confirm Specs", padx = 10, pady = 5, fg="white", bg ="#0A2858", command = getSpecs)
confirmSpec.grid(row = 100,column = 1 )

testButton = Button(root, text= "SaveSpecs", padx = 10, pady = 5, fg="white", bg ="#0A2858", command = saveSpecsToFile)
testButton.grid(row = 100,column = 4 )

addAllRows()

pv.drawSpecs(heuristic,"TestSpecs\\PreviewHeuristic",True)
img = ImageTk.PhotoImage(Image.open("TestSpecs\\PreviewHeuristicThumbnail.png"))
imgLabel = ttk.Label(image=img)
imgLabel.grid(row = 0, rowspan= 200, column = 8, columnspan = 200)

root.mainloop()


