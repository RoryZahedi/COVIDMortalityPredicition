import csv
from csv import reader
import sys #argv
import numpy as np

# lab notes
# -5th column is date dead
# -if date is 999999 means they lived
# -real date mean date they died
# -live  = 0
# -die = 1
# -The 2nd and 3rd columns, the patients’ date of entry to hospital and
# date of first symptom may have format either “date-month-year” or “data/month/year”


def loadCSV(filename):
    ds = list()
    with open(filename,'r') as file:
        csv_reader = reader(file)
        for row in csv_reader:
            if not row:
                continue
            ds.append(row)
    return ds

def getBookKeeping(data1):
    #init book
    book = [[0,0,0,0]]
    for i in range(0,len(data1[0])-1):
        l = [0,0,0,0]
        book.append(l)
    #book keeping    
    numDead = 0
    numAlive = 0
    for i in range(1,len(data1)-1): #-1?
        if data1[i][4] == "9999-99-99" or data1[i][4] == "9999/99/99":  
            numAlive+=1
            for j in range(0,len(data1[i])):
                if data1[i][j] == "1": #1|alive
                    book[j][0] += 1
                elif data1[i][j] == "2": #2|alive
                    book[j][1] += 1
        else:
            numDead+=1
            for j in range(0,len(data1[i])):
                if data1[i][j] == "1": #1 |dead
                    book[j][2] += 1
                elif data1[i][j] == "2": #2|dead
                    book[j][3] += 1      
    return (book,numDead,numAlive)

#main
file1 = sys.argv[1]
file2 = sys.argv[2]
data1 = loadCSV(file1)
data2 = loadCSV(file2)

book,numDead,numAlive = getBookKeeping(data1)
pTotalAlive = (numAlive)/(numAlive+numDead)
pTotalDead = (numDead)/(numAlive+numDead)
for i in range(1,len(data2)):
    pAlive = 1
    pDead = 1
    if(int(data2[i][7]) <30 and data2[i][18] == "2"):
        print("0")
        continue
    for j in range(0,len(data2[i])-1): 
        if data2[i][j] == "1": 
            pAlive*= ((book[j][0])/numAlive) #1|alive
            pDead*= ((book[j][2])/numDead) #1|dead
        elif data2[i][j] == "2": 
            pAlive*= ((book[j][1])/numAlive) #2|alive
            pDead*= ((book[j][3])/numDead) #2|dead
    pAlive*=pTotalAlive
    pDead*=pTotalDead
    if pAlive>=pDead:
        print("0")
    else:
        print("1")


        


    


